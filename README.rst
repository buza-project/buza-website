Buza
====

This is the code for Buza mobi site

Getting started
---------------

With Vagrant
^^^^^^^^^^^^

The easiest way to get a development instance of Buza up and running is to use `Vagrant`_.

.. _`Vagrant`: https://www.vagrantup.com/

After installing Vagrant, run the following to provision a Buza virtual machine::

    vagrant up

(This will take a while the first time you run it, but will be faster on subsequent runs.)

To run the Django development server, you can execute the following command::

    vagrant ssh -c 'cd /vagrant && pipenv run django-admin runserver 0.0.0.0:8000'

You can also log into the virtual machine and activate the project,
in order to run other Django development commands. For example::

    $ vagrant ssh
    vagrant@ubuntu-bionic:~$ cd /vagrant
    vagrant@ubuntu-bionic:/vagrant$ pipenv shell
    Loading .env environment variables...
    Launching subshell in virtual environment…
    (vagrant-gKDsaKU3) vagrant@ubuntu-bionic:/vagrant$ django-admin check
    System check identified no issues (0 silenced).
    (vagrant-gKDsaKU3) vagrant@ubuntu-bionic:/vagrant$

When you're finished working, you can stop the Vagrant virtual machine by running ``vagrant halt``.
Running ``vagrant up`` again will restart it.

To destroy the virtual machine completely, run ``vagrant destroy``.


With Pipenv
^^^^^^^^^^^

To set up a conventional Python development environment,
make sure you have the following tools installed:

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

