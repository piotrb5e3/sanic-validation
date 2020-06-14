import unittest

from sanic import Sanic
from sanic.response import json

from sanic_validation import validate_json, validate_args


class TestSimpleJSONNormalization(unittest.TestCase):
    _endpoint_schema = {
        'room_no': {
            'type': 'integer',
            'required': True,
            'coerce': int
        }
    }
    _app = None

    def setUp(self):
        self._app = Sanic('test-app')

        @self._app.route('/', methods=["POST"])
        @validate_json(self._endpoint_schema, clean=True)
        async def _simple_endpoint(request, valid_json):
            return json({'req_room_no': valid_json['room_no']})

    def test_numeric_string_value_should_normalize_correctly(self):
        _, response = self._app.test_client.post('/', json={'room_no': '517'})
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json['req_room_no'], 517)

    def test_non_numeric_string_value_should_raise_error(self):
        expected_errors = [{
            'entry_type': 'json_data_property',
            'entry': 'room_no',
            'rule': 'coerce',
            'constraint': True
        }, {
            'entry_type': 'json_data_property',
            'entry': 'room_no',
            'rule': 'type',
            'constraint': 'integer'
        }]
        _, response = self._app.test_client.post('/', json={'room_no': 'k-1'})
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json['error']['message'],
                         'Validation failed.')
        self.assertEqual(response.json['error']['type'], 'validation_failed')
        self.assertCountEqual(response.json['error']['invalid'],
                              expected_errors)


class TestSimpleArgsNormalization(unittest.TestCase):
    _endpoint_schema = {
        'room_no': {
            'type': 'integer',
            'required': True,
            'coerce': int
        }
    }
    _app = None

    def setUp(self):
        self._app = Sanic('test-app')

        @self._app.route('/')
        @validate_args(self._endpoint_schema, clean=True)
        async def _simple_endpoint(request, valid_args):
            return json({'req_room_no': valid_args['room_no']})

    def test_numeric_string_value_should_normalize_correctly(self):
        _, response = self._app.test_client.get('/', params={'room_no': '335'})
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json['req_room_no'], 335)

    def test_non_numeric_string_value_should_raise_error(self):
        expected_errors = [{
            'entry_type': 'query_argument',
            'entry': 'room_no',
            'rule': 'coerce',
            'constraint': True
        }, {
            'entry_type': 'query_argument',
            'entry': 'room_no',
            'rule': 'type',
            'constraint': 'integer'
        }]
        _, response = self._app.test_client.get('/', params={'room_no': 'k-1'})
        self.assertEqual(response.status, 400)
        self.assertEqual(response.json['error']['message'],
                         'Validation failed.')
        self.assertEqual(response.json['error']['type'], 'validation_failed')
        self.assertCountEqual(response.json['error']['invalid'],
                              expected_errors)
