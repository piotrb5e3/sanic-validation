# sanic-validation
[![Build Status](https://travis-ci.org/piotrb5e3/sanic-validation.svg?branch=master)](https://travis-ci.org/piotrb5e3/sanic-validation)

Validation for sanic endpoints.

## Installation
`pip install sanic-validation`

## Usage example

```
from sanic import Sanic
from sanic.response import json
from sanic_validation import validate_json


app = Sanic()

schema = {'name': {'type': 'string', 'required': True}}


@app.route('/')
@validate_json(schema)
async def _simple_endpoint(request):
    return json({'message': 'Hello ' + request.json['name']})

app.run('0.0.0.0')
```

### Schema format
Internally, sanic-validation uses [cerberus](https://github.com/pyeve/cerberus) as a validation provider.
Detailed format documentation can be found [here](http://docs.python-cerberus.org/en/stable/schemas.html).

### Example validation success
#### Request
```
GET / HTTP/1.1
Accept: application/json, */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 16
Content-Type: application/json
Host: localhost:8000
User-Agent: HTTPie/0.9.9

{
    "name": "John"
}
```

#### Response
```
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 24
Content-Type: application/json
Keep-Alive: 5

{
    "message": "Hello John"
}
```

### Example validation failure
#### Request
```
GET / HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: localhost:8000
User-Agent: HTTPie/0.9.9

```

#### Response
```
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
```