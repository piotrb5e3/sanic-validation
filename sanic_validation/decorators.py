from sanic.response import json
from cerberus import Validator

JSON_DATA_ENTRY_TYPE = 'json_data_property'
QUERY_ARG_ENTRY_TYPE = 'query_argument'


def validate_json(schema):
    validator = Validator(schema)

    def vd(f):
        def v(request, *args, **kwargs):
            validation_passed = validator.validate(request.json or {})
            if validation_passed and request.json is not None:
                return f(request, *args, **kwargs)
            else:
                return _validation_failed_response(validator,
                                                   JSON_DATA_ENTRY_TYPE)

        return v

    return vd


def validate_args(schema):
    validator = Validator(schema)

    def vd(f):
        def v(request, *args, **kwargs):
            validation_passed = validator.validate(request.raw_args or {})
            if validation_passed and request.raw_args is not None:
                return f(request, *args, **kwargs)
            else:
                return _validation_failed_response(validator,
                                                   QUERY_ARG_ENTRY_TYPE)

        return v

    return vd


def _validation_failed_response(validator, entry_type):
    return json(
        {
            'error': {
                'type': 'validation_failed',
                'message': 'Validation failed.',
                'invalid': _validation_failures_list(validator, entry_type)
            }
        },
        status=400)


def _validation_failures_list(validator, entry_type):
    return [
        _validation_error_description(error, entry_type)
        for error in _document_errors(validator)
    ]


def _document_errors(validator):
    return _traverse_tree(validator.document_error_tree)


def _traverse_tree(node):
    if not node.descendants:
        yield from node.errors

    for k in node.descendants:
        yield from _traverse_tree(node.descendants[k])


def _validation_error_description(error, entry_type):
    print(repr(error.schema_path))
    return {
        'entry_type': entry_type,
        'entry': _path_to_field(error),
        'rule': _rule(error),
        'constraint': _constraint(error)
    }


def _path_to_field(error):
    return '.'.join(map(str, error.document_path))


def _rule(error):
    return error.rule or 'allowed_field'


def _constraint(error):
    return error.constraint or False
