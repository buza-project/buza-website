from django import forms

from buza.models import User


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirmPassword = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone')

    def clean_ConfirmedPassword(self) -> str:
        """
        Check if the passwords match
        """
        password: str = self.cleaned_data['password']
        confirmPassword: str = self.cleaned_data['confirmPassword']
        if password != confirmPassword:
            raise forms.ValidationError('Passwords do not match')
        return confirmPassword


class UserEditForm(forms.ModelForm):
    """
    Allow users to edit all the extra information
    """
    class Meta:
        model = User
        fields = (
            'email',
            'phone',
            'photo',
            'first_name',
            'last_name',
            'school',
            'school_address',
            'grade',
            'bio')
