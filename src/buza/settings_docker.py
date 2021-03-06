"""
Django settings module for buza-website using django-environ.
The settings are used by the docker file
"""
import os

import environ

from buza.settings_base import *  # noqa: F401


env = environ.Env()

# Obtain a base instance directory.

DEBUG = False
TEMPLATE_DEBUG = False
COMPRESS_OFFLINE = True

SECRET_KEY = env('DJANGO_SECRET_KEY')
SOCIAL_AUTH_RAISE_EXCEPTIONS = os.environ.get('SOCIAL_AUTH_RAISE_EXCEPTIONS')
SOCIAL_AUTH_FACEBOOK_API_VERSION = '2.11'
LOGIN_ERROR_URL = '/'
LOGIN_REDIRECT_URL = os.environ.get('redirect_uri')

SOCIAL_AUTH_LOGIN_REDIRECT_URL = os.environ.get('SOCIAL_AUTH_LOGIN_REDIRECT_URL')
SOCIAL_AUTH_SANITIZE_REDIRECTS = os.environ.get('SOCIAL_AUTH_SANITIZE_REDIRECTS')
USE_X_FORWARDED_HOST = os.environ.get('USE_X_FORWARDED_HOST')
ROOT_URL = os.environ.get('ROOT_URL')
# social auth keys
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("GoogleKey", "none")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("GoogleSecret", "none")

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("FbKey", "none")
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("FbSecret", "none")

ALLOWED_HOSTS = ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'buza.co.za']

# settings.py
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "buza_answers"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 600,
    },
}
