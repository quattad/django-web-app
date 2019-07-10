from django.shortcuts import render, redirect
from django.contrib import messages  # specify what messages you want to add
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

"""
Message types:
message.debug
message.info
message.success
message.warning
"""

# Create a register view
"""
Usually if you build from scratch, need to rewrite a lot of form validations, etc
Best to create python classes that can generate HTML
Use user creation form 
"""


def register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():  # performs backend checks
            form.save()  # hash password to make sure it is secure, save to database.
            username = form.cleaned_data.get('username')  # validated form data will be in form.cleaned_data dictionary
            messages.success(request, f'Account created for {username}! You can now log in.')  # show success message
            return redirect('login') # TODO redirect user back to homepage
    return render(request, 'users/register.html', {'form': form})  # pass in form so that it can be accessed within the template


@login_required  # decorators add functionality to existing function
def profile(request):
    if request.method == 'GET':
        u_form = UserUpdateForm(instance=request.user)   # can populate form by passing in instance of object that it expects
        p_form = ProfileUpdateForm(instance=request.user.profile)
    else:
        u_form = UserUpdateForm(request.POST, instance=request.user)  # pass in POST data as well
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')  # show success message
            return redirect('profile')
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)  # why can just pass in context?
