import unittest

from sanic import Sanic
from sanic.response import text

from sanic_validation import validate_json


class TestEmptyJsonValidation(unittest.TestCase):
    _endpoint_schema = {'name': {'type': 'string', 'required': False}}
    _app = None

    def setUp(self):
        self._app = Sanic()

        @self._app.route('/', methods=["POST"])
        @validate_json(self._endpoint_schema)
        async def _simple_endpoint(request):
            return text('OK')

    def test_endpoint_should_not_accept_empty_body(self):
        _, response = self._app.test_client.post('/')
        self.assertEqual(response.status, 415)
        self.assertEqual(response.json['error']['message'],
                         'Expected JSON body.')
        self.assertEqual(response.json['error']['type'],
                         'unsupported_media_type')
        self.assertEqual(response.json['error']['invalid'], [{
            'entry_type': 'request_body',
            'entry': '',
            'rule': 'json',
            'constraint': True
        }])

    def test_endpoint_should_accept_empty_json_object(self):
        _, response = self._app.test_client.post('/', json={})
        self.assertEqual(response.status, 200)
        self.assertEqual(response.text, 'OK')
