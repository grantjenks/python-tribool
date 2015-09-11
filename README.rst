Tribool: Three-Valued Logic
===========================

`Tribool <http://www.grantjenks.com/docs/tribool/>`_ is an Apache2 licensed
Python module that implements three-valued logic.

Suppose for a moment that you're attempting to store a value across a network
connection. You begin with a simple protocol in which the server stores the
received value and then sends an acknowledgement to the client.  In this
design, the client experiences a delay between when the request is sent and the
acknowledgement is received. In that delay, it is impossible for the client to
know whether the value has been committed on the server.  In such cases, it's
useful to describe the commit state of the server from the client's perspective
as True, False, or Indeterminate.

Another example occurs in database systems. Consider a record that contains
a boolean field. Such a field may only be either True or False. But we want
to support the notion of committing a partial record in the case that the
record is large or the client does not have all relevant information. In this
scenario, we wish to commit neither True nor False as the value is currently
Unknown.

The Python Tribool module was designed for these cases by describing a logical
data type that supports three values: True, False, and Indeterminate. The third
value is best thought of as a state being either True or False. Given these
three values it's possible to define truth tables over the logical operators
`and`, `or` and `not` and to define equality and inequality relationships.

Features
--------

- Pure-Python (easy to hack with)
- Fully Documented
- 100% Test Coverage
- Pragmatic Design (mostly a few truth tables and thread-safe singleton pattern)
- Developed on Python 2.7
- Tested on CPython 2.6, 2.7, 3.2, 3.3, 3.4 and PyPy 2.5+, PyPy3 2.4+

Quickstart
----------

Installing Tribool is simple with
`pip <http://www.pip-installer.org/>`_::

  $ pip install tribool

You can access documentation in the interpreter with Python's built-in help
function::

  >>> from tribool import Tribool
  >>> help(Tribool)

Tutorial
--------

A Python Tribool may have any of three values::

  >>> from tribool import Tribool
  >>> Tribool(True)          # True
  >>> Tribool('False')       # False
  >>> Tribool(Tribool(None)) # Indeterminate

Those three values correspond to True, False and Indeterminate. To view that
value, convert the Tribool to a string::

  >>> print Tribool(True), Tribool(False), Tribool(None)
  True False Indeterminate

The logical operators are also defined over these values. For example, the
result of negation::

  >>> for value in (True, False, None):
  ...     print '~', Tribool(value), '=', ~Tribool(value)
  ~ True = False
  ~ False = True
  ~ Indeterminate = Indeterminate

Likewise for `and`, `or`, and `xor` the operators involving only True and
False are unchanged. And mostly those involving Indeterminate result in
Indeterminate. For example::

  >>> True & Tribool(None)  # True and Indeterminate = Indeterminate
  Tribool(None)
  >>> False | Tribool(None) # False or Indeterminate = Indeterminate
  Tribool(None)
  >>> None ^ Tribool(None)  # Indeterminate xor Indeterminate = Indeterminate
  Tribool(None)

But there are a couple cases where this is not so::

  >>> True | Tribool(None)  # True or Indeterminate = True
  Tribool(True)
  >>> False & Tribool(None) # False and Indeterminate = False
  Tribool(False)

Notice that the bitwise-operators, `&|^~`, have been used rather than the
short-circuiting `and`, `or`, `not`. Python supports short-circuiting operators
only for boolean values and you cannot implicitly convert a Tribool to a
boolean.  An attempt to do so will raise a `ValueError`::

  >>> not Tribool(True)
  Traceback (most recent call last):
    ...
  ValueError: Cannot implicitly convert Tribool to bool (use the bitwise
  (&, |, ^, ~) operators or insert a cast and use Tribool(...).value)

For this reason, you cannot directly use a Tribool in an `if` statement::

  >>> if Tribool(True): pass
  Traceback (most recent call last):
    ...
  ValueError: Cannot implicitly convert Tribool to bool ...

To test the value of a Tribool, use the `value` property::

  >>> print Tribool(True).value, Tribool(False).value, Tribool(None).value
  True False None
  >>> (Tribool(None) | True).value is True
  True
  >>> ready, committed = Tribool(True), Tribool(None)
  >>> if (ready & committed).value is not True:
  ...     print 'Still waiting.'
  Still waiting.

When the Tribool value is Indeterminate, the `value` property will be `None`.
For example::

  >>> status = Tribool(None)
  >>> # Do something that will update status.
  >>> while status.value is None:
  ...     time.sleep(1) # Busy-wait.
  >>> if status.value is True:
  ...     print 'Success'
  ... else:
  ...     print 'Error'

