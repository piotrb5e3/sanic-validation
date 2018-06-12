from sanic.response import json
from cerberus import Validator
from functools import wraps

JSON_DATA_ENTRY_TYPE = 'json_data_property'
QUERY_ARG_ENTRY_TYPE = 'query_argument'
REQ_BODY_ENTRY_TYPE = 'request_body'


def validate_json(schema, clean=False):
    '''Decorator. Validates request body json.

    When *clean* is true, normalized data is passed to the decorated method
    as *valid_json*.

    Args:
        schema (dict): Cerberus-compatible schema description
        clean (bool): should cleaned json be passed to the decorated method
    '''
    validator = Validator(schema)

    def vd(f):
        @wraps(f)
        def wrapper(request, *args, **kwargs):
            if request.json is None:
                return _request_body_not_json_response()
            validation_passed = validator.validate(request.json or {})
            if validation_passed:
                if clean:
                    kwargs['valid_json'] = validator.document
                return f(request, *args, **kwargs)
            else:
                return _validation_failed_response(validator,
                                                   JSON_DATA_ENTRY_TYPE)

        return wrapper

    return vd


def validate_args(schema, clean=False):
    '''Decorator. Validates querystring arguments.

    When *clean* is True, normalized data is passed to the decorated method
    as *valid_args*.

    Args:
        schema (dict): Cerberus-compatible schema description
        clean (bool): should cleaned args be passed to the decorated method
    '''
    validator = Validator(schema)

    def vd(f):
        @wraps(f)
        def wrapper(request, *args, **kwargs):
            validation_passed = validator.validate(request.raw_args)
            if validation_passed:
                if clean:
                    kwargs['valid_args'] = validator.document
                return f(request, *args, **kwargs)
            else:
                return _validation_failed_response(validator,
                                                   QUERY_ARG_ENTRY_TYPE)

        return wrapper

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
    if error.rule == 'coerce':
        return True
    return error.constraint or False


def _request_body_not_json_response():
    return json(
        {
            'error': {
                'type': 'unsupported_media_type',
                'message': 'Expected JSON body.',
                'invalid': [{
                    'entry_type': REQ_BODY_ENTRY_TYPE,
                    'entry': '',
                    'rule': 'json',
                    'constraint': True
                }],
            }
        },
        status=415)
