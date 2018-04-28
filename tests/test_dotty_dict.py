#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from dotty_dict import Dotty, dotty


class TestDottyBasics(unittest.TestCase):
    def test_create_empty_instance(self):
        dot = dotty()
        self.assertEqual(dot, {})

    def test_create_non_empty_instance(self):
        plain_dict = {'not': 'empty'}

        dot = dotty(plain_dict)
        self.assertEqual(dot, plain_dict)
        self.assertIsNot(dot, plain_dict)

    # noinspection PyTypeChecker
    def test_raise_attr_error_if_input_is_not_dict(self):
        with self.assertRaises(AttributeError):
            dotty(['not', 'valid'])

    def test_two_dotty_with_the_same_input_should_be_equal(self):
        first = dotty({'is': 'valid'})
        second = dotty({'is': 'valid'})

        self.assertEqual(first, second)

    def test_two_dotty_with_different_input_should_not_be_equal(self):
        first = dotty({'counter': 1})
        second = dotty({'counter': 2})

        self.assertNotEqual(first, second)

    def test_plain_dict_and_dotty_wrapper_should_be_equal(self):
        plain = {'a': 1, 'b': 2}
        dot = dotty(plain)
        self.assertEqual(dot, plain)

    def test_dotty_and_not_mapping_instance_should_not_be_equal(self):
        dot = dotty({'a': 1, 'b': 2})
        self.assertNotEqual(dot, [('a', 1), ('b', 2)])
        self.assertNotEqual(dot, ('a', 1))
        self.assertNotEqual(dot, {1, 2, 3})
        self.assertNotEqual(dot, 123)
        self.assertNotEqual(dot, 'a:1, b:2')


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
        self.dot['deep.deeper.escaped\.dot_key'] = 'it works!'
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
        result = dot['deep.deeper.escaped\.dot_key']
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
        result = dot['deep.deeper.escaped\\\\.dot_key']
        self.assertEqual(result, 'it works!')

    def test_use_custom_separator_and_custom_escape_char(self):
        sep = ','
        esc = '$'
        dot = Dotty({}, separator=sep, esc_char=esc)
        dot['abcd,efg,hij'] = 'test'
        dot['abcd,efg$,hij'] = 'test2'
        dot['abcd,efg\\$,hij'] = 'test3'
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


class TestDottyPrivateMembers(unittest.TestCase):
    def test_split_separator(self):
        dot = dotty()
        result = dot._split('chain.of.keys')
        self.assertListEqual(result, ['chain', 'of', 'keys'])

    def test_split_with_custom_separator(self):
        dot = Dotty({}, separator='#', esc_char='\\')
        result = dot._split('chain#of#keys')
        self.assertListEqual(result, ['chain', 'of', 'keys'])


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
        keys = list(sorted(self.dot.keys()))
        self.assertListEqual(keys, ['deep', 'flat_key'])

    def test_access_keys_from_deeply_nested_structure(self):
        keys = list(sorted(self.dot['deep.deeper'].keys()))
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

    def test_setdefault_flat(self):
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

    def test_setdefault_nested_key(self):
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
