import unittest
from sanic import Sanic
from sanic.response import json

from sanic_validation import validate_json, validate_args


class TestErrorResponseDetailForJson(unittest.TestCase):
    _endpoint_schema = {
        'name': {
            'type': 'string',
            'required': True
        },
        'job': {
            'type': 'dict',
            'schema': {
                'company_name': {
                    'type': 'string',
                    'minlength': 5
                },
                'position_name': {
                    'type': 'string',
                    'required': True
                }
            }
        },
        'past_workplaces': {
            'type': 'list',
            'schema': {
                'type': 'dict',
                'schema': {
                    'company_name': {
                        'type': 'string'
                    },
                    'responsibilities': {
                        'type': 'list',
                        'schema': {
                            'type': 'string'
                        }
                    }
                }
            }
        }
    }

    _request_data = {
        'name':
        1234,
        'job': {
            'company_name': 'abcd'
        },
        'past_workplaces': [{
            'company_name': 'hamburger stand',
            'responsibilities': ['flipping', 1234]
        }, {
            'company_name':
            5678,
            'responsibilities': [{
                'qualifier': '_123_xc'
            }, ['audit']]
        }, 'GGG inc.'],
        '_dummy':
        1234
    }

    _expected_errors = [{
        'rule': 'type',
        'entry_type': 'json_data_property',
        'entry': 'name',
        'constraint': 'string'
    }, {
        'rule': 'required',
        'entry_type': 'json_data_property',
        'entry': 'job.position_name',
        'constraint': True
    }, {
        'rule': 'minlength',
        'entry_type': 'json_data_property',
        'entry': 'job.company_name',
        'constraint': 5
    }, {
        'rule': 'type',
        'entry_type': 'json_data_property',
        'entry': 'past_workplaces.0.responsibilities.1',
        'constraint': 'string'
    }, {
        'rule': 'type',
        'entry_type': 'json_data_property',
        'entry': 'past_workplaces.1.responsibilities.0',
        'constraint': 'string'
    }, {
        'rule': 'type',
        'entry_type': 'json_data_property',
        'entry': 'past_workplaces.1.responsibilities.1',
        'constraint': 'string'
    }, {
        'rule': 'type',
        'entry_type': 'json_data_property',
        'entry': 'past_workplaces.1.company_name',
        'constraint': 'string'
    }, {
        'rule': 'type',
        'entry_type': 'json_data_property',
        'entry': 'past_workplaces.2',
        'constraint': 'dict'
    }, {
        'rule': 'allowed_field',
        'entry_type': 'json_data_property',
        'entry': '_dummy',
        'constraint': False
    }]

    _app = None

    def setUp(self):
        self._app = Sanic()

        @self._app.route('/', methods=["POST"])
        @validate_json(self._endpoint_schema)
        async def _endpoint(request):
            return json({'status': 'ok'})

    def test_response_should_contain_all_errors(self):
        _, response = self._app.test_client.post('/', json=self._request_data)

        self.assertEqual(response.status, 400)
        self.assertEqual(response.json['error']['message'],
                         'Validation failed.')
        self.assertEqual(response.json['error']['type'], 'validation_failed')

        self.assertCountEqual(response.json['error']['invalid'],
                              self._expected_errors)


class TestErrorResponseStatusForJson(unittest.TestCase):
    _endpoint_schema = {
        'name': {
            'type': 'string',
            'required': True
        },
    }

    _params_data = {}

    _expected_errors = [{
        'entry_type': 'json_data_property',
        'entry': 'name',
        'rule': 'required',
        'constraint': True
    }]

    def setUp(self):
        self._app = Sanic()

        @self._app.route('/', methods=["POST"])
        @validate_json(self._endpoint_schema, status_code=422)
        async def _endpoint(request):
            return json({'status': 'ok'})

    def test_response_should_use_provided_status_code(self):
        _, response = self._app.test_client.post('/', json=self._params_data)

        self.assertEqual(response.status, 422)
        self.assertEqual(response.json['error']['message'],
                         'Validation failed.')
        self.assertEqual(response.json['error']['type'], 'validation_failed')

        self.assertCountEqual(response.json['error']['invalid'],
                              self._expected_errors)


class TestErrorResponseDetailForParams(unittest.TestCase):
    _endpoint_schema = {
        'name': {
            'type': 'string',
            'required': True
        },
    }

    _params_data = {'job': 'cook'}

    _expected_errors = [{
        'entry_type': 'query_argument',
        'entry': 'job',
        'rule': 'allowed_field',
        'constraint': False
    }, {
        'entry_type': 'query_argument',
        'entry': 'name',
        'rule': 'required',
        'constraint': True
    }]

    def setUp(self):
        self._app = Sanic()

        @self._app.route('/')
        @validate_args(self._endpoint_schema)
        async def _endpoint(request):
            return json({'status': 'ok'})

    def test_response_should_contain_all_errors(self):
        _, response = self._app.test_client.get('/', params=self._params_data)

        self.assertEqual(response.status, 400)
        self.assertEqual(response.json['error']['message'],
                         'Validation failed.')
        self.assertEqual(response.json['error']['type'], 'validation_failed')

        self.assertCountEqual(response.json['error']['invalid'],
                              self._expected_errors)


class TestErrorResponseStatusForParams(unittest.TestCase):
    _endpoint_schema = {
        'name': {
            'type': 'string',
            'required': True
        },
    }

    _params_data = {}

    _expected_errors = [{
        'entry_type': 'query_argument',
        'entry': 'name',
        'rule': 'required',
        'constraint': True
    }]

    def setUp(self):
        self._app = Sanic()

        @self._app.route('/')
        @validate_args(self._endpoint_schema, status_code=422)
        async def _endpoint(request):
            return json({'status': 'ok'})

    def test_response_should_use_provided_status_code(self):
        _, response = self._app.test_client.get('/', params=self._params_data)

        self.assertEqual(response.status, 422)
        self.assertEqual(response.json['error']['message'],
                         'Validation failed.')
        self.assertEqual(response.json['error']['type'], 'validation_failed')

        self.assertCountEqual(response.json['error']['invalid'],
                              self._expected_errors)
