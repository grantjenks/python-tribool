# -*- coding: utf-8 -*-

import copy
import pickle
from math import ceil, floor

import nose
from nose.tools import raises

from .context import tribool
from tribool import Tribool

def test_init():
    """Test initializer values for Tribool."""
    for value in (True, False, None):
        assert Tribool(value).value == value
        assert Tribool(Tribool(value)).value == value

@raises(ValueError)
def test_init_raises():
    """Test intializer raises on bad input."""
    Tribool(0)

def test_not():
    for value in (True, False, None):
        assert (~Tribool(value)).value == Tribool._not[value]

def test_and():
    for value in (True, False, None):
        for other in (True, False, None):
            result = Tribool._and[value, other]
            assert (Tribool(value) & Tribool(other)).value == result
            assert (value & Tribool(other)).value == result
            assert (Tribool(value) & other).value == result

def test_or():
    for value in (True, False, None):
        for other in (True, False, None):
            result = Tribool._or[value, other]
            assert (Tribool(value) | Tribool(other)).value == result
            assert (value | Tribool(other)).value == result
            assert (Tribool(value) | other).value == result

def test_xor():
    for value in (True, False, None):
        for other in (True, False, None):
            result = Tribool._xor[value, other]
            assert (Tribool(value) ^ Tribool(other)).value == result
            assert (value ^ Tribool(other)).value == result
            assert (Tribool(value) ^ other).value == result

def test_cmp():
    for value in (True, False, None):
        for other in (True, False, None):
            tri_value = Tribool(value)
            tri_other = Tribool(other)

            _eq = Tribool._eq[value, other]
            assert (tri_value == tri_other).value == _eq

            _lt = Tribool._lt[value, other]
            assert (tri_value < tri_other).value == _lt

            tri_value != tri_other
            tri_value <= tri_other
            tri_value > tri_other
            tri_value >= tri_other

@raises(TypeError)
def test_bool():
    bool(Tribool())

def test_names():
    Yes, No, Maybe = map(Tribool, (True, False, None))
    assert Yes is Tribool('True')
    assert No is Tribool('False')
    assert Maybe is Tribool('None')
    assert Maybe is Tribool('Indeterminate')
    assert Maybe is Tribool('Maybe')
    assert Maybe is Tribool('Unknown')

def test_hash():
    Yes, No, Maybe = map(Tribool, (True, False, None))
    assert all(hash(value) for value in (Yes, No, Maybe))
    values = {Yes: 'Yes', No: 'No', Maybe: 'Maybe'}
    assert values[Yes] == 'Yes'
    assert values[No] == 'No'
    assert values[Maybe] == 'Maybe'

def test_is():
    Yes1, No1, Maybe1 = map(Tribool, (True, False, None))
    Yes2, No2, Maybe2 = map(Tribool, (True, False, None))
    assert Yes1 is Yes2
    assert No1 is No2
    assert Maybe1 is Maybe2

def test_id():
    Yes1, No1, Maybe1 = map(Tribool, (True, False, None))
    Yes2, No2, Maybe2 = map(Tribool, (True, False, None))
    assert id(Yes1) == id(Yes2)
    assert id(No1) == id(No2)
    assert id(Maybe1) == id(Maybe2)

@raises(TypeError)
def test_in():
    Yes, No, Maybe = map(Tribool, (True, False, None))
    assert Yes in (Yes, No, Maybe)
    No in (Yes, No, Maybe)

def test_contains():
    values = (Yes, No, Maybe) = list(map(Tribool, (True, False, None)))
    assert any(value is Tribool(True) for value in values)
    assert any(value is Tribool(False) for value in values)
    assert any(value is Tribool(None) for value in values)

def test_copy():
    Yes, No, Maybe = map(Tribool, (True, False, None))
    Yes_dup, No_dup, Maybe_dup = map(Tribool, (True, False, None))

    assert Yes is Yes_dup
    assert No is No_dup
    assert Maybe is Maybe_dup

    Yes_copy, No_copy, Maybe_copy = map(copy.copy, (Yes, No, Maybe))

    assert Yes is Yes_copy
    assert No is No_copy
    assert Maybe is Maybe_copy

    Yes_deep, No_deep, Maybe_deep = map(copy.deepcopy, (Yes, No, Maybe))

    assert Yes is Yes_deep
    assert No is No_deep
    assert Maybe is Maybe_deep

def test_pickle():
    Yes, No, Maybe = map(Tribool, (True, False, None))

    pickler = lambda value: pickle.loads(pickle.dumps(value))

    Yes_pickle, No_pickle, Maybe_pickle = map(pickler, (Yes, No, Maybe))

    assert Yes is Yes_pickle
    assert No is No_pickle
    assert Maybe is Maybe_pickle

def test_str():
    assert str(Tribool(True)) == 'True'
    assert str(Tribool(False)) == 'False'
    assert str(Tribool(None)) == 'Indeterminate'

def test_repr():
    assert repr(Tribool(True)) == 'Tribool(True)'
    assert repr(Tribool(False)) == 'Tribool(False)'
    assert repr(Tribool(None)) == 'Tribool(None)'

def test_check():
    for value in (True, False, None):
        Tribool(value)._check()

def test_ceil():
    Yes, No, Maybe = map(Tribool, (True, False, None))

    assert ceil(Yes)
    assert ceil(Maybe)
    assert not ceil(No)

def test_floor():
    Yes, No, Maybe = map(Tribool, (True, False, None))

    assert floor(Yes)
    assert not floor(Maybe)
    assert not floor(No)

if __name__ == '__main__':
    nose.run()
