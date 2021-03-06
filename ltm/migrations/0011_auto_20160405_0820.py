# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-05 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ltm', '0010_auto_20160404_0857'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualserver',
            name='status_availability',
            field=models.CharField(default='green', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='virtualserver',
            name='status_description',
            field=models.CharField(default='green', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='virtualserver',
            name='status_enabled',
            field=models.CharField(default='green', max_length=64),
            preserve_default=False,
        ),
    ]
