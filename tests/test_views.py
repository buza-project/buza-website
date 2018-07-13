from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from buza import models


class TestUserDetail(TestCase):

    def test_not_found(self) -> None:
        response = self.client.get(reverse('user-detail', kwargs=dict(pk=404)))
        assert HTTPStatus.NOT_FOUND == response.status_code

    def test_get(self) -> None:
        user = models.User.objects.create(
            first_name='Test',
            last_name='User',
            photo='example.jpeg',
            email='tester@example.com',
            bio='Example bio.',
        )
        response = self.client.get(reverse('user-detail', kwargs=dict(pk=user.pk)))
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'buza/user_detail.html')

        self.assertContains(response, 'Test User', count=2)
        self.assertContains(response, f'<img src="{user.photo.url}">', count=1)
        self.assertContains(response, 'Email: tester@example.com', count=1)
        self.assertContains(response, 'Bio: Example bio.', count=1)
