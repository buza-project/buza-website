from http import HTTPStatus

from django.forms import ModelForm
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from buza import models


class TestRegister(TestCase):
    """
    The `register` view should create users and log them in.
    """
    def setUp(self) -> None:
        self.path = reverse('register')

    def test_get(self) -> None:
        response = self.client.get(self.path)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'accounts/register.html')
        assert 'user_form' in response.context

    def test_get__authenticated(self)-> None:
        user: models.User = models.User.objects.create()
        self.client.force_login(user)
        response = self.client.get(self.path)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'accounts/register.html')
        assert 'user_form' in response.context

    def test_post__empty(self) -> None:
        """
        Test that when user submits an empty register from, the user is not created.
        """
        response: HttpResponse = self.client.post(self.path)
        assert HTTPStatus.OK == response.status_code
        assert self.assertTemplateUsed('accounts/register.html')

        form: ModelForm = response.context['user_form']  # noqa: E701
        assert [] == form.non_field_errors()
        assert {
            'username': ['This field is required.'],
            'password1': ['This field is required.'],
            'password2': ['This field is required.'],
        } == form.errors
        assert not form.is_valid()

    def test_post__passwords_mismatch(self) -> None:
        response: HttpResponse = self.client.post(self.path, data=dict(
            username='buza-user-12',
            password1='password',
            password2='mismatch',
        ))
        assert HTTPStatus.OK == response.status_code
        assert self.assertTemplateUsed('accounts/register.html')

        form: ModelForm = response.context['user_form']  # noqa: E701
        assert [] == form.non_field_errors()
        assert {
            'password2': ["The two password fields didn't match."],
        } == form.errors
        assert not form.is_valid()

    def test_post__valid_form(self) -> None:
        response = self.client.post(self.path, data=dict(
            username='buza-user-12',
            password1='secret',
            password2='secret',
        ))
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed('accounts/register_done.html')
        new_user: models.User = models.User.objects.get()
        assert new_user == response.context['new_user']

        assert {
            'bio': None,
            'date_joined': new_user.date_joined,
            'email': '',
            'first_name': '',
            'grade': 7,
            'id': new_user.pk,
            'is_active': True,
            'is_staff': False,
            'is_superuser': False,
            'last_login': None,
            'last_name': '',
            'password': new_user.password,
            'phone': '',
            'photo': '',
            'school': None,
            'school_address': None,
            'username': 'buza-user-12',
        } == models.User.objects.filter(pk=new_user.pk).values().get()


class TestUserUpdate(TestCase):

    def _authenticated_user(self) -> models.User:
        """
        Create and return an authenticated user.
        """
        user: models.User = models.User.objects.create()
        self.client.force_login(user)
        return user

    def test_get__anonymous(self) -> None:
        user: models.User = models.User.objects.create()
        response = self.client.get(reverse('user-update', kwargs=dict(pk=user.pk)))
        self.assertRedirects(response, f'/auth/login/?next=/users/{user.pk}/update/')

    def test_post__anonymous(self) -> None:
        user: models.User = models.User.objects.create()
        response = self.client.post(reverse('user-update', kwargs=dict(pk=user.pk)))
        self.assertRedirects(response, f'/auth/login/?next=/users/{user.pk}/update/')

    def test_get__authenticated(self) -> None:
        user = self._authenticated_user()
        response = self.client.get(reverse('user-update', kwargs=dict(pk=user.pk)))
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'accounts/edit.html')

        assert 'form' in response.context
        form: ModelForm = response.context['form']  # noqa: E701
        assert user == form.instance
        assert not form.is_bound

    def test_post__empty(self) -> None:
        user = self._authenticated_user()
        response = self.client.post(reverse('user-update', kwargs=dict(pk=user.pk)))
        self.assertRedirects(response, reverse('user-detail', kwargs=dict(pk=user.pk)))

    def test_post__blank(self) -> None:
        user = self._authenticated_user()
        response = self.client.post(
            path=reverse('user-update', kwargs=dict(pk=user.pk)),
            data={
                'email': '',
                'phone': '',
                'photo': '',
                'first_name': '',
                'last_name': '',
                'school': '',
                'school_address': '',
                'grade': '',
                'bio': '',
            },
        )
        self.assertRedirects(response, reverse('user-detail', kwargs=dict(pk=user.pk)))


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
            grade=7,
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
        self.assertContains(response, question.body, count=0)
        self.assertContains(response, subject.title, count=1)
        self.assertContains(response, answer.body, count=1)


