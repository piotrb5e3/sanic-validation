import unittest

from sanic import Sanic
from sanic.response import json

from sanic_validation import validate_json


class TestSimpleEndpointJsonValidation(unittest.TestCase):
    _endpoint_schema = {'name': {'type': 'string', 'required': True}}
    _app = None

    def setUp(self):
        self._app = Sanic()

        @self._app.route('/')
        @validate_json(self._endpoint_schema)
        async def _simple_endpoint(request):
            return json({'status': 'ok'})

    def test_should_fail_validation(self):
        _, response = self._app.test_client.get('/', json={})
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json['error']['message'],
                         'Validation failed.')
        self.assertEqual(response.json['error']['type'], 'validation_failed')

    def test_should_pass_validation(self):
        _, response = self._app.test_client.get('/', json={'name': 'john'})
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json['status'], 'ok')
