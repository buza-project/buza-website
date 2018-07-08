from http import HTTPStatus

from django.http import HttpResponse
from django.test import TestCase


class TestSmoke(TestCase):

    def test_smoke(self) -> None:
        response: HttpResponse = self.client.get('/')
        assert HTTPStatus.OK == response.status_code
