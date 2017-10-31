from django.db import models
import uuid

# Create your models here.
class Song(models.Model):
    """
    Model representing a song.
    """
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    #pid = models.ForeignKey('Playlist', on_delete=models.SET_NULL, null=True)
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
