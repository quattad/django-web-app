from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Quote(models.Model):
    title = models.CharField(max_length=100, default='title')
    content = models.TextField(max_length=1000)
    author = models.CharField(max_length=100, default='author')
    date_posted = models.DateTimeField(default=timezone.now)
    user_liked = models.ManyToManyField(User, related_name='user_liked', blank=True)  # check if additional options need to be added
    user_favourited = models.ManyToManyField(User, related_name='user_favourited', blank=True)

    def __str__(self):
        return self.content[:10]


class AuthorQuote(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name