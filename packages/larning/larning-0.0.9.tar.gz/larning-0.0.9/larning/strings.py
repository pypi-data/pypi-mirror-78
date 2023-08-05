from larning.strings_i import *
from typing import Callable
from pprint import pformat


def func_to_str(func: Callable, *args, **kwargs):
    indent = 1
    width = 80
    depth = 13
    sep = ", "
    args = [to_str(arg) for arg in args]
    kwargs = [key + "=" + to_str(value) for key, value in kwargs.items()]
    return func.__name__ + "({})".format(concatenate_with_separation(args + kwargs, sep))
