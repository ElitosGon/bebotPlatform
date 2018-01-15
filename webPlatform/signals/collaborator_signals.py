from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from webPlatform import models
from actstream.models import Follow, Action, following, followers
from notifications.signals import notify
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=Follow)
def model_post_save_Follow(sender, instance, **kwargs):
	if instance.id:
		# object_id, user_id
		user = User.objects.get(pk=instance.user_id)
		target = User.objects.get(pk=instance.object_id)
		verb = "Tienes un nuevo seguidor %s" % user.username
		if user:
			notify.send(user, recipient=target, verb=verb, target=user, lavel='info')

@receiver(post_save, sender=models.Project)
def model_post_save_Project(sender, instance, **kwargs):
	if instance.id:
		# user.id
		if instance.user:
			user = User.objects.get(pk=instance.user.id)
			project = models.Project.objects.get(pk=instance.id)
			followers_list = followers(user)
			verb = "El usuario %s a subido un nuevo proyecto: %s" % (user.username, instance.name)
			if followers_list:
				for follower in followers_list:
					notify.send(project.user, recipient=follower, verb=verb, target=project, lavel='info')

@receiver(post_delete, sender=models.Project)
def model_post_delete_Project(sender, instance, **kwargs):
	if instance.id:
		ctype = ContentType.objects.get(model='project')
		notifications = Notification.objects.filter(target_content_type=ctype, target_object_id=instance.id)
		notifications.delete()

@receiver(post_delete, sender=User)
def model_post_delete_User(sender, instance, **kwargs):
	if instance.id:
		ctype = ContentType.objects.get(app_label="auth", model="user")
		notifications = Notification.objects.filter(actor_content_type=ctype, actor_object_id=instance.id)
		notifications.delete()


			
		
			


