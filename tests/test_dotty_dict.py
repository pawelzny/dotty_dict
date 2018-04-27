#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from dotty_dict.dotty_dict import Dotty


class TestDottyBasics(unittest.TestCase):
    def test_create_empty_instance(self):
        dotty = Dotty()
        self.assertEqual(dotty, {})

    def test_create_non_empty_instance(self):
        plain_dict = {'not': 'empty'}

        dotty = Dotty(plain_dict)
        self.assertEqual(dotty, plain_dict)
        self.assertIsNot(dotty, plain_dict)

    def test_raise_attr_error_if_input_is_not_dict(self):
        with self.assertRaises(AttributeError):
            Dotty(['not', 'valid'])

    def test_two_dotty_with_the_same_input_should_be_equal(self):
        first = Dotty({'is': 'valid'})
        second = Dotty({'is': 'valid'})

        self.assertEqual(first, second)

    def test_two_dotty_with_different_input_should_not_be_equal(self):
        first = Dotty({'counter': 1})
        second = Dotty({'counter': 2})

        self.assertNotEqual(first, second)


class TestDottyValueAccess(unittest.TestCase):
    def setUp(self):
        self.dotty = Dotty({
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
        self.assertEqual(self.dotty['flat_key'], 'flat value')

    def test_non_existing_key_should_return_null(self):
        self.assertIsNone(self.dotty['not_existing'])

    def test_access_deep_nested_value(self):
        self.assertEqual(self.dotty['deep.nested'], 12)

    def test_access_middle_nested_value(self):
        self.assertDictEqual(self.dotty['deep.deeper.ridiculous'],
                             {'hell': 'is here'})

    def test_set_flat_value(self):
        self.dotty['new_flat'] = 'super flat'
        self.assertIn('new_flat', self.dotty)

    def test_set_deep_nested_value(self):
        self.dotty['deep.new_key'] = 'new value'
        self.assertIn('new_key', self.dotty['deep'])
