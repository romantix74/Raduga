# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-29 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0055_auto_20160825_1209'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['-order_num'], 'verbose_name': '\u0410\u043b\u044c\u0431\u043e\u043c', 'verbose_name_plural': '\u0410\u043b\u044c\u0431\u043e\u043c\u044b'},
        ),
        migrations.AddField(
            model_name='album',
            name='order_num',
            field=models.IntegerField(default=1, verbose_name=b'\xd0\xa1\xd0\xbe\xd1\x80\xd1\x82\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xba\xd0\xb0'),
            preserve_default=False,
        ),
    ]