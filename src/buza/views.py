from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from buza import models
from buza.forms import UserEditForm


# TODO: Migrate to class based views


class BuzaUserCreationForm(UserCreationForm):
    """
    Like Django's `UserCreationForm`, but point at Buza's `User` model.
    """

    class Meta(UserCreationForm.Meta):
        model = models.User


def register(request: HttpRequest) -> HttpResponse:
    """
    Register a user account.
    """
    if request.method == 'POST':
        user_form = BuzaUserCreationForm(request.POST)

        if user_form.is_valid():
            # Save the new user.
            new_user = user_form.save()
            return render(
                request,
                'accounts/register_done.html',
                {'new_user': new_user},
            )
    else:
        # User did not fill in form correctly
        user_form = BuzaUserCreationForm()
    return render(
        request,
        'accounts/register.html',
        {'user_form': user_form},
    )


@login_required  # type: ignore
def edit(request: HttpRequest) -> HttpResponse:
    """
    Allow user to edit their own profile.
    """
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            files=request.FILES,
            data=request.POST,
        )

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(
        request,
        'accounts/edit.html',
        {'user_form': user_form},
    )


class TopicDetail(generic.DetailView):
    model = models.Topic


class SubjectDetail(generic.DetailView):
    model = models.Subject


class SubjectList(generic.ListView):
    model = models.Subject

    def post(self, request, *args, **kwargs):
        if 'follow-subject' in request.POST:
            subject: models.Subject = models.Subject.objects.get(
                pk=request.POST['follow-subject'],
            )
            request.user.subjects.add(subject)
            return HttpResponseRedirect(reverse('subject-list'))
        elif 'unfollow-subject' in request.POST:
            subject = models.Subject.objects.get(
                pk=request.POST['unfollow-subject'],
            )
            request.user.subjects.remove(subject)
            return HttpResponseRedirect(reverse('subject-list'))
        return HttpResponseRedirect(
            reverse('subject-list'))


class UserSubjectsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'buza/my_subjects_list.html'


class UserDetail(generic.DetailView):
    model = models.User

    # Avoid conflicting with 'user' (the logged-in user)
    context_object_name = 'user_object'


class QuestionDetail(generic.DetailView):
    model = models.Question


class QuestionList(generic.ListView):
    model = models.Question
    ordering = ['-created']


class QuestionCreate(LoginRequiredMixin, generic.CreateView):
    model = models.Question
    fields = [
        'title',
        'body',
        'subject',
        'topics',
    ]

    def form_valid(self, form: ModelForm) -> HttpResponse:
        """
        Set the question's author to the posting user.
        """
        question: models.Question = form.instance
        author: models.User = self.request.user
        assert author.is_authenticated, author
        question.author = author
        return super().form_valid(form)

    def get_success_url(self) -> str:
        """
        Redirect to the question.
        """
        question: models.Question = self.object
        success_url: str = reverse('question-detail', kwargs=dict(pk=question.pk))
        return success_url


class QuestionUpdate(LoginRequiredMixin, generic.UpdateView):
    model = models.Question
    fields = [
        'title',
        'body',
        'subject',
        'topics',
    ]

    def get_object(self, queryset=None):
        """
        Permission check: Users can only edit their own questions.

        TODO (Pi): Use django-auth-utils for this?
        """
        question: models.Question = super().get_object(queryset)
        if question.author != self.request.user:
            raise PermissionDenied('You can only edit your own questions.')
        question.content_object_id = question.pk
        return question

    def get_success_url(self) -> str:
        """
        Redirect to the question.
        """
        question: models.Question = self.object
        success_url: str = reverse('question-detail', kwargs=dict(pk=question.pk))
        return success_url


class AnswerCreate(LoginRequiredMixin, generic.CreateView):
    """
    Post a new answer to a question.

    Expects `question_pk` as a view argument.
    """

    model = models.Answer
    fields = [
        'body',
    ]

    question: models.Question

    def dispatch(
            self,
            request: HttpRequest,
            *args: Any,
            question_pk: int,
            **kwargs: Any,
    ) -> HttpResponse:
        """
        Look up the question, and set `self.question`.
        """
        self.question = get_object_or_404(models.Question, pk=question_pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form: ModelForm) -> HttpResponse:
        """
        Set the answer's author to the posting user.
        """
        answer: models.Answer = form.instance
        author: models.User = self.request.user
        assert author.is_authenticated, author
        answer.author = author
        answer.question = self.question
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Add the question to the context.
        """
        context_data: Dict[str, Any] = super().get_context_data(**kwargs)
        context_data.setdefault('question', self.question)
        return context_data

    def get_success_url(self) -> str:
        """
        Redirect to the question.
        """
        answer: models.Answer = self.object
        question: models.Question = answer.question
        success_url: str = reverse('question-detail', kwargs=dict(pk=question.pk))
        return success_url


class AnswerUpdate(LoginRequiredMixin, generic.UpdateView):
    """
    Post a new answer to a question.

    Expects `question_pk` as a view argument.
    """

    model = models.Answer
    fields = [
        'body',
    ]

    def get_object(self, queryset: QuerySet = None) -> models.Answer:
        """
        Permission check: Users can only edit their own answers.

        TODO (Pi): Use django-auth-utils for this?
        """
        answer: models.Answer = super().get_object(queryset)
        if answer.author != self.request.user:
            raise PermissionDenied('You can only edit your own answers.')
        return answer

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Add the question to the context.
        """
        answer: models.Answer = self.object
        context_data: Dict[str, Any] = super().get_context_data(**kwargs)
        context_data.setdefault('question', answer.question)
        return context_data

    def get_success_url(self) -> str:
        """
        Redirect to the question.
        """
        answer: models.Answer = self.object
        question: models.Question = answer.question
        success_url: str = reverse('question-detail', kwargs=dict(pk=question.pk))
        return success_url
