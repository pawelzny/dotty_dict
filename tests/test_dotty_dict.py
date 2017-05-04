#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from collections import Mapping, UserDict

from dotty_dict.dotty_dict import Dotty


class TestDotty_dict(unittest.TestCase):

    def setUp(self):
        self.dotty = Dotty({
            'already': {
                'exist': {
                    'deep': 'key',
                },
            },
            'flat_key': 'i am here',
        })

    def tearDown(self):
        pass

    def test_dotty_type(self):
        # self.assertIsInstance(self.dotty, dict)
        self.assertIsInstance(self.dotty, Mapping)
        self.assertIsInstance(self.dotty, UserDict)
        self.assertIsInstance(self.dotty, Dotty)

    def test_key_split(self):
        key = 'super.deeply.nested.key'
        tree = self.dotty._split(key)

        self.assertEqual(len(tree), 4)
        self.assertEqual(tree[1], 'deeply')

    def test_key_single_leaf(self):
        self.dotty['single'] = 'test'

        self.assertEqual(self.dotty['single'], 'test')
        self.assertEqual(self.dotty.get('single'), 'test')

    def test_key_nested_leaf(self):
        self.dotty['single.nested'] = 'test'

        self.assertEqual(self.dotty['single']['nested'], 'test')

    def test_key_nested_leaf_update(self):
        self.dotty['already.exist.new'] = 'value'

        self.assertEqual(self.dotty['already']['exist']['deep'], 'key')
        self.assertEqual(self.dotty['already']['exist']['new'], 'value')

    def test_key_nested_leaf_replace(self):
        self.dotty['already.exist'] = {'new': 'value'}

        self.assertNotIn('deep', self.dotty['already']['exist'])
        self.assertEqual(self.dotty['already']['exist']['new'], 'value')

    def test_access_nested_value(self):
        deep1 = self.dotty['already.exist.deep']
        deep2 = self.dotty['already']['exist']['deep']

        self.assertEqual(deep1, deep2)

    def test_access_nested_value_not_exist(self):
        self.assertIsNone(self.dotty['already.exist.black_hole'])

    def test_work_with_not_dotty_dict_like_objects(self):
        # Assume dict-like objects does not support dot notation
        self.dotty['already.exist.custom'] = UserDict({
            'not_dotty': {
                'user_dict': 'I am deeply nested user dict value'
            }
        })

        # Accessing not existing key from dict-like object should raise KeyError
        self.assertRaises(KeyError, self.dotty['already.exist.custom.key_value'])

        # One can access not Dotty dict-like object with dot notation
        self.assertEqual(self.dotty['already.exist.custom.not_dotty.user_dict'],
                         'I am deeply nested user dict value')

        # one can add new key to not dotty dict-like object with dot notation
        self.dotty['already.exist.custom.not_dotty.new_key'] = 'new key inside not dotty dict'

        self.assertEqual(
            self.dotty['already.exist.custom'],
            {
                'not_dotty': {
                    'user_dict': 'I am deeply nested user dict value',
                    'new_key': 'new key inside not dotty dict',
                }
            }
        )

    def test_get_value_simple(self):
        self.assertEqual(self.dotty.get('flat_key'), 'i am here')

    def test_get_value_nested(self):
        self.assertEqual(self.dotty.get('already.exist.deep'), 'key')

    def test_get_default_value_simple(self):
        self.assertEqual(self.dotty.get('black_hole', 'default value'), 'default value')

    def test_get_default_value_nested(self):
        self.assertEqual(self.dotty.get('already.exist.black_hole', 'def value'), 'def value')

