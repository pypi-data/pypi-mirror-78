from larning.testing import name
from pytest import raises


@name(iter, 0, globals())
def _():
    assert iter([0]).__next__() == 0
    with raises(StopIteration):
        iter([]).__next__()
    a = iter([])
    assert a is a.__iter__()
