# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Board, Question, Answer
from accounts.models import Profile
from .forms import AskForm, EditQuestionForm, AnswerForm

# Create your views here.


# checks if the user is logged in
@login_required
def all_questions(request):

	questions = Question.objects.all()
	# some ordering logic for the questions
	return render(
		request, 'boards/questions.html',
		{'section': 'questions', 'questions': questions})


def view_question_delete_(request, question_id, question_slug, board_name=None):
	# we have a question, we need a board and a user
	question = Question.objects.get(pk=question_id)
	profile = request.user.user_profile
	answers = []
	if question.answers.all():
		answers = question.answers.all()

	return render(
		request, 'boards/question_view.html',
		{'question': question, 'board': question.board,
			'user': question.user, 'profile': profile, 'answers': answers})


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
	profile = request.user.user_profile
	# profile = Profile.objects.get(user=request.user)
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
			board = Board.objects.get(pk=request.POST['board'])
			new_question = Question(
				title=request.POST['title'],
				description=request.POST['description'],
				board=board,
				tags=request.POST['tags'],
				media=request.FILES.get('media', None),
				user=request.user)
			new_question.save()
			messages.success(request, 'Ask question complete')
			return render(
				request, 'boards/question_view.html',
				{'question': new_question,
					'board': new_question.board,
					'user': new_question.user,
					'profile': Profile.objects.get(pk=request.user.pk)})

	ask_form = AskForm(instance=request.user, files=request.FILES, data=request.POST)
	return render(request, 'boards/ask_question.html', {'form': ask_form})


@login_required
def edit_question(request, question_id, question_slug):
	question = Question.objects.get(pk=question_id)
	user = User.objects.get(pk=question.user.pk)
	profile = Profile.objects.get(pk=user.pk)
	if request.method == 'POST':
		edit_form = EditQuestionForm(files=request.FILES, instance=request.user, data=request.POST)
		if edit_form.is_valid():
			edit_form.save()
			question.update(
				request.POST['title'],
				request.POST['description'],
				request.FILES.get('media'),
				Board.objects.get(pk=request.POST['board']),
				request.POST['tags'])

			question.save()
			messages.success(request, 'Edit question complete')
			return render(
				request, 'boards/question_view.html',
				{'question': question, 'board': question.board,
					'user': question.user, 'profile': profile})
		else:
			messages.error(request, 'There was an error while editing your question')
	else:
		edit_form = EditQuestionForm(instance=question)

	return render(
		request, 'boards/edit_question.html',
		{'form': edit_form, 'user': user, 'question': question})


def view_question(request, question_id, question_slug, board_name=None):
	question = Question.objects.get(pk=question_id)
	user = request.user
	profile = user.user_profile
	answers = []
	has_answered = False
	if question.answers.all():
		answers = question.answers.all()
		# check if any of these answers are mine
		if answers.filter(user=request.user):
			has_answered = True

	if request.method == 'POST':
		answer_form = AnswerForm(
			files=request.FILES, instance=request.user, data=request.POST)
		if answer_form.is_valid():
			answer_form.save(commit=False)
			answer_form.question = question
			answer_form.save()
			new_answer = Answer(
				answer=request.POST['answer'],
				media=request.FILES.get('media'),
				question=question,
				user=user)
			new_answer.save()
			messages.success(request, 'Answer posted')
			return render(
				request, 'boards/question_view.html',
				{'question': question, 'board': question.board,
					'user': question.user, 'profile': profile,
					'answers': answers, 'has_answered': has_answered})
		else:
			messages.success(request, 'There was an error posting your reply')
	else:
		answer_form = AnswerForm()

	return render(
		request, 'boards/question_view.html',
		{'question': question, 'board': question.board,
			'user': question.user, 'profile': profile,
			'answers': answers,
			'answer_form': answer_form,
			'has_answered': has_answered})

