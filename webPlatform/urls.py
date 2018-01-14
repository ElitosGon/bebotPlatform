# -*- coding: utf-8 *-*
from django.conf.urls import url, include
from webPlatform.views import general_views, collaborator_views, register_views
from django.contrib.auth.views import password_reset, password_reset_confirm, password_reset_complete


urlpatterns = [
	# General
	url(r'^$', general_views.home, name= "home"), 
	url(r'^collaborators/$', general_views.collaborators, name= "collaborators"), 
	url(r'^collaborator/(?P<id>\d+)/$', general_views.collaborator, name= "collaborator"), 
	url(r'^projects/$', general_views.projects, name= "projects"), 


	# Collaborator
	url(r'^account/$', collaborator_views.my_account, name= "my_account"), 
	url(r'^account/update/$', collaborator_views.my_account_update, name= "my_account_update"),
	url(r'^account/change/password/$', collaborator_views.my_account_change_password, name= "my_account_change_password"), 
	url(r'^account/delete/$', collaborator_views.my_account_delete, name= "my_account_delete"),
	
	url(r'^account/projects/$', collaborator_views.my_projects, name= "my_projects"), 
	url(r'^account/project/create/$', collaborator_views.my_project_create, name= "my_project_create"), 
	url(r'^account/project/update/(?P<id>\d+)/$', collaborator_views.my_project_update, name= "my_project_update"), 
	url(r'^account/project/delete/(?P<id>\d+)/$', collaborator_views.my_project_delete, name= "my_project_delete"), 


	url(r'^project/like/(?P<id>\d+)/$', collaborator_views.like_project, name="like_project"),
	url(r'^project/unlike/(?P<id>\d+)/$', collaborator_views.unlike_project, name="unlike_project"),
	
	url(r'^project/lock/(?P<id>\d+)/$', collaborator_views.lock_project, name="lock_project"),
	url(r'^project/unlock/(?P<id>\d+)/$', collaborator_views.unlock_project, name="unlock_project"),


	url(r'^login/$', register_views.log_in, name= "log_in"), 
	url(r'^logout/$', register_views.log_out, name= "log_out"), 
    url(r'^password/reset/complete/$', password_reset_complete, {'template_name': 'registration/password_reset_complete.html' }, name='password_reset_complete'),
	url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),
	
]