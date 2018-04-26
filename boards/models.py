# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

from taggit.managers import TaggableManager
# Create your models here.


class Board(models.Model):
	'''the model for each class'''

	title = models.CharField(max_length=3, unique=True)
	description = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(editable=False)

	def save(self):
		self.slug = slugify(self.name)

	def __unicode__(self):
		return self.slug

	def __str__(self):
		return self.title


class Question(models.Model):
	'''each class has list of questions'''

	title = models.CharField(max_length=100, blank=False)
	description = models.CharField(max_length=400)
	media = models.FileField(upload_to='media/questions/')
	board = models.ForeignKey(Board, related_name='questions')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	user = models.ForeignKey(User, related_name='asked_by')
	slug = models.SlugField(editable=False)

	tags = TaggableManager()

	def save(self):
		self.slug = slugify(self.title)

	def __unicode__(self):
		return self.slug

	def __str__(self):
		return self.title


class Answer(models.Model):
	'''users can post questions that will display on the classroom'''

	answer = models.CharField(max_length=400)
	media = models.CharField(max_length=400)
	question = models.ForeignKey(Question, related_name="answers")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	user = models.ForeignKey(User, related_name='answered_by')


class Comment(models.Model):
	'''a comment can be for a question or an answer'''

	comment = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(null=True)
	user = models.ForeignKey(User, related_name='commented_by')

	class Meta:
		abstract = True


class QuestionComment(Comment):
	'''a comment for a question'''
	user = models.ForeignKey(User, related_name='question_commented_by')
	question = models.ForeignKey(Question, related_name="question_comments")


class AnswerComment(Comment):
	'''a comment for a question'''
	user = models.ForeignKey(User, related_name='answer_commented_by')
	answer = models.ForeignKey(Answer, related_name="reply_comments")
