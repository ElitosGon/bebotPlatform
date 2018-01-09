from __future__ import absolute_import
from webPlatform import models
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.views  import password_reset, password_reset_confirm
from django.contrib.auth.forms import PasswordChangeForm
from webPlatform.forms import register_forms
from django.urls import reverse

####### Login #####################################
def log_in(request):
	status = None
	if request.user.is_authenticated:
		return redirect('home')
	if request.method == 'POST':

		# BEGIN LOGIN 
		if request.POST['event'] == 'login':
			form = register_forms.LoginForm(request.POST)
			if form.is_valid():
				username = request.POST['username']
				password = request.POST['password']		
				if "@" in username:
					try:
						user_consult = User.objects.get(email=username)
						user = authenticate(username=user_consult.username, password=password)
						if user is not None:
							if user.is_active:
								login(request, user)
								return redirect('home')
							else:
								messages.add_message(request, messages.ERROR, 'Tu usuario esta inactivo.', extra_tags='login')
						else:
							messages.add_message(request, messages.ERROR, 'Email y/o clave incorrecta.', extra_tags='login')
					except User.DoesNotExist:
						messages.add_message(request, messages.ERROR, 'Email no encontrado.', extra_tags='login')
				else:
					user = authenticate(username=username, password=password)
					if user is not None:
						if user.is_active:
							login(request, user)
							return redirect('home')
						else:
							messages.add_message(request, messages.ERROR, 'Tu usuario esta inactivo.', extra_tags='login')
					else:
						messages.add_message(request, messages.ERROR, 'Nombre de usuario y/o clave incorrecta.', extra_tags='login')
			else:
				messages.add_message(request, messages.ERROR, 'Nombre de usuario y/o clave incorrecta.', extra_tags='login')
			# END LOGIN

		if request.POST['event'] == 'recover':
			# BEGIN RECOVER PASSWORD
			email = request.POST['email']
			if email != None:
				try:
					user = User.objects.get(email=email)
					messages.add_message(request, messages.SUCCESS, 'Te hemos enviado por correo electrónico instrucciones para configurar tu contraseña.', extra_tags='recover')
					form = register_forms.LoginForm()
					contexto = { 'form':form , 'status': 'recover'}
					password_reset(request, template_name="registration/log_in.html",
									email_template_name="registration/password_reset_email.html", 
									post_reset_redirect= reverse('log_in'))
				except User.DoesNotExist:
					messages.add_message(request, messages.ERROR, 'Email ingresado no se reconoce.', extra_tags='recover')

			# END RECOVER PASSWORD

		status = request.POST['event']

	form = register_forms.LoginForm()
	contexto = { 'form':form , 'status': status}
	return render(request, 'general/log_in.html', contexto , RequestContext(request))

####### LogOut #####################################
@login_required
def log_out(request):
	logout(request)
	return redirect('home')



