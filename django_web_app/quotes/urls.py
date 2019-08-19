from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='quotes-home'),
    path('favourites/', views.favourites, name='quotes-fav'),
    path('about/', views.about, name='quotes-about'),
    path('', views.landing, name='quotes-landing')
]