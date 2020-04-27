# Rango app
This is test project that is used to store interesting pages and categorize them. 
Technologies: Django 3, PostgreSQL, Javascript(Jquery). 
Google APIs are used to get pages search results.


# Installation

We will work with python3 environment.
#### Install pip first
``` bash
$sudo apt-get install python3-pip
```

#### Then install virtualenv using pip3
``` bash
$sudo pip3 install virtualenv
```

#### Install PostgreSQL and PgAdmin for your system
Ubuntu installation guide example: https://linuxhint.com/install-pgadmin4-ubuntu/

#### Install packages required for psycopg2
``` bash
$sudo apt-get update

$sudo apt-get install libpq-dev python3-dev
```

#### Now create a virtual environment inside your project root directory
``` bash
$virtualenv ve
```
#### Inside your project's root directory
``` bash
$source ve/bin/activate

(ve)$pip install -r requirements.txt
```
#### Create your rango/settings_local.py file
rewrite DATABASES setting with your own in settings_local.py

#### Setup local database
``` bash
(ve)$python manage.py migrate

(ve)$python manage.py createsuperuser

(ve)$python manage.py makemigrations rangoapp
```
