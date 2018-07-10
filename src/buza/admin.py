from django.contrib import admin

from .models import BuzaUser


class BuzaAdmin(admin.ModelAdmin):
    # Register your models here.
    list_display = ['user_name', 'school', 'reputation']


admin.site.register(BuzaUser, BuzaAdmin)
