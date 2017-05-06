=====
Usage
=====

**Dotty_dict** follows dict interfaces and all rules applied to dictionaries.
Dotty can be created by placing a standard dictionary with comma-separated
list of key: value pairs within Dotty constructor.

Overview
--------

Import and create dotty_dict on various way using Dotty() class.

| *class* **Dotty(**kwarg)**
| *class* **Dotty(mapping, **kwarg)**
| *class* **Dotty(iterable, **kwarg)**

.. code:: python

    >>> from dotty_dict import Dotty
    >>> Dotty()
    {}
    >>> Dotty({'foo': 4098, 'bar': 4127})
    {'foo': 4098, 'bar': 4127}
    >>> Dotty(foo=4098, bar=4127)
    {'foo': 4098, 'bar': 4127}
    >>> Dotty([('foo', 4098), ('bar', 4127)])
    {'foo': 4098, 'bar': 4127}
    >>> Dotty({'foo.bar.baz': 4098, 'foo.bar.fizz': 4127})
    {'foo': {'bar': {'baz': 4098, 'fizz': 4127}}}
    >>> Dotty([('foo.bar.baz', 4098), ('foo.bar.fizz', 4127)])
    {'foo': {'bar': {'baz': 4098, 'fizz': 4127}}}


Deeply nested keys in action
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use dotty_dict as normal dictionary but with special power of dot notation keys.

.. code:: python

    >>> from dotty_dict import Dotty
    >>> dotty = Dotty({'first': {'second': {'deep': 'i am here!'}}})
    >>> dotty['first.second.deeper.better.faster.stronger'] = 'ohh!'
    >>> dotty
    {'first': {'second': {'deep': 'i am here!', 'deeper': {'better': {'faster': {'stronger': 'ohh!'}}}}}}

.. note::

    Dotty dictionaries compare equal if and only if they have the same (key, value) pairs.
    Order comparisons (‘<’, ‘<=’, ‘>=’, ‘>’) raise TypeError.

Methods and operations
----------------------

Dotty dict supports all dictionary method and operations for single, not nested keys.

.. seealso::

    Python `mapping-types-dict <https://docs.python.org/3/library/stdtypes.html#mapping-types-dict>`_
    generic documentation
    and `types.MappingProxyType <https://docs.python.org/3/library/types.html#types.MappingProxyType>`_
    which can be used to create a read-only view of a dotty_dict.

**len(** *dotty* **)**
^^^^^^^^^^^^^^^^^^^^^^

Return the number of items in the *dotty* dictionary.

**dotty[** *key.key.key* **]**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return the item of d with dot notation key. Returns None if key is not in the map.

.. code:: python

    >>> from dotty_dict import Dotty
    >>> dotty = Dotty({'foo.bar': 'baz'})
    >>> dotty['foo.bar'] += ' & fizz'
    >>> dotty
    {'foo': {'bar': 'baz & fizz'}}
    >>> dotty['foo.bar']
    'baz & fizz'

**dotty[** *key* **] = value**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Set deeply nested *dotty[key.key.key]* to value.

.. code:: python

    >>> from dotty_dict import Dotty
    >>> dotty = Dotty()
    >>> dotty['foo.bar'] = 'baz'
    >>> dotty
    {'foo': {'bar': 'baz'}}

**del dotty[** *key* **]**
^^^^^^^^^^^^^^^^^^^^^^^^^^

Remove *dotty[key]* from dotty dict. Raises a
`KeyError <https://docs.python.org/3/library/exceptions.html#KeyError>`_ if key is not in the map.

.. warning::

    Nested keys are not supported yet.

**k in dotty**
^^^^^^^^^^^^^^

Return *True* if d has a key key, else *False*.

.. warning::

    Nested keys are not supported yet.

**key not in dotty**
^^^^^^^^^^^^^^^^^^^^

Equivalent to *not key in dotty*.

.. warning::

    Nested keys are not supported yet.

**iter(** *dotty* **)**
^^^^^^^^^^^^^^^^^^^^^^^

Return an iterator over the keys of the dictionary.
This is a shortcut for iter(dotty.keys()).

**clear()**
^^^^^^^^^^^

Remove all items from *dotty* dict.

**copy()**
^^^^^^^^^^

Return a shallow copy of the dictionary.

