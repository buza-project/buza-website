from django.test import TestCase

from buza.models import BuzaUser


class TestBuzaUser(TestCase):

    def test_email_user(self):
        email_user = BuzaUser(login="user@buza.com", password="12345", username="1234")
        self.assertEqual("user@buza.com", email_user.email)

    def test_phone_user(self):
        phone_user = BuzaUser(login="0764270487", password="12345", username="1234")
        self.assertEqual("0764270487", phone_user.phone)
