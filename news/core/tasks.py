import logging
 
from django.urls import reverse
from news.celery import app
from .models import Article 
from .utils import webpage_info

@app.task
def update_article_info(article_id):
    article = Article.objects.get(id=article_id)
    article.title, article.word_count, article.content = webpage_info(article.url)
    article.save()