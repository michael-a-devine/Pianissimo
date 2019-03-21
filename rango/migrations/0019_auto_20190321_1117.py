# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-21 11:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0018_auto_20190321_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='piece',
            name='id',
        ),
        migrations.AlterField(
            model_name='piece',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 21, 11, 17, 23, 933426)),
        ),
        migrations.AlterField(
            model_name='piece',
            name='title',
            field=models.CharField(max_length=128, primary_key=True, serialize=False),
        ),
    ]