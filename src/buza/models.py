from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # authentication fields
    phone = models.CharField(
        _('phone number'),
        blank=True,
        max_length=11,
    )
    # school fields
    school = models.CharField(_('school name'), blank=True, null=True, max_length=100)
    school_address = models.CharField(
        _('school address'),
        blank=True, null=True,
        max_length=300,
    )
    grade = models.IntegerField(blank=True, null=True, default=7)
    # users personal fields
    photo = models.ImageField(_('profile photo'),
                              upload_to='users/%Y/%m/%d',
                              blank=True)
    bio = models.CharField(blank=True, null=True, max_length=250)

    # FIXME: subjects = models.ManyToManyField(Board, related_name="my_boards")

    def __str__(self) -> str:
        return str(self.username)
