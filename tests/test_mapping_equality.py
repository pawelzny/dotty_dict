import unittest
from collections import OrderedDict

from dotty_dict import dotty


class TestMixedKeyEquality(unittest.TestCase):
    def test_mixed_keys_compare_without_sorting(self):
        # Numeric and string keys are both supported, but cannot be ordered.
        values = {'name': 'sample', 1: 'one', None: 'empty'}
        for other in (values, dict(reversed(list(values.items()))),
                      OrderedDict(reversed(list(values.items()))), dotty(values.copy())):
            with self.subTest(other=type(other).__name__):
                self.assertEqual(dotty(values.copy()), other)
                self.assertEqual(other, dotty(values.copy()))

    def test_different_mixed_key_mappings_are_not_equal(self):
        values = {'name': 'sample', 1: 'one'}
        for other in ({'name': 'changed', 1: 'one'}, {'name': 'sample', 2: 'one'},
                      {'name': 'sample'}, {'name': 'sample', 1: 'one', None: 'extra'}):
            with self.subTest(other=other):
                self.assertNotEqual(dotty(values.copy()), other)

    def test_nested_mixed_keys_compare_as_mappings(self):
        self.assertEqual(dotty({'outer': {1: 'one', 'two': 2}}),
                         {'outer': {'two': 2, 1: 'one'}})
