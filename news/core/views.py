from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import Http404
from urllib.request import urlopen
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.pagination import LimitOffsetPagination

from .models import Channel, Article
from .serializers import ArticleSerializer, ChannelSerializer
from .utils import webpage_info
from .tasks import update_article_info


## Show the list of articles and Add a new article  
class ArticleList(APIView):
    serializer_class = ArticleSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    # Adding Swagger data
    @swagger_auto_schema(manual_parameters=[openapi.Parameter('channel_id', openapi.IN_QUERY, description="Channel ID", type=openapi.TYPE_STRING),
                                            openapi.Parameter('min_word_count', openapi.IN_QUERY, description="min word count", type=openapi.TYPE_STRING),
                                            openapi.Parameter('max_word_count', openapi.IN_QUERY, description="max word count", type=openapi.TYPE_STRING),
                                            openapi.Parameter('limit', openapi.IN_QUERY, description="page size", type=openapi.TYPE_STRING),
                                            openapi.Parameter('offset', openapi.IN_QUERY, description="page offset", type=openapi.TYPE_STRING)],
                         responses={200: openapi.Response('Returns a list of articles', ArticleSerializer)},
                         operation_description='Get the list of articles')
    # Show the list of articles
    def get(self, request, *args, **kwargs):
        min_word_count = self.request.query_params.get('min_word_count')
        max_word_count = self.request.query_params.get('max_word_count')
        channel_id = self.request.query_params.get('channel_id')
        
        articles = Article.objects.all()
        if min_word_count:
            articles = articles.filter(word_count__gte=min_word_count)
        if max_word_count:
            articles = articles.filter(word_count__lte=max_word_count)
        if channel_id:
            articles = articles.filter(channel__id=channel_id)

        paginator = LimitOffsetPagination()
        articles = paginator.paginate_queryset(articles, request)

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Adding Swagger data
    @swagger_auto_schema(request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'url': openapi.Schema(type=openapi.TYPE_STRING),
                                 'channel': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),
                         manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer 'Token'", type=openapi.TYPE_STRING)],
                         responses={200: openapi.Response('Returns an article', ArticleSerializer)},
                         operation_description='Add a new article')
    # Add a new article
    def post(self, request, *args, **kwargs):
        url = request.data.get('url')
        data = {'url':url, 'user':request.user.id, 'channel':request.data.get('channel')}
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            # If it is not possible to open the url, return an error
            try:
                page = urlopen(url).read()
            except:
                data={"message":"We are not able to open the url, please try another url."}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()
            # Caculate the word count in the background with redis and celery
            update_article_info.delay(serializer.data['id'])
            # Return the data for the new article immediately 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## Get the detail of an article or Delete it
class ArticleDetail(APIView):
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404
    
     
    @swagger_auto_schema(responses={200: openapi.Response('Returns an article', ArticleSerializer)},
                         operation_description='Get an article by ID')
    def get(self, request, pk):
        article = self.get_object(pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer 'Token'", type=openapi.TYPE_STRING)],
                         operation_description='Delete an article by ID')
    def delete(self, request, pk, format=None):
        article = self.get_object(pk=pk)
        if article.user:
            if article.user.id == request.user.id:
                article.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

## Show the list of channels and Add a new channel  
class ChannelList(APIView):
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(responses={200: openapi.Response('Returns a list of channels', ChannelSerializer)},
                         operation_description='Get the list of channels')
    def get(self, request, *args, **kwargs):
        channels = Channel.objects.all()
        serializer = ChannelSerializer(channels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'name': openapi.Schema(type=openapi.TYPE_STRING)
                             },
                         ),
                         manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer 'Token'", type=openapi.TYPE_STRING)],
                         responses={200: openapi.Response('Returns a channel', ChannelSerializer)},
                         operation_description='Add a new channel')
    def post(self, request, *args, **kwargs):
        name = request.data.get('name')
        data = {'name':name, 'user':request.user.id}
        serializer = ChannelSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

## Get the detail of a channel or Delete it
class ChannelDetail(APIView):
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_object(self, pk):
        try:
            return Channel.objects.get(pk=pk)
        except Channel.DoesNotExist:
            raise Http404

    @swagger_auto_schema(responses={200: openapi.Response('Returns a channel', ChannelSerializer)},
                         operation_description='Get a channel by ID')
    def get(self, request, pk):
        channel = self.get_object(pk=pk)
        serializer = ChannelSerializer(channel)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="Bearer 'Token'", type=openapi.TYPE_STRING)],
                         operation_description='Delete a channel by ID')
    def delete(self, request, pk, format=None):
        channel = self.get_object(pk=pk)
        if channel.user:
            if channel.user.id == request.user.id:
                channel.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
        
        