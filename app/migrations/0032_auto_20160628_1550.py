# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20160628_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place_residing_choices',
            name='email',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u044b\u0439 \u0430\u0434\u0440\u0435\u0441'),
        ),
        migrations.AlterField(
            model_name='place_residing_choices',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d'),
        ),
    ]