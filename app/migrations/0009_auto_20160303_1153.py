# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-03 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20160229_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='phoneNumber',
            field=models.CharField(default=0, max_length=30, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d'),
            preserve_default=False,
        ),
    ]