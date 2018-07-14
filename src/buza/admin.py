from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from buza import models


@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    """
    Extend the base Django UserAdmin with support for some Buza fields.
    """

    list_display = list(DjangoUserAdmin.list_display) + ['grade']
    list_filter = list(DjangoUserAdmin.list_filter) + ['grade']

    fieldsets = list(DjangoUserAdmin.fieldsets[:1]) + [
        (_('Buza fields'), {'fields': [
            'phone',
            'grade',
            'photo',
            'bio',
        ]}),
    ] + list(DjangoUserAdmin.fieldsets[1:])
