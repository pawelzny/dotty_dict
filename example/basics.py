#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


def wrap_existing_dict():
    from dotty_dict import dotty

    data = {'status': 'ok', 'code': 200, 'data': {'timestamp': 1525018224,
                                                  'payload': []}}
    data = dotty(data)
    assert data['data.timestamp'] == 1525018224
    # end of wrap_existing_dict


def create_new_dotty():
    from dotty_dict import dotty

    data = dotty()
    data['status'] = 'ok'
    data['data.timestamp'] = 1525018224
    data['data.fancy.deeply.nested.key.for'] = 'fun'

    assert data == {'status': 'ok',
                    'data': {
                        'timestamp': 1525018224,
                        'fancy': {
                            'deeply': {
                                'nested': {
                                    'key': {
                                        'for': 'fun',
                                    },
                                },
                            },
                        },
                    }}
    # end of create_new_dotty


def builtin_methods():
    from dotty_dict import dotty

    dot = dotty({'status': 'ok',
                 'data': {
                     'timestamp': 1525018224,
                     'fancy': {
                         'deeply': {
                             'nested': {
                                 'key': {
                                     'for': 'fun',
                                 },
                             },
                         },
                     },
                 }})

    # get value, return None if not exist
    assert dot.get('data.payload') is None

    # pop key
    assert dot.pop('data.fancy.deeply.nested.key') == {'for': 'fun'}

    # get value and set new value if not exist
    assert dot.setdefault('data.payload', []) == []
    assert 'payload' in dot['data']

    # check what changed
    assert dot == {'status': 'ok',
                   'data': {
                       'timestamp': 1525018224,
                       'fancy': {
                           'deeply': {
                               'nested': {},
                           },
                       },
                       'payload': [],
                   }}

    # get keys
    assert list(sorted(dot.keys())) == ['data', 'status']
    # end of builtin_methods
