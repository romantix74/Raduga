# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-10 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_auto_20160406_0914'),
    ]

    operations = [
        migrations.AddField(
            model_name='participation',
            name='place',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='\u041c\u0435\u0441\u0442\u043e'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='member2',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u0423\u0447\u0430\u0441\u0442\u043d\u0438\u043a N2'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='member3',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u0423\u0447\u0430\u0441\u0442\u043d\u0438\u043a N3'),
        ),
    ]