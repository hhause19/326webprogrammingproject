# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-03 01:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=200)),
                ('image', models.FileField(upload_to='PlaylistPhotos')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.FileField(default='default.png', upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('title', models.CharField(max_length=200)),
                ('artist', models.CharField(max_length=200)),
                ('album', models.CharField(max_length=200)),
                ('genre', models.CharField(max_length=200)),
                ('sid', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular song across whole library', primary_key=True, serialize=False)),
                ('hasVideo', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='YoutubePlaylist',
            fields=[
                ('vid', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular video playlist', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('playlist', jsonfield.fields.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(to='SpoTV.Song'),
        ),
        migrations.AddField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
