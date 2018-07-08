# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from .models import Board, Question, Answer
from project.accounts.models import Profile
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


@login_required
def all_boards(request):
    boards = Board.objects.all()
    update_boards()
    return render(request, 'boards/boards.html', {'boards': boards})


@login_required
def board_questions(request, board_name):
    board = Board.objects.get(Q(title=board_name) | Q(slug=board_name))
    questions = Question.objects.filter(board=board)
    return render(request, 'boards/questions.html', {'questions': questions})


@login_required
def my_boards(request):
    profile = request.user.user_profile
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
        ask_form = AskForm(
            files=request.FILES,
            instance=request.user,
            data=request.POST,
        )

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

    ask_form = AskForm(
        instance=request.user, files=request.FILES, data=request.POST)
    return render(request, 'boards/ask_question.html', {'form': ask_form})


@login_required
def edit_question(request, question_id, question_slug):
    question = Question.objects.get(pk=question_id)
    user = User.objects.get(pk=question.user.pk)
    profile = Profile.objects.get(pk=user.pk)
    if request.method == 'POST' and 'answer-question':
        edit_form = EditQuestionForm(
            files=request.FILES, instance=request.user, data=request.POST)
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
    user = question.user
    profile = user.user_profile
    answer_form = AnswerForm()
    try:
        answers = question.answers.all()
    except:
        answers = []
    if request.method == 'POST' and 'vote-up-answer' in request.POST:
        answer_id = request.POST['vote-up-answer']
        answer = question.answers.get(pk=answer_id)
        answer.votes.up(request.user.pk)
    elif request.method == 'POST' and 'vote-down-answer' in request.POST:
        answer_id = request.POST['vote-down-answer']
        answer = question.answers.get(pk=answer_id)
        answer.votes.down(request.user.pk)
    elif request.method == 'POST' and 'vote-up-question' in request.POST:
        question.votes.up(request.user.pk)
    elif request.method == 'POST' and 'star' in request.POST:
        question.votes.starred(request.user.pk)
    elif request.method == 'POST' and 'answer-button' in request.POST:
        answer_form = AnswerForm(
            files=request.FILES, data=request.POST)
        # check if the user has already replied
        if question.answers.filter(user=request.user).count() > 0:
            messages.success(request, 'Answer update')

        elif answer_form.is_valid():
            new_answer = Answer(
                answer=request.POST['answer'],
                media=request.FILES.get('media'),
                question=question,
                user=request.user)
            new_answer.save()
            answers = question.answers.all()
            messages.success(request, 'Answer posted')
            # replace with http redirect url
            return render(
                request, 'boards/question_view.html',
                {'question': question, 'board': question.board,
                 'user': question.user, 'profile': profile,
                 'answers': answers})
        else:
            messages.success(request, 'There was an error posting your reply')

    return render(
        request, 'boards/question_view.html',
        {'question': question, 'board': question.board,
         'user': question.user, 'profile': profile,
         'answers': answers,
         'answer_form': answer_form})
