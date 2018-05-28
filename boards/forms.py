from django import forms
from .models import Question


class AskForm(forms.ModelForm):

	class Meta:
		model = Question
		fields = ('title', 'description', 'board', 'media', 'tags')
