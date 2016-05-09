# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 17:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_auto_20160317_0909'),
        ('ltm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualserver',
            name='device',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.Device'),
        ),
    ]