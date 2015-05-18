# -*- coding: utf-8 -*-

import nose
from nose.tools import raises

from context import tribool
from tribool import Tribool

def test_init():
    """Test initializer values for Tribool."""
    for value in (True, False, None):
        assert Tribool(value)._value == value
        assert Tribool(Tribool(value))._value == value

@raises(ValueError)
def test_init_raises():
    """Test intializer raises on bad input."""
    Tribool(0)

def test_not():
    for value in (True, False, None):
        assert (~Tribool(value))._value == Tribool._not[value]

def test_and():
    for value in (True, False, None):
        for other in (True, False, None):
            result = Tribool._and[value, other]
            assert (Tribool(value) & Tribool(other))._value == result
            assert (value & Tribool(other))._value == result
            assert (Tribool(value) & other)._value == result

def test_or():
    for value in (True, False, None):
        for other in (True, False, None):
            result = Tribool._or[value, other]
            assert (Tribool(value) | Tribool(other))._value == result
            assert (value | Tribool(other))._value == result
            assert (Tribool(value) | other)._value == result

def test_xor():
    for value in (True, False, None):
        for other in (True, False, None):
            result = Tribool._xor[value, other]
            assert (Tribool(value) ^ Tribool(other))._value == result
            assert (value ^ Tribool(other))._value == result
            assert (Tribool(value) ^ other)._value == result

def test_cmp():
    for value in (True, False, None):
        for other in (True, False, None):
            tri_value = Tribool(value)
            tri_other = Tribool(other)

            _eq = Tribool._eq[value, other]
            assert (tri_value == tri_other)._value == _eq

            _lt = Tribool._lt[value, other]
            assert (tri_value < tri_other)._value == _lt

            tri_value != tri_other
            tri_value <= tri_other
            tri_value > tri_other
            tri_value >= tri_other

@raises(ValueError)
def test_bool():
    bool(Tribool())

@raises(ValueError)
def test_int():
    int(Tribool())

@raises(ValueError)
def test_index():
    values = [0, 1, 2, 3]
    values[Tribool(True)]

def test_str():
    assert str(Tribool(True)) == 'True'
    assert str(Tribool(False)) == 'False'
    assert str(Tribool(None)) == 'Indeterminate'

def test_check():
    for value in (True, False, None):
        Tribool(value)._check()

def test_repr():
    assert repr(Tribool(True)) == 'Tribool(True)'
    assert repr(Tribool(False)) == 'Tribool(False)'
    assert repr(Tribool(None)) == 'Tribool(None)'

if __name__ == '__main__':
    nose.run()
