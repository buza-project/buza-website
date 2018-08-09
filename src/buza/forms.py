from django import forms

from buza.models import User


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
