# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Board, Question, Answer

# Create your views here.


def home(request):
	boards = Board.objects.all()

	# looks for template named home and passes a var called boards
	return render(request, 'boards/home.html', {'boards': boards})


def board_questions_view(request, subject):
	'''view all set of questions for a board'''

	boards = Board.objects.all()
	questions = Question.objects.filter(board=subject)
	return render(request, 'boards/home.html', {'boards': boards})


def question_view(request, id, slug):
	'''view a specific question, by slugname or id'''
	question = Question.objects.get(id=id)
	if not question:
		question = Question.objects.get(slug=slug)
	answers = Answer.objects.filter(question=question)
	return render(
		request, 'boards/home.html', {'question': question, 'answers': answers})
