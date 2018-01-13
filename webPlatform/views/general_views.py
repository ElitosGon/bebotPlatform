from __future__ import absolute_import
from webPlatform import models
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
			collaborators = collaborators.filter(Q(user__first_name__icontains=query) |
												 Q(user__username__icontains=query) | 
												 Q(user__last_name__icontains=query)).distinct()
		
		page = request.GET.get('page', 1)
		paginator = Paginator(collaborators, 5)

		try:
			collaborators = paginator.page(page)
		except PageNotAnInteger:
			collaborators = paginator.page(1)
		except EmptyPage:
			collaborators = paginator.page(paginator.num_pages)

		context = {'collaborators' : collaborators}
		return render(request,'general/collaborators.html', context ,RequestContext(request))
	else:
		return Http404

####### Collaborator Id ############################
def collaborator(request, id):
	if request.method == 'GET':
		collaborator = models.Profile.objects.get(pk=id)
		if collaborator:
			query = request.GET.get("search")
			provider = request.GET.get("provider")
			projects = models.Project.objects.filter(user=collaborator.user.id, is_public=True).order_by('-updated_at')
			
			if query:
				projects = projects.filter(Q(name__icontains=query) |
										   Q(description__icontains=query) |
										   Q(source__name__icontains=query) |
										   Q(providers__name__icontains=query) |
										   Q(services__name__icontains=query) |
										   Q(tags__name__icontains=query)).distinct()

			if provider != '0' and provider != None:
				projects = projects.filter(providers__id=provider).distinct()
			
			page = request.GET.get('page', 1)
			paginator = Paginator(projects, 5)

			try:
				projects = paginator.page(page)
			except PageNotAnInteger:
				projects = paginator.page(1)
			except EmptyPage:
				projects = paginator.page(paginator.num_pages)

			context = {'collaborator': collaborator, 'projects': projects }
			return render(request,'general/collaborator.html', context ,RequestContext(request))
		else:
			return Http404
	else:
		return Http404

def projects(request):
	if request.method == 'GET':
		projects = models.Project.objects.filter(is_public=True).order_by('-updated_at')	
		if projects:
			query = request.GET.get("search")
			provider = request.GET.get("provider")
			
			if query:
				projects = projects.filter(Q(name__icontains=query) |
										   Q(description__icontains=query) |
										   Q(source__name__icontains=query) |
										   Q(providers__name__icontains=query) |
										   Q(services__name__icontains=query) |
										   Q(tags__name__icontains=query)).distinct()

			if provider != '0' and provider != None:
				projects = projects.filter(providers__id=provider).distinct()
			
			page = request.GET.get('page', 1)
			paginator = Paginator(projects, 5)

			try:
				projects = paginator.page(page)
			except PageNotAnInteger:
				projects = paginator.page(1)
			except EmptyPage:
				projects = paginator.page(paginator.num_pages)

			context = {'projects': projects}
			return render(request,'general/projects.html', context ,RequestContext(request))
		else:
			return Http404
	else:
		return Http404