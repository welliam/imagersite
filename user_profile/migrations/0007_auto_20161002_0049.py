# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 00:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_auto_20160916_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='camera_type',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='genre',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='website',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
