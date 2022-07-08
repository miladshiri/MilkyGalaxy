from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ArticleList, ChannelList, ArticleDetail, ChannelDetail


urlpatterns = [
    path('articles/', ArticleList.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetail.as_view(), name='article_datail'),
    path('channels/', ChannelList.as_view(), name='channels'),
    path('channels/<int:pk>/', ChannelDetail.as_view(), name='channel_detail'),
]

