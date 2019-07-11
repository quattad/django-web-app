from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Each class is going to be its own table in the database
class Post(models.Model):
    title = models.CharField(max_length=100)  # character field
    content = models.TextField(max_length=1000)
    date_posted = models.DateTimeField(default=timezone.now)  # don't pass in now as a function
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # if author is deleted, delete their post as well. however, user is not deleted alongside post; one-way deletion.

# Function to generate string representing Post object
    def __str__(self):
        return self.title

    # redirect vs reverse: redirect simply sends user to url; reverse sends back the entire URL as a string, let view handle the URL

    def get_absolute_url(self):  # get URL from any specific instance of a post
        return reverse('post-detail', kwargs={'pk': self.pk})  # get full path to post-detail route. requires a specific post with a primary key