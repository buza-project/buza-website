from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from buza import models
from buza.forms import UserEditForm, UserRegistrationForm


# TODO: Migrate to class based views


def register(request: HttpRequest) -> HttpResponse:
    """
    Register a user account.
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object, but do not save it as of yet.
            new_user = user_form.save(commit=False)

            # Set the selected password
            new_user.set_password(user_form.cleaned_data['password'])
            # now we can save the user
            new_user.save()
            return render(
                request,
                'accounts/register_done.html',
                {'new_user': new_user},
            )
    else:
        # User did not fill in form correctly
        user_form = UserRegistrationForm()
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


class UserDetail(generic.DetailView):
    model = models.User


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
    ]
    question: models.Question

    def dispatch(
            self,
            request: HttpRequest,
            *args: Any,
            pk: int,
            **kwargs: Any,
    ) -> HttpResponse:
        """
        Look up the question, and set `self.question`.
        """
        self.question = get_object_or_404(models.Question, pk=pk)
        if not request.user.is_authenticated:
            print("I am logged in")
            return redirect_to_login(request.get_full_path())
        if self.question.author != request.user:
            return HttpResponseRedirect(
                reverse('question-detail', kwargs=dict(pk=self.question.pk)))
        return super().dispatch(request, *args, **kwargs)

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
