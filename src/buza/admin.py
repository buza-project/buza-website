from django.contrib import admin

from .models import User


class BuzaAdmin(admin.ModelAdmin):
    # Register your models here.
    list_display = ['username', 'school', 'grade']


admin.site.register(User, BuzaAdmin)
