from django import forms

from buza.models import BuzaUser as User


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
        fields = ('username', 'email', 'phone')

    # check if the passwords match

    def clean_ConfirmedPassword(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirmPassword']:
            raise forms.ValidationError('Passwords do not match')
        return cd['confirmPassword']


class UserEditForm(forms.ModelForm):
    # allow users to edit all the extra information
    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'photo',
            'full_name',
            'school',
            'school_address',
            'grade',
            'bio')
