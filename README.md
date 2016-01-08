#Jeffit_v2
Reddit clone written in python using django web framework and twitter's bootstrap.

#Getting up and running

The steps below will get you up and running with a local development environment. We assume you have the following installed:

    pip
    virtualenv

First make sure to create and activate a virtualenv, then open a terminal at the project root and install the requirements for local development:

    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ python manage.py syncdb
    $ python manage.py runserver

For the time being there is no separate production specific settings because the project is not yet production ready.

#Deployment

* TODO: Add Procfile