class TestQuestionList(TestCase):
    def setUp(self) -> None:
        self.user: models.User = models.User.objects.create()
        self.maths: models.Subject = models.Subject.objects.create(
            title='Mathematics',
            short_title='maths',
        )
        self.biology: models.Subject = models.Subject.objects.create(
            title='Biology',
            short_title='bio',
        )
        self.question: models.Question = models.Question.objects.create(
            title="this is a queston",
            author=self.user,
            subject=self.maths,
            grade=7,
        )
        self.answer: models.Answer = models.Answer.objects.create(
            question=self.question,
            author=self.user,
        )
        self.path = reverse('question-list')

    def test_get__one_question(self) -> None:
        """
        Test Question list view with one question
        """
        response = self.client.get(reverse('question-list'))
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'buza/question_list.html')

        self.assertNotContains(response, "Follow")
        self.assertNotContains(response, "Following")
        self.assertQuerysetEqual(response.context['subject_list'], [
            '<Subject: Biology>',
            '<Subject: Mathematics>',
        ])
        self.assertContains(response, self.maths.title, count=2)
        self.assertContains(response, self.biology.title, count=1)
        self.assertContains(response, "@" + self.user.username)
        self.assertContains(response, self.question.title)
        self.assertContains(response, "now")
        self.assertContains(response, self.answer.body)

    def test_get__unauthenticated(self) -> None:
        """
        Unauthenticated users can view but not follow subjects
        :return:
        """
        response = self.client.get(self.path)
        assert HTTPStatus.OK == response.status_code
        self.assertNotContains(response, "Follow")
        self.assertNotContains(response, "Following")
        self.assertContains(response, self.maths.title, count=2)
        self.assertContains(response, self.biology.title, count=1)
        self.assertContains(response, "@" + self.user.username)
        self.assertContains(response, self.answer.body)
        # test the humanizer
        self.assertContains(response, "now")

        # Listed by title.
        self.assertQuerysetEqual(response.context['subject_list'], [
            '<Subject: Biology>',
            '<Subject: Mathematics>',
        ])

    def test_get__no_followed_subjects(self) -> None:
        """
        Logged in users can view the list of subjects and follow them
        """
        self.client.force_login(self.user)
        response = self.client.get(self.path)
        assert HTTPStatus.OK == response.status_code
        self.assertContains(response, "follow")
        self.assertContains(response, "&#9733;")
        self.assertContains(response, "following", 0)
        self.assertContains(response, self.maths.title, count=2)
        self.assertContains(response, self.biology.title, count=1)
        self.assertContains(response, "@" + self.user.username)
        self.assertContains(response, self.question.title)
        self.assertContains(response, "now")
        self.assertContains(response, self.answer.body)

        # Listed by title.
        self.assertQuerysetEqual(response.context['subject_list'], [
            '<Subject: Biology>',
            '<Subject: Mathematics>',
        ])

    def test_get__followed_subjects(self) -> None:
        """
        When follow a question, the UI updates
        :return:
        """
        self.client.force_login(self.user)
        self.user.subjects.add(self.maths)
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, 'buza/question_list.html')
        assert HTTPStatus.OK == response.status_code
        self.assertContains(response, "following")
        self.assertContains(response, "follow")
        self.assertContains(response, "@" + self.user.username)
        self.assertContains(response, self.question.title)
        self.assertContains(response, "now")
        self.assertContains(response, self.answer.body)
        # Maths (followed) listed first.
        self.assertQuerysetEqual(response.context['subject_list'], [
            '<Subject: Mathematics>',
            '<Subject: Biology>',
        ])

    def test_get__long_subject_names(self) -> None:
        """
        When follow a question, the UI updates
        :return:
        """
        self.client.force_login(self.user)
        self.user.subjects.add(self.maths)

        ems: models.Subject = models.Subject.objects.create(
            title='Economics and Management Sciences',
            short_title='EMS',
        )
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, 'buza/question_list.html')
        assert HTTPStatus.OK == response.status_code
        # test that EMS is truncated
        self.assertNotContains(response, ems.title)
        self.assertContains(response, 'Economics and Manage...')

        # regular question list tests
        self.assertContains(response, "@" + self.user.username)
        self.assertContains(response, self.question.title)
        self.assertContains(response, "now")

    def test_post_unauthenticated(self) -> None:
        """Redirect unauthenticated user's posts """

        response: HttpResponse = self.client.post(self.path, data={
            'follow-subject': self.maths.pk,
        })

        assert HTTPStatus.FOUND == response.status_code
        self.assertRedirects(response, f'/auth/login/?next=/')

    def test_post__follow_subject(self) -> None:
        """Redirect unauthenticated user's posts """
        self.client.force_login(self.user)
        path = reverse('subject-detail', kwargs=dict(pk=self.maths.pk))
        response: HttpResponse = self.client.post(path, data={
            'follow-subject': self.maths.pk,
        })

        assert HTTPStatus.FOUND == response.status_code
        self.assertRedirects(response, f'/subjects/{self.maths.pk}/')
        self.assertEqual(self.user.subjects.all().count(), 1)

        response = self.client.get(response.url)
        self.assertContains(response, "following")
        self.assertContains(response, "follow")
        # Maths (followed) listed first.
        self.assertQuerysetEqual(response.context['subject_list'], [
            '<Subject: Mathematics>',
            '<Subject: Biology>',
        ])

        self.assertContains(response, "@" + self.user.username)
        self.assertContains(response, self.question.title)
        self.assertContains(response, "now")
        self.assertContains(response, self.answer.body)

    def test_post__unfollow_in_subjectlist(self) -> None:
        """Redirect unauthenticated user's posts """
        self.client.force_login(self.user)

        # follow and unfollow a subject
        path = reverse('subject-detail', kwargs=dict(pk=self.maths.pk))
        self.client.post(path, data={
            'follow-subject': self.maths.pk,

        })
        response: HttpResponse = self.client.post(self.path, data={
            'following-subject': self.maths.pk,

        })

        assert HTTPStatus.FOUND == response.status_code
        self.assertRedirects(response, f'/subjects/{self.maths.pk}/')
        self.assertEqual(self.user.subjects.all().count(), 0)

        response = self.client.get(response.url)
        self.assertNotContains(response, "following")
        self.assertContains(response, "follow")
        # Maths (followed) listed first.
        self.assertQuerysetEqual(response.context['subject_list'], [
            '<Subject: Biology>',
            '<Subject: Mathematics>',
        ])

        self.assertContains(response, "@" + self.user.username)
        self.assertContains(response, self.question.title)
        self.assertContains(response, "now")
        self.assertContains(response, self.answer.body)


