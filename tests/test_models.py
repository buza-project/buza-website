from django.test import TestCase

from buza import models


class TestUser(TestCase):

    def test_defaults(self) -> None:
        user = models.User.objects.create()
        assert {
            'bio': None,
            'date_joined': user.date_joined,
            'email': '',
            'first_name': '',
            'grade': 7,
            'id': user.pk,
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'last_login': None,
            'last_name': '',
            'password': '',
            'phone': '',
            'photo': '',
            'school': None,
            'school_address': None,
            'username': '',
        } == models.User.objects.filter(pk=user.pk).values().get()

    def test_repr(self) -> None:
        assert '<User: test>' == repr(models.User(username='test'))


class TestQuestion(TestCase):

    def test_repr(self) -> None:
        user = models.User(username='tester')
        question = models.Question(
            author=user,
            title='Example question?',
        )
        assert '<Question: By tester: Example question?>' == repr(question)
