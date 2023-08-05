from larning.testing import name
from collections.abc import Iterable as abc_Iterable
from collections.abc import Iterator as abc_Iterator
from larning.abc import Printable
from pytest import raises


@name(Printable, 0, globals())
def _():
    class A(Printable):
        ...

    assert "__str__" in A.__dict__["__abstractmethods__"]

    class B(A):
        ...

    with raises(TypeError):
        B()


@name(abc_Iterable, 0, globals())
def _():
    class A(abc_Iterable):
        ...

    assert "__iter__" in A.__dict__["__abstractmethods__"]
    assert "__next__" not in A.__dict__["__abstractmethods__"]


@name(abc_Iterator, 0, globals())
def _():
    class A(abc_Iterator):
        ...

    assert "__iter__" not in A.__dict__["__abstractmethods__"]
    assert "__next__" in A.__dict__["__abstractmethods__"]
