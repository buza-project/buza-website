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
        subject: models.Subject = models.Subject.objects.create(title="maths")
        question = models.Question.objects.create(
            author=user,
            title='Example question?',
            body='A question.',
            subject=subject,
        )
        answer: models.Answer = models.Answer.objects.create(
            body='An answer',
            question=question,
            author=user,
        )
        path = reverse('question-detail', kwargs=dict(pk=question.pk))
        response = self.client.get(path)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'buza/question_detail.html')

        assert question == response.context['question']
        self.assertContains(response, question.title, count=2)
        self.assertContains(response, question.body, count=1)
        self.assertContains(response, subject.title, count=1)
        self.assertContains(response, answer.body, count=1)


class TestQuestionList(TestCase):

    def test_get__empty(self) -> None:
        """
        Test Question list view
        """
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
            'subject': ['This field is required.'],
            'title': ['This field is required.'],
        } == form.errors
        assert not form.is_valid()

    def test_post__success(self) -> None:
        """
        Question post redirects to question view
        """
        user: models.User = models.User.objects.create()
        self.client.force_login(user)
        subject: models.Subject = models.Subject.objects.create(title="maths")
        response = self.client.post(reverse('question-create'), data=dict(
            title='This is a title',
            body='This is a body',
            subject=subject.pk,
        ))
        print(models.Question.objects.all())
        question: models.Question = models.Question.objects.get()
        assert {
            'author_id': user.pk,
            'body': 'This is a body',
            'created': question.created,
            'id': question.pk,
            'modified': question.modified,
            'title': 'This is a title',
            'subject_id': subject.pk,
        } == models.Question.objects.filter(pk=question.pk).values().get()
        self.assertRedirects(response, f'/questions/{question.pk}/')


