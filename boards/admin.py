# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from boards.models import Board, Question

# Register your models here.


admin.site.register(Board)
admin.site.register(Question)
