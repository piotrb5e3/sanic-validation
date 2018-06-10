.. _usage:

Usage
=====

Validating JSON
---------------
To validate body JSON, use the :func:`~sanic_validation.validate_json` decorator::

    @app.route('/')
    @validate_json(schema)
    async def hello(request):
        return text("OK")

If all fields in schema are optional, then an empty JSON object ``{}`` will be accepted,
but an empty request body will be rejected.


Validating querystring arguments
--------------------------------
To validate querystring arguments, use the :func:`~sanic_validation.validate_args` decorator::

    @app.route('/')
    @validate_args(schema)
    async def hello(request):
        return text("OK")

All argument values are strings. To use validation rules for other types use coercion rules
(see Normalization_).


Error response format
---------------------
In case of an error the request returns with status of 400.
Example error response::

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

Fields definitions:

*type*:
    machine readable description of the problem
*message*:
    user readable description of the problem
*invalid*:
    list containing all validation errors
*entry_type*:
    type of the incorrect entry (json data, querystring parameter, etc)
*entry*:
    path to the incorrect entry
*rule*:
    rule that failed validation
*constraint*:
    expected value for the rule


Schema
------
sanic-validation uses Cerberus as the validation library.
For the list of available rules see `Cerberus' schema documentation`_.


Normalization
-------------
Normalization for the purpose of validation is supported,
but you'll have to manually coerce types in the request handler.
See `Cerberus' normalization documentation`_ for the list of normalization rules.


Extending
---------
Custom rules, data types and coercers can be easily added.
Consult `Cerberus' customization documentation`_ for details.



.. _Cerberus' schema documentation: http://docs.python-cerberus.org/en/stable/validation-rules.html
.. _Cerberus' normalization documentation: http://docs.python-cerberus.org/en/stable/normalization-rules.html
.. _Cerberus' customization documentation: http://docs.python-cerberus.org/en/stable/customize.html

