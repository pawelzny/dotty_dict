=====
Usage
=====

**Dotty** dictionary follows dict interfaces and all rules applied to dictionaries.
`Read more in Python documentation <https://docs.python.org/3/library/stdtypes.html#mapping-types-dict>`_

**Dotty** can be created by placing a standard dictionary with comma-separated list of key: value pairs
within **Dotty** constructor, for example::

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

Overview
--------

To use **Dotty** in a project::

    >>> from dotty_dict import Dotty

    >>> dotty = Dotty({'first': {'second': {'deep': 'i am here!'}}})
    >>> dotty['first.second.deeper.better.faster.stronger'] = 'ohh!'
    >>> dotty
    {'first': {'second': {'deep': 'i am here!', 'deeper': {'better': {'faster': {'stronger': 'ohh!'}}}}}}

Methods
-------

Ultimate goal is to match all Python dictionary method to work with deeply nested **Dotty** keys.

**d[** *'key.key.key'* **]**
++++++++++++++++++++++++++++

Return the item of d with dot notation key. Returns None if key is not in the map.

::

    >>> from dotty_dict import Dotty

    >>> dotty = Dotty({'foo.bar': 'baz'})
    >>> dotty['foo.bar'] += ' & fizz'
    >>> dotty
    {'foo': {'bar': 'baz & fizz'}}


**.get(** *'key.key.key'* **[,** *default* **])**
+++++++++++++++++++++++++++++++++++++++++++++++++

If deeply nested key is in dictionary return it's value,
but if key doesn't exist or it's value is None then return optional default value,
default defaults to None.

::

    >>> from dotty_dict import Dotty
    >>> dotty = Dotty()
    >>> dotty['foo.bar.baz'] = 'fizz'
    >>> value = dotty.get('foo.bar.baz', 'buzz')
    >>> value
    'fizz'
    >>> value = dotty.get('fizz.buzz', 'foo')
    >>> value
    'foo'

