"""
Django settings module for buza-website using django-environ.
"""
import environ

from buza.settings_base import *  # noqa: F401


env = environ.Env()


DEBUG = env('DJANGO_DEBUG', default=False)
SECRET_KEY = env('DJANGO_SECRET_KEY')

DATABASES = {
    'default': env.db('DJANGO_DATABASE_URL'),
}

STATIC_ROOT = env('DJANGO_STATIC_ROOT')
STATIC_URL = env('DJANGO_STATIC_URL', default='/static/')

MEDIA_ROOT = env('DJANGO_MEDIA_ROOT')
MEDIA_URL = env('DJANGO_MEDIA_URL', default='/media/')
