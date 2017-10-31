# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-31 07:56
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('SpoTV', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YouTubePlaylist',
            fields=[
                ('vid', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular video playlist', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('playlist', jsonfield.fields.JSONField()),
            ],
        ),
    ]