class TestQuestionCreate(TestCase):

    def setUp(self) -> None:
        self.subject: models.Subject = models.Subject.objects.create(
            title='mathematics',
            short_title='maths',
        )
        self.user: models.User = models.User.objects.create()

    def test_get__anonymous(self) -> None:
        response = self.client.get(reverse(
            'question-create',
            kwargs=dict(subject_pk=self.subject.pk),
        ))
        self.assertRedirects(
            response,
            f'/auth/login/?next=/questions/{self.subject.pk}/ask/',
        )

    def test_post__anonymous(self) -> None:
        response = self.client.post(reverse(
            'question-create',
            kwargs=dict(subject_pk=self.subject.pk),
        ))
        self.assertRedirects(
            response,
            f'/auth/login/?next=/questions/{self.subject.pk}/ask/',
        )

    def test_get__authenticated(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(reverse(
            'question-create',
            kwargs=dict(subject_pk=self.subject.pk),
        ))
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'buza/question_form.html')
        self.assertContains(response, 'Question Summary', count=1)
        self.assertContains(
            response,
            'Give a detailed description of your question',
            count=1,
        )

    def test_post__empty(self) -> None:
        self.client.force_login(self.user)
        response = self.client.post(reverse(
            'question-create',
            kwargs=dict(subject_pk=self.subject.pk),
        ))
        assert HTTPStatus.OK == response.status_code

        assert 'form' in response.context
        form: ModelForm = response.context['form']  # noqa: E701
        assert [] == form.non_field_errors()
        assert {
            'title': ['This field is required.'],
        } == form.errors
        assert not form.is_valid()

    def test_post__success(self) -> None:
        """
        Question post redirects to question view
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse(
            'question-create',
            kwargs=dict(subject_pk=self.subject.pk)),
            data=dict(
                title='This is a title',
                body='This is a body',
                grade=7,
        ))
        question: models.Question = models.Question.objects.get()
        assert {
            'author_id': self.user.pk,
            'body': 'This is a body',
            'created': question.created,
            'id': question.pk,
            'modified': question.modified,
            'title': 'This is a title',
            'subject_id': self.subject.pk,
            'grade': question.grade,
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
            grade=7,
        )

    def test_get__anonymous(self) -> None:
        response = self.client.get(
            reverse('question-update', kwargs=dict(pk=self.question.pk)),
        )
        self.assertRedirects(
            response,
            f'/auth/login/?next=/questions/{self.question.pk}/edit/',
        )

    def test_post__anonymous(self) -> None:
        response = self.client.get(
            reverse('question-update', kwargs=dict(pk=self.question.pk)),
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
            reverse('question-update', kwargs=dict(pk=self.question.pk)),
        )
        assert HTTPStatus.FORBIDDEN == response.status_code

    def test_post__not_author(self) -> None:
        """
        Only authors can post questions changes
        """
        self.client.force_login(self.other_user)
        response = self.client.post(reverse(
            'question-update',
            kwargs=dict(pk=self.question.pk)), data=dict(
            title='This is a title updated',
            body='This is an updated body',
        ))
        assert HTTPStatus.FORBIDDEN == response.status_code

    def test_post__author_update(self)-> None:
        """
        Question update allows author to update the question

        """
        self.client.force_login(self.author)
        path = reverse('question-update', kwargs=dict(pk=self.question.pk))
        response = self.client.post(path, data=dict(
            title='This is a title updated',
            body='This is an updated body',
            subject=self.subject.pk,
            grade=7,
        ))

        question: models.Question = models.Question.objects.get()
        assert {
            'author_id': self.author.pk,
            'body': 'This is an updated body',
            'created': question.created,
            'id': question.pk,
            'modified': question.modified,
            'title': 'This is a title updated',
            'subject_id': question.subject.pk,
            'grade': question.grade,
        } == models.Question.objects.filter(pk=question.pk).values().get()
        self.assertRedirects(response, f'/questions/{self.question.pk}/')


class TestAnswerCreate(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user = models.User.objects.create()
        self.subject: models.Subject = models.Subject.objects.create(title="maths")
        self.question = models.Question.objects.create(
            author=self.user,
            title='question',
            subject=self.subject,
            grade=7,
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
            grade=12,
        )
        self.answer: models.Answer = models.Answer.objects.create(
            author=self.answer_author,
            body='This is an answer',
            question=self.question,
        )
        self.path = reverse('answer-update', kwargs=dict(pk=self.answer.pk))

    def test_get__anonymous(self) -> None:
        response = self.client.get(self.path)
        self.assertRedirects(
            response,
            f'/auth/login/?next=/answers/{self.answer.pk}/edit/',
        )

    def test_get__authenticated(self) -> None:
        self.client.force_login(self.answer_author)
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, 'buza/answer_form.html')
        assert self.question == response.context['question']
        assert self.answer == response.context['answer']

    def test_post__anonymous(self) -> None:
        response = self.client.post(self.path)
        self.assertRedirects(
            response,
            f'/auth/login/?next=/answers/{self.answer.pk}/edit/',
        )

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
        response = self.client.post(self.path, data=dict(
            body='This is an updated answer',
        ))
        assert HTTPStatus.FORBIDDEN == response.status_code


class TestSubjectDetails(TestCase):

    def setUp(self) -> None:
        self.user: models.User = models.User.objects.create()
        self.maths: models.Subject = models.Subject.objects.create(
            title="Mathematics",
            description="the study of numbers",
        )

        self.biology: models.Subject = models.Subject.objects.create(
            title='Biology',
            short_title='bio',
        )
        self.question: models.Question = models.Question.objects.create(
            author=self.user,
            title='Example question?',
            body='A question.',
            subject=self.maths,
            grade=7,
        )
        self.path = reverse('subject-detail', kwargs=dict(pk=self.maths.pk))

    def test_not_found(self) -> None:
        response = self.client.get(reverse('subject-detail', kwargs=dict(pk=404)))
        assert HTTPStatus.NOT_FOUND == response.status_code
        self.assertTemplateUsed(response, '404.html')

    def test_get_authenticated(self) -> None:
        response = self.client.get(self.path)
        assert HTTPStatus.OK == response.status_code
        self.assertTemplateUsed(response, 'buza/subject_detail.html')

        self.assertContains(response, self.maths.title)
        self.assertContains(response, "Ask New  Question")
        self.assertContains(response, self.biology.title, count=1)
        self.assertContains(response, self.question.title, count=1)
        self.assertNotContains(response, "Follow")
        self.assertNotContains(response, "Following")
        # Listed subjects by title.
        self.assertQuerysetEqual(response.context['subject_list'], [
            '<Subject: Biology>',
            '<Subject: Mathematics>',
        ])

    def test_get__authenticated__subject_short_title(self) -> None:
        self.maths: models.Subject = models.Subject.objects.create(
            title="mathematics",
            short_title="maths",
            description="the study of numbers",
        )
        self.client.force_login(self.user)
        path = reverse('subject-detail', kwargs=dict(pk=self.maths.pk))
        response = self.client.get(path)

        assert HTTPStatus.OK == response.status_code
        self.assertContains(response, self.maths.title)
        self.assertContains(
            response,
            "Ask New " + self.maths.short_title + " Question",
        )

    def test_post_unauthenticated(self) -> None:
        """Redirect unauthenticated user's posts """

        response: HttpResponse = self.client.post(self.path, data={
            'follow-subject': self.maths.pk,
        })

        assert HTTPStatus.FOUND == response.status_code
        self.assertRedirects(response, f'/auth/login/?next=/subjects/{self.maths.pk}/')

    def test_post__follow_subject(self) -> None:
        """Redirect unauthenticated user's posts """
        self.client.force_login(self.user)
        response: HttpResponse = self.client.post(self.path, data={
            'follow-subject': self.maths.pk,

        })

        assert HTTPStatus.FOUND == response.status_code
        self.assertRedirects(response, f'/subjects/{self.maths.pk}/')
        self.assertEqual(self.user.subjects.all().count(), 1)

        response = self.client.get(response.url)
        self.assertContains(response, "following")
        self.assertContains(response, "follow")
        # Maths (followed) listed first.
        self.assertContains(response, self.maths.title, count=3)
        self.assertQuerysetEqual(response.context['subject_list'], [
            '<Subject: Mathematics>',
            '<Subject: Biology>',
        ])

    def test_get__no_followed_subjects(self) -> None:
        """
        Test subject list and question list
        """
        self.client.force_login(self.user)
        response = self.client.get(self.path)

        assert HTTPStatus.OK == response.status_code
        # Question list and button
        self.assertContains(response, "Ask New  Question")
        self.assertContains(response, self.question.title, count=1)
        # Subjects listing
        self.assertContains(response, "follow")
        self.assertContains(response, "&#9733;")
        self.assertContains(response, "following", 0)
        self.assertContains(response, self.maths.title, count=3)
        self.assertContains(response, self.biology.title, count=1)

        # Listed subjects by title.
        self.assertQuerysetEqual(response.context['subject_list'], [
            '<Subject: Biology>',
            '<Subject: Mathematics>',
        ])

    def test_get__followed_subjects(self) -> None:
        """
        When follow a question, the UI updates
        :return:
        """
        self.client.force_login(self.user)
        self.user.subjects.add(self.maths)
        response = self.client.get(self.path)
        self.assertTemplateUsed(response, 'buza/subject_detail.html')
        assert HTTPStatus.OK == response.status_code
        self.assertContains(response, "following")
        self.assertContains(response, "follow")

        # Maths (followed) listed first.
        self.assertQuerysetEqual(response.context['subject_list'], [
            '<Subject: Mathematics>',
            '<Subject: Biology>',
        ])

    def test_post__unfollow_subject(self) -> None:
        """Redirect unauthenticated user's posts """
        self.client.force_login(self.user)

        # follow and unfollow a subject
        self.client.post(self.path, data={
            'follow-subject': self.maths.pk,

        })
        response: HttpResponse = self.client.post(self.path, data={
            'following-subject': self.maths.pk,

        })

        assert HTTPStatus.FOUND == response.status_code
        self.assertRedirects(response, f'/subjects/{self.maths.pk}/')
        self.assertEqual(self.user.subjects.all().count(), 0)

        response = self.client.get(response.url)
        self.assertNotContains(response, "following")
        self.assertContains(response, "follow")
        # Maths (followed) listed first.
        self.assertQuerysetEqual(response.context['subject_list'], [
            '<Subject: Biology>',
            '<Subject: Mathematics>',
        ])


class Test404PageNotFound(TestCase):

    def test_url_not_found(self):
        response = self.client.get('404/not-found/test')
        self.assertTemplateUsed(response, '404.html')
        self.assertContains(
            response,
            'We could not find the page you were looking for',
            status_code=HTTPStatus.NOT_FOUND,
        )
        self.assertContains(response, 'Take me home', status_code=HTTPStatus.NOT_FOUND)
