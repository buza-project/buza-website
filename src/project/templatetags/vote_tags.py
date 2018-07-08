from __future__ import absolute_import

from django import template
from django.contrib.auth.models import AnonymousUser
from django import get_version

from project.vote.models import UP

register = template.Library()


@register.simple_tag
def vote_exists(model, user=AnonymousUser(), action=UP):
    if get_version() >= '2.0':
        if user.is_anonymous:
            return False
    elif user.is_anonymous():
        return False
    return model.votes.exists(user.pk, action=action)


@register.simple_tag
def vote_count(model):
    return model.votes.count()


@register.simple_tag
def is_starred(model, user=AnonymousUser):
    if get_version() >= '2.0':
        if user.is_anonymous:
            return False
    elif user.is_anonymous():
        return False
    return model.votes.get_star(user.pk)
