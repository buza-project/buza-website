"""
Base Django settings for a buza-website instance.
"""
import os
from pathlib import Path

import environ
from django.urls import reverse_lazy


env = environ.Env()

# Assume we're running from a Git checkout directory.
checkout_dir: Path = Path(__file__).parent.parent.parent
assert checkout_dir.joinpath('.git').exists(), checkout_dir

ROOT_URLCONF = 'buza.urls'

INSTALLED_APPS = [
    # Buza
    'buza',

    # Third-party apps
    'crispy_forms',
    'taggit',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'django.contrib.humanize',
]

MIDDLEWARE = [
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]

AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.google.GooglePlusAuth',
    'django.contrib.auth.backends.ModelBackend',
]
# Internationalization
USE_I18N = True
USE_L10N = True
USE_TZ = True


# django.contrib.auth
AUTH_USER_MODEL = 'buza.User'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')
LOGIN_REDIRECT_URL = reverse_lazy('home')

# django-crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'


STATICFILES_DIRS = [
    # Path to Yarn's packages
    str(checkout_dir.joinpath('node_modules')),
]

# Include the local host by default for development.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

BASE_DIR = os.environ.get('BASE_DIR') or str(checkout_dir.joinpath('buza-instance'))
base_dir = env.path('BASE_DIR')


DATABASES = {
    'default': env.db(
        'DJANGO_DATABASE_URL',
        default=f'sqlite:///' + base_dir('buza.sqlite3'),
    ),
}

SECRET_KEY = 'secret-key'

MEDIA_ROOT = os.environ.get("MEDIA_ROOT", "media")

STATIC_ROOT = os.environ.get("STATIC_ROOT", "static")
STATIC_URL = env('DJANGO_STATIC_URL', default='/static/')

# Internationalization
LANGUAGE_CODE = env('DJANGO_LANGUAGE_CODE', default='en-ZA')
TIME_ZONE = env('DJANGO_TIME_ZONE', default='Africa/Johannesburg')
