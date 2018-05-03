# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Board, Question, Answer

# Create your views here.


# checks if the user is logged in
def all_questions(request):

	questions = Question.objects.all()
	# some ordering logic for the questions
	print(questions)
	return render(request, 'boards/questions.html', {'section': 'all_questions', 'questions': questions})


def view_question(request, pk, slug):
	questions = Question.objects.get(pk=pk)
	# view one specific question

	return render(request, 'boards/questions.html', {'section': 'all_questions', 'questions': questions})


@login_required
def all_classrooms(request):
	boards = Board.objects.all()

	return render(request, 'boards/classrooms.html', {'section': 'classrooms', 'boards': boards})


@login_required
def all_users(request):
	users = User.objects.all()
	return render(request, 'boards/users.html', {'section': 'all_users', 'users': users})
