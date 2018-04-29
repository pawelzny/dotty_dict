========
Examples
========

Yes, I know it's dangerous to follow code examples.
Usually examples aren't in sync with real source code.

But I found a solution ... I hope!

.. note:: | All examples are derived from real code hooked to Pytest.
          | Every change in source code enforce change in examples.
          | **Outdated examples == failed build**.
          |
          | You can check at https://github.com/pawelzny/dotty_dict/blob/master/tests/test_examples.py

.. seealso:: Look at :ref:`Public API` for more details.


******
Basics
******

The easiest way to use Dotty dict is with function factory.
Factory takes only one, optional dictionary as argument.

If leaved empty, factory function will create new, empty dictionary.


Wrap existing dict
==================

.. literalinclude:: ../example/basics.py
   :language: python
   :dedent: 4
   :start-after: wrap_existing_dict
   :end-before: # end of wrap_existing_dict


Create new dotty
================

.. literalinclude:: ../example/basics.py
   :language: python
   :dedent: 4
   :start-after: create_new_dotty
   :end-before: # end of create_new_dotty


Builtin methods
===============

Dotty exposes all native to dict, builtin methods.
Only change is made to method which uses key as input to accept dot notation.

.. literalinclude:: ../example/basics.py
   :language: python
   :dedent: 4
   :start-after: builtin_methods
   :end-before: # end of builtin_methods


********
Advanced
********

Lets simulate more real scenario. API requests and responses are often very complex
with many deeply nested keys. And when you need to check one of them it may
looks like: ``res.get('data', {}).get('service', {}).get('status', {}).get('current', False)``.

**It's awful!** All this empty dictionary fallback to dig in for current status!


Make API request
================

In this scenario we will send post request to create new user with superuser privileges.
Below there is example response as dictionary, and then the way to check granted privileges.

.. literalinclude:: ../example/advanced.py
   :language: python
   :dedent: 4
   :start-after: api_request
   :end-before: # end of api_request
   :emphasize-lines: 45


Escape character
================

In some cases we want to preserve dot in key name and do not treat it
as keys separator. It can by done with escape character.

.. literalinclude:: ../example/advanced.py
   :language: python
   :dedent: 4
   :start-after: escape_character
   :end-before: # end of escape_character


Escape the escape character
===========================

What if escape character should be preserved as integral key name,
but it happens to be placed right before separator character?

The answer is: Escape the escape character.

.. warning:: Be careful because backslashes in Python require special treatment.

.. literalinclude:: ../example/advanced.py
   :language: python
   :dedent: 4
   :start-after: escape_the_escape_character
   :end-before: # end of escape_the_escape_character


*************
Customization
*************

By default Dotty uses dot as keys separator and backslash as escape character.
In special occasions you may want to use different set of chars.

Customization require using Dotty class directly instead of factory function.


Custom separator
================

In fact any valid string can be used as separator.

.. literalinclude:: ../example/customization.py
   :language: python
   :dedent: 4
   :start-after: custom_separator
   :end-before: # end of custom_separator


Custom escape char
==================

As separator, escape character can be any valid string
not only single character.

.. literalinclude:: ../example/customization.py
   :language: python
   :dedent: 4
   :start-after: custom_escape_char
   :end-before: # end of custom_escape_char
