# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-25 09:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_director_fest_num'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0440\u0430\u043d\u044b')),
            ],
            options={
                'verbose_name': '\u0441\u0442\u0440\u0430\u043d\u0430',
                'verbose_name_plural': '\u0441\u0442\u0440\u0430\u043d\u044b',
            },
        ),
        migrations.AlterField(
            model_name='director',
            name='country',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Country', verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430'),
        ),
    ]
