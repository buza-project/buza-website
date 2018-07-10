"""
Base Django settings for a buza-website instance.
"""
from django.urls import reverse_lazy


ROOT_URLCONF = 'project.urls'

INSTALLED_APPS = [
    # Buza
    'buza',
    'project.accounts',
    'project.boards',
    'project.vote',

    # Third-party apps
    'taggit',
    'tinymce',
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

LOGIN_REDIRECT_URL = reverse_lazy('all_questions')
AUTH_USER_MODEL = 'buza.BuzaUser'
