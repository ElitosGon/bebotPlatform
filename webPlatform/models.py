
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


# Create your models here.
class Profile(models.Model):
	# SIMPLE FIELD 
	description = models.CharField(default="", max_length=600, verbose_name="Descripción", null=True, blank=True)
	avatar = ResizedImageField(size=[200,200], null=True, verbose_name="Foto perfil", blank=True, upload_to='documents/avatar/%Y/%m/%d')

	# RELATION FIELD
	user = models.OneToOneField(auth.models.User, related_name="profile", blank=True, null=True, on_delete=models.CASCADE)

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
