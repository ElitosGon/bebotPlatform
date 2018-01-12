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
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
            messages.add_message(request, messages.SUCCESS, 'Perfil actualizado con éxito.', extra_tags='my_account_update')
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
            messages.add_message(request, messages.SUCCESS, 'Tu contraseña ha sido cambiada con éxito.', extra_tags='my_account_change_password')
            return redirect('my_account')
        else:
            messages.add_message(request, messages.ERROR, 'Error al cambiar contraseña.', extra_tags='my_account_change_password')
    else:
        form = collaborator_forms.PasswordChangeForm(request.user)
    return render(request, 'collaborator/my_account_change_password.html', {'form': form }, RequestContext(request))

####### My account delete ####################
@login_required
@transaction.atomic
def my_account_delete(request):
    user = User.objects.get(pk=request.user.pk)
    user.delete()
    logout(request)
    return redirect('home')

####### Project likes ####################
@login_required
@transaction.atomic
def like_project(request, id):
    project = models.Project.objects.get(pk=id)
    project.votes.up(request.user.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

####### Project unlike ####################
@login_required
@transaction.atomic
def unlike_project(request, id):
    project = models.Project.objects.get(pk=id)
    project.votes.delete(request.user.id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

####### Follow user ####################
@login_required
@transaction.atomic
def follow_user(request, id):
    user_followed = User.objects.get(pk=id)
    user_following = User.objects.get(pk=request.user.id)
    user_following.profile.follows.add(user_followed)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

####### Unfollow user ####################
@login_required
@transaction.atomic
def unfollow_user(request, id):
    user_followed = User.objects.get(pk=id)
    user_following = User.objects.get(pk=request.user.id)
    user_following.profile.follows.remove(user_followed)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

####### Own Projects
@login_required
def my_projects(request):
    if request.method == 'GET':
        query = request.GET.get("search")
        provider = request.GET.get("provider")
        projects = models.Project.objects.filter(user=request.user.id).order_by('-updated_at')

        if query:
                projects = projects.filter(Q(name__icontains=query) |
                                           Q(description__icontains=query) |
                                           Q(source__name__icontains=query) |
                                           Q(providers__name__icontains=query) |
                                           Q(services__name__icontains=query) |
                                           Q(tags__name__icontains=query)).distinct()

        if provider != '0' and provider != None:
            projects = projects.filter(providers__id=provider).distinct()

        if projects:
            page = request.GET.get('page', 1)
            paginator = Paginator(projects, 5)

            try:
                projects = paginator.page(page)
            except PageNotAnInteger:
                projects = paginator.page(1)
            except EmptyPage:
                projects = paginator.page(paginator.num_pages)

            return render(request,'collaborator/my_projects.html', {'projects': projects} , RequestContext(request))

        return render(request,'collaborator/my_projects.html', None , RequestContext(request))
    else:
        return render(request,'error/404.html', None, RequestContext(request))

@login_required
@transaction.atomic
def my_project_create(request):
    storage = messages.get_messages(request)
    storage.used = True
    form = collaborator_forms.ProjectForm()

    if request.method == 'POST':
        form = collaborator_forms.ProjectForm(request.POST)
        if form.is_valid():
            try:
                project = form.save()
                project.user = request.user
                project.save()
                messages.add_message(request, messages.SUCCESS, "Projecto %s registrado con éxito." % project.name, extra_tags='my_project_create')
                return redirect('my_projects')
            except:
                messages.add_message(request, messages.ERROR, "Problema al registar proyecto.", extra_tags='my_project_create')
        else:
            messages.add_message(request, messages.ERROR, "Problema al registar proyecto.", extra_tags='my_project_create')

    context = {'form': form}

    return render(request, 'collaborator/my_project_create.html', context , RequestContext(request))

@login_required
@transaction.atomic
def my_project_update(request, id):
    project = models.Project.objects.get(pk=id)
    if request.method == 'POST':
        form = collaborator_forms.ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Registro actualizado con éxito.', extra_tags='my_project_update')
            return redirect('my_projects')
        else:
            messages.add_message(request, messages.ERROR, 'Error al actualizar registro.', extra_tags='my_project_update')
    else:
        form = collaborator_forms.ProjectForm(instance=project)
    return render(request, 'collaborator/my_project_update.html', { 'form': form }, RequestContext(request))

@login_required
@transaction.atomic
def my_project_delete(request, id):
    project = models.Project.objects.get(pk=id)
    project.delete()
    messages.add_message(request, messages.SUCCESS, 'Proyecto borrado con éxito.', extra_tags='my_project_delete')
    return redirect('my_projects')