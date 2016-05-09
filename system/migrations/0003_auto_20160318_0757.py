# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-18 12:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_auto_20160317_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='system.DeviceGroup'),
            preserve_default=False,
        ),
    ]
