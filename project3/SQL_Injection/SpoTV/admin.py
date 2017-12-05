from django.contrib import admin
from .models import Song, Playlist, Profile

# Register your models here.
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'genre', 'hasVideo')
admin.site.register(Song, SongAdmin)

admin.site.register(Playlist)
admin.site.register(Profile)
