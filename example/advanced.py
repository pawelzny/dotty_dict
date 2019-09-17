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


def list_embedded():
    from dotty_dict import dotty

    # dotty supports embedded lists
    # WARNING!
    # Dotty used to support lists only with dotty_l.
    # This feature is depreciated - now lists have native support.

    dot = dotty({
        'annotations': [
            {'label': 'app', 'value': 'webapi'},
            {'label': 'role', 'value': 'admin'},
        ],
        'spec': {
             'containers': [
                 ['gpu', 'tensorflow', 'ML'],
                 ['cpu', 'webserver', 'sql'],
            ]
        }
    })

    assert dot['annotations.0.label'] == 'app'
    assert dot['annotations.0.value'] == 'webapi'
    assert dot['annotations.1.label'] == 'role'
    assert dot['annotations.1.value'] == 'admin'
    assert dot['spec.containers.0.0'] == 'gpu'
    assert dot['spec.containers.0.1'] == 'tensorflow'
    assert dot['spec.containers.0.2'] == 'ML'
    assert dot['spec.containers.1.0'] == 'cpu'
    assert dot['spec.containers.1.1'] == 'webserver'
    assert dot['spec.containers.1.2'] == 'sql'
    # end of list_embedded


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
