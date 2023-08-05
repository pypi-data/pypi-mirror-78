from typing import Sequence
from collections.abc import Callable
from functools import singledispatch
from pydantic import validate_arguments
from pprint import pformat


@singledispatch
def to_str(obj):
    default_str = object.__str__(obj)
    actual_str = str(obj)
    return obj.__class__.__name__ + to_str(obj.__dict__) if default_str == actual_str else actual_str


@to_str.register(type(None))
@to_str.register(int)
def _(basic):
    return str(basic)


@to_str.register(str)
@to_str.register(dict)
@to_str.register(list)
@to_str.register(set)
@to_str.register(tuple)
def _(pretty):
    return pformat(pretty)


@to_str.register(Callable)
def _(func):
    return func.__name__


@validate_arguments
def concatenate_with_separation(strings: Sequence[str], separator: str) -> str:
    return "".join(s if i == 0 else separator + s for i, s in enumerate(strings))
