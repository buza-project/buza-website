from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Successfully logged in ')
                else:
                    return HttpResponse('Your account is not yet active')
            else:
                return HttpResponse('Username and password do not match a user')
    else:
        # the request was not a post
        form = LoginForm()
        return render(request, 'registration/login.html', {'form': form})


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
    '''the view for creating user accounts'''
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # create a new user objec but do not save it as of yet
            new_user = user_form.save(commit=False)

            # Set the selected password
            new_user.set_password(user_form.cleaned_data['password'])
            # now we can save the user
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            profile.save()
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
        profile_form = ProfileEditForm(
            instance=request.user.user_profile,
            files=request.FILES,
            data=request.POST,
        )
        if user_form.is_valid() and profile_form.is_valid():
            # get the user's userinfo and their profile details
            user_form.save()
            profile_form.save(request.user)

            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        try:
            profile = request.user.user_profile
        except:
            profile = Profile.objects.create(user=request.user)
            profile.save()
        profile_form = ProfileEditForm(instance=profile)
    return render(
        request,
        'accounts/edit.html',
        {'user_form': user_form, 'profile_form': profile_form},
    )


@login_required
def view(request):
    return render(
        request, 'accounts/edit.html',
        {'user': request.user, 'profile': request.user.user_profile})
