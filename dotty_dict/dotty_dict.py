#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Mapping, UserDict


class Dotty:
    def __init__(self, dictionary: dict = None):
        if dictionary is None:
            self._data = {}
        elif not isinstance(dictionary, Mapping):
            raise AttributeError('Dictionary must be type of dict')
        else:
            self._data = dictionary

    def __eq__(self, other):
        return sorted(self._data.items()) == sorted(other.items())

    def __getattr__(self, item):
        return getattr(self._data, item)

    def __getitem__(self, item):
        def search(items, data):
            it = items.pop(0)
            data = data.get(it)
            if data is None:
                return None
            if items:
                return search(items, data)
            else:
                return data

        return search(item.split('.'), self._data)

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, item):
        return item in self._data


# class DottyOLD(UserDict):
#     """Dotty dictionary with support_for['dot.notation.keys'].
#
#     Dotty dict-like object allow to access deeply nested keys using dot notation.
#     Create Dotty from dict or other dict-like object to use magic of Dotty.
#     """
#
#     def __init__(self, dictionary: dict):
#         super.__init__(dictionary)
#
#     def __getitem__(self, key):
#         """Get value from deeply nested key.
#
#         If key does not exist return None instead of raising KeyError exception.
#
#         :param (str) key: Single key or dot separated nested keys.
#         :return: Value or None.
#         """
#         tree = self._split(key)
#
#         item = dict(self.data)
#         for leaf in tree:
#             if leaf in item:
#                 item = item[leaf]
#
#             else:
#                 return self.__missing__(leaf)
#
#         return item
#
#     def __missing__(self, leaf):
#         """
#         Return None if nested leaf does not exist.
#
#         :param (str) leaf: Single key in dot noted key.
#         :return: Default value.
#         """
#         return None
#
#     def __setitem__(self, key, value):
#         """
#         Set recursively new key:value item into Dotty dict. Allow to set deeply nested keys.
#
#         :param (str) key:
#         :param (any) value:
#         :return:
#         """
#
#         def insert_into_dict(dictionary, leaf, val):
#             """
#             Recursively insert new keys and value at last to Dotty dictionary.
#
#             :param (dict|Dotty) dictionary:
#             :param (str) leaf:
#             :param (any) val:
#             :return: New dictionary
#             :rtype: dict
#             """
#             if len(tree) > 0:
#                 """
#                 Create or update deeply nested dictionaries if there is more leaf to follow.
#                 """
#                 if leaf in dictionary and isinstance(dictionary[leaf], dict):
#                     """
#                     If dictionary leaf is instance of dict, convert it to Dotty dict
#                     then update instead of override.
#                     """
#                     dictionary[leaf] = Dotty(dictionary[leaf])
#                     dictionary[leaf].update(
#                         insert_into_dict(dictionary[leaf], tree.pop(0), val)
#                     )
#
#                 elif leaf in dictionary and isinstance(dictionary[leaf], Mapping):
#                     """
#                     If dictionary leaf is instance of dict-like object, update it
#                     instead of override.
#                     """
#                     dictionary[leaf].update(
#                         insert_into_dict(dictionary[leaf], tree.pop(0), val)
#                     )
#
#                 else:
#                     """
#                     If dictionary leaf is not a dict nor dict-like object,
#                     override val with new Dotty dict.
#                     """
#                     dictionary[leaf] = insert_into_dict(
#                         Dotty(dictionary), tree.pop(0), val
#                     )
#
#                 return dictionary
#
#             """
#             Assign val to last leaf in tree then return dictionary.
#             """
#             dictionary[leaf] = val
#
#             return dictionary
#
#         tree = self._split(key)
#         self.data = insert_into_dict(dict(self.data), tree.pop(0), value)
#
#     @staticmethod
#     def _split(key):
#         """
#         Split dot notation key string to leafs.
#
#         :param (str) key: Dot notated key.None
#         :return: List of leafs.
#         """
#         return key.split('.')
#
#     def get(self, key, default=None):
#         """
#         Get dictionary value if exists otherwise get default value.
#
#         :param (str) key: Dot notated key.
#         :param (any) default: Default value if value does not exist.
#         :return:
#         """
#         return self.__getitem__(key) or default
