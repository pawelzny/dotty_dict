#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import importlib
import os
from inspect import getmembers, isfunction

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


def fetch_all_examples_for_testing():
    """Fetch all functions from every module in example package.

    This list of functions will be used in test_example module running by py.test.
    This helps to include all examples automatically.

    :return: List of example functions
    :rtype: list
    """
    example_func = []
    for f in glob.glob(os.path.dirname(__file__) + "/*.py"):
        if os.path.isfile(f) and not os.path.basename(f).startswith('_'):
            mod = importlib.import_module('example.{}'.format(os.path.basename(f)[:-3]))
            example_func.extend([o[1] for o in getmembers(mod) if isfunction(o[1])])

    return example_func
