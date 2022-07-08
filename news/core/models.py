from django.db import models
from django.contrib.auth.models import User

class Channel(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    created = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)

    def __str__(self):
        return self.name


class Article(models.Model):
    url = models.URLField(max_length = 2048)
    channel = models.ForeignKey(Channel, on_delete = models.CASCADE)
    title = models.CharField(max_length=255, blank = True, null = True)
    word_count = models.IntegerField(blank = True, null = True)
    content = models.TextField(blank = True, null = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True)
    created = models.DateTimeField(auto_now_add = True, auto_now = False, blank = True)

    def __str__(self):
        return self.url[:20]

    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
    