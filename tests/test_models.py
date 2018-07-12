from django.test import TestCase

from buza import models


class TestBuzaUser(TestCase):

    def test_repr(self):
        assert '<BuzaUser: test>' == repr(models.BuzaUser(username='test'))
