#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Mapping


def dotty(dictionary=None):
    """Factory function for Dotty class.

    :param dict dictionary: Any dictionary or dict-like object
    :return: Dotty instance
    """
    if dictionary is None:
        dictionary = {}
    return Dotty(dictionary, separator='.', esc_char='\\')


class Dotty:
    def __init__(self, dictionary, separator, esc_char):
        if not isinstance(dictionary, Mapping):
            raise AttributeError('Dictionary must be type of dict')
        else:
            self._data = dictionary
        self.separator = separator
        self.esc_char = esc_char

    def __repr__(self):
        return 'Dotty(dictionary={}, separator={!r}, esc_char={!r})'.format(
            self._data, self.separator, self.esc_char)

    def __eq__(self, other):
        try:
            return sorted(self._data.items()) == sorted(other.items())
        except AttributeError:
            return False

    def __getattr__(self, item):
        return getattr(self._data, item)

    def __getitem__(self, item):
        def get_from(items, data):
            it = items.pop(0)
            data = data[it]
            if items:
                return get_from(items, data)
            else:
                return data

        return get_from(self._split(item), self._data)

    def __setitem__(self, key, value):
        def set_to(items, data):
            item = items.pop(0)
            if items:
                if item not in data:
                    data[item] = {}
                set_to(items, data[item])
            else:
                data[item] = value

        set_to(self._split(key), self._data)

    def __contains__(self, item):
        def search_in(items, data):
            it = items.pop(0)
            if items and it in data:
                return search_in(items, data[it])
            return it in data

        return search_in(self._split(item), self._data)

    def __delitem__(self, key):
        def del_key(items, data):
            it = items.pop(0)
            if items and it in data:
                return del_key(items, data[it])
            elif not items and it in data:
                del data[it]
            elif not items and it not in data:
                raise KeyError(it)

        del_key(self._split(key), self._data)

    def __len__(self):
        return len(self._data)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key, default=None):
        def pop_from(items, data):
            it = items.pop(0)
            if items:
                data = data[it]
                return pop_from(items, data)
            else:
                return data.pop(it, default)

        return pop_from(self._split(key), self._data)

    def setdefault(self, key, default=None):
        if key in self._data:
            return self.__getitem__(key)
        self.__setitem__(key, default)
        return default

    def to_dict(self):
        return self._data

    def _split(self, key):
        esc_stamp = (self.esc_char + self.separator, '<#esc#>')
        skp_stamp = ('\\' + self.esc_char + self.separator, '<#skp#>' + self.separator)

        stamp_esc = ('<#esc#>', self.separator)
        stamp_skp = ('<#skp#>', self.esc_char)

        key = key.replace(*skp_stamp).replace(*esc_stamp)
        keys = key.split(self.separator)
        for i, k in enumerate(keys):
            keys[i] = k.replace(*stamp_esc).replace(*stamp_skp)

        return keys
