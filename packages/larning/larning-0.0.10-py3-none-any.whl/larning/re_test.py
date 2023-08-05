from re import sub
from larning.testing import name
from larning.re import to_func_name


@name(sub, 1, globals())
def _():
    assert sub(r"[ab]", "f", "acb") == "fcf"
    assert sub(r"\W", "f", "a..c__b--") == "affc__bff"


@name(to_func_name, 1, globals())
def _():
    assert to_func_name("a_1") == "a_1"
    assert to_func_name("A.-?*:;1 2") == "a______1_2"
