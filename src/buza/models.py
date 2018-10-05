from functools import partial
from typing import Union

from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from taggit import models as tags
from taggit.managers import TaggableManager


# Shortcuts:
_CharField = partial(models.CharField, max_length=1024)


class TimestampedModel(models.Model):
    """
    Base class with `created` and `modified` fields.
    """
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class Subject(models.Model):
    title = _CharField()
    description = models.TextField()

    def __str__(self) -> str:
        return str(self.title)


class Topic(tags.TagBase):
    description = models.TextField()

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    def __str__(self) -> str:
        return f'By {self.name}'


class QuestionTopic(tags.GenericTaggedItemBase):
    tag = models.ForeignKey(
        Topic,
        on_delete=models.PROTECT,
        related_name="question_topics",
    )


class User(AbstractUser):

    # Authentication fields
    phone = models.CharField(
        _('phone number'),
        blank=True,
        max_length=11,
    )

    # School fields
    school = models.CharField(_('school name'), blank=True, null=True, max_length=100)
    school_address = models.CharField(
        _('school address'),
        blank=True, null=True,
        max_length=300,
    )
    grade = models.IntegerField(blank=True, null=True, default=7)

    # Personal fields
    photo = models.ImageField(_('profile photo'),
                              upload_to='users/%Y/%m/%d',
                              blank=True)
    bio = models.CharField(blank=True, null=True, max_length=250)

    subjects = models.ManyToManyField(Subject)

    def __str__(self) -> str:
        return str(self.username)


#: Helper type for Django request users: either anonymous or signed-in.
RequestUser = Union[AnonymousUser, User]


class Question(TimestampedModel, models.Model):

    author = models.ForeignKey(User, on_delete=models.PROTECT)

    title = _CharField(
        verbose_name='Question Summary',
        help_text='Write a short sentence summarising your question',
    )
    body = models.TextField(
        blank=True,
        verbose_name='Question Description',
        help_text='Give a detailed description of your question')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    topics = TaggableManager(
        through=QuestionTopic,
        help_text="List all the relevant topics for this question. " +
                  "Example: Triangles, Equations, Photosynthesis.",
        verbose_name='Topics')
    grade = models.IntegerField(
        validators=[MinValueValidator(7), MaxValueValidator(12)],
        help_text="Which grade it this question most relevant for? " +
                  "By default this will be the grade that you are in.",
    )

    def __str__(self) -> str:
        return f'By {self.author}: {self.title}'


class Answer(TimestampedModel, models.Model):

    author = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    body = models.TextField()

    def __str__(self) -> str:
        question: Question = self.question
        return f'By {self.author} to question {question.pk}: {question.title}'
