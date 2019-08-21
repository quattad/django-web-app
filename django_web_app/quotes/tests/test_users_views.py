from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from users.views import register, profile, change_password
from mixer.backend.django import mixer
import pytest

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

    def test_users_register_view_test_url_exists_at_desired_location(self):
        """
        Check that register URL exists
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get('/register/')

        self.assertEqual(response.status_code, 200)

    def test_users_register_view_test_url_accessible_by_name(self):
        """
        Check that register accessible by name 'register'
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)

############################################################################
#############################  USERS/PROFILE    ############################
############################################################################
class TestProfileViews(TestCase):

    @classmethod  # ensure class parameter gets passed
    def setUpClass(cls):  # pass in class instance
        """
        Instantiate items that will be repeated throughout tests to prevent
        repeated instantiation; saves time
        """
        super(TestProfileViews, cls).setUpClass()  # calls setUpClass of TestCase
        cls.factory = RequestFactory()
        cls.client = Client()

    def test_users_register_view_test_url_exists_at_desired_location(self):
        """
        Check that profile URL exists
        """

        self.client.force_login(mixer.blend(User))
        response = self.client.get('/profile/')

        self.assertEqual(response.status_code, 200)

    def test_users_profile_view_test_url_accessible_by_name(self):
        """
        Check that profile accessible by name 'profile'
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)    

    ######################### AUTHENTICATION #########################
    def test_users_profile_view_authenticated(self):
        """
        Check only authenticated users can access profile
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('profile'))

        assert response.status_code == 200  # check if request was successful

    def test_users_profile_view_unauthenticated(self):
        """
        Check if unauthenticated users cannot access profile view and are redirected to login page
        """
        response = self.client.get(reverse('profile'))

        self.assertRedirects(response, '%s?next=%s' % (reverse('login'), reverse('profile')))


    ######################### RESPONSE ##########################
    def test_users_views_profile_get_response_success(self):
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)

    def test_users_views_profile_post_response_success(self):
        self.client.force_login(mixer.blend(User))
        response = self.client.post(reverse('profile'))

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
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('change-password'))

        self.assertEqual(response.status_code, 200)

    def test_users_change_password_views_post_response_success(self):
        self.client.force_login(mixer.blend(User))
        response = self.client.post(reverse('change-password'))

        self.assertEqual(response.status_code, 200)