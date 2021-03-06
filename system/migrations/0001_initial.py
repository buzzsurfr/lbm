# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('classification', models.CharField(choices=[('F5 BIG-IP', 'F5 BIG-IP')], default='F5 BIG-IP', max_length=200)),
                ('version', models.CharField(max_length=32)),
                ('connection', models.CharField(default='bigsuds', max_length=200)),
                ('hostname', models.CharField(max_length=200)),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
