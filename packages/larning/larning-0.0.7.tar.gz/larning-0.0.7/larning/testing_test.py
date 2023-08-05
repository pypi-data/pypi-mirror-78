from larning.testing import name, input_manager, argv_manager
from pydantic import ValidationError
from pytest import raises
from sys import argv

# name TESTˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇˇ
def basic_func():
    return 0


@name(basic_func, "1", globals())
def a_test_with_bad_name():
    return 1


@name(basic_func, "2", globals())
def _():
    return 2


@name(basic_func, "3", globals())
def _():
    return 3


class basic_class:
    def basic_method(self):
        ...

    @classmethod
    def basic_classmethod(cls):
        ...

    @staticmethod
    def basic_staticmethod():
        ...

    @property
    def basic_property(self):
        ...

    @basic_property.setter
    def basic_property(self):
        ...


@name(basic_class, "0", globals())
def _basic_class():
    ...


@name(basic_class.basic_method, "0", globals())
def _basic_method():
    ...


@name(basic_class.basic_classmethod, "0", globals())
def _basic_classmethod():
    ...


@name(basic_class.basic_staticmethod, "0", globals())
def _basic_staticmethod():
    ...


@name(basic_class.basic_property.fget, "0", globals())
def _basic_property_fget():
    ...


@name(basic_class.basic_property.fset, "1", globals())
def _basic_property_fset():
    ...


AAAAAAAAAAAAAAaa = 1
g = globals()
aaaaaaaaaa = 1
#####################################################################################################################
def test_name():
    assert basic_func() == 0
    assert a_test_with_bad_name() == 1
    assert _() == 3
    assert globals()["basic_func"]() == 0
    assert globals()["a_test_with_bad_name"]() == 1
    assert globals()["_"]() == 3
    assert globals()["test_basic_func_1"]() == 1
    assert globals()["test_basic_func_2"]() == 2
    assert globals()["test_basic_func_3"]() == 3
    assert a_test_with_bad_name.__name__ == "test_basic_func_1"
    assert _.__name__ == "test_basic_func_3"
    assert globals()["test_basic_func_1"] is globals()["a_test_with_bad_name"]
    assert globals()["test_basic_func_2"] is not globals()["_"]
    assert globals()["test_basic_func_3"] is globals()["_"]
    assert globals()["test_basic_class_0"] is globals()["_basic_class"]
    assert globals()["test_basic_class_basic_method_0"] is globals()["_basic_method"]
    assert globals()["test_basic_class_basic_classmethod_0"] is globals()["_basic_classmethod"]
    assert globals()["test_basic_class_basic_staticmethod_0"] is globals()["_basic_staticmethod"]
    assert globals()["_basic_property_fget"] is not globals()["_basic_property_fset"]
    assert globals()["_basic_property_fset"] is globals()["test_basic_class_basic_property_1"]
    with raises(ValidationError):
        name(basic_class.basic_property, "0", globals())(basic_func)
    with raises(NameError):
        name(basic_class, "1", globals())(basic_func)
        name(basic_class, "1", globals())(basic_func)


# name TEST^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def test_input_manager():
    with input_manager("a"):
        assert input() == "a"


def test_argv_manager():
    o = list(argv)
    with argv_manager("a", "b"):
        assert argv == ["a", "b"]
    assert argv == o
