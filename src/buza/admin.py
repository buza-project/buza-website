from django.contrib import admin

from buza import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'school', 'grade']


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    ordering = ['-created']
    list_display = ['title', 'author', 'created']
    search_fields = ['title', 'author__username']

    raw_id_fields = ['author']
    readonly_fields = ['created', 'modified']
