##### Installation Instructions

```
$ cd <path-to>/taxi-info
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ foreman start web
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
```
