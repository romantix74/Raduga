# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-25 07:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0053_auto_20160825_0951'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='img',
            new_name='image',
        ),
        migrations.RenameField(
            model_name='foto',
            old_name='img',
            new_name='image',
        ),
    ]