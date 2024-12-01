#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from dotty_dict import dotty


class NoneSerializable:
    def __str__(self):
        return "test"


class TestListInDotty(unittest.TestCase):

    def test_should_to_dict(self):
        dot = dotty({
            "date": NoneSerializable()
        })

        self.assertEqual(dot.to_dict(), {'date': 'test'})
