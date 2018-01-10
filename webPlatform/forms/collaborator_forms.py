from django import forms
from webPlatform import models
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre usuario'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellido'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Correo'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 7, 'class':'form-control', 'placeholder':'Descripción'}))
    avatar = forms.ImageField()
    class Meta:
        model = models.Profile
        fields = ('description', 'avatar')

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput({'class':'form-control', 'placeholder':''}))
    new_password1 = forms.CharField(widget=forms.PasswordInput({'class':'form-control', 'placeholder':''}))
    new_password2 = forms.CharField(widget=forms.PasswordInput({'class':'form-control', 'placeholder':''}))
    
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

