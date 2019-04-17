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

DEBUG = env('DJANGO_DEBUG')
SECRET_KEY = env('DJANGO_SECRET_KEY')
SOCIAL_AUTH_RAISE_EXCEPTIONS = os.environ.get('SOCIAL_AUTH_RAISE_EXCEPTIONS')
SOCIAL_AUTH_FACEBOOK_API_VERSION = '2.8'
LOGIN_ERROR_URL = '/'

# social auth keys
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("GoogleKey", "none")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("GoogleSecret", "none")

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("FbKey", "none")
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("FbSecret", "none")

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
