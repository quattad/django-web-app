from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.forms import PasswordChangeForm
from users.views import register, profile, change_password
from mixer.backend.django import mixer
import pytest

# For forms testing
from users.forms import UserRegisterForm

# For messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

# Import test engines
from django.test import TestCase
from selenium import webdriver

############################################################################
#############################  USERS/REGISTER   ############################
############################################################################
@pytest.mark.django_db
class TestRegisterViews(TestCase):

    @classmethod 
    def setUpClass(cls):
        super(TestRegisterViews, cls).setUpClass()
        cls.factory = RequestFactory()
        cls.client = Client()

    def test_users_views_register_test_url_exists_at_desired_location(self):
        """
        Check that register URL exists
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get('/register/')

        self.assertEqual(response.status_code, 200)

    def test_users_views_register_test_url_accessible_by_name(self):
        """
        Check that register accessible by name 'register'
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)

    ######################### RESPONSE ##########################
    def test_users_views_register_get_response_success(self):
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)

    def test_users_views_register_post_response_success(self):
        data = {'username': 'test1','email': 'test1@gmail.com','password1': 'Wowamazingpassword123!','password2': 'Wowamazingpassword123!'}
        response = self.client.post(reverse('register'), data)

        # Should redirect to login page after registration
        self.assertEqual(response.status_code, 302)

############################################################################
#############################  USERS/PROFILE  ##############################
############################################################################
class TestProfileViews(TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Instantiate items that will be repeated throughout tests to prevent
        repeated instantiation; saves time
        """
        super(TestProfileViews, cls).setUpClass()  # calls setUpClass of TestCase
        cls.factory = RequestFactory()
        cls.client = Client()

    def test_users_views_profile_url_exists_at_desired_location(self):
        """
        Check that profile URL exists
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get('/profile/')

        self.assertEqual(response.status_code, 200)

    def test_users_views_profile_url_accessible_by_name(self):
        """
        Check that profile accessible by name 'profile'
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)    

    ######################### AUTHENTICATION #########################
    def test_users_views_profile_authenticated(self):
        """
        Check only authenticated users can access profile
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('profile'))

        assert response.status_code == 200  # check if request was successful

    def test_users_views_profile_unauthenticated(self):
        """
        Check if unauthenticated users cannot access profile view and are redirected to login page
        """
        response = self.client.get(reverse('profile'))

        self.assertRedirects(response, '%s?next=%s' % (reverse('login'), reverse('profile')))


    ######################### RESPONSE ##########################
    def test_users_views_profile_get_response_success(self):
        """
        Check if GET request returns successful response
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)

    def test_users_views_profile_post_response_success(self):
        """
        Check if successful POST request to update profile results in a HttpResponseObject with status code 302
        """
        self.client.force_login(mixer.blend(User))

        data = {'username': 'test1','email': 'test1@gmail.com'}
        response = self.client.post(reverse('profile'), data)

        self.assertEqual(response.status_code, 302)
    
    def test_users_views_profile_post_response_failure(self):
        """
        Check if failed POST request to update profile results in error message and returns HttpResponseObject with status code 200
        """
        self.client.force_login(mixer.blend(User))

        data = {'username': '','email': 'test1@gmail.com'}
        response = self.client.post(reverse('profile'), data)

        self.assertEqual(response.status_code, 200)

############################################################################
########################   USERS/CHANGE_PASSWORD   #########################
############################################################################

class TestChangePasswordViews(TestCase):

    @classmethod  # ensure class parameter gets passed
    def setUpClass(cls):  # pass in class instance
        """
        Instantiate items that will be repeated throughout tests to prevent
        repeated instantiation; saves time
        """
        super(TestChangePasswordViews, cls).setUpClass()  # calls setUpClass of TestCase
        cls.factory = RequestFactory()
        cls.client = Client()

    def test_users_change_password_views_test_url_exists_at_desired_location(self):
        """
        Check URL exists
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get('/changepassword/')

        self.assertEqual(response.status_code, 200)

    def test_users_change_password_views_test_url_accessible_by_name(self):
        """
        Check that profile accessible by name 'changepassword'
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('change-password'))

        self.assertEqual(response.status_code, 200)    

    ######################### AUTHENTICATION #########################
    def test_users_change_password_view_authenticated(self):
        """
        Check only authenticated users can access profile
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('change-password'))

        assert response.status_code == 200  # check if request was successful

    def test_users_change_password_view_unauthenticated(self):
        """
        Check if unauthenticated users cannot access profile view and are redirected to login page
        """
        response = self.client.get(reverse('change-password'))

        self.assertRedirects(response, '%s?next=%s' % (reverse('login'), reverse('change-password')))

    ######################### RESPONSE ##########################
    def test_users_change_password_views_get_response_success(self):
        """
         Check successful POST request returns redirect to profile
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('change-password'))

        self.assertEqual(response.status_code, 200)

    def test_users_change_password_views_post_response_success(self):
        """
         Check successful POST request returns redirect to profile
        """
        user = mixer.blend(User)
        
        # Login user
        self.client.login(username=user.username, password=user.password)
        data = {'old_password': user.password, 'new_password1': 'Wowamazingpassword123!', 'new_password2': 'Wowamazingpassword123!'}

        response = self.client.post(reverse('change-password'), data)

        self.assertEqual(response.status_code, 302)

    def test_users_change_password_views_post_response_failure(self):
        """
        Check failed POST request returns status code 200 to load change password page with error msg
        """
        self.client.force_login(mixer.blend(User))

        # Pass in empty data
        data = {}

        response = self.client.post(reverse('change-password'), data)

        self.assertEqual(response.status_code, 200)