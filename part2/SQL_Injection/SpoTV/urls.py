from django.conf.urls import url
from . import views

urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'^myplaylists/$', views.myplaylists, name='playlists'),
     url(r'^myplaylists/(?P<pk>\d+)$', views.myplaylistdetail, name='playlistdetail'),
     url(r'^accinfo/$', views.accinfo, name='accinfo'),
     url(r'^preference/$', views.preference, name='prefer'),
]
