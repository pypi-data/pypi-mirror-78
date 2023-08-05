from pydantic import validate_arguments
from typing import Union, Callable
from larning.strings import concatenate_with_separation
from larning.testing_i import *
from larning.re import to_func_name


@validate_arguments
def name(tested: Callable, name: str, globals: dict):
    def decorator(func):
        new_name = to_func_name(concatenate_with_separation(["test", tested.__qualname__, name], separator="_"))
        if new_name in globals.keys():
            raise NameError("GIVE UNIQUE NAME FOR THE TEST")
        func.__name__ = new_name
        globals[new_name] = func
        return func

    return decorator
