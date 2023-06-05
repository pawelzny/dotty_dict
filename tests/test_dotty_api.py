#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from dotty_dict import Dotty, dotty


class TestDottyPrivateMembers(unittest.TestCase):
    def test_split_separator(self):
        dot = dotty()
        result = dot._split('chain.of.keys')
        self.assertListEqual(result, ['chain', 'of', 'keys'])

    def test_split_with_custom_separator(self):
        dot = Dotty({}, separator='#', esc_char='\\')
        result = dot._split('chain#of#keys')
        self.assertListEqual(result, ['chain', 'of', 'keys'])


class TestDottyPublicMembers(unittest.TestCase):
    def test_to_dict(self):
        plain_dict = {'very': {'deeply': {'nested': {'thing': 'spam'}}}}
        dot = dotty(plain_dict)
        self.assertIsInstance(dot.to_dict(), dict)
        self.assertEqual(sorted(dot.to_dict().items()), sorted(plain_dict.items()))

    def test_nested_dotty_object_to_dict(self):
        expected_dict = {'hello': {'world': 1}, 'nested': {'dotty': {'wazaa': 3}}}
        top_dot = dotty({'hello': {'world': 1}})
        nested_dot = dotty({'wazaa': 3})
        top_dot['nested.dotty'] = nested_dot
        self.assertDictEqual(top_dot.to_dict(), expected_dict)

    def test_nested_dotty_in_list_to_dict(self):
        expected_dict = {'testlist': [{'dot1': 1}, {'dot2': 2}]}
        dot_list = [dotty({'dot1': 1}), dotty({'dot2': 2})]
        top_dot = dotty({'testlist': dot_list})
        self.assertDictEqual(top_dot.to_dict(), expected_dict)


class TestDictSpecificMethods(unittest.TestCase):
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

    def test_access_keys(self):
        keys = sorted(self.dot.keys())
        self.assertListEqual(keys, ['deep', 'flat_key'])

    def test_access_keys_from_deeply_nested_structure(self):
        keys = sorted(self.dot['deep.deeper'].keys())
        self.assertListEqual(keys, ['ridiculous', 'secret'])

    def test_iterate(self):
        keys = sorted(key for key in self.dot)
        self.assertListEqual(keys, ['deep', 'flat_key'])

    def test_iterate_from_deeply_nested_structure(self):
        keys = sorted(key for key in self.dot['deep.deeper'])
        self.assertListEqual(keys, ['ridiculous', 'secret'])

    def test_get_value_without_default(self):
        result = self.dot.get('deep.nested')
        self.assertEqual(result, 12)

    def test_get_value_with_default(self):
        result = self.dot.get('deep.other', False)
        self.assertFalse(result)

    def test_return_dotty_length(self):
        self.assertEqual(len(self.dot), 2)

    def test_pop_from_dotty_flat(self):
        result = self.dot.pop('flat_key')
        self.assertEqual(result, 'flat value')
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

    def test_pop_with_default_value(self):
        result = self.dot.pop('not_existing', 'abcd')
        self.assertEqual(result, 'abcd')
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
        })

    def test_pop_nested_key(self):
        result = self.dot.pop('deep.nested')
        self.assertEqual(result, 12)
        self.assertDictEqual(self.dot._data, {
            'flat_key': 'flat value',
            'deep': {
                'deeper': {
                    'secret': 'abcd',
                    'ridiculous': {
                        'hell': 'is here',
                    },
                },
            },
        })

    def test_pop_nested_key_with_default_value(self):
        result = self.dot.pop('deep.deeper.not_existing', 'abcd')
        self.assertEqual(result, 'abcd')
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
        })

    def test_setdefault_flat_not_existing(self):
        result = self.dot.setdefault('next_flat', 'new default value')
        self.assertEqual(result, 'new default value')
        self.assertDictEqual(self.dot._data, {
            'flat_key': 'flat value',
            'next_flat': 'new default value',
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

    def test_setdefault_flat_existing(self):
        self.dot['next_flat'] = 'original value'
        result = self.dot.setdefault('next_flat', 'new default value')
        self.assertEqual(result, 'original value')
        self.assertDictEqual(self.dot._data, {
            'flat_key': 'flat value',
            'next_flat': 'original value',
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

    def test_setdefault_nested_key_not_existing(self):
        result = self.dot.setdefault('deep.deeper.next_key', 'new default value')
        self.assertEqual(result, 'new default value')
        self.assertDictEqual(self.dot._data, {
            'flat_key': 'flat value',
            'deep': {
                'nested': 12,
                'deeper': {
                    'next_key': 'new default value',
                    'secret': 'abcd',
                    'ridiculous': {
                        'hell': 'is here',
                    },
                },
            },
        })

    def test_setdefault_nested_key_existing(self):
        self.dot['deep.deeper.next_key'] = 'original value'
        result = self.dot.setdefault('deep.deeper.next_key', 'new default value')
        self.assertEqual(result, 'original value')
        self.assertDictEqual(self.dot._data, {
            'flat_key': 'flat value',
            'deep': {
                'nested': 12,
                'deeper': {
                    'next_key': 'original value',
                    'secret': 'abcd',
                    'ridiculous': {
                        'hell': 'is here',
                    },
                },
            },
        })

    def test_copy(self):
        first = dotty({'a': 1, 'b': 2})
        second = first.copy()

        self.assertIsInstance(second, Dotty)
        self.assertEqual(first, second)
        self.assertIsNot(first, second)
        self.assertIsNot(first._data, second._data)

    def test_fromkeys(self):
        dot = dotty().fromkeys({'a', 'b', 'c'}, value=10)
        self.assertDictEqual(dot.to_dict(), {'a': 10, 'b': 10, 'c': 10})
        self.assertIsInstance(dot, Dotty)
