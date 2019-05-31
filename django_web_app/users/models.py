from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # one to one relationship with User model. CASCADE-> if User is deleted, Profile will be deleted
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')  # images uploaded to profile_pics directory

    def __str__(self):
        return f'Profile: {self.user.username}'  # will only be updated if migrations are saved. 'python manage.py makemigrations' followed by 'python manage.py migrate'

    # Must overwrite default save method to use Pillow to resize images
    # Method is run after model is saved. Already exists in parent class but we want to create our own customized one
    # *args, **kwargs allow for variable number of
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # run parent class save method. large image should be saved, however we want to resize it.
        img = Image.open(self.image.path)  # open image of current instance

        # check if image is greater than 300px
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)  # tuple of max size
            img.thumbnail(output_size)
            img.save(self.image.path)  # save back to same path to overwrite self.image.path