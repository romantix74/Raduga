# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0026_auto_20160625_1306'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place_residing_choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='\u041c\u0435\u0441\u0442\u043e \u043f\u0440\u043e\u0436\u0438\u0432\u0430\u043d\u0438\u044f')),
                ('email', models.CharField(max_length=30, verbose_name='\u042d\u043b\u0435\u043a\u0442\u0440\u043e\u043d\u043d\u044b\u0439 \u0430\u0434\u0440\u0435\u0441')),
                ('phone', models.CharField(max_length=30, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d')),
            ],
            options={
                'verbose_name': '\u041c\u0435\u0441\u0442\u043e \u043f\u0440\u043e\u0436\u0438\u0432\u0430\u043d\u0438\u044f',
                'verbose_name_plural': '\u041c\u0435\u0441\u0442\u0430 \u043f\u0440\u043e\u0436\u0438\u0432\u0430\u043d\u0438\u044f',
            },
        ),
    ]