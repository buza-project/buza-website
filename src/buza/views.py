from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic

from buza import models

from .forms import UserEditForm, UserRegistrationForm


# Migrate to class based views


def register(request):
    """the view for creating user accounts"""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # create a new user objec but do not save it as of yet
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
        # user did not fill in form correctly
        user_form = UserRegistrationForm()
    return render(
        request,
        'accounts/register.html',
        {'user_form': user_form},
    )


# allowing users to edit their own profiles
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            files=request.FILES,
            data=request.POST,
        )

        if user_form.is_valid():
            # get the user's userinfo and their profile details
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
