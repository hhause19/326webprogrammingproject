from django.contrib import admin
from .models import Song
# Register your models here.
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'genre', 'date', 'hasVideo')
admin.site.register(Song, SongAdmin)
