# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-19 02:14
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0002_ForKey2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to=settings.AUTH_USER_MODEL),
        ),
    ]
