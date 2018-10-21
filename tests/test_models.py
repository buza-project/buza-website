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


class TestSubject(TestCase):

    def test_repr(self) -> None:
        subject = models.Subject(
            title='Biology',
            description='The study of life',
        )
        assert '<Subject: Biology>' == repr(subject)


class TestQuestion(TestCase):

    def test_repr(self) -> None:
        user = models.User(username='tester')
        question = models.Question(
            author=user,
            title='Example question?',
        )
        assert '<Question: By tester: Example question?>' == repr(question)


class TestTopic(TestCase):

    def test_repr(self) -> None:
        topic: models.Topic = models.Topic(name='tester')
        assert '<Topic: By tester>' == repr(topic)


class TestQuestionopic(TestCase):

    def test_repr(self) -> None:
        topic: models.Topic = models.Topic(name='tester')
        questiontopic: models.QuestionTopic = models.QuestionTopic(tag=topic)
        assert '<QuestionTopic: None tagged with By tester>' == repr(questiontopic)


class TestAnswer(TestCase):

    def test_repr(self) -> None:
        user = models.User.objects.create(username='tester')
        self.subject: models.Subject = models.Subject.objects.create(title="maths")
        question: models.Question = models.Question.objects.create(
            author=user,
            title='Example question?',
            subject=self.subject,
            grade=7,
        )
        answer: models.Answer = question.answer_set.create(
            author=user,
            body='Example Answer.',
        )
        expected = f'<Answer: By tester to question {question.pk}: Example question?>'
        assert expected == repr(answer)
