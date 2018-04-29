#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import Mapping

__author__ = 'Paweł Zadrożny'
__copyright__ = 'Copyright (c) 2017, Paweł Zadrożny'


def dotty(dictionary=None):
    """Factory function for Dotty class.

    Create Dotty wrapper around existing or new dictionary.

    :param dict dictionary: Any dictionary or dict-like object
    :return: Dotty instance
    """
    if dictionary is None:
        dictionary = {}
    return Dotty(dictionary, separator='.', esc_char='\\')


class Dotty:
    """Dictionary and dict-like objects wrapper.

    Dotty wraps dictionary and provides proxy for quick accessing to deeply
    nested keys and values using dot notation.

    Dot notation can be customize in special cases. Let's say dot character
    has special meaning, and you want to use other character for accessing
    deep keys.

    Dotty does not copy original dictionary but it operates on it.
    All changes made in original dictionary are reflected in dotty wrapped dict
    and vice versa.

    :param dict dictionary: Any dictionary or dict-like object
    :param str separator: Character used to chain deep access.
    :param str esc_char: Escape character for separator.
    """

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

    def __str__(self):
        return str(self._data)

    def __eq__(self, other):
        try:
            return sorted(self._data.items()) == sorted(other.items())
        except AttributeError:
            return False

    def __len__(self):
        return len(self._data)

    def __getattr__(self, item):
        return getattr(self._data, item)

    def __contains__(self, item):
        def search_in(items, data):
            """Recursively search for deep key in dict.

            :param list items: List of dictionary keys
            :param data: Portion of dictionary to operate on
            :return bool: Predicate of key existence
            """
            it = items.pop(0)
            if items and it in data:
                return search_in(items, data[it])
            return it in data

        return search_in(self._split(item), self._data)

    def __getitem__(self, item):
        def get_from(items, data):
            """Recursively get value from dictionary deep key.

            :param list items: List of dictionary keys
            :param data: Portion of dictionary to operate on
            :return: Value from dictionary
            :raises KeyError: If key does not exist
            """
            it = items.pop(0)
            data = data[it]
            if items:
                return get_from(items, data)
            else:
                return data

        return get_from(self._split(item), self._data)

    def __setitem__(self, key, value):
        def set_to(items, data):
            """Recursively set value to dictionary deep key.

            :param list items: List of dictionary keys
            :param data: Portion of dictionary to operate on
            """
            item = items.pop(0)
            if items:
                if item not in data:
                    data[item] = {}
                set_to(items, data[item])
            else:
                data[item] = value

        set_to(self._split(key), self._data)

    def __delitem__(self, key):
        def del_key(items, data):
            """Recursively remove deep key from dict.

            :param list items: List of dictionary keys
            :param data: Portion of dictionary to operate on
            :raises KeyError: If key does not exist
            """
            it = items.pop(0)
            if items and it in data:
                return del_key(items, data[it])
            elif not items and it in data:
                del data[it]
            elif not items and it not in data:
                raise KeyError(it)

        del_key(self._split(key), self._data)

    def copy(self):
        """Returns a shallow copy of dictionary wrapped in Dotty.

        :return: Dotty instance
        """
        return dotty(self._data.copy())

    @staticmethod
    def fromkeys(seq, value=None):
        """Create a new dictionary with keys from seq and values set to value.

        New created dictionary is wrapped in Dotty.

        :param seq: Sequence of elements which is to be used as keys for the new dictionary
        :param value: Value which is set to each element of the dictionary
        :return: Dotty instance
        """
        return dotty(dict.fromkeys(seq, value))

    def get(self, key, default=None):
        """Get value from deep key or default if key does not exist.

        This method match 1:1 with dict .get method except that it
        accepts deeply nested key with dot notation.

        :param str key: Single key or chain of keys
        :param Any default: Default value if deep key does not exist
        :return: Any or default value
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    def pop(self, key, default=None):
        """Pop key from Dotty.

        This method match 1:1 with dict .pop method except that
        it accepts deeply nested key with dot notation.

        :param str key: Single key or chain of keys
        :param Any default: If default is provided will be returned
        :raises KeyError: If key does not exist and default has not been provided
        :return: Any or default value
        """

        def pop_from(items, data):
            it = items.pop(0)
            if items:
                data = data[it]
                return pop_from(items, data)
            else:
                return data.pop(it, default)

        return pop_from(self._split(key), self._data)

    def setdefault(self, key, default=None):
        """Get key value if exist otherwise set default value under given key
        and return its value.

        This method match 1:1 with dict .setdefault method except that
        it accepts deeply nested key with dot notation.

        :param str key: Single key or chain of keys
        :param Any default: Default value for not existing key
        :return: Value under given key or default
        """
        if key in self._data:
            return self.__getitem__(key)
        self.__setitem__(key, default)
        return default

    def to_dict(self):
        """Return wrapped dictionary.

        This method does not copy wrapped dictionary.

        :return dict: Wrapped dictionary
        """
        return self._data

    def _split(self, key):
        """Split dot notated chain of keys.

        Works with custom separators and escape characters.

        :param str key: Single key or chain of keys
        :return list: List of keys
        """
        esc_stamp = (self.esc_char + self.separator, '<#esc#>')
        skp_stamp = ('\\' + self.esc_char + self.separator, '<#skp#>' + self.separator)

        stamp_esc = ('<#esc#>', self.separator)
        stamp_skp = ('<#skp#>', self.esc_char)

        key = key.replace(*skp_stamp).replace(*esc_stamp)
        keys = key.split(self.separator)
        for i, k in enumerate(keys):
            keys[i] = k.replace(*stamp_esc).replace(*stamp_skp)

        return keys
