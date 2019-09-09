from django.test import TestCase, RequestFactory, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from quotes.views import home, favourites
from mixer.backend.django import mixer
import pytest

# For messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware

# Import necessary models for test databases
from ..models import Quote  # import from one dir up

############################################################################
#############################  QUOTES/HOME   ###############################
############################################################################
@pytest.mark.django_db
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestHomeViews(TestCase):
    @classmethod  # ensure class parameter gets passed
    def setUpClass(cls):  # pass in class instance
        """
        Instantiate items that will be repeated throughout tests to prevent
        repeated instantiation; saves time
        """
        super(TestHomeViews, cls).setUpClass()  # calls setUpClass of TestCase
        cls.factory = RequestFactory()
        cls.client = Client()

        # Create total of 10 Quotes to save in test database
        quotes = mixer.cycle(10).blend(Quote)
        for quote in quotes:
            quote.save()

        # Create liked and favourited quotes
        quote_1 = Quote.objects.get(id=1)
        quote_2 = Quote.objects.get(id=2)

        quote_1.check_liked = True
        quote_2.check_favourited = True

        quote_1.save()
        quote_2.save()

    def test_database(self):
        """
        Check if database works
        """
        quote_from_db = mixer.blend(Quote, id=mixer.SELECT)
        assert quote_from_db in Quote.objects.all()

    def test_database_total(self):
        """
        Check if database successfully saved 10 objects generated from mixer
        """
        assert len(Quote.objects.all()) == 10

    ######################### AUTHENTICATION #########################

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

    ######################### RESPONSE #########################

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
        request = self.factory.get(reverse('quotes-home'))

        request.user = mixer.blend(User)
        response = home(request)
        
        self.assertEqual(response.status_code, 200)

    def test_quotes_home_view_uses_correct_template(self):
        """
        Checks if page renders template quotes-home.html
        """
        request = self.factory.get(reverse('quotes-home'))
        request.user = mixer.blend(User)
        response = home(request)
        self.assertEqual(response.status_code, 200)

        self.client.force_login(request.user)
        response = self.client.get(reverse('quotes-home'))
        self.assertTemplateUsed(response, 'quotes/home.html')

    def test_quotes_home_view_pagination_five(self):
        """
        Checks if pagination is successful with 10 quotes
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('quotes-home'))

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

    ######################### POST REQUESTS / DATA MANIPULATION #########################
    def test_quotes_home_view_post_like_quote(self):
        """
        Check user sending a submit_user_like POST request / liking new quote
        """

        user_1 = mixer.blend(User)
        self.client.force_login(user_1)
        quote = mixer.blend(Quote)
        response = self.client.post(reverse('quotes-home'), {
            "submit_user_like": quote.id,
            })
        
        self.assertEqual(response.status_code, 302)

    def test_quotes_home_view_post_unlike_quote_already_liked(self):
        """
        Check user sending a submit_user_like POST request for Quote entry
        with check_liked == True / unlike quote 
        """

        user_1 = mixer.blend(User)
        self.client.force_login(user_1)

        response = self.client.post(reverse('quotes-home'), { 
            "submit_user_like": 1
        })
        
        self.assertEqual(response.status_code, 302)

    def test_quotes_home_view_post_fav_quote_not_fav(self):
        """
        Check user sending a submit_user_fav POST request / favouriting quote
        """

        user_1 = mixer.blend(User)
        self.client.force_login(user_1)
        quote = mixer.blend(Quote)

        response = self.client.post(reverse('quotes-home'), {
            "submit_user_favourite": quote.id,
            })
        
        self.assertEqual(response.status_code, 302)

    def test_quotes_home_view_post_unfav_quote_already_fav(self):
        """
        Check user sending a submit_user_like POST request for Quote entry
        with check_liked == True / unlike quote 
        """

        user_1 = mixer.blend(User)
        self.client.force_login(user_1)

        response = self.client.post(reverse('quotes-home'), {
            "submit_user_favourite": 2
        })
        
        self.assertEqual(response.status_code, 302)

    ######################### CONDITIONALS #########################
    def test_quotes_home_view_post_anonymous_like(self):
        """
        Checks that POST request for both Like if unauthenticated user, should redirect to login page
        """
        
        response = self.client.post(reverse('quotes-home'), {
            "submit_user_like": 1
            })

        self.assertRedirects(response, '%s?next=%s' % (reverse('login'), reverse('quotes-home')))

    def test_quotes_home_view_post_anonymous_fav(self):
        """
        Checks that POST request for both Like if unauthenticated user, should redirect to login page
        """

        response = self.client.post(reverse('quotes-home'), {
            "submit_user_favourite": 2
            })

        self.assertRedirects(response, '%s?next=%s' % (reverse('login'), reverse('quotes-home')))

############################################################################
#############################     FAVOURITES     ###########################
############################################################################

@pytest.mark.django_db
@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestFavouritesView(TestCase):
    @classmethod  # ensure class parameter gets passed
    def setUpClass(cls):  # pass in class instance
        """
        Instantiate items that will be repeated throughout tests to prevent
        repeated instantiation; saves time
        """
        super(TestFavouritesView, cls).setUpClass()  # calls setUpClass of TestCase
        cls.factory = RequestFactory()
        cls.client = Client()

        # Create total of 10 Quotes to save in test database
        quotes = mixer.cycle(10).blend(Quote)
        for quote in quotes:
            quote.save()

        # Create favourited quote
        quote_1 = Quote.objects.get(id=1)
        quote_1.check_favourited = True
        quote_1.save()

    ######################### AUTHENTICATION #########################
    def test_quotes_fav_view_authenticated(self):
        """
        Check only authenticated users can access fav view
        """
        path = reverse('quotes-fav')
        request = self.factory.get(path)  # create new instance with RF, get(path)
        request.user = mixer.blend(User)  # creates new user instance

        response = favourites(request)
        assert response.status_code == 200  # check if request was successful

    def test_quotes_fav_view_unauthenticated(self):
        """
        Check unauthenticated users cannot access home view
        """
        path = reverse('quotes-fav')
        request = self.factory.get(path)  # create new instance with RF, get(path)
        request.user = AnonymousUser()  # creates new user instance

        response = favourites(request)
        assert 'login' in response.url   # check if request was successful. 302 is redirect code - should be to login view
    

    ######################### RESPONSE ##########################
    def test_quotes_favourites_view_get_response_success(self):
        self.client.force_login(mixer.blend(User))
        response = self.client.get(reverse('quotes-fav'))

        self.assertEqual(response.status_code, 200)

    def test_quotes_favourites_view_post_response_success(self):
        self.client.force_login(mixer.blend(User))
        response = self.client.post(reverse('quotes-fav'))

        self.assertEqual(response.status_code, 302)

    ######################### POST REQUESTS / DATA MANIPULATION #########################

    def test_quotes_fav_view_post_unfav_quote(self):
        """
        Check user sending a submit_user_favourite POST request to unfav quote
        """
        self.client.force_login(mixer.blend(User))
        response = self.client.post(reverse('quotes-fav'), {
            "submit_user_favourite": 1,
            })
        
        self.assertEqual(response.status_code, 302)

    ######################### CONDITIONALS #########################
    def test_quotes_fav_view_invalid_request(self):
        """
        Check that 404 is returned when request is not GET or POST
        """

        self.client.force_login(mixer.blend(User))

############################################################################
#############################     LANDING        ###########################
############################################################################
class TestLandingView(TestCase):
    @classmethod  # ensure class parameter gets passed
    def setUpClass(cls):  # pass in class instance
        """
        Instantiate items that will be repeated throughout tests to prevent
        repeated instantiation; saves time
        """
        super(TestLandingView, cls).setUpClass()  # calls setUpClass of TestCase
        cls.factory = RequestFactory()
        cls.client = Client()

    def test_quotes_landing_url_get_response_success(self):
        """
        Returns landing page; simple get request should succeed
        """
        response = self.client.get(reverse('quotes-landing'))
        self.assertEqual(response.status_code, 200)