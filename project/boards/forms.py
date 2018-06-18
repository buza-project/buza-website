from django import forms
from .models import Question, Answer
from tinymce.widgets import TinyMCE


class AskForm(forms.ModelForm):
	title = forms.CharField(max_length=100)
	description = forms.CharField(
		widget=TinyMCE(attrs={'required': True, 'cols': 30, 'rows': 10}))
	media = forms.ImageField(
		required=False,
		help_text='any files to clarify your question')
	tags = forms.CharField(max_length=40, required=False)
	# label='3 Upload file 1',
	# help_text='*'

	class Meta:
		model = Question
		fields = ('board', )


class EditQuestionForm(forms.ModelForm):
	# users should not be able to edit titles
	title = forms.CharField(max_length=100)
	description = forms.CharField(
		widget=TinyMCE(attrs={'required': True, 'cols': 30, 'rows': 10}))
	media = forms.ImageField(
		required=False,
		help_text='any files to clarify your question')
	tags = forms.CharField(max_length=40, required=False)

	class Meta:
		model = Question
		fields = ('board', 'media', 'title', 'description', 'tags')


class AnswerForm(forms.ModelForm):
	media = forms.FileField(
		required=False,
		help_text='any files to clarify your answer')

	class Meta:
		model = Answer
		fields = ('answer', 'media')
