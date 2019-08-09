from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  DeleteView,
                                  UpdateView)
from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all()  # pass in data from database
    }
    return render(request, 'blog/home.html', context)


# Should be a ListView
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # looking at <app>/<model>_<viewtype>.html. however, reset where it should look
    context_object_name = 'posts'  # either loop over object_list or set one more object in list view and set as 'posts'
    ordering = ['-date_posted']  # - sign changes the ordering from newest to oldest


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # actually not required, since by default the template name is <app>/<model>_<viewtype>.html


# LoginRequiredMixin allows PostCreateView class to inherit from LoginRequiredMixin class
class PostCreateView(LoginRequiredMixin, CreateView):
    # Must override form_valid method for create view; add author before form is submitted
    model = Post
    fields = ['title', 'content']

    # overriding form-valid method
    def form_valid(self, form):
        form.instance.author = self.request.user  # take form instance and set author to current logged in user
        return super().form_valid(form)  # run form_valid method on parent class 'super()'


# LoginRequiredMixin allows PostCreateView class to inherit from LoginRequiredMixin class
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # Must override form_valid method for create view; add author before form is submitted
    model = Post
    fields = ['title', 'content']

    # overriding form-valid method
    def form_valid(self, form):
        form.instance.author = self.request.user  # take form instance and set author to current logged in user
        return super().form_valid(form)  # run form_valid method on parent class 'super()'

    # UserPassesTestMixin will make use of test_func to check if certain passes are allowed
    def test_func(self):
        post = self.get_object() # get post that it is currently updating
        if self.request.user == post.author: # check if currently logged in user is current post author
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object() # get post that it is currently updating
        if self.request.user == post.author: # check if currently logged in user is current post author
            return True
        return False


def about(request):
    return render(request, 'blog/about.html',
                  {'title': 'About'}
                  )
