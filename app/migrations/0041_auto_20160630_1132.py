# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 07:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_auto_20160630_1018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='director',
            old_name='home_number',
            new_name='homeNumber',
        ),
    ]
