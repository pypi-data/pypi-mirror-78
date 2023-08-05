from logging import getLogger, DEBUG, StreamHandler, Formatter, FileHandler
from functools import partial
from os.path import realpath, abspath, dirname
from os import getcwd
from typing import Union, Callable, Type


def get_logger(obj: Union[str, type, Callable,] = None):
    if isinstance(obj, str) or obj is None:
        return getLogger(obj)
    return getLogger(obj.__module__ + "." + obj.__qualname__)


def get_logger_func(
    func: str, name: str,
):
    return getattr(getLogger(name), func)


get_debug, get_info, get_warning, get_error, get_critical = [
    partial(get_logger_func, funcname) for funcname in ["debug", "info", "warning", "error", "critical"]
]
