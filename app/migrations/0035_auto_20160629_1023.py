# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0034_auto_20160628_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place_residing_choices',
            name='db_name',
        ),
        migrations.AddField(
            model_name='place_residing_choices',
            name='id',
            field=models.AutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]