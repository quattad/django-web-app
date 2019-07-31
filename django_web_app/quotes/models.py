from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Quote(models.Model):
    title = models.CharField(max_length=100, default='title')
    content = models.TextField(max_length=1000)
    author = models.CharField(max_length=100, default='author')
    date_posted = models.DateTimeField(auto_now_add=True)
    user_liked = models.ManyToManyField(User, related_name='user_liked', blank=True)  # check if additional options need to be added
    user_favourited = models.ManyToManyField(User, related_name='user_favourited', blank=True)
    no_user_likes = models.PositiveIntegerField(default=0)
    no_user_favourites = models.PositiveIntegerField(default=0)
    check_liked = models.BooleanField(default=False)
    check_favourited = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:10]

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)