*classmethod* **fromkeys(** *seq[, value]* **)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new dictionary with keys from seq and values set to value.
`fromkeys() <https://docs.python.org/3/library/stdtypes.html#dict.fromkeys>`_
is a class method that returns a new dictionary. value defaults to None.

**From keys with default value set to** *None*

.. code:: python

    >>> from dotty_dict import Dotty
    >>> dotty = Dotty.fromkeys(['foo.bar', 'foo.baz', 'foo.fizz'])
    >>> dotty
    {'foo': {'bar': None, 'baz': None, 'fizz': None}}

**From keys with default value set to** *"buzz"*

.. code:: python

    >>> from dotty_dict import Dotty
    >>> dotty = Dotty.fromkeys(['foo.bar', 'foo.baz', 'foo.fizz'], 'buzz')
    >>> dotty
    {'foo': {'bar': 'buzz', 'baz': 'buzz', 'fizz': 'buzz'}}

**get(** *key.key.key[, default]* **)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return the value for deeply nested key if key is in the dotty dictionary, else default.
If default is not given, it defaults to None.

.. code:: python

    >>> from dotty_dict import Dotty
    >>> dotty = Dotty()
    >>> dotty['foo.bar.baz'] = 'fizz'
    >>> value = dotty.get('foo.bar.baz', 'buzz')
    >>> value
    'fizz'
    >>> value = dotty.get('fizz.buzz', 'foo')
    >>> value
    'foo'

**items()**
^^^^^^^^^^^

Return a new view of the dictionary’s items ((*key*, *value*) pairs).

.. seealso::

    See the documentation of `view objects <https://docs.python.org/3/library/stdtypes.html#dict-views>`_

**keys()**
^^^^^^^^^^

Return a new view of the dictionary’s keys. See the documentation of view objects.

.. seealso::

    See the documentation of `view objects <https://docs.python.org/3/library/stdtypes.html#dict-views>`_

**pop(** *key[, default]* **)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If key is in the dictionary, remove it and return its value, else return default.
If default is not given and key is not in the dictionary, a
`KeyError <https://docs.python.org/3/library/exceptions.html#KeyError>`_ is raised.

.. warning::

    Nested keys are not supported yet.

**popitem()**
^^^^^^^^^^^^^

Remove and return an arbitrary (*key*, *value*) pair from the dictionary.
`popitem() <https://docs.python.org/3/library/stdtypes.html#dict.popitem>`_
is useful to destructively iterate over a dictionary, as often used in set algorithms.
If the dictionary is empty, calling `popitem() <https://docs.python.org/3/library/stdtypes.html#dict.popitem>`_
raises a `KeyError <https://docs.python.org/3/library/exceptions.html#KeyError>`_.

.. code:: python

    >>> from dotty_dict import Dotty
    >>> dotty = Dotty({'foo.bar.baz': 'fizz'})
    >>> dotty
    {'foo': {'bar': {'baz': 'fizz'}}}
    >>> dotty.popitem()
    ('foo', {'bar': {'baz': 'fizz'}})
    >>> dotty
    {}

**setdefault(** *key[, default]* **)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If key is in the dictionary, return its value. If not, insert key with a value of
default and return default. default defaults to None.

.. warning::

    This method is available and IDE shows it as valid and working method,
    but there is known bug which always returns None even when default is set to other value.

**update(** *[other]* **)**
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Update the dictionary with the key/value pairs from other, overwriting existing keys. Return *None*.
`update() <https://docs.python.org/3/library/stdtypes.html#dict.update>`_ accepts either
another dictionary object or an iterable of key/value pairs
(as tuples or other iterables of length two). If keyword arguments are specified,
the dictionary is then updated with those key/value pairs: dotty.update(red=1, blue=2).

.. code::

    >>> from dotty_dict import Dotty
    >>> dotty = Dotty({'foo.bar': 'baz'})
    >>> dotty.update({'foo.fizz': 'buzz'})
    >>> dotty
    {'foo': {'bar': 'baz', 'fizz': 'buzz'}}
    >>> dotty.update(red=1, blue=2)
    >>> dotty
    {'blue': 2, 'foo': {'bar': 'baz', 'fizz': 'buzz'}, 'red': 1}

**values()**
^^^^^^^^^^^^

Return a new view of the dictionary’s values.

.. seealso::

    See the `documentation of view objects <https://docs.python.org/3/library/stdtypes.html#dict-views>`_.
