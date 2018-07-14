from django.contrib import admin

from buza import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'school', 'grade']


class AnswerInline(admin.TabularInline):
    extra = 0
    model = models.Answer

    fields = ['author', 'body']
    raw_id_fields = ['author']


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    ordering = ['-created']
    list_display = ['title', 'author', 'created']
    search_fields = ['title', 'author__username']

    raw_id_fields = ['author']
    readonly_fields = ['created', 'modified']

    inlines = [AnswerInline]


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    ordering = ['-created']
    list_display = ['body', 'author', 'question', 'created']
    search_fields = [
        'body',
        'author__username',
        'question__author__username',
        'question__title',
    ]

    raw_id_fields = ['author', 'question']
    readonly_fields = ['created', 'modified']
