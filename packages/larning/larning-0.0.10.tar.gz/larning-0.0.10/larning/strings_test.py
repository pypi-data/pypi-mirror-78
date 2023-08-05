from larning.strings import concatenate_with_separation, func_to_str, to_str
from pydantic import ValidationError
from pytest import raises
from larning.testing import name


def test_a():
    assert concatenate_with_separation(["a", "a"], ".") == "a.a"
    assert concatenate_with_separation(["", "a"], ".") == ".a"
    assert concatenate_with_separation(["", ""], ".") == "."
    assert concatenate_with_separation(["a"], ".") == "a"
    assert concatenate_with_separation([1, 2], 2) == "122"
    assert concatenate_with_separation([1.2], 2) == "1.2"
    with raises(ValidationError):
        concatenate_with_separation("a", ".")


@name(func_to_str, 1, globals())
def _():
    class A:
        ...

    a = A()
    a.key = "value"
    s = func_to_str(func_to_str, 1, None, k="k", a={2: 3})
    assert s == "func_to_str(1, None, k='k', a={2: 3})"
    s = func_to_str(func_to_str)
    assert s == "func_to_str()"


@name(to_str, 1, globals())
def _():
    class A:
        ...

    a = A()
    a.a = 1
    a.b = "b"
    assert "A{'a': 1, 'b': 'b'}" == to_str(a)
    assert "1" == to_str(1)
    assert "'a'" == to_str("a")
    assert "[1, 'a']" == to_str([1, "a"])
    s = to_str({1, "a"})
    assert "{1, 'a'}" == s or s == "{'a', 1}"
    assert "{'k': 'v', 'k2': 'v2'}" == to_str({"k": "v", "k2": "v2"})
    assert "<lambda>" == to_str(lambda: 1)


@name(str, 1, globals())
def _():
    class A:
        def __str__(self):
            return 1

    a = A()
    a.__str__() == object.__str__(a)
