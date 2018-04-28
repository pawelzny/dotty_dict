#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from dotty_dict import dotty


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
