from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from buza import models


@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    """
    Extend the base Django UserAdmin with support for some Buza fields.
    """

    date_hierarchy = 'date_joined'
    ordering = ['-date_joined']
    list_display = list(DjangoUserAdmin.list_display) + ['grade', 'date_joined']
    list_filter = list(DjangoUserAdmin.list_filter) + ['grade']

    fieldsets = list(DjangoUserAdmin.fieldsets[:1]) + [
        (_('Buza fields'), {'fields': [
            'phone',
            'grade',
            'photo',
            'bio',
        ]}),
    ] + list(DjangoUserAdmin.fieldsets[1:])


class AnswerInline(admin.TabularInline):
    extra = 0
    model = models.Answer

    fields = ['author', 'body']
    raw_id_fields = ['author']


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    ordering = ['-created']
    list_display = ['title', 'author', 'created', 'subject']
    search_fields = ['title', 'author__username', 'subject__title']
    list_filter = ['subject']

    raw_id_fields = ['author', 'subject']
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


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    ordering = ['-title']
    list_display = ['title', 'description']
    search_fields = ['title', 'description']


class QuestionTopicsInline(admin.TabularInline):
    extra = 0
    model = models.QuestionTopic
    fields = ['content_type']


@admin.register(models.Topic)
class TopicsAdmin(admin.ModelAdmin):
    search_fields = ['tag']
    fields = ['name', 'description']

    inlines = [QuestionTopicsInline]
