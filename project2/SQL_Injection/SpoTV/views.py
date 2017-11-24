from django.shortcuts import render
from .models import Song, Playlist, User, YoutubePlaylist
from django.views import generic
from .forms import SignUpForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
import jsonfield
# Create your views here.

def index(request):
    #get the titles of all the playlists
    all_titles = Playlist.objects.values_list('pname')
    propic = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').photo
    fname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').fname
    lname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').lname
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


def myplaylists(request):
    propic = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').photo
    fname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').fname
    lname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').lname
    usrname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').usrname
    email = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').email
    playlists = Playlist.objects.all()
    return render(
        request,
        'myplaylists.html',
        context={'playlists':playlists, 'propic': propic, 'fname': fname, 'lname': lname}
    )

def myplaylistdetail(request,pk):
    propic = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').photo
    fname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').fname
    lname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').lname
    usrname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').usrname
    email = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').email
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

def accinfo(request):
    #get the account information
    propic = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').photo
    fname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').fname
    lname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').lname
    usrname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').usrname
    email = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').email
    return render(
        request,
        'accinfo.html',
        context={'propic': propic, 'fname': fname, 'lname': lname, 'usrname': usrname, 'email': email}
    )

def preference(request):
    propic = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').photo
    fname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').fname
    lname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').lname
    usrname = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').usrname
    email = User.objects.get(uid = '25fc7c5f15b24a018eeac09d58913a69').email
    songlists = Song.objects.all()
    return render(
        request,
        'preference.html',
        context={'songs':songlists, 'propic': propic, 'fname': fname, 'lname': lname}
    )

def login(request):
    return render(
        request,
        'login.html',
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

def spotify_auth(request):
    return render(
        request,
        'registration/spotify_auth.html',
        context={}
    )
