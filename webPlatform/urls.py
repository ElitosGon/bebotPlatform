# -*- coding: utf-8 *-*
from django.conf.urls import url, include
from webPlatform.views import admin_views, general_views, collaborator_views, register_views
from django.contrib.auth.views import password_reset, password_reset_confirm, password_reset_complete


urlpatterns = [
	# Home
	url(r'^$', general_views.home, name= "home"), 
	url(r'^login/$', register_views.log_in, name= "log_in"), 
	url(r'^logout/$', register_views.log_out, name= "log_out"), 
      

    url(r'^password/reset/complete/$', password_reset_complete, {'template_name': 'registration/password_reset_complete.html' }, name='password_reset_complete'),
	url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),
	


]