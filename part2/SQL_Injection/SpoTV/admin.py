from django.contrib import admin
from .models import Song, YoutubePlaylist, Playlist, User
# Register your models here.
admin.site.register(YoutubePlaylist)
# Register your models here.
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'genre', 'date', 'hasVideo')
admin.site.register(Song, SongAdmin)

admin.site.register(Playlist)

class UserAdmin(admin.ModelAdmin):
    list_display =  ('fname', 'lname', 'usrname', )
admin.site.register(User, UserAdmin)
