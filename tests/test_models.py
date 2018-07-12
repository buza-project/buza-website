from django.test import TestCase

from buza import models


class TestUser(TestCase):

    def test_repr(self):
        assert '<User: test>' == repr(models.User(username='test'))
