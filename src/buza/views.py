from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
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
