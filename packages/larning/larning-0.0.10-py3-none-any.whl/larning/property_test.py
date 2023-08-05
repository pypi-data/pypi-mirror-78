from larning.testing import name
from larning.property import with_property
from pytest import raises


@name(property, 1, globals())
def _():
    @with_property("first", "second", "third", "fourth", "fifth")
    class A:
        @property
        def basic_property(self):
            return self._basic_property

        @basic_property.setter
        def basic_property_(self, var):
            self._basic_property = var

        def third_getter(self):
            return 3

        def fourth_setter(self, x):
            self._fourth = 4

        def fifth_deleter(self):
            ...

    # basic
    assert type(A) == type
    assert "basic_property_" in A.__dict__.keys()
    assert type(A.__dict__["basic_property"]) == property == type(A.first)
    #
    a = A()
    assert ("first" not in a.__dict__.keys()) and (not hasattr(a, "first"))
    # first
    with raises(AttributeError):
        a.first
    with raises(AttributeError):
        getattr(a, "first")
    with raises(AttributeError):
        a.__getattribute__("first")
    a.first = 1
    assert hasattr(a, "first") and ("first" not in a.__dict__.keys())
    assert hasattr(a, "_first") and ("_first" in a.__dict__.keys())
    assert a.first == 1 == getattr(a, "first") == a.__getattribute__("first")
    assert a._first == 1 == getattr(a, "_first") == a.__getattribute__("_first") == a.__dict__["_first"]
    del a.first
    assert (not hasattr(a, "first")) and ("first" not in a.__dict__.keys())
    assert (not hasattr(a, "_first")) and ("_first" not in a.__dict__.keys())
    # second
    a.second = 1
    assert a.second == 1
    assert a._second == 1
    # third
    a.third = 1
    assert a.third == 3
    assert a._third == 1
    # fourth
    a.fourth = 1
    assert a.fourth == 4
    assert a._fourth == 4
    # fifth
    a.fifth = 1
    assert hasattr(a, "fifth") and ("fifth" not in a.__dict__.keys())
    assert hasattr(a, "_fifth") and ("_fifth" in a.__dict__.keys())
    del a.fifth
    assert hasattr(a, "fifth") and ("fifth" not in a.__dict__.keys())
    assert hasattr(a, "_fifth") and ("_fifth" in a.__dict__.keys())
