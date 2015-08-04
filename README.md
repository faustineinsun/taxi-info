##### Installation Instructions

```
$ cd <path-to>/taxi-info
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ vim ~/.bash_profile
export DATABASE_URL=mysql://...
$ source ~/.bash_profile

// save valid login username and password into MySQL
$ heroku run python manage.py syncdb
$ heroku run python manage.py shell
>>> import django
>>> django.setup()
>>> from demo.models import Account
>>> a=Account(username="open",password="sesame")
>>> a.save()
>>> a.username
'open'
>>> a.password
'sesame'
>>> Account.objects.all()

// save trip data into MySQL 
python demo/libs/dataprocessing/saveToMySQL.py <path-to>/trip_data_1.csv

$ foreman start web  # not `$ python manage.py runserver` since we use the global variable from .env
```

##### Others

```
$ git push       # push to Github
$ git push heroku master      # push to heroku
$ heroku open

$ heroku logs

$ heroku ps:scale web=1
$ heroku ps     # lists the running dynos
$ heroku config

$ python manage.py startapp demo

$ python manage.py makemigrations demo
$ python manage.py sqlmigrate demo 0001
$ python manage.py check
$ python manage.py migrate
$ python manage.py shell

MySQL superuser
http://127.0.0.1:8000/admin
```
