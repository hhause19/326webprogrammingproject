from django.contrib import admin
from .models import Song, YoutubePlaylist
# Register your models here.
admin.site.register(Song)
admin.site.register(YoutubePlaylist)
