from larning.metaclass import CollectorType
from larning.testing import name


@name(CollectorType.__init__, 1, globals())
def _():
    class A(metaclass=CollectorType):
        A = 1

        def __init__(self, a, k=None):
            self.a, self.k = a, k

    assert A._objects == set()
    assert A.A == 1
    a = A(1, k=2)
    assert a.a == 1 and a.k == 2
    assert a._objects == {a}
    for i in A:
        assert i == a


@name(CollectorType.clear, 1, globals())
def _():
    class A(metaclass=CollectorType):
        ...

    a = A()
    b = A()
    assert A._objects == {a, b}
    A.clear()
    assert A._objects == set()
