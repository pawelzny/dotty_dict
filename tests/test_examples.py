#!/usr/bin/env python
# -*- coding: utf-8 -*-

from example import fetch_all_examples_for_testing

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


def test_examples():
    """Entry point for examples functions.

    All examples are stores in example module
    in form of functions with assertions.

    Any exception raised in example will break tests.
    """
    for func in fetch_all_examples_for_testing():
        func()
