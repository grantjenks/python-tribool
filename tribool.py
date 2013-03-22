# -*- coding: utf-8 -*-

class Tribool:
    """Tribool implementation of three-valued logic.

    Tribool represents True, False, or Indeterminate using a private
    value set to True, False, or None respectively.
    """

    def __init__(self, value=None):
        """Intialize Tribool object.

        Tribool(value) -- value may be one of True, False, None, or Tribool.

        None is representative of an indeterminate boolean value.
        """
        self._value = self._resolve(value)

    def __invert__(self):
        """Logical negation of Tribool value."""
        return Tribool(Tribool._not[self._value])

    def __and__(self, that):
        """Logical AND of Tribool and other value."""
        return Tribool(Tribool._and[self._value, self._resolve(that)])

    def __rand__(self, that):
        """Logical AND of Tribool and other value."""
        return Tribool(Tribool._and[self._value, self._resolve(that)])

    def __or__(self, that):
        """Logical OR of Tribool and other value."""
        return Tribool(Tribool._or[self._value, self._resolve(that)])

    def __ror__(self, that):
        """Logical OR of Tribool and other value."""
        return Tribool(Tribool._or[self._value, self._resolve(that)])

    def __xor__(self, that):
        """Logical XOR of Tribool and other value."""
        return Tribool(Tribool._xor[self._value, self._resolve(that)])

    def __rxor__(self, that):
        """Logical XOR of Tribool and other value."""
        return Tribool(Tribool._xor[self._value, self._resolve(that)])

    def __eq__(self, that):
        """Logical equality of Tribool and other value."""
        return Tribool(Tribool._eq[self._value, self._resolve(that)])

    def __ne__(self, that):
        """Logical inequality of Tribool and other value."""
        return not Tribool(Tribool._eq[self._value, self._resolve(that)])

    def __lt__(self, that):
        """Logical less than of Tribool and other value."""
        return Tribool(Tribool._lt[self._value, self._resolve(that)])

    def __le__(self, that):
        """Logical less than or equal of Tribool and other value."""
        return (Tribool(Tribool._lt[self._value, self._resolve(that)])
                | (self == that))

    def __gt__(self, that):
        """Logical greater than of Tribool and other value."""
        return ~(self <= that)

    def __ge__(self, that):
        """Logical greater than or equal of Tribool and other value."""
        return ~(self < that)

    def __nonzero__(self):
        """Raise ValueError on conversion to bool.

        When this occurs, it may indicate that the logical operators:
        (and, or, not) were used. Python does not permit overloading these
        operators. Use the bitwise (&, |, ^) operators instead.
        Likewise, if the comparison operators (<, <=, >, >=) were used
        then a type conversion using Tribool(...) is required.
        """
        raise ValueError('Cannot convert Tribool to bool'
                         ' (use the bitwise (&, |, ^) operators'
                         ' or insert a cast to Tribool(...))')

    def __index__(self):
        """Raise ValueError on conversion to int."""
        raise ValueError('Cannot convert Tribool to index')

    def __trunc__(self):
        """Raise ValueError on truncation."""
        raise ValueError('Connect truncate Tribool')

    def __str__(self):
        """String representing Tribool value."""
        return 'Indeterminate' if self._value is None else str(self._value)

    def __repr__(self):
        """String representation of Tribool."""
        return 'Tribool({0})'.format(str(self._value))

    def _resolve(self, that):
        """Resolve given value to one of True, False, or None.

        Raises ValueError if given value's type is unsupported.
        """
        if isinstance(that, Tribool):
            return that._value
        elif isinstance(that, bool) or (that is None):
            return that
        else:
            raise ValueError('Unsupported Type')

    def _check(self):
        """Check invariant of Tribool."""
        assert (self._value in (True, False, None))
        return self

    """Logic tables for operators."""

    _not = { True : False,
             False : True,
             None : None }

    _and = { (True, True) : True,
             (True, False) : False,
             (True, None) : None,
             (False, True) : False,
             (False, False) : False,
             (False, None) : False,
             (None, True) : None,
             (None, False) : False,
             (None, None) : None }

    _or = { (True, True) : True,
            (True, False) : True,
            (True, None) : True,
            (False, True) : True,
            (False, False) : False,
            (False, None) : None,
            (None, True) : True,
            (None, False) : None,
            (None, None) : None }

    _xor = { (True, True) : False,
             (True, False) : True,
             (True, None) : None,
             (False, True) : True,
             (False, False) : False,
             (False, None) : None,
             (None, True) : None,
             (None, False) : None,
             (None, None) : None }

    _eq = { (True, True) : True,
            (True, False) : False,
            (True, None) : None,
            (False, True) : False,
            (False, False) : True,
            (False, None) : None,
            (None, True) : None,
            (None, False) : None,
            (None, None) : None }

    _lt = { (True, True) : False,
            (True, False) : False,
            (True, None) : False,
            (False, True) : True,
            (False, False) : False,
            (False, None) : None,
            (None, True) : None,
            (None, False) : False,
            (None, None) : None }

__title__ = 'tribool'
__version__ = '0.0.5'
__build__ = 0x000005
__author__ = 'Grant Jenks'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2012 Grant Jenks'
