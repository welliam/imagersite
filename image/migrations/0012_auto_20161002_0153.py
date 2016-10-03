# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-02 01:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0011_auto_20161002_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cover_for', to='image.Photo'),
        ),
    ]
