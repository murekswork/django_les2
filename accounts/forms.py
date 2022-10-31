from django.forms import ModelForm
from setuptools.msvc import winreg

from .models import User, Profile
from django import forms


class SignUpForm(ModelForm):
    username = forms.CharField(max_length=50, min_length=3)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=50)
    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(ModelForm):

    image_url = forms.URLField(max_length=550)
    nickname = forms.CharField(max_length=50)
    age = forms.IntegerField()
    about = forms.CharField(max_length=1024)

    class Meta:
        model = Profile
        exclude = ['balance', 'user']