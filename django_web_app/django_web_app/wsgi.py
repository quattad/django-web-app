"""
WSGI config for django_web_app project.

It exposes the WSGI callable as a module-level variable named ``application``.
Allows web application to communicate with the web server

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_web_app.settings')

application = get_wsgi_application()
