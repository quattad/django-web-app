from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from quotes.views import home
from mixer.backend.django import mixer
import pytest

# Import test engines
from django.test import TestCase
from selenium import webdriver

# Import necessary models for test databases
from ..models import Quote  # import from one dir up

@pytest.mark.django_db
class TestHomeViews(TestCase):

    @classmethod  # ensure class parameter gets passed
    def setUpClass(cls):  # pass in class instance
        """
        Instantiate items that will be repeated throughout tests to prevent
        repeated instantiation; saves time
        """
        super(TestHomeViews, cls).setUpClass()  # calls setUpClass of TestCase
        cls.factory = RequestFactory()

        # Create total of 10 Quotes to save in test database
        quotes = mixer.cycle(10).blend(Quote)
        for quote in quotes:
            quote.save()

    def test_database(self):
        """
        Check if database works
        """
        quote_from_db = mixer.blend(Quote, id=mixer.SELECT)
        assert quote_from_db in Quote.objects.all()

    def test_database_total(self):
        """
        Check if database successfully saved 5 objects generated from mixer
        """
        assert len(Quote.objects.all()) == 10

    def test_quotes_home_view_authenticated(self):
        """
        Check only authenticated users can access home view
        """
        path = reverse('quotes-home')
        request = self.factory.get(path)  # create new instance with RF, get(path)
        request.user = mixer.blend(User)  # creates new user instance

        response = home(request)
        assert response.status_code == 200  # check if request was successful

    def test_quotes_home_view_unauthenticated(self):
        """
        Check unauthenticated users cannot access home view
        """
        path = reverse('quotes-home')
        request = self.factory.get(path)  # create new instance with RF, get(path)
        request.user = AnonymousUser()  # creates new user instance

        response = home(request)
        assert 'login' in response.url   # check if request was successful. 302 is redirect code - should be to login view

    def test_quotes_home_view_url_exists_at_desired_location(self):
        """
        Checks if page accessible via url i.e. /quotes
        """
        request = self.factory.get('/quotes/')
        request.user = mixer.blend(User)
        response = home(request)

        self.assertEqual(response.status_code, 200)

    def test_quotes_home_view_url_accessible_by_name(self):
        """
        Checks if page accessible via name in urls.py i.e. quotes-home
        """
        request = self.factory.get('/quotes/')
        request.user = mixer.blend(User)
        response = home(request)
        
        self.assertEqual(response.status_code, 200)

    def test_quotes_home_view_uses_correct_template(self):
        """
        Checks if page renders template quotes-home.html
        """
        request = self.factory.get(reverse('quotes-home'))
        user_1 = mixer.blend(User)
        request.user = user_1
        response = home(request)
        self.assertEqual(response.status_code, 200)

        self.client.force_login(user_1)
        response = self.client.get(reverse('quotes-home'))
        self.assertTemplateUsed(response, 'quotes/home.html')

    def test_quotes_home_view_pagination_five(self):
        """
        Checks if pagination is successful with 10 quotes
        """
        # Test if request to view returns status code 200
        request = self.factory.get(reverse('quotes-home'))
        request.user = mixer.blend(User)
        response = home(request)
        self.assertEqual(response.status_code, 200)
        
        self.client.force_login(request.user)
        response = self.client.get(reverse('quotes-home'))
        print(response.context)

        self.assertTrue('quotes' in response.context)
        self.assertTrue(response.context['quotes'].has_other_pages())
    
    # def test_quotes_home_view_lists_all_quotes 
        """
        Checks if second page has only 1 quote since 4 quotes per page by default
        """

    # def test_quotes_home_view_quote_fetch_quotes_from_db(self):
        """
        Checks if existing quotes in the database can be fetched successfully and
        no of likes, no of favourites, boolean fields check_liked and check_favourited
        fetched successfully.
        See check = Quotes.objects.filter... line 
        """

# class TestFavouritesView(TestCase):