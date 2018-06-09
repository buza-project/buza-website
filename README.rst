gem
=========================

This is an application scaffold for Molo_.

Getting started
---------------
In a separate terminal::

	$ redis-server

To set up enviroment::

    $ virtualenv ve
    $ source ve/bin/activate
    $ pip install -e .
    $ ./manage.py migrate
    $ ./manage.py createsuperuser
    $ ./manage.py runserver


To deactivate server and virtual environment:
---------------
	press CTRL R
	$ deactivate

You can now connect access the demo site on http://localhost:8000

To get started::

	* log in to : http://localhost:8000

.. _Molo: https://molo.readthedocs.org
