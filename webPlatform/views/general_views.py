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
from django.contrib.auth.decorators import login_required
from actstream import registry
from django.core.mail import send_mail
from templated_email import send_templated_mail, get_templated_mail
from django.shortcuts import render, redirect
from django.conf import settings
import json
import urllib

####### HOME #####################################
def home(request):
	if request.method == 'GET':
		providers = models.Provider.objects.all()
		services = models.Service.objects.all()
		context = {'services': services, 'providers': providers}
		return render(request,'general/home.html', context , RequestContext(request))
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
			num_project = projects.count

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

			context = {'collaborator': collaborator, 'projects': projects, 'num_project': num_project}
			return render(request,'general/collaborator.html', context ,RequestContext(request))
		else:
			return Http404
	else:
		return Http404

############## Projects #####################
def projects(request):
	if request.method == 'GET':
		projects = models.Project.objects.filter(is_public=True).order_by('-updated_at')    
		if projects:
			query = request.GET.get("search")
			provider = request.GET.get("provider")
			service = request.GET.get("service")
			
			if query:
				projects = projects.filter(Q(name__icontains=query) |
										   Q(description__icontains=query) |
										   Q(source__name__icontains=query) |
										   Q(providers__name__icontains=query) |
										   Q(services__name__icontains=query) |
										   Q(tags__name__icontains=query)).distinct()

			if provider != '0' and provider != None:
				projects = projects.filter(providers__id=provider).distinct()

			if service != '0' and service != None:
				projects = projects.filter(services__id=service).distinct()
			
			page = request.GET.get('page', 1)
			paginator = Paginator(projects, 5)

			try:
				projects = paginator.page(page)
			except PageNotAnInteger:
				projects = paginator.page(1)
			except EmptyPage:
				projects = paginator.page(paginator.num_pages)

			providers = models.Provider.objects.all()
			services = models.Service.objects.all()
			context = {'projects': projects, 'services': services, 'providers': providers}
			return render(request,'general/projects.html', context ,RequestContext(request))
		else:
			return Http404
	else:
		return Http404

####### Contact #####################################
def contact(request):
	if request.method == 'GET':
		return render(request,'general/contact.html', None , RequestContext(request))
	elif request.method == 'POST':
		name = request.POST.get("name")
		email = request.POST.get("email")
		message = request.POST.get("message")

		''' Begin reCAPTCHA validation '''
		recaptcha_response = request.POST.get('g-recaptcha-response')
		url = 'https://www.google.com/recaptcha/api/siteverify'
		values = {
			'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
			'response': recaptcha_response
		}
		data = urllib.parse.urlencode(values).encode()
		req =  urllib.request.Request(url, data=data)
		response = urllib.request.urlopen(req)
		result = json.loads(response.read().decode())
		''' End reCAPTCHA validation '''

		if result['success']:
			email_send = get_templated_mail(
				template_name='contact_us',
				from_email=settings.EMAIL_HOST_USER,
				to=["elias.gonzalezma@usach.cl"],
				context={
					'message':message,
					'name':name,
					'from' : email,
				}
			)

			email_send.send()
			messages.add_message(request, messages.SUCCESS, 'Mensaje enviado con éxito!!.', extra_tags='contact')
		else:
			messages.add_message(request, messages.ERROR, 'Re-Captcha invalido.', extra_tags='contact')
		return render(request,'general/contact.html', None , RequestContext(request))
	else:
		return render(request,'error/404.html', None, RequestContext(request))