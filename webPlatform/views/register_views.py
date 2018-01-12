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
from django.db import transaction

####### Login #####################################
@transaction.atomic
def log_in(request):
	storage = messages.get_messages(request)
	storage.used = True
	status = None
	form_sign_up = register_forms.SignUpForm()
	form_log_in = register_forms.LoginForm()

	if request.user.is_authenticated:
		return redirect('home')
	if request.method == 'POST':

		# BEGIN LOGIN 
		if request.POST['event'] == 'login':
			form_log_in = register_forms.LoginForm(request.POST)
			if form_log_in.is_valid():
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
					password_reset(request, template_name="registration/log_in.html",
									email_template_name="registration/password_reset_email.html", 
									post_reset_redirect= reverse('log_in'))
				except User.DoesNotExist:
					messages.add_message(request, messages.ERROR, 'Email ingresado no se reconoce.', extra_tags='recover')

			# END RECOVER PASSWORD

		if request.POST['event'] == 'signup':
			# BEGIN SIGNUP
			form_sign_up = register_forms.SignUpForm(request.POST, request.FILES or None)
			if form_sign_up.is_valid():
				try:
					user = form_sign_up.save()
					user.refresh_from_db()
					user.profile.description = form_sign_up.cleaned_data.get('description')
					user.profile.avatar = form_sign_up.cleaned_data.get('avatar')
					user.save()
					raw_password = form_sign_up.cleaned_data.get('password1')
					user = authenticate(username=user.username, password=raw_password)
					messages.add_message(request, messages.SUCCESS, "Usuario %s creado con exito." % user.username, extra_tags='login')
					status = None
					form_sign_up = register_forms.SignUpForm()
					form_log_in = register_forms.LoginForm()
					context = { 'form_log_in':form_log_in ,'form_sign_up': form_sign_up,'status': status}
					return render(request, 'general/log_in.html', context , RequestContext(request))
				except:
					messages.add_message(request, messages.ERROR, "Problema al crear usuario.", extra_tags='signup')
			else:
				messages.add_message(request, messages.ERROR, "Problema al crear usuario.", extra_tags='signup')
			# END SIGNUP

		
		status = request.POST['event']

	context = { 
				 'form_log_in':form_log_in ,
				 'form_sign_up': form_sign_up,
				 'status': status
			    }

	return render(request, 'general/log_in.html', context , RequestContext(request))

####### LogOut #####################################
@login_required
def log_out(request):
	logout(request)
	return redirect('home')