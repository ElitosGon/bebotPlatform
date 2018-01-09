from __future__ import absolute_import
from webPlatform import models
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.conf import settings

####### HOME #####################################
def home(request):
	if request.method == 'GET':
		return render(request,'general/home.html', None , RequestContext(request))
	else:
		return render(request,'error/404.html', None, RequestContext(request))

