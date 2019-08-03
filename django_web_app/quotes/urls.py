from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='quotes-home'),
    path('favourites/', views.favourites, name='quotes-fav')
]