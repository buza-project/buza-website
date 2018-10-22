"""
Like `settings_env`, but set more development defaults.

The idea is that ``DJANGO_SETTINGS_MODULE=buza.settings_env_dev``
should provide a usable starting development configuration
but still allow overriding any individual settings.
"""
import os
from pathlib import Path


# Assume we're running from a Git checkout directory.
checkout_dir: Path = Path(__file__).parent.parent.parent
assert checkout_dir.joinpath('.git').exists(), checkout_dir

# If BASE_DIR is not set, set and create a default for it.
if 'BASE_DIR' not in os.environ:
    os.environ['BASE_DIR'] = str(checkout_dir.joinpath('buza-instance'))
    Path(os.environ['BASE_DIR']).mkdir(exist_ok=True)

# Set a few more defaults for development.
os.environ.setdefault('DJANGO_SECRET_KEY', 'buza-website example dev')
os.environ.setdefault('DJANGO_DEBUG', 'True')

STATICFILES_DIRS = [
    # Path to Yarn's packages
    str(checkout_dir.joinpath('node_modules')),
]

# Include the local host by default for development.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

from buza.settings_env import *  # noqa: F401 isort:skip
