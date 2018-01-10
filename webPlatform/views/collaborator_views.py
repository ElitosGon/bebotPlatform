from __future__ import absolute_import
from webPlatform import models
from django.shortcuts import render, redirect
from django.template import RequestContext
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from webPlatform.forms import collaborator_forms
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

####### My account #####################################
@login_required
def my_account(request):
    if request.method == 'GET':
        return render(request,'collaborator/my_account.html', None , RequestContext(request))
    else:
        return render(request,'error/404.html', None, RequestContext(request))

####### My account update ##############################
@login_required
@transaction.atomic
def my_account_update(request):
    if request.method == 'POST':
        user_form = collaborator_forms.UserForm(request.POST, instance=request.user)
        profile_form = collaborator_forms.ProfileForm(request.POST, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(request, messages.SUCCESS, 'Perfil actualizado con exito.', extra_tags='my_account_update')
            return redirect('my_account')
        else:
            messages.add_message(request, messages.ERROR, 'Error al actualizar perfil.', extra_tags='my_account_update')
    else:
        user_form = collaborator_forms.UserForm(instance=request.user)
        profile_form = collaborator_forms.ProfileForm(instance=request.user.profile)
        profile = models.Profile.objects.get(pk=request.user.profile.id)
    return render(request, 'collaborator/my_account_update.html', { 'user_form': user_form, 'profile_form': profile_form, 'profile': profile }, RequestContext(request))

####### My account change password ####################
@login_required
@transaction.atomic
def my_account_change_password(request):
    if request.method == 'POST':
        form = collaborator_forms.PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            messages.add_message(request, messages.SUCCESS, 'Tu contraseña ha sido cambiada con exito.', extra_tags='my_account_change_password')
            return redirect('my_account')
        else:
            messages.add_message(request, messages.ERROR, 'Error al cambiar contraseña.', extra_tags='my_account_change_password')
    else:
        form = collaborator_forms.PasswordChangeForm(request.user)
    return render(request, 'collaborator/my_account_change_password.html', {'form': form }, RequestContext(request))