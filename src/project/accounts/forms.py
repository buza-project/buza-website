from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
	# additional fields
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	confirmPassword = forms.CharField(
		label='Confirm Password', widget=forms.PasswordInput)
	# get the values that are already in the model

	class Meta:
		model = User
		fields = ('username', 'first_name', 'email')

	# check if the passwords match

	def clean_ConfirmedPassword(self):
		cd= self.cleaned_data
		if cd['password'] != cd['confirmPassword']:
			raise forms.ValidationError('Passwords do not match')
		return cd['confirmPassword']


class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
	# allow users to edit all the extra information
	class Meta:
		model = Profile
		fields = ('photo', 'school', 'grade', 'bio')