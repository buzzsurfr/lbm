# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-01 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ltm', '0008_auto_20160401_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='status_availability',
            field=models.CharField(default='AVAILABILITY_STATUS_GREEN', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='status_description',
            field=models.CharField(default='The object is available in some capacity.', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='node',
            name='status_enabled',
            field=models.CharField(default='ENABLED_STATUS_ENABLED', max_length=64),
            preserve_default=False,
        ),
    ]