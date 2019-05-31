from django.contrib import admin
from .models import Post

# Include Post table administration under Django admin GUI
admin.site.register(Post)