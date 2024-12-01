#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pickle
from dotty_dict import dotty


class TestListInDotty(unittest.TestCase):

    def test_should_serialize_and_deserialize(self):
        data = {
            "a": 1
        }
        dot = dotty(data)

        serialized = pickle.dumps(dot)
        deserialized = pickle.loads(serialized)

        self.assertEqual(deserialized, data)
