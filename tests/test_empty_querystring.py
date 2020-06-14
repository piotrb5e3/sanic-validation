import unittest

from sanic import Sanic
from sanic.response import text

from sanic_validation import validate_args


class TestEmptyQuerystringValidation(unittest.TestCase):
    _endpoint_schema = {'name': {'type': 'string', 'required': False}}
    _app = None

    def setUp(self):
        self._app = Sanic('test-app')

        @self._app.route('/')
        @validate_args(self._endpoint_schema)
        async def _simple_endpoint(request):
            return text('OK')

    def test_endpoint_should_accept_empty_querystring(self):
        _, response = self._app.test_client.get('/')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.text, 'OK')
