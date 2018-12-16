"""
Django settings module for buza-website using django-environ.
"""
import os

import environ

from buza.settings_base import *  # noqa: F401


env = environ.Env()

# Obtain a base instance directory.
base_dir = env.path('BASE_DIR')


DEBUG = env('DJANGO_DEBUG', default=False)
SECRET_KEY = env('DJANGO_SECRET_KEY')
SOCIAL_AUTH_RAISE_EXCEPTIONS = env('SOCIAL_AUTH_RAISE_EXCEPTIONS', default=False)
SOCIAL_AUTH_FACEBOOK_API_VERSION = '2.8'

DATABASES = {
    'default': env.db(
        'DJANGO_DATABASE_URL',
        default=f'sqlite:///' + base_dir('buza.sqlite3'),
    ),
}

STATIC_ROOT = env('DJANGO_STATIC_ROOT', default=base_dir('static_root'))
STATIC_URL = env('DJANGO_STATIC_URL', default='/static/')

MEDIA_ROOT = env('DJANGO_MEDIA_ROOT', default=base_dir('media_root'))
MEDIA_URL = env('DJANGO_MEDIA_URL', default='/media/')

# Internationalization
LANGUAGE_CODE = env('DJANGO_LANGUAGE_CODE', default='en-ZA')
TIME_ZONE = env('DJANGO_TIME_ZONE', default='Africa/Johannesburg')

# social auth keys
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("GoogleKey", "none")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("GoogleSecret", "none")

SOCIAL_AUTH_FACEBOOK_KEY = os.environ.get("FbKey", "none")
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ.get("FbSecret", "none")
