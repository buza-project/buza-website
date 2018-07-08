Buza
=========================

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


To deactivate server and virtual environment:
---------------
	press CTRL R
	$ deactivate

You can now connect access the demo site on http://localhost:8000

To get started::

	* log in to : http://localhost:8000
