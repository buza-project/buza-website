from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from buza.models import User


class UserEditForm(forms.ModelForm):
    """
    Allow users to edit all the extra information
    """

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Save Changes'))

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
