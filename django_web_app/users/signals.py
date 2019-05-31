# Shouldn't put in models.py file to avoid problems with importing

from django.db.models.signals import post_save  # gets fired after an object is saved. should get a signal once user is createds
from django.contrib.auth.models import User  # this will be the 'sender' i.e. what sends the signal. must have complementary receiver
from django.dispatch import receiver
from .models import Profile


# Runs every time a user is created
@receiver(post_save, sender=User)  # when a User is saved, then send signal. decorator receiver indicates that function create_profile is the receiver
def create_profile(sender, instance, created, **kwargs):  # all arguments are passed in by post_save
    if created:  # if a user is created, execute if statement
        Profile.objects.create(user=instance)


# Runs every time a user is saved
@receiver(post_save, sender=User)  # when a User is saved, then send signal. decorator receiver indicates that function create_profile is the receiver
def save_profile(sender, instance, created, **kwargs):  # all arguments are passed in by post_save
    instance.profile.save()  # instance is the user. must import signals into ready function of users.apps.py file