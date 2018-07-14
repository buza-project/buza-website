"""
Django settings module buza-website for Tox.
"""

from buza.settings_base import *  # noqa: F401


SECRET_KEY = 'buza-website Tox'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

# XXX: For django-tinymce:
STATIC_URL = '/static/'
