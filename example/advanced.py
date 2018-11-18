#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2018, Pawelzny'


def api_request():
    def make_request(payload):
        """Fake request for example purpose.

        :param dict payload: Example payload
        :return dict: Example response
        """
        return {
            'status': {
                'code': 200,
                'msg': 'User created',
            },
            'data': {
                'user': {
                    'id': 123,
                    'personal': {
                        'name': 'Arnold',
                        'email': 'arnold@dotty.dict',
                    },
                    'privileges': {
                        'granted': ['login', 'guest', 'superuser'],
                        'denied': ['admin'],
                        'history': {
                            'actions': [
                                ['superuser granted', '2018-04-29T17:08:48'],
                                ['login granted', '2018-04-29T17:08:48'],
                                ['guest granted', '2018-04-29T17:08:48'],
                                ['created', '2018-04-29T17:08:48'],
                                ['signup_submit', '2018-04-29T17:08:47'],
                            ],
                        },
                    },
                },
            },
        }

    from dotty_dict import dotty

    request = dotty()
    request['request.data.payload'] = {'name': 'Arnold',
                                       'email': 'arnold@dotty.dict',
                                       'type': 'superuser'}
    request['request.data.headers'] = {'content_type': 'application/json'}
    request['request.url'] = 'http://127.0.0.1/api/user/create'

    response = dotty(make_request(request.to_dict()))

    assert response['status.code'] == 200
    assert 'superuser' in response['data.user.privileges.granted']
    # end of api_request


def escape_character():
    from dotty_dict import dotty

    dot = dotty({
        'deep': {
            'key': 'value',
        },
        'key.with.dot': {
            'deeper': 'other value',
        },
    })

    # how to access deeper value?
    assert dot[r'key\.with\.dot.deeper'] == 'other value'
    # end of escape_character


def escape_the_escape_character():
    from dotty_dict import dotty

    dot = dotty({
        'deep': {
            'key': 'value',
        },
        'key.with_backslash\\': {  # backslash at the end of key
            'deeper': 'other value',
        },
    })

    # escape first dot and escape the escape character before second dot
    assert dot[r'key\.with_backslash\\.deeper'] == 'other value'
    # end of escape_the_escape_character
