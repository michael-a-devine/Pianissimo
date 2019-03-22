# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-22 11:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0039_auto_20190321_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='piece',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='piece',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 22, 11, 32, 33, 73822)),
        ),
    ]
