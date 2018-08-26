"""
Django settings module for buza-website using django-environ.
"""
import os
from pathlib import Path

# Configure Django App for Heroku.
import django_heroku
import environ

from buza.settings_base import *  # noqa: F401


# Assume we're running from a Git checkout directory.
checkout_dir: Path = Path(__file__).parent.parent.parent

env = environ.Env()


if 'BASE_DIR' not in os.environ:
    os.environ['BASE_DIR'] = str(checkout_dir.joinpath('buza-instance'))
    Path(os.environ['BASE_DIR']).mkdir(exist_ok=True)
# Obtain a base instance directory.


DEBUG = env('DJANGO_DEBUG', default=False)
SECRET_KEY = env('DJANGO_SECRET_KEY', default="buza.key")
'''
DATABASES = {
    'default': env.db(
        'DJANGO_DATABASE_URL',
        default=f'sqlite:///' + base_dir('buza.sqlite3'),
    ),
 }
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'buza',
        'USER': 'sewagodimo',
        'PASSWORD': 'educationcanchangetheworld',
        'HOST': '',
        'PORT': '',
    },
}

LANGUAGE_CODE = env('DJANGO_LANGUAGE_CODE', default='en-ZA')
TIME_ZONE = env('DJANGO_TIME_ZONE', default='Africa/Johannesburg')


# Set a few more defaults for development.
os.environ.setdefault('DJANGO_SECRET_KEY', 'buza-website example dev')
os.environ.setdefault('DJANGO_DEBUG', 'True')

django_heroku.settings(locals())
