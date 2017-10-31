from django.db import models
from django.urls import reverse
import uuid

class User(models.Model):
    '''
    user info
    '''
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular User")
    fname = models.CharField(max_length=200)
    lname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    usrname = models.CharField(max_length=200)
    #password will be done separately needs to be hashed
    photo = models.FileField(upload_to=None, max_length=100)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title


    def get_absolute_url(self):
        """
        Returns the url to access a particular book instance.
        """
        return reverse('user-detail', args=[str(self.id)])

# Create your models here.

class Playlist(models.Model):
	userid = models.CharField(max_length=200)
	pname = models.CharField(max_length=200)
	date = models.DateField()
	image = models.CharField(max_length = 1000)
	def __str__(self):
		return self.pname


class Song(models.Model):
    """
    Model representing a song.
    """
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    pid = models.ForeignKey('Playlist', on_delete=models.SET_NULL, null=True)
    sid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular song across whole library")
    hasVideo = models.BooleanField(null=False)
    date = models.DateField(auto_now=False, auto_now_add=False)

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
