from http import HTTPStatus

from django.forms import ModelForm
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

    def test_get__anonymous(self) -> None:
        response = self.client.get(reverse('edit'))
        self.assertRedirects(response, '/auth/login/?next=/edit/')

    def test_post__anonymous(self) -> None:
        response = self.client.post(reverse('edit'))
        self.assertRedirects(response, '/auth/login/?next=/edit/')

    def test_get__authenticated(self) -> None:
        user = self._authenticated_user()
        response = self.client.get(reverse('edit'))
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'accounts/edit.html')

        assert 'user_form' in response.context
        form: views.UserEditForm = response.context['user_form']  # noqa: E701
        assert user == form.instance
        assert not form.is_bound

    def test_post__empty(self) -> None:
        user = self._authenticated_user()
        response = self.client.post(reverse('edit'))
        self._assert_successful(user, response)

    def test_post__blank(self) -> None:
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


class TestQuestionDetail(TestCase):

    def test_not_found(self) -> None:
        response = self.client.get(reverse('user-detail', kwargs=dict(pk=404)))
        assert HTTPStatus.NOT_FOUND == response.status_code

    def test_get(self) -> None:
        user = models.User.objects.create()
        question = models.Question.objects.create(
            author=user,
            title='Example question?',
            body='A question.',
        )
        path = reverse('question-detail', kwargs=dict(pk=question.pk))
        response = self.client.get(path)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'buza/question_detail.html')

        assert question == response.context['question']
        self.assertContains(response, question.title, count=2)
        self.assertContains(response, question.body, count=1)

        # TODO: Answer display.


class TestQuestionList(TestCase):

    def test_get__empty(self) -> None:
        response = self.client.get(reverse('question-list'))
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'buza/question_list.html')

        self.assertQuerysetEqual(response.context['question_list'], [])


class TestQuestionCreate(TestCase):

    def test_get__anonymous(self) -> None:
        response = self.client.get(reverse('question-create'))
        self.assertRedirects(response, '/auth/login/?next=/questions/ask/')

    def test_post__anonymous(self) -> None:
        response = self.client.post(reverse('question-create'))
        self.assertRedirects(response, '/auth/login/?next=/questions/ask/')

    def test_get__authenticated(self) -> None:
        user: models.User = models.User.objects.create()
        self.client.force_login(user)
        response = self.client.get(reverse('question-create'))
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'buza/question_form.html')

    def test_post__empty(self) -> None:
        user: models.User = models.User.objects.create()
        self.client.force_login(user)
        response = self.client.post(reverse('question-create'))
        assert HTTPStatus.OK == response.status_code

        assert 'form' in response.context
        form: ModelForm = response.context['form']  # noqa: E701
        assert [] == form.non_field_errors()
        assert {
            'title': ['This field is required.'],
        } == form.errors
        assert not form.is_valid()

    def test_post__success(self) -> None:
        user: models.User = models.User.objects.create()
        self.client.force_login(user)
        response = self.client.post(reverse('question-create'), data=dict(
            title='This is a title',
            body='This is a body',
        ))
        question: models.Question = models.Question.objects.get()
        assert {
            'author_id': user.pk,
            'body': 'This is a body',
            'created': question.created,
            'id': question.pk,
            'modified': question.modified,
            'title': 'This is a title',
        } == models.Question.objects.filter(pk=question.pk).values().get()
        self.assertRedirects(response, f'/questions/{question.pk}/')


class TestAnswerCreate(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user = models.User.objects.create()
        self.question = models.Question.objects.create(
            author=self.user,
            title='question',
        )
        self.path = reverse('answer-create', kwargs=dict(question_pk=self.question.pk))

    def test__not_found(self) -> None:
        path = reverse('answer-create', kwargs=dict(question_pk=404))
        # Anonymous:
        assert HTTPStatus.NOT_FOUND == self.client.get(path).status_code
        assert HTTPStatus.NOT_FOUND == self.client.post(path).status_code
        # Authenticated:
        self.client.force_login(self.user)
        assert HTTPStatus.NOT_FOUND == self.client.get(path).status_code
        assert HTTPStatus.NOT_FOUND == self.client.post(path).status_code

    def test___anonymous(self) -> None:
        expected_url = f'/auth/login/?next=/questions/{self.question.pk}/answer/'
        self.assertRedirects(self.client.get(self.path), expected_url)
        self.assertRedirects(self.client.post(self.path), expected_url)

    def test_get__authenticated(self) -> None:
        self.client.force_login(self.user)
        response: HttpResponse = self.client.get(self.path)
        assert HTTPStatus.OK == response.status_code
        assert self.assertTemplateUsed('buza/question_form.html')
        assert self.question == response.context['question']

    def test_post__empty(self) -> None:
        self.client.force_login(self.user)
        path = reverse('answer-create', kwargs=dict(question_pk=self.question.pk))
        response: HttpResponse = self.client.post(path)
        assert HTTPStatus.OK == response.status_code
        assert self.assertTemplateUsed('buza/question_form.html')
        assert self.question == response.context['question']
