#Rango app
This is test project that is used to store interesting pages and categorize them. 
Technologies: Django 3, PostgreSQL, Javascript(Jquery). 
Google APIs are used to get pages search results.


#Installation

We will work with python3 environment.
<h4>Install pip first</h4>
$sudo apt-get install python3-pip

<h4>Then install virtualenv using pip3</h4>
$sudo pip3 install virtualenv

<h4>Install PostgreSQL and PgAdmin for your system</h4>
Ubuntu installation guide example: https://linuxhint.com/install-pgadmin4-ubuntu/

<h4>Install packages required for psycopg2</h4>
$sudo apt-get update

$sudo apt-get install libpq-dev python3-dev

<h4>Now create a virtual environment inside your project root directory</h4>
$virtualenv ve

<h4>Inside your project's root directory</h4>
$source ve/bin/activate

(ve)$pip install -r requirements.txt

<h4>Create your rango/settings_local.py file</h4>
rewrite DATABASES setting with your own in settings_local.py

<h4>Setup local database</h4>

(ve)$python manage.py migrate

(ve)$python manage.py createsuperuser

(ve)$python manage.py makemigrations rangoapp

