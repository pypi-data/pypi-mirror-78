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


@name(CollectorType.__init__, 2, globals())
def _():
    class A(metaclass=CollectorType):
        ...

    class B(A):
        ...

    b = B()
    assert b in B and b in A
    a = A()
    assert a not in B and a in A


@name(CollectorType.__init__, 3, globals())
def _():
    class A(metaclass=CollectorType):
        ...

    class B(A):
        def __init__(self):
            ...

    b = B()
    assert b in B and b not in A
    a = A()
    assert a not in B and a in A


@name(CollectorType.__init__, 4, globals())
def _():
    class A(metaclass=CollectorType):
        ...

    class B(A, metaclass=type):
        ...

    b = B()
    assert b in B and b in A


@name(CollectorType.__init__, 5, globals())
def _():
    class A(metaclass=CollectorType):
        ...

    class B(A, metaclass=type):
        def __init__(self):
            ...

    b = B()
    assert b in B and b not in A


@name(CollectorType.clear, 1, globals())
def _():
    class A(metaclass=CollectorType):
        ...

    a = A()
    b = A()
    assert A._objects == {a, b}
    A.clear()
    assert A._objects == set()
