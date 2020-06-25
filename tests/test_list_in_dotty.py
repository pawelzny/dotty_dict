#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from dotty_dict import dotty_l as dotty


class TestListInDotty(unittest.TestCase):
    def setUp(self):
        self.dot = dotty({
            'field1': 'Value of F1',
            'field2': 'Value of F2',
            'field3': [
                {
                    'subfield1': 'Value of subfield1 (item 0)',
                    'subfield2': 'Value of subfield2 (item 0)'
                },
                {
                    'subfield1': 'Value of subfield1 (item 1)',
                    'subfield2': 'Value of subfield2 (item 1)'
                },
            ],
            'field4': 'Not wanted',
            'field5': [
                {
                    'subfield1': [{'subsubfield': 'Value of sub subfield (item 0)'}]
                }
            ],
            'field6': ['a', 'b']
        })

    def test_root_level_list_element(self):
        self.assertEqual(self.dot['field6.0'], 'a')

    def test_access_subfield1_of_field3(self):
        self.assertEqual(self.dot['field3.0.subfield1'], 'Value of subfield1 (item 0)')
        self.assertEqual(self.dot['field3.1.subfield1'], 'Value of subfield1 (item 1)')

    def test_access_sub_sub_field(self):
        self.assertEqual(self.dot['field5.0.subfield1.0.subsubfield'], 'Value of sub subfield (item 0)')

    def test_access_multidimensional_lists(self):
        dot = dotty({
            'field': [
                [{'subfield': 'Value of subfield (item 0,0)'}],
                [{'subfield': 'Value of subfield (item 0,1)'}]
            ]
        })
        self.assertEqual(dot['field.1.0.subfield'], 'Value of subfield (item 0,1)')

    def test_dotty_contains_subfield_of_field(self):
        self.assertIn('field3.0.subfield2', self.dot)

    def test_dotty_not_contains_out_of_range_subfield(self):
        self.assertNotIn('field3.3.subfield1', self.dot)

    def test_assert_key_error_if_index_is_not_integer(self):
        with self.assertRaises(KeyError):
            val = self.dot['field3.subfield1']  # noqa

    def test_assert_index_error_if_index_is_out_of_range(self):
        with self.assertRaises(IndexError):
            val = self.dot['field3.4.subfield1']  # noqa

    def test_assert_get_returns_default_if_index_is_out_of_range(self):
        val = self.dot.get('field3.4.subfield1')
        assert val is None

    def test_set_subfield_in_list(self):
        dot = dotty()

        dot['field.0.subfield'] = 'Value of subfield (item 0)'
        dot['field.1.subfield'] = 'Value of subfield (item 1)'
        dot['field.1.subfield2'] = 'Value of subfield2 (item 1)'

        self.assertDictEqual(dot.to_dict(), {
            'field': [
                {'subfield': 'Value of subfield (item 0)'},
                {'subfield': 'Value of subfield (item 1)', 'subfield2': 'Value of subfield2 (item 1)'}
            ],
        })

    def test_update_subfield_in_list(self):
        dot = dotty({
            'field': [
                {'subfield': 'Value of subfield (item 0)'},
                {'subfield': 'Value of subfield (item 1)', 'subfield2': 'Value of subfield2 (item 1)'}
            ],
        })

        dot['field.0.subfield'] = 'updated value'

        self.assertDictEqual(dot.to_dict(), {
            'field': [
                {'subfield': 'updated value'},
                {'subfield': 'Value of subfield (item 1)', 'subfield2': 'Value of subfield2 (item 1)'}
            ],
        })

    def test_delete_subfield(self):
        dot = dotty({'field': [
            {
                'subfield1': 'Value of subfield1 (item 0)',
                'subfield2': 'Value of subfield2 (item 0)'
            },
        ]})

        del dot['field.0.subfield2']

        self.assertDictEqual(dot.to_dict(), {'field': [
            {'subfield1': 'Value of subfield1 (item 0)'},
        ]})

    def test_list_as_return_value(self):
        dot = dotty({
            'field': [
                'list_field0',
                'list_field1'
            ]
        })

        self.assertEqual(dot['field.0'], 'list_field0')
        self.assertEqual(dot['field.1'], 'list_field1')
        self.assertTrue('field.0' in dot)
        self.assertTrue('field.1' in dot)
        self.assertFalse('field.2' in dot)


class TestMultipleSelectList(unittest.TestCase):
    def setUp(self):
        self.dot = dotty({
            'field1': [
                {
                    "subfield1": "value01",
                    "subfield2": "value02"
                },
                {
                    "subfield1": "value11",
                    "subfield2": "value12"
                },
                {
                    "subfield1": "value21",
                    "subfield2": "value22"
                },
                {
                    "subfield1": "value31",
                    "subfield2": "value32"
                }
            ],
            "field2": [
                {
                    "subfield1": [
                        {
                            "nestedsubfield1": "nestedvalue001",
                            "nestedsubfield2": "nestedvalue002"
                        },
                        {
                            "nestedsubfield1": "nestedvalue011",
                            "nestedsubfield2": "nestedvalue012"
                        }                    ]
                },
                {
                    "subfield1": [
                        {
                            "nestedsubfield1": "nestedvalue101",
                            "nestedsubfield2": "nestedvalue102"
                        },
                        {
                            "nestedsubfield1": "nestedvalue111",
                            "nestedsubfield2": "nestedvalue112"
                        }                    ]
                }
            ]
        })

    def test_whole_shallow_multiple_list(self):
        expected_list = ['value01', 'value11', 'value21', 'value31']
        self.assertListEqual(self.dot['field1.:.subfield1'], expected_list)

    def test_whole_nested_multiple_list(self):
        expected_list = [['nestedvalue001', 'nestedvalue011'],
                         ['nestedvalue101', 'nestedvalue111']]
        self.assertListEqual(self.dot['field2.:.subfield1.:.nestedsubfield1'], expected_list)

    def test_left_side_slice(self):
        expected_list = ['value21', 'value31']
        self.assertListEqual(self.dot['field1.2:.subfield1'], expected_list)

    def test_right_side_slice(self):
        expected_list = ['value01', 'value11']
        self.assertListEqual(self.dot['field1.:2.subfield1'], expected_list)

    def test_both_side_slice(self):
        expected_list = ['value11', 'value21']
        self.assertListEqual(self.dot['field1.1:3.subfield1'], expected_list)

    def test_step_slice(self):
        expected_list = ['value01', 'value21']
        self.assertListEqual(self.dot['field1.::2.subfield1'], expected_list)
