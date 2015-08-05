### Installation Instructions

```
$ cd <path-to>/taxi-info
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ vim ~/.bash_profile
export DATABASE_URL=mysql://...
export REDISCLOUD_URL=redis://...
$ source ~/.bash_profile

$ python manage.py runserver  
app now is running on http://127.0.0.1:8000/
// not `$ foreman start web`, it needs Heroku account
```

---

### Others

##### Save info to DB 

```
$ pip install mysql-connector-python --allow-external mysql-connector-python

// save valid login username and password into MySQL
$ heroku run python manage.py syncdb
$ heroku run python manage.py shell
>>> import django
>>> django.setup()
>>> from django.contrib.auth.models import User
>>> u = User.objects.create_user('open', '', 'sesame')
>>> u.save()
>>> User.objects.all()

// save trip data into MySQL 
$ python demo/libs/dataprocessing/saveToMySQL.py <path-to>/trip_data_1.csv
or $ sbin/saveDataToMySQL.sh

// generate GeoJSON and save to Redis
$ python demo/libs/dataprocessing/queryMySQLSaveGeoJsonInRedisByHour.py 
or $ sbin/generateGeoJsonSaveToRedis.sh 
```

##### Git 

```
$ git push       # push to Github
$ git push heroku master      # push to heroku
$ heroku open
```

##### Heroku

```
$ heroku config
$ heroku logs
$ heroku ps:scale web=1
$ heroku ps     # lists the running dynos
```

##### Django MySQL

```
$ python manage.py startapp demo

$ python manage.py makemigrations demo
$ python manage.py sqlmigrate demo 0001
$ python manage.py check
$ python manage.py migrate
$ python manage.py shell
```
