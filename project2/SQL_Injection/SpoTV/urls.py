from django.conf.urls import url
from . import views

urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'^myplaylists/$', views.myplaylists, name='playlists'),
     url(r'^myplaylists/(?P<pk>\d+)$', views.myplaylistdetail, name='playlistdetail'),
     url(r'^accinfo/$', views.accinfo, name='accinfo'),
     url(r'^login/$', views.login, name = 'login'),
     url(r'^preference/$', views.preference, name='prefer'),
     url(r'^search/$', views.playlist_filter, name = 'search'),
     url(r'^search/(?P<pk>\d+)$', views.myplaylistdetail, name = 'playlistdetail'),
]
