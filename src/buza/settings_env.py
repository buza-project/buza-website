"""
Django settings module for buza-website using django-environ.
"""
import environ

from buza.settings_base import *  # noqa: F401


env = environ.Env()

# Obtain a base instance directory.
base_dir = env.path('BASE_DIR')


DEBUG = env('DJANGO_DEBUG', default=False)
SECRET_KEY = env('DJANGO_SECRET_KEY')

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
