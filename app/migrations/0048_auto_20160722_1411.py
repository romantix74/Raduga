# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-22 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_auto_20160722_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='obed',
            field=models.BooleanField(verbose_name='\u041e\u0431\u0435\u0434'),
        ),
        migrations.AlterField(
            model_name='food',
            name='ugin',
            field=models.BooleanField(verbose_name='\u0423\u0436\u0438\u043d'),
        ),
        migrations.AlterField(
            model_name='food',
            name='zavtrak',
            field=models.BooleanField(verbose_name='\u0417\u0430\u0432\u0442\u0440\u0430\u043a'),
        ),
    ]
