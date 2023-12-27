#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from dotty_dict import dotty
from pandas import DataFrame
from pandas.testing import assert_frame_equal


class TestDottyPandas(unittest.TestCase):

    def setUp(self):

        self._prime_df = DataFrame([['tom', 10], ['nick', 15], ['juli', 14]],
                                   columns=['Name', 'Age'])

        self.dot = dotty(
            {
                'df': {
                    'first': DataFrame([['tom', 10], ['nick', 15], ['juli', 14]],
                                       columns=['Name', 'Age']),
                    'second': DataFrame([['tam', 10], ['nick', 15], ['juli', 14]],
                                        columns=['Name', 'Age'])
                },
            }
        )

    def test_get_dataframe(self):

        self.setUp()
        self.assertTrue(isinstance(self.dot.get('df.first'), DataFrame),
                        'pandas Dataframe get function failed')

    def test_eq_dataframe(self):

        self.setUp()
        assert_frame_equal(self._prime_df, self.dot['df.first'],
                           'pandas Dataframe equality failed with '
                           'assert_frame_equal() method')

        self.assertTrue(self._prime_df.equals(self.dot['df.first']),
                        'pandas Dataframe quality failed '
                        'with equals() method')

    def test_not_eq_dataframe(self):

        self.setUp()
        self.assertFalse(self._prime_df.equals(self.dot['df.second']),
                         'pandas Dataframe inequality failed')
