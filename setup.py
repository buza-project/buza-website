import os

from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

install_requires = [
    'Django==2.1',
    'django-environ==0.4.5',
    'django-heroku==0.3.1',
    'django-taggit==0.23.0',
    'flake8==3.5.0',
    'flake8-commas==2.0.0',
    'gunicorn==19.9.0',
    'idna==2.7',
    'isort==4.3.4',
    'mypy==0.620',
    'pluggy==0.7.1',
    'psycopg2==2.7.5',
    'psycopg2-binary==2.7.5',
    'pycodestyle==2.3.1',
    'pyflakes==1.6.0',
    'PyJWT==1.6.4',
    'Pillow==5.2.0',
    'pyparsing==2.2.0',
    'pytest==3.7.2',
    'pytest-django==3.4.2',
    'python3-openid==3.1.0',
    'requests==2.19.1',
    'requests-oauthlib==1.0.0',
    'setuptools-scm==3.1.0',
    'social-auth-app-django==2.1.0',
    'social-auth-core==1.7.0',
    'tox==3.2.1',
    'whitenoise==4.0',
]

setup(
    name='buza-website',
    description='buza',
    version='0.0.1',
    long_description=README,
    classifiers=[
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Ctrl Space',
    author_email='dev@buza.com',
    url='None',
    license='BSD',

    package_dir={'': 'src'},
    packages=find_packages('src'),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={},
)
