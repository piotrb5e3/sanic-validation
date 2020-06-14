import unittest

from sanic import Sanic
from sanic.response import json

from sanic_validation import validate_json, validate_args


class TestSimpleEndpointJsonValidation(unittest.TestCase):
    _endpoint_schema = {'name': {'type': 'string', 'required': True}}
    _app = None

    def setUp(self):
        self._app = Sanic()

        @self._app.route('/', methods=["POST"])
        @validate_json(self._endpoint_schema)
        async def _simple_endpoint(request):
            return json({'status': 'ok'})

    def test_should_fail_validation(self):
        _, response = self._app.test_client.post('/', json={})
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json['error']['message'],
                         'Validation failed.')
        self.assertEqual(response.json['error']['type'], 'validation_failed')

    def test_should_pass_validation(self):
        _, response = self._app.test_client.post('/', json={'name': 'john'})
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json['status'], 'ok')


class TestSimpleEndpointArgsValidation(unittest.TestCase):
    _endpoint_schema = {'name': {'type': 'string', 'required': True}}
    _app = None

    def setUp(self):
        self._app = Sanic()

        @self._app.route('/')
        @validate_args(self._endpoint_schema)
        async def _simple_endpoint(request):
            return json({'status': 'ok'})

    def test_should_fail_for_empty_validation(self):
        _, response = self._app.test_client.get('/')
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json['error']['message'],
                         'Validation failed.')
        self.assertEqual(response.json['error']['type'], 'validation_failed')

    def test_should_pass_validation(self):
        _, response = self._app.test_client.get('/', params={'name': 'john'})
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json['status'], 'ok')


class TestSimpleEndpointArgsTypeNormalizationValidation(unittest.TestCase):
    _endpoint_schema = {
        'val': {'type': 'integer', 'required': True, 'coerce': int}}
    _app = None

    def setUp(self):
        self._app = Sanic()

        @self._app.route('/')
        @validate_args(self._endpoint_schema)
        async def _simple_endpoint(request):
            return json({'status': 'ok'})

    def test_should_fail_for_empty_validation(self):
        _, response = self._app.test_client.get('/')
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json['error']['message'],
                         'Validation failed.')
        self.assertEqual(response.json['error']['type'], 'validation_failed')

    def test_should_pass_with_string_validation(self):
        _, response = self._app.test_client.get('/', params={'val': '420'})
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json['status'], 'ok')

    def test_should_pass_with_int_validation(self):
        _, response = self._app.test_client.get('/', params={'val': 420})
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json['status'], 'ok')

    def test_should_fail_for_wrong_type_validation(self):
        _, response = self._app.test_client.get('/', params={'val': 'True'})
        self.assertEqual(response.json['error']['message'],
                         'Validation failed.')
        self.assertEqual(response.json['error']['type'], 'validation_failed')
