from django.urls import path
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView)
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),  # convert to an actual view using method as_view(). looks for naming convention <app>/<model>__<viewtype>.html
    #  create URL pattern that contains variable to redirect to blog e.g. post/1, post/2. pk is primary key of post to view, specify with int
    # stick to conventions and use pk
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/create', PostCreateView.as_view(), name='post-create'),  # follows same template as update. create new template called 'post_form.html'
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]