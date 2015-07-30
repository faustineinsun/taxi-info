##### Installation Instructions

```
$ cd <path-to>/taxi-info
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ python manage.py sqlmigrate demo 0001
$ python manage.py shell
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

$ foreman start web  # or $ python manage.py runserver
```

##### Others

```
$ git push       # push to Github
$ git push heroku master      # push to heroku
$ heroku open

$ heroku run python manage.py syncdb
$ heroku run python manage.py shell
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
