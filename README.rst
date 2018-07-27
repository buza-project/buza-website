Buza
====

This is the code for Buza mobi site

Getting started
---------------
Requirements::

    - python3.6
    - For instructions on how to use python3.6 by default:
    http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/
    - For instructions on how to use virtualenv with python3.6:
    https://stackoverflow.com/questions/47822740/how-to-use-virtualenv-with-python3-6-on-ubuntu-16-04

To set up your working directory::

    $ mkdr build
    $ cd build
    $ mkdr media_root
    $ cd ..

To set up environment::

    $ virtualenv -p python3 ve
    $ source ve/bin/activate
    $ pip3 install -e .
    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    $ ./manage.py runserver

Or, using ``pipenv`` (Recommended)::

    $ cp .env.example .env
    * update DJANGO_DATABASE_URL in the .env file to direct your relative url
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


Git pre-commit hook
-------------------

To run our main quick checks before each commit, add the following to ``.git/hooks/pre-commit``::

    #!/bin/sh -e

    mypy -i src tests
    flake8
    isort --check-only

