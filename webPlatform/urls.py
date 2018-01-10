# -*- coding: utf-8 *-*
from django.conf.urls import url, include
from webPlatform.views import admin_views, general_views, collaborator_views, register_views
from django.contrib.auth.views import password_reset, password_reset_confirm, password_reset_complete


urlpatterns = [
	# General
	url(r'^$', general_views.home, name= "home"), 
	
	# Collaborator
	url(r'^account/$', collaborator_views.my_account, name= "my_account"), 
	url(r'^account/update/$', collaborator_views.my_account_update, name= "my_account_update"),
	url(r'^account/change/password/$', collaborator_views.my_account_change_password, name= "my_account_change_password"), 



	url(r'^login/$', register_views.log_in, name= "log_in"), 
	url(r'^logout/$', register_views.log_out, name= "log_out"), 
    url(r'^password/reset/complete/$', password_reset_complete, {'template_name': 'registration/password_reset_complete.html' }, name='password_reset_complete'),
	url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),
	



]