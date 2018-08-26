from django import template

from buza import models


register = template.Library()


@register.simple_tag
def topic_question_list(topic_name: str):
    return models.Question.objects.filter(topics__name__in=[topic_name])


@register.simple_tag
def user_subjects_list(user):
    # chek if the user is logged in
    # get all the subjects a user follows
    subject_set = models.Subject.objects.all()
    subjects = list(subject_set)

    if user.is_anonymous or not user.subjects.all():
        return subjects

    for subject in subjects:
        if subject in user.subjects.all():
            subjects.remove(subject)
            subjects = [subject] + subjects
    return subjects
