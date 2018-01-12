
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-
import os, sys
from django.db import models
from django.contrib import auth
from django_resized import ResizedImageField
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from vote.models import VoteModel



# Create your models here.
class TypeTag(models.Model):
	# SIMPLE FIELD
	name = models.CharField(default="", max_length=100, verbose_name="Nombre", null=True, blank=True)
	description = models.CharField(default="", max_length=600, verbose_name="Descripción", null=True, blank=True)

	# TIMESTAMP FIELD
	created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Fecha creación")
	updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name="Fecha última modificación")
	
	def __str__(self):
		return self.name

class Tag(models.Model):
	# SIMPLE FIELD
	name = models.CharField(default="", max_length=100, verbose_name="Nombre", null=True, blank=True)
	description = models.CharField(default="", max_length=600, verbose_name="Descripción", null=True, blank=True)
	
	#RELATION FIELD
	type_tag = models.ForeignKey(auth.models.User, related_name="tags", verbose_name="Tipo de tag", blank=True, null=True, on_delete=models.SET_NULL)
	
	# TIMESTAMP FIELD
	created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Fecha creación")
	updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name="Fecha última modificación")

	def __str__(self):
		return self.name

class Provider(models.Model):
	# SIMPLE FIELD
	name = models.CharField(default="", max_length=100, verbose_name="Nombre", null=True, blank=True)
	description = models.CharField(default="", max_length=600, verbose_name="Descripción", null=True, blank=True)
	in_library = models.BooleanField(verbose_name="¿Esta integrado en BeBot Library?", blank=True, default=True)

	# TIMESTAMP FIELD
	created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Fecha creación")
	updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name="Fecha última modificación")

	def __str__(self):
		return self.name

class Source(models.Model):
	# SIMPLE FIELD
	name = models.CharField(default="", max_length=100, verbose_name="Nombre", null=True, blank=True)
	description = models.CharField(default="", max_length=600, verbose_name="Descripción", null=True, blank=True)

	# TIMESTAMP FIELD
	created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Fecha creación")
	updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name="Fecha última modificación")

	def __str__(self):
		return self.name
	
class Service(models.Model):
	# SIMPLE FIELD
	name = models.CharField(default="", max_length=100, verbose_name="Nombre", null=True, blank=True)
	description = models.CharField(default="", max_length=600, verbose_name="Descripción", null=True, blank=True)
	url = models.CharField(default="", max_length=600, verbose_name="Enlace a pagina oficial", null=True, blank=True)
	category = models.CharField(default="", max_length=100, verbose_name="Clasificación propia del proveedor", null=True, blank=True)
	in_library = models.BooleanField(verbose_name="¿Esta integrado en BeBot Library?", blank=True, default=True)

	#RELATION FIELD
	provider = models.ForeignKey(Provider, related_name="servicios", verbose_name="Proveedor del servicio", blank=True, null=True, on_delete=models.SET_NULL)
	
	# TIMESTAMP FIELD
	created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Fecha creación")
	updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name="Fecha última modificación")

	def __str__(self):
		return self.name

class Profile(models.Model):
	# SIMPLE FIELD 
	description = models.CharField(default="", max_length=600, verbose_name="Descripción", null=True, blank=True)
	avatar = ResizedImageField(size=[200,200], null=True, verbose_name="Foto perfil", blank=True, upload_to='documents/avatar/%Y/%m/%d')

	# RELATION FIELD
	user = models.OneToOneField(auth.models.User, related_name="profile", blank=True, null=True, on_delete=models.CASCADE)
	follows = models.ManyToManyField(auth.models.User, related_name='followed_by', verbose_name="Seguidores", blank=True)

	# TIMESTAMP FIELD
	created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Fecha creación")
	updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name="Fecha última modificación")

	def __str__(self):
		return "%d" %self.id

@receiver(post_save, sender=auth.models.User)
def update_user_profile(sender, instance, created, **kwargs):
    try:
    	if created:
        	Profile.objects.create(user=instance)
    	instance.profile.save()
    except:	
    	return instance

class Project(VoteModel, models.Model):
	# SIMPLE FIELD 
	name = models.CharField(default="", max_length=100, verbose_name="Nombre", null=True, blank=True)
	description = models.CharField(default="", max_length=600, verbose_name="Descripción", null=True, blank=True)
	url = models.CharField(default="", max_length=600, verbose_name="Enlace a código fuente", null=True, blank=True)
	is_public = models.BooleanField(verbose_name="¿Es visible?", blank=True, default=True)
	number_likes = models.IntegerField(verbose_name="Número de likes", null=True, blank=True)
	
	# RELATION FIELD
	user = models.ForeignKey(auth.models.User, related_name="proyectos", verbose_name="Dueño del registro", blank=True, null=True, on_delete=models.SET_NULL)
	source = models.ForeignKey(Source, related_name="fuente", verbose_name="Proveedor código fuente", blank=True, null=True, on_delete=models.SET_NULL)
	providers = models.ManyToManyField(Provider, related_name='proveedores', verbose_name="Proveedores utilizados", blank=True)
	services = models.ManyToManyField(Service, related_name='servicios', verbose_name="Servicios utilizados", blank=True)
	tags = models.ManyToManyField(Tag, related_name='tags', verbose_name="Tags que describen el proyecto", blank=True)
	

	# TIMESTAMP FIELD
	created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name="Fecha creación")
	updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name="Fecha última modificación")

	def __str__(self):
		return "%d" %self.name



