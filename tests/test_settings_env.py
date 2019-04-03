import importlib
import os
from typing import Any, Dict
from unittest import mock

from buza import settings_base


def _get_settings(settings_module: object) -> Dict[str, Any]:
    """
    Helper: Render a Django settings module as a dictionary.
    """
    _vars: Dict[str, Any] = vars(settings_module)
    return {
        name: value for (name, value) in _vars.items()
        if name.isupper()
    }


def test_settings_env() -> None:
    """
    Verify that `buza.settings_env` renders as expected.
    """
    # Patch the environment with test variables.
    test_environ = {
        'BASE_DIR': '/base',
        'DJANGO_SECRET_KEY': 'secret key',
    }
    with mock.patch.dict(os.environ, test_environ, clear=True):
        from buza import settings_env
        importlib.reload(settings_env)  # Make sure this gets reloaded.

    expected_settings = {
        # Use buza.settings_base as a base, so we only list the additions here.
        **_get_settings(settings_base),
        'DEBUG': False,
        'SECRET_KEY': 'secret key',
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'HOST': '',
                'NAME': '/base/buza.sqlite3',
                'PASSWORD': '',
                'PORT': '',
                'USER': '',
            },
        },
        'STATIC_ROOT': '/base/static_root',
        'STATIC_URL': '/static/',
        'MEDIA_ROOT': '/base/media_root',
        'MEDIA_URL': '/media/',
        'LANGUAGE_CODE': 'en-ZA',
        'TIME_ZONE': 'Africa/Johannesburg',
        'LOGIN_ERROR_URL': '/',
        'SOCIAL_AUTH_FACEBOOK_API_VERSION': '2.8',
        'SOCIAL_AUTH_FACEBOOK_KEY': 'none',
        'SOCIAL_AUTH_FACEBOOK_SECRET': 'none',
        'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY': 'none',
        'SOCIAL_AUTH_RAISE_EXCEPTIONS': False,
        'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET': 'none',
        'ALLOWED_HOSTS': ['127.0.0.1', '0.0.0.0'],
    }
    assert expected_settings == _get_settings(settings_env)
