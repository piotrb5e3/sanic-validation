import unittest

from sanic_validation import validate_json, validate_args


class TestFunctionMetadataPreserved(unittest.TestCase):
    _dummy_schema = {'name': {'type': 'string', 'required': False}}

    def test_validate_json(self):
        @validate_json(self._dummy_schema)
        def fun1(request):
            '''Docstring 1'''
            pass

        self.assertEqual(fun1.__name__, 'fun1')
        self.assertEqual(fun1.__doc__, 'Docstring 1')

    def test_validate_args(self):
        @validate_args(self._dummy_schema)
        def fun2(request):
            '''Docstring 2'''
            pass

        self.assertEqual(fun2.__name__, 'fun2')
        self.assertEqual(fun2.__doc__, 'Docstring 2')
