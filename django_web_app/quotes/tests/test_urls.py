from django.urls import reverse, resolve

class TestUrls:
    def test_quotes_home_url(self):
        """
        One assert statement per function
        Check 'quotes-home' url
        """
        path = reverse('quotes-home')  # if any keyword arguments in url e.g. /<int:pk>, must specify kwarg
        assert resolve(path).view_name == 'quotes-home'  # resolve is opposite of reverse; takes path and finds view name
