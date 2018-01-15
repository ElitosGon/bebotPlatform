from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

class WebplatformConfig(AppConfig):
    name = 'webPlatform'
    verbose_name = _('webPlatform')

    def ready(self):
    	from django.contrib.auth.models import User
    	from actstream import registry
    	registry.register(self.get_model('Profile'))
    	registry.register(User)
    	import webPlatform.signals.collaborator_signals

        

