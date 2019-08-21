from django.shortcuts import render, redirect
from django.contrib import messages  # specify messages to add
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash 
from social_django.models import UserSocialAuth

"""
Message types: message.debug, message.info, message.success, message.warning
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


@login_required 
def profile(request):
    user = request.user
    
    if request.method == 'GET':
        u_form = UserUpdateForm(instance=request.user)   # populate form by passing in instance of object that it expects
        p_form = ProfileUpdateForm(instance=request.user.profile)
    else:
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')  # show success message
            return redirect('profile')
        else:
            messages.error(request, 'Please resolve the error below')

    # Allow users to link / delink their social media accounts
    # Facebook Linking
    try: 
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    # Google OAuth2 Linking
    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    # Check number of social accounts linked; do not allow delinkage if < 1
    check_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'facebook_login': facebook_login,
        'google_login': google_login,
        'check_disconnect': check_disconnect
    }

    return render(request, 'users/profile.html', context)

@login_required
def change_password(request):
    if request.method == "GET":
        password_form = PasswordChangeForm(request.user)
    if request.method == "POST":
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)  # creates and updates new session hash
            messages.success(request, "Your password was successfully changed!")
            return redirect('profile')
        else:
            messages.error(request, 'Password change error! The following errors were found: ')
    return render(request, 'users/change-password.html', {'password_form':password_form})