Tribools also work with equality/inequality relationships. Comparing Tribools
returns a Tribool because the result may be ambiguous. For the less-than and
greater-than relationships, True corresponds to 1 and False to 0 just as with
boolean data types. The Indeterminate value is either 0 or 1 which has some
unusual implications. Some example inequalities::

  >>> Tribool(False) < Tribool(True)
  Tribool(True)
  >>> Tribool(False) == Tribool(False)
  Tribool(True)
  >>> Tribool(False) > Tribool(True)
  Tribool(False)

The unusual implication of the Indeterminate value is that it is not equal
to itself::

  >>> print Tribool(True) >= Tribool(None)
  True
  >>> print Tribool(False) < Tribool(None)
  Indeterminate
  >>> print Tribool(None) == Tribool(None)
  Indeterminate

When an object is not equal to itself, strange things can happen. Fortunately
Python defines two notions of equality. The first is defined by the `is`
relationship and may not be overriden. The second is defined by the `__eq__`
method. To behave as value types, Tribool objects are singletons. Threrefore
two Tribools with the same value will have matching `id` values. For example::

  >>> (id(Tribool(True)), id(Tribool(True)), id(Tribool(True)))
  (4426760848, 4426760848, 4426760848)
  >>> (id(Tribool(None)), id(Tribool(None)), id(Tribool(None)))
  (4426719568, 4426719568, 4426719568)

This is accomplished by overriding the `__new__` constructor and implementing
a thread-safe singleton pattern. As singletons, Tribool objects are immutable
and comparable using the `is` operator. Judicious use often results in code
that is more readable::

  >>> Succeeded, TryAgain = Tribool(True), Tribool(None)
  >>> status = Tribool(None)
  >>> while status is TryAgain:
  ...     status = try_something()
  >>> if status is Succeeded:
  ...     print 'Success!'

Tribool objects are also hashable and work inside `dict`s and map-like types::

  >>> display = {
  ...     Tribool(True): 'Success',
  ...     Tribool(False): 'Error',
  ...     Tribool(None): 'Try Again',
  ... }
  >>> print display[Tribool(None)]
  Try Again

A surprising result occurs however with containers. When using the `in`
operator, objects are tested for membership using equality. But this occurs
in several steps, the first of which is using the `is` operator followed by
the `__eq__` method. In case the `__eq__` method fails to return a boolean-
typed value, an implicit conversion occurs which Tribool does not permit.
For example::

  >>> Success, Error, Unknown = map(Tribool, (True, False, None))
  >>> Success in [Success, Error, Unknown] # Works!
  True
  >>> Error in [Success, Error, Unknown]   # Fails
  Traceback (most recent call last):
    ...
  ValueError: Cannot implicitly convert Tribool to bool ...

The latter attempt fails because `Error is Success` returns False and so
`Error == Success` is tried. That returns `Tribool(False)` which does not
have type `bool` and so an implicit conversion occurs. To achieve the
affect of the `in` operator use the `any` built-in and a generator expression
like so::

  >>> statuses = [Success, Success, Unknown, Error]
  >>> any(status is Error for status in statuses)
  True

To obey the singleton pattern, Tribool also implements the `__copy__` and
`__deepcopy__` methods as part of the `copy` module protocol. Pickling is
another method of copying objects and so `__reduce__` is implemented as part of
the `pickle` protocol. Note also that Tribool inherits directly from `tuple` to
prevent mutation of its internal state.

The Python Tribool module has many uses but it was originally designed to
support the notion of `three-valued logic as found in SQL
<http://en.wikipedia.org/wiki/Null_(SQL)>`_. SQL defines similar rules for
its Null value type in logical expressions. `Django's NullBooleanField
<https://docs.djangoproject.com/en/stable/ref/models/fields/#nullbooleanfield>`_
is an example where these ideas intersect.

Some readers will be familiar with `Boost.Tribool
<http://www.boost.org/doc/libs/release/doc/html/tribool.html>`_, an
implementation of the Tribool datatype in C++. While the semantics of both
packages are the same, the design of the Boost implementation differs a great
deal. In particular, Boost defines a new `indeterminate` keyword rather than
using the `null` value in C++. An `Indeterminate` object was considered in the
design of this module but discarded in favor of Python's built-in `None`.

Reference and Indices
---------------------

* `Tribool Documentation`_
* `Tribool at PyPI`_
* `Tribool at GitHub`_
* `Tribool Issue Tracker`_

.. _`Tribool Documentation`: http://www.grantjenks.com/docs/tribool/
.. _`Tribool at PyPI`: https://pypi.python.org/pypi/tribool/
.. _`Tribool at GitHub`: https://github.com/grantjenks/python_tribool/
.. _`Tribool Issue Tracker`: https://github.com/grantjenks/python_tribool/issues/

License
-------

Copyright 2015 Grant Jenks

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
