from django.shortcuts import render
from .models import Song, Playlist, YoutubePlaylist, Profile
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
import jsonfield
# Create your views here.
@login_required
def index(request):
    #get the titles of all the playlists
    profile = Profile.objects.get(user=request.user)
    #playlists = request.user.playlist_set.all()
    playlists = Playlist.objects.filter(user=request.user)
    all_titles = playlists.values_list('pname')
    propic = profile.photo
    fname = request.user.first_name
    lname = request.user.last_name
    playlists = Playlist.objects.all()
    #playlistjson = YoutubePlaylist.objects.get(vid = '92fef807a09e497f87ab51d127dd8c89').playlist
    #objects.values_list('eng_name', flat=True)
    json = YoutubePlaylist.objects.get(vid = '92fef807a09e497f87ab51d127dd8c89').playlist

    return render(
        request,
        'index.html',
        context={'all_titles': all_titles, 'propic': propic, 'fname': fname, 'lname': lname,'playlists': playlists, 'json':json}
    )


#Used to filter the playlist based on user input.
@login_required
def playlist_filter(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''

    playlists = Playlist.objects.filter(pname__icontains = search_text)

    return render(
        request,
        'playlist_search.html',
        context = {'filtered_playlists': playlists})

@login_required
def myplaylists(request):
    profile = Profile.objects.get(user=request.user)
    propic = profile.photo
    fname = request.user.first_name
    lname = request.user.last_name
    usrname = request.user.username
    email = request.user.email
    playlists = Playlist.objects.all()
    return render(
        request,
        'myplaylists.html',
        context={'playlists':playlists, 'propic': propic, 'fname': fname, 'lname': lname}
    )

@login_required
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

@login_required
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

@login_required
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

def logout(request):
  auth.logout(request)
  # Redirect to a success page.
  return HttpResponseRedirect("login.html")

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

@login_required
def spotify_auth(request):
    return render(
        request,
        'registration/spotify_auth.html',
        context={}
    )

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


def addplaylist(request):
    if request.method == 'POST':
        form = AddPlaylistForm(request.POST)
        if form.is_valid():
            form.save()
            pname = form.cleaned_data.get('pname')
            return redirect('myplaylists')
    else:
        form = AddPlaylistForm()
    return render(request, 'addplaylist.html', {'form': form})

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
