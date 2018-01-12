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

class ProjectForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 7, 'class':'form-control', 'placeholder':'Descripción'}))
    url = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enlace a código fuente'}))
    
    class Meta:
        model = models.Project
        fields = ['name', 'description', 'url', 'is_public', 'source', 'providers', 'services', 'tags']

        widgets = {
            'is_public': forms.CheckboxInput(attrs={'class':'form-control','name':'is_public', 'data-toggle':'toggle', 'type':'checkbox', 'data-on':'Public', 'data-off':'Privado'}),
            'source': forms.Select(attrs={'mobile': 'true','class':'dropdown-product selectpicker', 'data-live-search':'true', 'title': 'Seleccionar fuente'}),
            'providers': forms.SelectMultiple(attrs={'mobile': 'true','class':'dropdown-product selectpicker', 'data-live-search':'true', 'title': 'Seleccionar proveedores'}),
            'services': forms.SelectMultiple(attrs={'mobile': 'true','class':'dropdown-product selectpicker', 'data-live-search':'true', 'title': 'Seleccionar servicios'}),
            'tags': forms.SelectMultiple(attrs={'mobile': 'true','class':' dropdown-product selectpicker', 'data-live-search':'true', 'title': 'Seleccionar etiquetas'}),
        }

    def __init__(self, *a, **kw):
        super(ProjectForm, self).__init__(*a, **kw)
        self.fields['name'].required = True
        self.fields['description'].required = True
        self.fields['url'].required = False
        self.fields['is_public'].initial = True
        self.fields['source'].required = True
        self.fields['providers'].required = False
        self.fields['services'].required = False
        self.fields['tags'].required = False
        
