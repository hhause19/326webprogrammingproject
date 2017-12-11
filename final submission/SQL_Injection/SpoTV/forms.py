from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Playlist

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class AddPlaylistForm(ModelForm):

    #name = forms.CharField(max_length=200, required=True)
    class Meta:
        model = Playlist
        fields = '__all__'
