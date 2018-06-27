# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import resolve
from django.core.urlresolvers import reverse

from project.boards.views import home
# Adding tests for al models.

# Tests for boards models


class HomeTests(TestCase):
	'''test that the comeview takes the user to the right views'''
	# has to be logged in first

	def test_home_view_status_code(self):
		url = reverse('home')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_home_url_resolves_home_view(self):
		view = resolve('/')
		self.assertEquals(view.func, home)


class TestQuestion(TestCase):
	"""test if users can add questions"""