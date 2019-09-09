from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing, name='quotes-landing'),
    path('home/', views.home, name='quotes-home'),
    path('favourites/', views.favourites, name='quotes-fav')
]