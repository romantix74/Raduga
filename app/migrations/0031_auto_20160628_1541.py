# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 11:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_auto_20160628_1527'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place_residing_choices',
            name='id',
        ),
        migrations.AddField(
            model_name='place_residing_choices',
            name='db_name',
            field=models.CharField(default='empty', max_length=50, primary_key=True, serialize=False, verbose_name='\u0421\u043e\u043a\u0440\u0430\u0449\u0435\u043d\u043d\u043e\u0435 \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435'),
            preserve_default=False,
        ),
    ]