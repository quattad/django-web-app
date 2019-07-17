from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.
class Quote(models.Model):
    content = models.CharField(max_length=100)
    author_quote = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)
    user_liked = models.ManyToManyField(User)  # check if additional options need to be added

    def __str__(self):
        return self.title[:10]


class AuthorQuote(models.Model):
    name = models.CharField(max_length=100)
