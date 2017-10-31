from django.contrib import admin
<<<<<<< HEAD
from .models import Song, YoutubePlaylist
# Register your models here.
admin.site.register(Song)
admin.site.register(YoutubePlaylist)
=======
from .models import *
# Register your models here.
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album', 'genre', 'date', 'hasVideo')
admin.site.register(Song, SongAdmin)

admin.site.register(Playlist)

class UserAdmin(admin.ModelAdmin):
    list_display =  ('fname', 'lname', 'usrname', )
admin.site.register(User, UserAdmin)
>>>>>>> 0cb049b6af3b3024a2a38f59cc4f0d6334c2ef17
