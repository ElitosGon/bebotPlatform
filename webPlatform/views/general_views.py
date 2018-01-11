from __future__ import absolute_import
from webPlatform import models
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from django.http import Http404

####### HOME #####################################
def home(request):
	if request.method == 'GET':
		return render(request,'general/home.html', None , RequestContext(request))
	else:
		return render(request,'error/404.html', None, RequestContext(request))

####### Collaborators ############################
def collaborators(request):
	if request.method == 'GET':
		collaborators = models.Profile.objects.all().order_by('updated_at')
		query = request.GET.get("search")
		
		if query:
			collaborators = collaborators.filter(Q(user__first_name__icontains=query) & Q(user__username__icontains=query) & Q(user__last_name__icontains=query)).distinct()
		
		contexto = {
			'collaborators' : collaborators
		}

		return render(request,'general/collaborators.html', contexto ,RequestContext(request))
	else:
		return Http404

####### Collaborator Id ############################
def collaborator(request, id):
	if request.method == 'GET':
		collaborator = models.Profile.objects.get(pk=id)
		if collaborator:
			contexto = {'collaborator': collaborator}
			return render(request,'general/collaborator.html', contexto ,RequestContext(request))
		else:
			return Http404
	else:
		return Http404