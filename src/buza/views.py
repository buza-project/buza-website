from django.contrib import messages
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.views import generic

from buza import models

from .forms import UserEditForm, UserRegistrationForm


# Migrate to class based views


def logged_out(request):
    print('logged out')
    logout(request)
    # return redirect('logout')
    return render(request, 'registration/logout.html', {'section': 'logged_out'})


# Changing the user's password
@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_done')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change_index.html', {'form': form})


@login_required
def password_change_done(request):
    '''resetting your password'''
    return render(
        request,
        'registration/password_change_done_index.html',
        {'section': 'password_done'},
    )


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
