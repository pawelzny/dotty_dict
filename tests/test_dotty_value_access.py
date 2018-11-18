#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from dotty_dict import Dotty, dotty


class TestDottyValueAccess(unittest.TestCase):
    def setUp(self):
        self.dot = dotty({
            'flat_key': 'flat value',
            'deep': {
                'nested': 12,
                'deeper': {
                    'secret': 'abcd',
                    'ridiculous': {
                        'hell': 'is here',
                    },
                },
            },
        })

    def test_access_flat_value(self):
        self.assertEqual(self.dot['flat_key'], 'flat value')

    # noinspection PyUnusedLocal
    def test_raise_key_error_if_key_does_not_exist(self):
        with self.assertRaises(KeyError):
            val = self.dot['not_existing']  # noqa

    def test_access_deep_nested_value(self):
        self.assertEqual(self.dot['deep.nested'], 12)

    def test_access_middle_nested_value(self):
        self.assertDictEqual(self.dot['deep.deeper.ridiculous'],
                             {'hell': 'is here'})

    def test_set_flat_value(self):
        self.dot['new_flat'] = 'super flat'
        self.assertIn('new_flat', self.dot)

    def test_set_deep_nested_value(self):
        self.dot['deep.new_key'] = 'new value'
        self.assertIn('new_key', self.dot['deep'])

    def test_set_new_deeply_nested_value(self):
        self.dot['other.chain.of.keys'] = True
        self.assertDictEqual(self.dot._data, {
            'flat_key': 'flat value',
            'deep': {
                'nested': 12,
                'deeper': {
                    'secret': 'abcd',
                    'ridiculous': {
                        'hell': 'is here',
                    },
                },
            },
            'other': {
                'chain': {
                    'of': {
                        'keys': True,
                    },
                },
            },
        })

    def test_dotty_has_flat_key(self):
        self.assertIn('flat_key', self.dot)

    def test_dotty_has_deeply_nested_key(self):
        self.assertIn('deep.nested', self.dot)

    def test_dotty_has_not_flat_key(self):
        self.assertNotIn('some_key', self.dot)

    def test_dotty_has_not_deeply_nested_key(self):
        self.assertNotIn('deep.other.chain', self.dot)

    def test_has_in(self):
        result = 'deep.deeper.secret' in self.dot
        self.assertTrue(result)

    def test_has_not_in(self):
        result = 'deep.other' in self.dot
        self.assertFalse(result)

    def test_delete_flat_key(self):
        del self.dot['flat_key']
        self.assertDictEqual(self.dot._data, {
            'deep': {
                'nested': 12,
                'deeper': {
                    'secret': 'abcd',
                    'ridiculous': {
                        'hell': 'is here',
                    },
                },
            },
        })

    def test_delete_nested_key(self):
        del self.dot['deep.deeper.secret']
        self.assertDictEqual(self.dot._data, {
            'flat_key': 'flat value',
            'deep': {
                'nested': 12,
                'deeper': {
                    'ridiculous': {
                        'hell': 'is here',
                    },
                },
            },
        })

    def test_raise_key_error_on_delete_not_existing_key(self):
        with self.assertRaises(KeyError):
            del self.dot['deep.deeper.key']

    def test_set_value_with_escaped_separator(self):
        self.dot[r'deep.deeper.escaped\.dot_key'] = 'it works!'
        self.assertDictEqual(self.dot._data, {
            'flat_key': 'flat value',
            'deep': {
                'nested': 12,
                'deeper': {
                    'escaped.dot_key': 'it works!',
                    'secret': 'abcd',
                    'ridiculous': {
                        'hell': 'is here',
                    },
                },
            },
        })

    def test_get_value_with_escaped_separator(self):
        dot = dotty({
            'flat_key': 'flat value',
            'deep': {
                'nested': 12,
                'deeper': {
                    'escaped.dot_key': 'it works!',
                    'secret': 'abcd',
                    'ridiculous': {
                        'hell': 'is here',
                    },
                },
            },
        })
        result = dot[r'deep.deeper.escaped\.dot_key']
        self.assertEqual(result, 'it works!')

    def test_get_value_with_escaped_escape_separator(self):
        dot = dotty({
            'flat_key': 'flat value',
            'deep': {
                'nested': 12,
                'deeper': {
                    'escaped\\': {
                        'dot_key': 'it works!',
                    },
                    'secret': 'abcd',
                    'ridiculous': {
                        'hell': 'is here',
                    },
                },
            },
        })
        result = dot[r'deep.deeper.escaped\\.dot_key']
        self.assertEqual(result, 'it works!')

    def test_use_custom_separator_and_custom_escape_char(self):
        sep = ','
        esc = '$'
        dot = Dotty({}, separator=sep, esc_char=esc)
        dot['abcd,efg,hij'] = 'test'
        dot['abcd,efg$,hij'] = 'test2'
        dot[r'abcd,efg\$,hij'] = 'test3'
        self.assertDictEqual(dot._data, {
            'abcd': {
                'efg': {
                    'hij': 'test',
                },
                'efg,hij': 'test2',
                'efg$': {
                    'hij': 'test3',
                },
            },
        })
