**********
Dotty-Dict
**********

:Info: Dictionary wrapper for quick access to deeply nested keys.
:Author: Paweł Zadrożny @pawelzny <pawel.zny@gmail.com>

.. image:: https://circleci.com/gh/pawelzny/dotty_dict/tree/master.svg?style=shield&circle-token=77f51e87481f339d69ca502fdbb0c2b1a76c0369
   :target: https://circleci.com/gh/pawelzny/dotty_dict/tree/master
   :alt: CI Status

.. image:: https://readthedocs.org/projects/vo/badge/?version=latest
   :target: http://dotty-dict.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/dotty_dict.svg
   :target: https://pypi.org/project/dotty_dict/
   :alt: PyPI Repository Status

.. image:: https://img.shields.io/github/release/pawelzny/dotty_dict.svg
   :target: https://github.com/pawelzny/dotty_dict
   :alt: Release Status

.. image:: https://img.shields.io/pypi/status/dotty_dict.svg
   :target: https://pypi.org/project/dotty_dict/
   :alt: Project Status

.. image:: https://img.shields.io/pypi/pyversions/dotty_dict.svg
   :target: https://pypi.org/project/dotty_dict/
   :alt: Supported python versions

.. image:: https://img.shields.io/pypi/implementation/dotty_dict.svg
   :target: https://pypi.org/project/dotty_dict/
   :alt: Supported interpreters

.. image:: https://img.shields.io/pypi/l/dotty_dict.svg
   :target: https://github.com/pawelzny/dotty_dict/blob/master/LICENSE
   :alt: License


Features
========

* Simple wrapper around python dictionary and dict like objects
* Two wrappers with the same dict are considered equal
* Access to deeply nested keys with dot notation: ``dot['deeply.nested.key']``
* Create, read, update and delete nested keys of any length
* Expose all dictionary methods like ``.get``, ``.pop``, ``.keys`` and other


Installation
============

.. code:: bash

   pipenv install dotty-dict  # or pip install dotty-dict


* **Package**: https://pypi.org/project/dotty-dict/
* **Source**: https://github.com/pawelzny/dotty_dict


Documentation
=============

* Full documentation: http://dotty-dict.readthedocs.io
* Public API: http://dotty-dict.readthedocs.io/en/latest/api.html
* Examples and usage ideas: http://dotty-dict.readthedocs.io/en/latest/examples.html


TODO
====

* key=value caching to speed up lookups and low down memory consumption


Quick Example
=============

Create new dotty using factory function.

.. code-block:: python

   >>> from dotty_dict import dotty
   >>> dot = dotty({'plain': {'old': {'python': 'dictionary'}}})
   >>> dot['plain.old']
   {'python': 'dictionary'}


You can start with empty dotty

.. code-block:: python

   >>> from dotty_dict import dotty
   >>> dot = dotty()
   >>> dot['very.deeply.nested.thing'] = 'spam'
   >>> dot
   Dotty(dictionary={'very': {'deeply': {'nested': {'thing': 'spam'}}}}, separator='.', esc_char='\\')

   >>> dot['very.deeply.spam'] = 'indeed'
   >>> dot
   Dotty(dictionary={'very': {'deeply': {'nested': {'thing': 'spam'}, 'spam': 'indeed'}}}, separator='.', esc_char='\\')

   >>> del dot['very.deeply.nested']
   >>> dot
   Dotty(dictionary={'very': {'deeply': {'spam': 'indeed'}}}, separator='.', esc_char='\\')

   >>> dot.get('very.not_existing.key')
   None
