from django.shortcuts import render
from .models import Song, Playlist, Profile
from django.contrib.auth.models import User
from django.views import generic
from .forms import SignUpForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, update_session_auth_hash
from django.shortcuts import render, redirect
from django.conf import settings
import jsonfield
import os
import time
import spotipy
import spotipy.util as util
import spotipy.oauth2
from spotipy.oauth2 import SpotifyClientCredentials
from oauth2client.client import GoogleCredentials
import google.oauth2.credentials
from oauth2client import GOOGLE_TOKEN_URI
from social_django.models import UserSocialAuth
from social_django.utils import psa
from django.http import HttpRequest, HttpResponse
import requests
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Create your views here.
SCOPES = [
'https://www.googleapis.com/auth/youtube',
'https://www.googleapis.com/auth/youtube.upload',
'https://www.googleapis.com/auth/plus.me',
'https://www.googleapis.com/auth/youtube.force-ssl'
]
CLIENT_SECRETS_FILE = os.path.join('SpoTV', 'static', "client_secret_535317070838-8oosnkbgb01pb0v7n6n172l867f37sk3.apps.googleusercontent.com.json")

@login_required(login_url='login/')
def index(request):
    #get the titles of all the playlists
    profile = Profile.objects.get(user=request.user)
    saved_playlists = Playlist.objects.filter(user=request.user)
    playlists = []
    videoIds = []
    youtube_pid = 'noplaylistselected'
    propic = profile.photo
    fname = request.user.first_name
    lname = request.user.last_name
    pid = 0

    #show video playlist for selected playlist
    if request.GET.get('playlist-id'):
        pid = request.GET.get('playlist-id')
        saved_playlists = Playlist.objects.filter(user=request.user)
        p = Playlist.objects.get(user=request.user,id=pid)
        youtube_pid = p.videoID
        return render(request, 'index.html', context={'propic': propic, 'fname': fname, 'lname': lname,'playlists':saved_playlists,'pid':pid,'playlistID':youtube_pid})

    #used to create a playlist
    if request.GET.get('create_video'):
        user = request.user
        social = UserSocialAuth.objects.get(user=user, provider='google-oauth2')
        access_token = social.extra_data['access_token']
        refresh_token = social.extra_data.get('refresh_token')
        pid = request.GET.get('create')
        p = Playlist.objects.get(user=request.user,id=pid)
        pname = p.pname
        songs = p.songs.all()

        #initial variables for creds
        token_expiry = None
        token_uri = GOOGLE_TOKEN_URI
        SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '535317070838-8oosnkbgb01pb0v7n6n172l867f37sk3.apps.googleusercontent.com'
        SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'EO6ZgGr97P8jPfNIOzGkaXiI'
        user_agent = 'Python client library'
        revoke_uri = None

        #credentials for using the youtube api
        credentials = GoogleCredentials(
            access_token,
            SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            refresh_token,
            token_expiry,
            token_uri,
            user_agent,
            revoke_uri=revoke_uri
        )

        youtube = build('youtube', 'v3', credentials = credentials)

        #create playlist
        youtube_pid = add_playlist(youtube, pname)

        #iterate through songs
        for s in songs:
            songname = s.title
            artist = s.artist
            query = songname + " " + artist
            response = requests.get(
            'https://www.googleapis.com/youtube/v3/search',
            params={'access_token': social.extra_data['access_token'],'maxResults':'1',
            'q':query,
            'type':'video',
            'part':'snippet',
            })

        #get the id of the video
            if response:
                search_videos = []
                for search_result in response.json().get('items', []):
                    search_videos.append(search_result['id']['videoId'])
                videoIds.append(search_videos[0])
            search_videos = []

        #add id to playlist
        for vid in videoIds:
            playlist_items_insert(youtube,youtube_pid, vid)

        #save id to db
        p.videoID = youtube_pid
        p.save()

        #need to wait for videos to actually get added
        time.sleep(5)

        return render(request, 'index.html', context={'propic': propic, 'fname': fname, 'lname': lname,'playlists':saved_playlists,'pid':pid,'playlistID':youtube_pid})
    #used for importing playlist
    if request.GET.get('import'):
        user = request.user
        instance = UserSocialAuth.objects.get(user=user, provider='spotify')
        access_token = instance.access_token
        if access_token:
            sp = spotipy.Spotify(auth=access_token)
            u = sp.current_user()
            spotid = u['id']
            plists = sp.user_playlists(spotid)
            for pl in plists['items']:
                if pl['owner']['id'] == spotid:
                    playlists.append(pl['name'])
                    p = Playlist(user=request.user,pname = pl['name'])
                    p.save()
                    results = sp.user_playlist(spotid, pl['id'],fields="tracks,next")
                    tracks = results['tracks']
                    saveSongs(tracks, p)
                    while tracks['next']:
                        tracks = sp.next(tracks)
                        saveSongs(tracks, p)
            return render(request, 'index.html', context={'propic': propic, 'fname': fname, 'lname': lname,'playlists': playlists,'pid':pid, 'playlistID':youtube_pid})
    else:
        return render(
            request,
            'index.html',
            context={'propic': propic, 'fname': fname, 'lname': lname,'playlists': saved_playlists,'pid':pid, 'playlistID':youtube_pid}
        )

def saveSongs(tracks, p):
    for i, item in enumerate(tracks['items']):
        s = Song()
        track = item['track']
        s.title = track['name']
        s.artist = track['artists'][0]['name']
        s.hasVideo = False
        s.save()
        p.songs.add(s)

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

