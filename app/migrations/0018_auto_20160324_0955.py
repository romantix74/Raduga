# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-24 06:55
from __future__ import unicode_literals

import app.models
from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20160324_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='scan_passport',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to=app.models.make_upload_path, verbose_name='\u0421\u043a\u0430\u043d \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430, \u0443\u0434\u043e\u0441\u0442\u043e\u0432\u0435\u0440\u044f\u044e\u0449\u0435\u0433\u043e \u043b\u0438\u0447\u043d\u043e\u0441\u0442\u044c'),
        ),
    ]
