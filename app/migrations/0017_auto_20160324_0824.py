# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 05:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20160323_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participation',
            name='list_member',
        ),
        migrations.AddField(
            model_name='participation',
            name='list_member',
            field=models.IntegerField(default=0, verbose_name='\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u0443\u0447\u0430\u0441\u0442\u043d\u0438\u043a\u043e\u0432'),
            preserve_default=False,
        ),
    ]
