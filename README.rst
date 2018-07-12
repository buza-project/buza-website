Buza
====

This is the code for Buza mobi site

Getting started
---------------
To set up environment::

    $ virtualenv ve
    $ source ve/bin/activate
    $ pip install -e .
    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    $ ./manage.py runserver

Or, using ``pipenv``::

    $ cp .env.example .env
    $ pipenv install --dev
    $ pipenv shell
    $ django-admin migrate
    $ django-admin createsuperuser
    $ django-admin runserver


Running checks and tests
------------------------

To run all the static checks and tests, invoke Tox::

    $ tox

To run the checks and tests individually, see the "commands" section of ``tox.ini``.
