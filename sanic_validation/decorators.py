from sanic.response import json
from cerberus import Validator


def validate_json(schema):
    validator = Validator(schema)

    def vd(f):
        def v(request, *args, **kwargs):
            validation_passed = validator.validate(request.json or {})
            if validation_passed and request.json is not None:
                return f(request, *args, **kwargs)
            else:
                return _validation_failed_response(validator)

        return v

    return vd


def _validation_failed_response(validator):
    return json(
        {
            'error': {
                'type': 'validation_failed',
                'message': 'Validation failed.',
                'invalid': _validation_failures_list(validator)
            }
        },
        status=400)


def _validation_failures_list(validator):
    return [
        _validation_error_description(e) for e in _document_errors(validator)
    ]


def _document_errors(validator):
    return _traverse_tree(validator.document_error_tree)


def _traverse_tree(node):
    if not node.descendants:
        yield from node.errors

    for k in node.descendants:
        yield from _traverse_tree(node.descendants[k])


def _validation_error_description(error):
    print(repr(error.schema_path))
    return {
        'entry_type': 'json_data_property',
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
