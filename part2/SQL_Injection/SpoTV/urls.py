from django.conf.urls import url
from . import views

urlpatterns = [
     url(r'^$', views.index, name='index'),
     url(r'^myplaylists/$', views.myplaylists, name='playlists'),
     url(r'^accinfo/$', views.accinfo, name='accinfo'),
]
