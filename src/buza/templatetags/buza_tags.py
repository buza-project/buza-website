from django import template

from buza import models


register = template.Library()


@register.simple_tag
def topic_question_list(topic_name: str):
    return models.Question.objects.filter(topics__name__in=[topic_name])