def search_list_by_keyword(client, **kwargs):
    response = client.search().list(
        **kwargs
    ).execute()
    return response

def add_playlist(youtube, t):
    body = dict(
        snippet=dict(
            title=t,
            description='Created with SpoTV'
            ),
        status=dict(
            privacyStatus='public'
        )
    )

    playlists_insert_response = youtube.playlists().insert(
        part='snippet,status',
        body=body
        ).execute()
    return playlists_insert_response['id']

def playlist_items_insert(youtube, pid, vid):
    body = dict(
        snippet=dict(
            playlistId=pid,
            resourceId=dict(
                kind='youtube#video',
                videoId=vid
            )
        ),
    )
    response = youtube.playlistItems().insert(
        part='snippet,status',
        body=body
    ).execute()

    return pid

#Used to filter the playlist based on user input.
@login_required(login_url='login/')
def playlist_filter(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    playlists = Playlist.objects.filter(pname__icontains = search_text, user=request.user)

    return render(
        request,
        'playlist_search.html',
        context = {'filtered_playlists': playlists})

@login_required(login_url='login/')
def myplaylists(request):
    profile = Profile.objects.get(user=request.user)
    propic = profile.photo
    fname = request.user.first_name
    lname = request.user.last_name
    usrname = request.user.username
    email = request.user.email
    playlists = Playlist.objects.filter(user=request.user)
    return render(
        request,
        'myplaylists.html',
        context={'playlists':playlists, 'propic': propic, 'fname': fname, 'lname': lname}
    )

@login_required(login_url='login/')
def myplaylistdetail(request,pk):
    profile = Profile.objects.get(user=request.user)
    propic = profile.photo
    fname = request.user.first_name
    lname = request.user.last_name
    usrname = request.user.username
    email = request.user.email
    try:
        playlist_id=Playlist.objects.get(pk=pk)
    except Playlist.DoesNotExist:
        raise Http404("Playlist does not exist")

    #book_id=get_object_or_404(Book, pk=pk)

    return render(
        request,
        'playlistdetail.html',
        context={'playlist':playlist_id, 'propic': propic, 'fname': fname, 'lname': lname}
    )

@login_required(login_url='login/')
def accinfo(request):
    #get the account information
    profile = Profile.objects.get(user=request.user)
    propic = profile.photo
    fname = request.user.first_name
    lname = request.user.last_name
    usrname = request.user.username
    email = request.user.email
    return render(
        request,
        'accinfo.html',
        context={'propic': propic, 'fname': fname, 'lname': lname, 'usrname': usrname, 'email': email}
    )

@login_required(login_url='login/')
def preference(request):
    profile = Profile.objects.get(user=request.user)
    propic = profile.photo
    fname = request.user.first_name
    lname = request.user.last_name
    usrname = request.user.username
    email = request.user.email
    songlists = Song.objects.all()
    return render(
        request,
        'preference.html',
        context={'songs':songlists, 'propic': propic, 'fname': fname, 'lname': lname}
    )

def login(request):
    return render(
        request,
        'registration/login.html',
        context={}
    )

@login_required(login_url='login/')
def logout(request):
  auth.logout(request)
  UserSocialAuth.objects.remove(user=request.user, provider='spotify')
  # Redirect to a success page.
  return HttpResponseRedirect("/login/")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('spotify_auth')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required(login_url='login/')
def spotify_auth(request):
    return render(
        request,
        'registration/spotify_auth.html',
        context={}
    )

@login_required(login_url='login/')
def spotify_auth_success(request):
    user = request.user
    instance = UserSocialAuth.objects.get(user=user, provider='spotify')
    access_token = instance.access_token
    if access_token:
        sp = spotipy.Spotify(auth=access_token)
        results = sp.current_user()
        return render(request, 'registration/spotify_auth_success.html', context={'access_token':access_token, 'results':results})

    return render(request, 'registration/spotify_auth_success.html', context={'access_token':access_token, 'results':results})

@login_required(login_url='login/')
def youtube_auth(request):
    return render(
        request,
        'registration/youtube_auth.html',
        context={}
    )

@login_required(login_url='login/')
def youtube_auth_success(request):
    user = request.user
    social = UserSocialAuth.objects.get(user=user, provider='google-oauth2')
    access_token = social.extra_data['access_token']
    response = requests.get(
    'https://www.googleapis.com/plus/v1/people/me/',
    params={'access_token': social.extra_data['access_token']}
    )
    if response:
        id = response.json()['displayName']
        return render(request, 'registration/youtube_auth_success.html', context={'access_token':access_token, 'results':id})

    return render(request, 'registration/youtube_auth_success.html', context={'access_token':access_token, 'results':results})

@login_required(login_url='login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accinfo.html', {
        'form': form
    })

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Playlist

class PlaylistCreate(CreateView):
    model = Playlist
    fields = ['pname','date','songs']
    labels = { 'pname':'Name', }
    success_url = reverse_lazy('playlist-detail', args=[1])

class PlaylistUpdate(UpdateView):
    model = Playlist
    fields = ['pname','songs',]
    success_url = reverse_lazy('playlists')

class PlaylistDelete(DeleteView):
    model = Playlist
    success_url = reverse_lazy('playlists')

from django.views import generic

class PlaylistListView(generic.ListView):
    model = Playlist

class PlaylistDetailView(generic.DetailView):
    model = Playlist
