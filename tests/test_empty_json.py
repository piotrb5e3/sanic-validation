import unittest

from sanic import Sanic
from sanic.response import text

from sanic_validation import validate_json


class TestEmptyJsonValidation(unittest.TestCase):
    _endpoint_schema = {'name': {'type': 'string', 'required': False}}
    _app = None

    def setUp(self):
        self._app = Sanic()

        @self._app.route('/')
        @validate_json(self._endpoint_schema)
        async def _simple_endpoint(request):
            return text('OK')

    def test_endpoint_should_not_accept_empty_body(self):
        _, response = self._app.test_client.get('/')
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json['error']['message'],
                         'Validation failed.')
        self.assertEqual(response.json['error']['type'], 'validation_failed')

    def test_endpoint_should_accept_empty_json_object(self):
        _, response = self._app.test_client.get('/', json={})
        self.assertEqual(response.status, 200)
        self.assertEqual(response.text, 'OK')
