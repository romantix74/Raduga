# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-19 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20160317_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='director',
            name='addressInstitution',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441 \u0443\u0447\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='director',
            name='city',
            field=models.CharField(max_length=200, verbose_name='\u0413\u043e\u0440\u043e\u0434 \u043d/\u043f.'),
        ),
        migrations.AlterField(
            model_name='director',
            name='country',
            field=models.CharField(max_length=200, verbose_name='\u0421\u0442\u0440\u0430\u043d\u0430'),
        ),
        migrations.AlterField(
            model_name='director',
            name='director',
            field=models.CharField(max_length=200, verbose_name='\u0420\u0443\u043a\u043e\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c'),
        ),
        migrations.AlterField(
            model_name='director',
            name='email',
            field=models.CharField(max_length=200, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='director',
            name='groupName',
            field=models.CharField(max_length=200, verbose_name='\u041a\u043e\u043b\u043b\u0435\u043a\u0442\u0438\u0432'),
        ),
        migrations.AlterField(
            model_name='director',
            name='institution',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u0423\u0447\u0440\u0435\u0436\u0434\u0435\u043d\u0438\u0435'),
        ),
        migrations.AlterField(
            model_name='director',
            name='phoneNumber',
            field=models.CharField(max_length=200, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d'),
        ),
        migrations.AlterField(
            model_name='director',
            name='postalAddress',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u041f\u043e\u0447\u0442\u043e\u0432\u044b\u0439 \u0430\u0434\u0440\u0435\u0441'),
        ),
        migrations.AlterField(
            model_name='director',
            name='site',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u0421\u0430\u0439\u0442'),
        ),
        migrations.AlterField(
            model_name='director',
            name='teacher',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u041f\u0435\u0434\u0430\u0433\u043e\u0433/\u0445\u043e\u0440\u0435\u043e\u0433\u0440\u0430\u0444'),
        ),
        migrations.AlterField(
            model_name='participation',
            name='file_music',
            field=models.FileField(blank=True, null=True, upload_to=b'./music/', verbose_name='\u0410\u0443\u0434\u0438\u043e\u0437\u0430\u043f\u0438\u0441\u044c'),
        ),
    ]