# -*- coding: utf-8 *-*
from django.conf.urls import url, include
from webPlatform.views import admin_views, general_views, collaborator_views, register_views

urlpatterns = [
      # Home
      url(r'^$', general_views.Home, name= "Home"), 

]