class TestQuestionUpdate(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.author = models.User.objects.create(username='author')
        self.subject: models.Subject = models.Subject.objects.create(title="maths")
        self.other_user = models.User.objects.create(username='otheruser')
        self.question = models.Question.objects.create(
            author=self.author,
            title='question',
            subject=self.subject,
        )

    def test_get__anonymous(self) -> None:
        response = self.client.get(
            reverse('question-edit',
                    kwargs=dict(pk=self.question.pk)),
        )
        self.assertRedirects(
            response,
            f'/auth/login/?next=/questions/{self.question.pk}/edit/',
        )

    def test_post__anonymous(self) -> None:
        response = self.client.get(
            reverse('question-edit',
                    kwargs=dict(pk=self.question.pk)),
        )
        self.assertRedirects(
            response,
            f'/auth/login/?next=/questions/{self.question.pk}/edit/',
        )

    def test_get__not_author(self) -> None:
        """
        Users can only edit questions they own
        """
        self.client.force_login(self.other_user)
        response = self.client.get(
            reverse('question-edit',
                    kwargs=dict(pk=self.question.pk)),
        )
        self.assertRedirects(
            response,
            '/questions/1/',
        )

    def test_post__not_author(self) -> None:
        """
        Only authors can post questions changes
        """
        self.client.force_login(self.other_user)
        response = self.client.post(reverse(
            'question-edit',
            kwargs=dict(pk=self.question.pk)), data=dict(
            title='This is a title updated',
            body='This is an updated body',
        ))
        self.assertRedirects(
            response,
            '/questions/1/',
        )

    def test_update_author(self)-> None:
        """
        Question update allows author to login

        """
        self.client.force_login(self.author)
        response = self.client.post(reverse(
            'question-edit',
            kwargs=dict(pk=self.question.pk)), data=dict(
            title='This is a title updated',
            body='This is an updated body',
            subject=self.question.pk,
        ))
        question: models.Question = models.Question.objects.get()
        assert {
            'author_id': self.author.pk,
            'body': 'This is an updated body',
            'created': question.created,
            'id': question.pk,
            'modified': question.modified,
            'title': 'This is a title updated',
            'subject_id': self.subject.pk,
        } == models.Question.objects.filter(pk=question.pk).values().get()
        self.assertRedirects(response, f'/questions/{question.pk}/')


class TestAnswerCreate(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user = models.User.objects.create()
        self.subject: models.Subject = models.Subject.objects.create(title="maths")
        self.question = models.Question.objects.create(
            author=self.user,
            title='question',
            subject=self.subject,
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
        """
        Test that when an unauthenticated user tries to answer a question
        they are redirected to the home page
        """
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
        """
        Test that when an authenticated user submits an empty answer
        the answer is not posted
        """
        self.client.force_login(self.user)
        response: HttpResponse = self.client.post(self.path)
        assert HTTPStatus.OK == response.status_code
        assert self.assertTemplateUsed('buza/question_form.html')
        assert self.question == response.context['question']

        form: ModelForm = response.context['form']  # noqa: E701
        assert [] == form.non_field_errors()
        assert {'body': ['This field is required.']} == form.errors
        assert not form.is_valid()

    def test_post__valid(self) -> None:
        """
        Test that when an authenticated user submits a valid answer
        the answer is posted
        """
        self.client.force_login(self.user)
        response: HttpResponse = self.client.post(self.path, data={
            'body': 'An example answer',
        })
        answer: models.Answer = models.Answer.objects.get()
        assert {
            'author_id': self.user.pk,
            'created': answer.created,
            'id': answer.pk,
            'modified': answer.modified,
            'body': 'An example answer',
            'question_id': 1,
        } == models.Answer.objects.filter(pk=answer.pk).values().get()
        self.assertRedirects(response, f'/questions/{answer.question.pk}/')


class TestAnswerUpdate(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.author: models.User = models.User.objects.create()
        self.answer_author: models.User = \
            models.User.objects.create(username='answer_author')
        self.subject: models.Subject = models.Subject.objects.create(title="maths")
        self.question: models.Question = models.Question.objects.create(
            author=self.author,
            title='question',
            subject=self.subject,
        )
        self.answer: models.Answer = models.Answer.objects.create(
            author=self.answer_author,
            body='This is an answer',
            question=self.question,
        )
        self.path = reverse(
            'answer-edit',
            kwargs=dict(pk=self.answer.pk, question_pk=self.question.pk))

    def test_get_anonymous(self) -> None:
        response = self.client.get(self.path)
        self.assertRedirects(response, '/auth/login/?next=/questions/1/answer/1/edit')

    def test_post_anonymous(self) -> None:
        response = self.client.post(self.path)
        self.assertRedirects(response, '/auth/login/?next=/questions/1/answer/1/edit')

    def test_post__authenticated(self) -> None:
        self.client.force_login(self.answer_author)
        response = self.client.post(
            self.path,
            data=dict(
                body='This is an updated answer',
            ),
        )
        assert \
            'This is an updated answer' == \
            models.Answer.objects.filter(pk=self.answer.pk).get().body
        self.assertRedirects(response, f'/questions/{self.question.pk}/')

    def test_post__authenticated__not_owner(self) -> None:
        """
        Only the question authors are allowed to edit the question
        """
        self.client.force_login(self.author)
        response = self.client.post(
            self.path,
            data=dict(
                body='This is an updated answer',
            ),
        )
        assert \
            'This is an answer' == \
            models.Answer.objects.filter(pk=self.answer.pk).get().body
        self.assertRedirects(response, f'/questions/{self.question.pk}/')


class TestSubjectList(TestCase):
    """
        Test Subject list view
    """

    def setUp(self) -> None:
        self.user: models.User = models.User.objects.create()
        self.first_subject: models.Subject = \
            models.Subject.objects.create(title="maths")
        self.second_subject: models.Subject = \
            models.Subject.objects.create(title="bio")
        self.path = reverse('subject-list')

    def test_get__unauthenticated(self) -> None:
        """
        Unauthenticated users can view but not follow questions
        :return:
        """
        response = self.client.get(self.path)
        assert HTTPStatus.OK == response.status_code
        self.assertNotContains(response, "Follow")
        self.assertNotContains(response, "Unfollow")
        self.assertContains(response, self.first_subject.title, count=1)
        self.assertContains(response, self.second_subject.title, count=1)

    def test_get__no_followed_subjects(self) -> None:
        """
        Logged in users can view the list of questions and follow them
        """
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        assert HTTPStatus.OK == response.status_code
        self.assertContains(response, "Follow", count=models.Subject.objects.count())
        self.assertContains(response, "Unfollow", 0)
        self.assertContains(response, self.first_subject.title, count=1)
        self.assertContains(response, self.second_subject.title, count=1)

    def test_get__followed_subjects(self) -> None:
        """
        When follow a question, the UI updates
        :return:
        """
        self.client.force_login(self.user)
        self.user.subjects.add(self.first_subject)
        response = self.client.get(self.path)
        assert HTTPStatus.OK == response.status_code
        self.assertContains(response, "Unfollow", count=self.user.subjects.count())
        self.assertContains(
            response,
            "Follow",
            count=models.Subject.objects.count() - self.user.subjects.count())


class TestSubjectDetails(TestCase):

    def test_not_found(self) -> None:
        response = self.client.get(reverse('subject-detail', kwargs=dict(pk=404)))
        assert HTTPStatus.NOT_FOUND == response.status_code

    def test_get(self) -> None:
        user = models.User.objects.create()
        subject: models.Subject = models.Subject.objects.create(
            title="maths",
            description="the study of numbers",
        )
        question = models.Question.objects.create(
            author=user,
            title='Example question?',
            body='A question.',
            subject=subject,
        )
        path = reverse('subject-detail', kwargs=dict(pk=subject.pk))
        response = self.client.get(path)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'buza/subject_detail.html')

        self.assertContains(response, subject.title)
        self.assertContains(response, subject.description, count=1)
        self.assertContains(response, question.title, count=1)


class TestUserSubjectsView(TestCase):
    def setUp(self) -> None:
        self.user: models.User = models.User.objects.create()
        self.first_subject: models.Subject = \
            models.Subject.objects.create(title="maths")
        self.second_subject: models.Subject = \
            models.Subject.objects.create(title="bio")
        self.path = reverse('my-subject-list', kwargs=dict(pk=self.user.pk))

    def test_get__anonymous(self) -> None:
        """
        Anonymous users are redirected
        """
        response = self.client.get(self.path)
        self.assertRedirects(response, '/auth/login/?next=/subjects/my-subjects/1/')

    def test_get__with_no_followed_subjects(self) -> None:
        """
        My subject view is empty before users follow any subjects
        :return:
        """
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed('buza/my_subjects_list.html')
        self.assertContains(response, 'Followed Subjects')
        self.assertNotContains(response, self.first_subject.title)
        self.assertNotContains(response, self.second_subject.title)

    def test_get__with_followed_subjects(self) -> None:
        """
        My subject view is empty before users follow any subjects
        :return:
        """
        self.client.force_login(self.user)
        self.user.subjects.add(self.first_subject)
        response = self.client.get(self.path)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed('buza/my_subjects_list.html')
        self.assertContains(response, 'Followed Subjects')
        self.assertContains(response, self.first_subject.title, count=1)
        self.assertNotContains(response, self.second_subject.title)
