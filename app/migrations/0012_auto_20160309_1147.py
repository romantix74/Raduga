# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-09 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_news_date_creation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='news_title',
            field=models.CharField(max_length=128),
        ),
    ]