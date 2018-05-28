# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Board, Question, Answer
from django.http import HttpResponse
from accounts.models import Profile
from .forms import AskForm

# Create your views here.


# checks if the user is logged in
@login_required
def all_questions(request):

	questions = Question.objects.all()
	# some ordering logic for the questions
	return render(
		request, 'boards/questions.html',
		{'section': 'questions', 'questions': questions})


def view_question(request, question_id, question_slug, board_name):
	# we have a question, we need a board and a user
	question = Question.objects.get(pk=question_id)
	profile = question.user.user_profile
	return render(
		request, 'boards/question_view.html',
		{'question': question, 'board': question.board, 'user': question.user, 'profile': profile})


@login_required
def all_boards(request):
	boards = Board.objects.all()
	update_boards()
	return render(request, 'boards/boards.html', {'boards': boards})


@login_required
def board_questions(request, board_name):
	print("this is a board " + board_name)
	try:
		board = Board.objects.get(title=board_name)
	except:
		board = Board.objects.get(slug=board_name)

	questions = Question.objects.filter(board=board)
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
	return render(
		request, 'boards/users.html', {'section': 'all_users', 'users': users})


def update_boards():
	boards = Board.objects.all()
	# update board values first
	for board in boards:
		board.users_count = board.my_boards.all().count()
		board.questions_count = board.questions.all().count()
		board.save()


@login_required
def ask_question(request):
	if request.method == 'POST':
		ask_form = AskForm(files=request.FILES, instance=request.user, data=request.POST)

		if ask_form.is_valid():
			new_question = ask_form.save(commit=False)
			new_question.user = request.user
			new_question.save()
			return render(request, 'boards/question_view.html', {'question': new_question, 'board': new_question.board, 'user': new_question.user, 'profile': new_question.user.user_profile})

		# else:
		# 	return HttpResponse(ask_form.errors.media)
	ask_form = AskForm(instance=request.user, data=request.POST)
	return render(request, 'boards/ask_question.html', {'form': ask_form})