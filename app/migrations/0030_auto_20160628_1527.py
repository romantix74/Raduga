# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 11:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20160628_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='residing',
            name='place_of_residing',
            field=models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to='app.Place_residing_choices', verbose_name='\u041c\u0435\u0441\u0442\u043e \u043f\u0440\u043e\u0436\u0438\u0432\u0430\u043d\u0438\u044f'),
        ),
    ]
