# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from .models import Board

# Create your views here.


def home(request):
	return HttpResponse('Buza is Here')
	boards = Board.objects.all()
	board_names = list()

	for board in boards:
		board_names.append(board.name)

	response_html = '<br>'.join(board_names)

	return HttpResponse(response_html)
