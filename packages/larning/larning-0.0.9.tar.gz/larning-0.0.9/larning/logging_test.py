from larning.testing import name
from larning.logging import get_logger
from logging import getLogger, WARNING, DEBUG, StreamHandler, Formatter
from larning import __name__ as larning_name


@name(getLogger, 1, globals())
def _():
    l1 = getLogger("")
    l2 = getLogger("")
    l3 = getLogger("root")
    l4 = getLogger()
    l5 = getLogger("__main__")
    assert (l1 is l2 is l4) and (l2 is not l3) and (l4 is not l5)
    assert l1.name == "root" == l3.name == l4.name
    assert __name__ == "larning.logging_test"
    assert larning_name == "larning"


def basic_func():
    ...


class basic_class:
    def basic_method(self):
        ...

    @classmethod
    def basic_classmethod(cls):
        ...

    @staticmethod
    def basic_staticmethod():
        ...

    class nested_class:
        @property
        def a(self):
            ...

        @a.setter
        def a(self):
            ...


@name(get_logger, 1, globals())
def _():
    assert get_logger().name == "root"
    assert get_logger("a").name == "a"
    assert get_logger(basic_func).name == "larning.logging_test.basic_func"
    assert get_logger(basic_class).name == "larning.logging_test.basic_class"
    assert get_logger(basic_class.basic_method).name == "larning.logging_test.basic_class.basic_method"
    assert get_logger(basic_class.basic_classmethod).name == "larning.logging_test.basic_class.basic_classmethod"
    assert get_logger(basic_class.basic_staticmethod).name == "larning.logging_test.basic_class.basic_staticmethod"
    assert get_logger(basic_class.nested_class).name == "larning.logging_test.basic_class.nested_class"
    assert get_logger(basic_class.nested_class.a.fget).name == "larning.logging_test.basic_class.nested_class.a"
    assert get_logger(basic_class.nested_class.a.fset).name == "larning.logging_test.basic_class.nested_class.a"
