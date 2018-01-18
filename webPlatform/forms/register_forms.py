from django import forms
from webPlatform import models
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'input id':'sender-email', 'placeholder':'Nombre usuario'}))
    password1 = forms.CharField(widget=forms.PasswordInput({'class':'form-control', 'placeholder':'Contraseña'}))
    password2 = forms.CharField(widget=forms.PasswordInput({'class':'form-control', 'placeholder':'Corfirmar Contraseña'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 7, 'class':'form-control', 'placeholder':'Descripción'}))
    avatar = forms.ImageField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'description', 'avatar')

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'input id':'sender-email', 'placeholder':'Nombre usuario'}))
    password = forms.CharField(widget=forms.PasswordInput({'class':'form-control', 'placeholder':'Contraseña'}))

