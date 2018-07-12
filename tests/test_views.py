from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from buza import models


class TestUserDetail(TestCase):

    def test_get__anonymous(self) -> None:
        response = self.client.get(reverse('view'))
        self.assertRedirects(response, '/accounts/login/?next=/account/view/')

    def test_get__authenticated(self) -> None:
        user = models.User.objects.create()
        self.client.force_login(user)
        response = self.client.get(reverse('view'))
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'accounts/edit.html')
        assert 'user' in response.context
        assert user == response.context['user']
