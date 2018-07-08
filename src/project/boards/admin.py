# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from project.boards.models import (Answer, AnswerComment, Board, Question,
                                   QuestionComment)


# Register your models here.


admin.site.register(Board)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswerComment)
admin.site.register(QuestionComment)
