from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django import forms
import uuid
import jsonfield

class Profile(models.Model):
    '''
    user info
    '''
    media_root = settings.MEDIA_ROOT
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    photo = models.FileField(default='default.png')

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.user.username


    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('user-detail', args=[str(self.id)])

class Song(models.Model):
    """
    Model representing a song.
    """
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    sid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular song across whole library")
    hasVideo = models.BooleanField(null=False)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title


    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('song-detail', args=[str(self.id)])

class Playlist(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    pname = models.CharField(max_length=200)
    image = models.FileField(upload_to='PlaylistPhotos', max_length=100)
    songs = models.ManyToManyField(Song)
    videoID = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.pname

    def get_absolute_url(self):
        return reverse('playlist-detail', args=[str(self.image)])
