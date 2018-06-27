from gem.settings import *  # noqa: F401, F403
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'buza_test.db',
    }
}

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
        },
    },
}

DEBUG = True
CELERY_ALWAYS_EAGER = True

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
