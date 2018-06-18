# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import resolve
from django.core.urlresolvers import reverse

from .views import home
# Create your tests here.


class HomeTests(TestCase):
	'''test that the comeview takes the user to the right views'''

	def test_home_view_status_code(self):
		url = reverse('home')
		response = self.client.get(url)
		self.assertEquals(response.status_code, 200)

	def test_home_url_resolves_home_view(self):
		view = resolve('/')
		self.assertEquals(view.func, home)
