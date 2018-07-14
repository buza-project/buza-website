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
        'DJANGO_SECRET_KEY': 'secret key',
        'DJANGO_DATABASE_URL': 'sqlite:////base/buza.sqlite',
        'DJANGO_STATIC_ROOT': '/base/static_root/',
        'DJANGO_MEDIA_ROOT': '/base/media_root/',
    }
    # Upstream issue: https://github.com/python/typeshed/pull/2173
    with mock.patch.dict(os.environ, test_environ, clear=True):  # type: ignore
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
                'NAME': '/base/buza.sqlite',
                'PASSWORD': '',
                'PORT': '',
                'USER': '',
            },
        },
        'STATIC_ROOT': '/base/static_root/',
        'STATIC_URL': '/static/',
        'MEDIA_ROOT': '/base/media_root/',
        'MEDIA_URL': '/media/',
    }
    assert expected_settings == _get_settings(settings_env)
