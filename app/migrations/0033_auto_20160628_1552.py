# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 11:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20160628_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place_residing_choices',
            name='name',
            field=models.CharField(max_length=50, verbose_name='\u041c\u0435\u0441\u0442\u043e \u043f\u0440\u043e\u0436\u0438\u0432\u0430\u043d\u0438\u044f'),
        ),
    ]
