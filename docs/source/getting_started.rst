.. _getting_started:

Getting started
===============


Installation
------------
Installation from PyPi::

    pip install sanic-validation


Simple example
----------------
Code of the *hello service*::

    from sanic import Sanic
    from sanic.response import json
    from sanic_validation import validate_json

    app = Sanic()

    schema = {'name': {'type': 'string', 'required': True}}


    @app.route('/')
    @validate_json(schema)
    async def hello(request):
        return json({'message': 'Hello ' + request.json['name']})

    app.run('0.0.0.0')

An example of a bad request::

    POST / HTTP/1.1
    Accept: */*
    Accept-Encoding: gzip, deflate
    Connection: keep-alive
    Host: localhost:8000
    User-Agent: HTTPie/0.9.9

And the response::

    HTTP/1.1 400 Bad Request
    Connection: keep-alive
    Content-Length: 168
    Content-Type: application/json
    Keep-Alive: 5

    {
        "error": {
            "invalid": [
                {
                    "constraint": true,
                    "entry": "name",
                    "entry_type": "json_data_property",
                    "rule": "required"
                }
            ],
            "message": "Validation failed.",
            "type": "validation_failed"
        }
    }
