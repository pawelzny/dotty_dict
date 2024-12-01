#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pickle
from dotty_dict import dotty


class TestListInDotty(unittest.TestCase):

    def test_1(self):
        data = {
            "A": {
                "B": {
                    "C": {
                        "D": 1,
                        "E": 2
                    }
                }
            }
        }
        dot = dotty(data)

        del dot['A.B.C.D']

        self.assertEqual(dot.to_dict(), {'A': {'B': {'C': {'E': 2}}}})



    def test_2(self):
        data = {
            "A": {
                "B": {
                    "C": {
                        "D": 1
                    }
                }
            }
        }
        dot = dotty(data)

        del dot['A.B.C.D']

        self.assertEqual(dot.to_dict(), {})
