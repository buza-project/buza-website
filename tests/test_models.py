from django.test import TestCase

from buza.models import BuzaUser


class TestBUzaUser(TestCase):

    def test_email_user(self):
        email_user = BuzaUser(login="user@buza.com", password="12345", user_name="1234")
        self.assertEqual(email_user.email, "user@buza.com")

    def test_phone_user(self):
        phone_user = BuzaUser(login="0764270487", password="12345", user_name="1234")
        self.assertEqual(phone_user.email, "user@buza.com")
