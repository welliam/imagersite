# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-19 14:26
from __future__ import unicode_literals

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('image', '0012_auto_20161002_0153'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
