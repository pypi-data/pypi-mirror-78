from contextlib import contextmanager


@contextmanager
def null_manager(*args, **kwargs):
    yield


def null_func(*args, **kwargs):
    ...
