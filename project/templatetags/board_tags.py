from __future__ import absolute_import

from django import template
from django.contrib.auth.models import AnonymousUser
from django import get_version

register = template.Library()


@register.simple_tag
def already_answered(question, user=AnonymousUser()):
	if get_version() >= '2.0':
		if user.is_anonymous:
			return False
	if question.answers.all():
		answers = question.answers.all()
		print(answers.filter(user=user))
		# check if any of these answers are mine
		if answers.filter(user=user):
			return True
	return False
