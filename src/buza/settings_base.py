"""
Base Django settings for a buza-website instance.
"""
from django.urls import reverse_lazy


ROOT_URLCONF = 'buza.urls'

INSTALLED_APPS = [
    # Buza
    'buza',

    # Third-party apps
    'crispy_forms',
    'taggit',
    # 'social_django',

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
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

# Internationalization
USE_I18N = True
USE_L10N = True
USE_TZ = True


# django.contrib.auth
AUTH_USER_MODEL = 'buza.User'
LOGIN_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')
LOGIN_REDIRECT_URL = reverse_lazy('home')


# django-crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'
