Buza
====

This is the code for Buza mobi site

Getting started
---------------

Make sure you have the following tools installed:

* Pipenv_
* Yarn_

.. _Pipenv: https://docs.pipenv.org/install/#installing-pipenv
.. _Yarn: https://yarnpkg.com/lang/en/docs/install/

Django requires the ``DJANGO_SETTINGS_MODULE`` environment variable to run.
To set this and get started, copy the ``env.example`` file to ``.env``::

    $ cp .env.example .env

(Pipenv will `automatically load`_ the environment variables defined in this ``.env`` file.)

.. _`automatically load`: https://docs.pipenv.org/advanced/#automatic-loading-of-env

Fetch the Yarn dependencies::

    $ yarn

Install the Pipenv dependencies, and activate the environment::

    $ pipenv install --dev
    $ pipenv shell

Initialise the database, and run the Django development server::

    $ django-admin migrate
    $ django-admin createsuperuser
    $ django-admin runserver


Running checks and tests
------------------------

To run all the static checks and tests, invoke Tox::

    $ tox

To run the checks and tests individually, see the "commands" section of ``tox.ini``.


Git pre-commit hook
-------------------

To run our main quick checks before each commit, add the following to ``.git/hooks/pre-commit``::

    #!/bin/sh -e

    mypy -i src tests
    flake8
    isort --check-only

