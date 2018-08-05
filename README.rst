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

Copy the example ``.env`` file,
and edit the example paths to point to your working directory::

    $ cp .env.example .env

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

