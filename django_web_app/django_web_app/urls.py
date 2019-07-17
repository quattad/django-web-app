"""django_web_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as users_views

# Import libraries to manage static files
from django.conf import settings
from django.conf.urls.static import static

# Use include for routing, should be the best way
urlpatterns = [
    path('', include('blog.urls')),
    path('quotes/', include('quotes.urls')),
    path('admin/', admin.site.urls),
    path('register/', users_views.register, name='register'),
    path('profile/', users_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),  # pass location as an argument into as_view function to change default directory for html
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout')
]

# Add this only if we are in debug mode. i.e. not ideal for production!
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # add static media URL