# sanic-validation
[![PyPI](https://img.shields.io/pypi/v/sanic-validation)](https://pypi.org/project/sanic-validation/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic-validation)
[![Build Status](https://travis-ci.org/piotrb5e3/sanic-validation.svg?branch=master)](https://travis-ci.org/piotrb5e3/sanic-validation)
[![Read the Docs](https://img.shields.io/readthedocs/sanic-validation)](https://sanic-validation.readthedocs.io/en/stable/)

sanic-validation is an extension to sanic that simplifies validating request data.

## Installation
`pip install sanic-validation`

## Documentation
Documentation is available at [ReadTheDocs](https://sanic-validation.readthedocs.io/en/stable/).

## Usage example
```
from sanic import Sanic
from sanic.response import json
from sanic_validation import validate_args

app = Sanic('demo-app')

schema = {'name': {'type': 'string', 'required': True}}


@app.route('/')
@validate_args(schema)
async def hello(request):
    return json({'message': 'Hello ' + request.args['name']})

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
