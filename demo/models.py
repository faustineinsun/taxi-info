from django.db import models

# Create your models here.

class Account(models.Model):
    username = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=40)

    def __str__(self):          # __unicode__ on Python 2
        if hasattr(self, '__unicode__'):
            return unicode(self.username).encode('utf-8')
        return self.username

    def __str__(self):          # __unicode__ on Python 2
        if hasattr(self, '__unicode__'):
            return unicode(self.password).encode('utf-8')
        return self.password

class Record(models.Model):
    hack_license = models.CharField(max_length=80)
    pickup_datetime = models.CharField(max_length=40)
    dropoff_datetime = models.CharField(max_length=40)
    passenger_count = models.CharField(max_length=40)
    trip_distance = models.CharField(max_length=40)
    pickup_longitude = models.CharField(max_length=40)
    pickup_latitude = models.CharField(max_length=40)
    dropoff_longitude = models.CharField(max_length=40)
    dropoff_latitude = models.CharField(max_length=40)
