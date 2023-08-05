from larning.output.i import *
from contextlib import contextmanager

HLINE = "#" * line_length
DOWN = "ˇ" * line_length
UP = "^" * line_length


@contextmanager
def between(func=print):
    func(on_white(DOWN))
    yield
    func(on_white(UP))
