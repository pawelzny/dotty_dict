==========
dotty_dict
==========


.. image:: https://img.shields.io/pypi/v/dotty_dict.svg
        :target: https://pypi.python.org/pypi/dotty_dict

.. image:: https://img.shields.io/travis/pawelzny/dotty_dict.svg
        :target: https://travis-ci.org/pawelzny/dotty_dict

.. image:: https://readthedocs.org/projects/dotty-dict/badge/?version=latest
        :target: https://dotty-dict.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/pawelzny/dotty_dict/shield.svg
     :target: https://pyup.io/repos/github/pawelzny/dotty_dict/
     :alt: Updates


Safely get nested dict value by dot notation key.

Dotty dict-like object allow to access deeply nested keys using dot notation.
Create Dotty from dict or other dict-like object to use magic of Dotty.


* Free software: MIT license
* Documentation: https://dotty-dict.readthedocs.io.


Features
--------
* Accessing deeply nested key using dot notation
* Returns None if key does not exist instead of raising KeyError exception
* Assigning to deeply nested existing or not yet existing key
* Get deeply nested value or provided default value with .get() method

TODO

* Escape dot sign to allow accessing keys with dot in it

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

