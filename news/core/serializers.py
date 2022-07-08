from rest_framework import serializers
from .models import Channel, Article
from .utils import webpage_info

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'user', 'created']

class ArticleSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Article
        fields = ['id', 'url', 'title', 'word_count', 'user', 'created', 'channel']
        read_only_fields = ['title', 'word_count', 'content']
