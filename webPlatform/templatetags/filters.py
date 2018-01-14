from django.contrib.contenttypes.models import ContentType
from django.template import Variable, Library, Node, TemplateSyntaxError
from django.template.loader import render_to_string
from django.template.loader import get_template

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

from actstream.models import Follow, Action
from webPlatform import models

register = Library()

@register.filter(name='followers_num')
def followers_num(user):
    """
    Returns number of followers users for the given user
    ::
        {{ request.user|followers_num }}
    """
    return Follow.objects.followers_qs(user).count()

@register.filter(name='projects_num')
def projects_num(user):
    """
    Returns number of projects for the given user
    ::
        {{ request.user|projects_num }}
    """
    projects = models.Project.objects.filter(user=user.id, is_public=True)
    return projects.count()

@register.filter(name='project_likes')
def project_likes(project):
    """
    Returns number of likes for the given project
    ::
        {{ project|user_like }}
    """
    project = models.Project.objects.get(pk=project.id)
    return project.votes.count()

@register.filter(name='is_user_like_project')
def is_user_like_project(project, user_id):
    """
    Returns True if the user likes the project
    ::
        {{ project|is_user_like_project:user_id }}
    """
    project = models.Project.objects.get(pk=project.id)
    return project.votes.exists(user_id)




			