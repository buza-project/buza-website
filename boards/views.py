# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Board, Question, Answer
from accounts.models import Profile

# Create your views here.


# checks if the user is logged in
@login_required
def all_questions(request):

	questions = Question.objects.all()
	# some ordering logic for the questions
	return render(request, 'boards/questions.html', {'section': 'questions', 'questions': questions})


def view_question(request, pk, slug):
	questions = Question.objects.get(pk=pk)
	# view one specific question

	return render(request, 'boards/questions.html', {'section': 'all_questions', 'questions': questions})


@login_required
def all_boards(request):
	boards = Board.objects.all()
	update_boards()
	return render(request, 'boards/boards.html', {'boards': boards})


@login_required
def board_questions(request, board_name):
	print("waz the issue")
	questions = Question.objects.filter(title=board_name)
	return render(request, 'boards/questions.html', {'questions': questions})


@login_required
def my_boards(request):
	# profile = request.user.user_profile
	profile = Profile.objects.get(author_id=request.user)
	my_boards = profile.boards.all()
	return render(request, 'boards/boards.html', {'boards': my_boards})


@login_required
def all_users(request):
	users = User.objects.all()
	return render(request, 'boards/users.html', {'section': 'all_users', 'users': users})


def update_boards():
	boards = Board.objects.all()
	# update board values first
	for board in boards:
		board.users_count = board.my_boards.all().count()
		board.questions_count = board.questions.all().count()
		board.save()
