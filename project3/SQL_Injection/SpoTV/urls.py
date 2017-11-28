from django.conf.urls import url
from django.conf.urls import include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'^myplaylists/$', views.myplaylists, name='playlists'),
     url(r'^myplaylists/(?P<pk>\d+)$', views.myplaylistdetail, name='playlist-detail'),
     url(r'^accinfo/$', views.accinfo, name='accinfo'),
     url(r'^login/$', views.login, name = 'login'),
     url(r'^logout/$', views.logout, {'next_page': '/login/'}, name='logout'),
     url(r'^signup/$', views.signup, name = 'signup'),
     url(r'^spotify_auth/$', views.spotify_auth, name = 'spotify_auth'),
     url(r'^preference/$', views.preference, name='prefer'),
     url(r'^search/$', views.playlist_filter, name = 'search'),
     url(r'^search/(?P<pk>\d+)$', views.myplaylistdetail, name = 'playlist-detail'),
     url(r'^password/$', views.change_password, name='change_password'),
     url(r'^accounts/', include('django.contrib.auth.urls')),
     url(r'^myplaylists/create/$', views.PlaylistCreate.as_view(), name= 'playlist_create'),
     url(r'^myplaylists/(?P<pk>\d+)/update/$', views.PlaylistUpdate.as_view(), name='playlist_update'),
     url(r'^myplaylists/(?P<pk>\d+)/delete/$', views.PlaylistDelete.as_view(), name='playlist_delete'),
     url(r'^myplaylists/$', views.PlaylistListView.as_view(), name='playlist'),

]
