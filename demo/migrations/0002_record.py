# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hack_license', models.CharField(max_length=80)),
                ('pickup_datetime', models.CharField(max_length=40)),
                ('dropoff_datetime', models.CharField(max_length=40)),
                ('passenger_count', models.CharField(max_length=40)),
                ('trip_distance', models.CharField(max_length=40)),
                ('pickup_longitude', models.CharField(max_length=40)),
                ('pickup_latitude', models.CharField(max_length=40)),
                ('dropoff_longitude', models.CharField(max_length=40)),
                ('dropoff_latitude', models.CharField(max_length=40)),
            ],
        ),
    ]
