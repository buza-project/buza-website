from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from buza import models, views


class TestUserUpdate(TestCase):

    def _authenticated_user(self) -> models.User:
        """
        Create and return an authenticated user.
        """
        user: models.User = models.User.objects.create()
        self.client.force_login(user)
        return user

    def _assert_successful(self, user: models.User, response: HttpResponse) -> None:
        """
        Helper: Assert a successful form post.
        """
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'accounts/edit.html')

        assert 'user_form' in response.context
        form: views.UserEditForm = response.context['user_form']  # noqa: E701
        assert user == form.instance
        assert [] == form.non_field_errors()
        assert {} == form.errors
        assert form.is_valid()

    def test_get__anonymous(self):
        response = self.client.get(reverse('edit'))
        self.assertRedirects(response, '/auth/login/?next=/edit/')

    def test_post__anonymous(self):
        response = self.client.post(reverse('edit'))
        self.assertRedirects(response, '/auth/login/?next=/edit/')

    def test_get__authenticated(self):
        user = self._authenticated_user()
        response = self.client.get(reverse('edit'))
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'accounts/edit.html')

        assert 'user_form' in response.context
        form: views.UserEditForm = response.context['user_form']  # noqa: E701
        assert user == form.instance
        assert not form.is_bound

    def test_post__empty(self):
        user = self._authenticated_user()
        response = self.client.post(reverse('edit'))
        self._assert_successful(user, response)

    def test_post__blank(self):
        user = self._authenticated_user()
        response = self.client.post(reverse('edit'), data={
            'email': '',
            'phone': '',
            'photo': '',
            'first_name': '',
            'last_name': '',
            'school': '',
            'school_address': '',
            'grade': '',
            'bio': '',
        })
        self._assert_successful(user, response)


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
