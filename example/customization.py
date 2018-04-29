#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


def custom_separator():
    from dotty_dict import Dotty

    dot = Dotty({'deep': {'deeper': {'harder': 'faster'}}}, separator='$', esc_char='\\')

    assert dot['deep$deeper$harder'] == 'faster'
    # end of custom_separator


def custom_escape_char():
    from dotty_dict import Dotty

    dot = Dotty({'deep.deeper': {'harder': 'faster'}}, separator='.', esc_char='#')

    assert dot['deep#.deeper.harder'] == 'faster'
    # end of custom_escape_char
