from django import forms
from webPlatform import models
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'input id':'sender-email', 'placeholder':'Nombre usuario'}))
	password = forms.CharField(widget=forms.PasswordInput({'class':'form-control', 'placeholder':'Contraseña'}))

class RecoverForm(forms.Form):
	new_password1 = forms.CharField(widget=forms.PasswordInput({'class':'form-control', 'placeholder':'Nueva contraseña'}))
	new_password2 = forms.CharField(widget=forms.PasswordInput({'class':'form-control', 'placeholder':'Confirmar contraseña'}))
