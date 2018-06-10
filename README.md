# sanic-validation
[![Build Status](https://travis-ci.org/piotrb5e3/sanic-validation.svg?branch=master)](https://travis-ci.org/piotrb5e3/sanic-validation)

sanic-validation is an extension to sanic that simplifies validating request data.

## Installation
`pip install sanic-validation`

## Documentation
Documentation is available at [ReadTheDocs](https://sanic-validation.readthedocs.io/en/stable/).

## Usage example
```
from sanic import Sanic
from sanic.response import json
from sanic_validation import validate_json


app = Sanic()

schema = {'name': {'type': 'string', 'required': True}}


@app.route('/')
@validate_json(schema)
async def hello_service(request):
    return json({'message': 'Hello ' + request.json['name']})

app.run('0.0.0.0')
```

## Building the documentation
### Requirements
* Python
* Sphinx
* make

### Building
```
python setup.py install
cd docs
make html
```
