from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


# Models will be added to the db


class BuzaUser(AbstractBaseUser, PermissionsMixin):
    # authentication fields
    email = models.EmailField(
        _('email address'),
        blank=True,
    )
    phone = models.CharField(
        _('phone number'),
        blank=True,
        max_length=11,
    )
    username = models.CharField(
        _('user name'),
        blank=True,
        null=True,
        unique=True,
        max_length=15,
    )
    # school fields
    school = models.CharField(_('school name'), blank=True, null=True, max_length=100)
    school_address = models.CharField(
        _('school address'),
        blank=True, null=True,
        max_length=300,
    )
    grade = models.IntegerField(blank=True, default=7)
    # users personal fields
    photo = models.ImageField(_('profile photo'),
                              upload_to='users/%Y/%m/%d',
                              blank=True)
    bio = models.CharField(blank=True, null=True, max_length=250)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    full_name = models.CharField(
        _('name and surname'),
        blank=True, null=True,
        max_length=100,
    )

    # users can have multiple boards
    # subjects = models.ManyToManyField(Board, related_name="my_boards")

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['']

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return 'Profile for user {}'.format(self.user)
