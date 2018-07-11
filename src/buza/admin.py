from django.contrib import admin

from .models import BuzaUser


class BuzaAdmin(admin.ModelAdmin):
    # Register your models here.
    list_display = ['username', 'school', 'grade']


admin.site.register(BuzaUser, BuzaAdmin)
