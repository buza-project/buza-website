from django.contrib import admin

from buza import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'school', 'grade']
