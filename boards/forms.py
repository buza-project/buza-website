from django import forms
from .models import Question
from tinymce.widgets import TinyMCE


class AskForm(forms.ModelForm):
	title = forms.CharField(max_length=100)
	description = forms.CharField(
		widget=TinyMCE(attrs={'required': True, 'cols': 30, 'rows': 10}))
	media = forms.FileField(
		required=False,
		help_text='any files to clearify your question')
	tags = forms.CharField(required=False)
	# label='3 Upload file 1',
	# help_text='*'

	class Meta:
		model = Question
		fields = ('board', )
