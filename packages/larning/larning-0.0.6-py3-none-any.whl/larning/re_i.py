from re import sub


def to_func_name(name: str):
    return sub(r"\W", "_", name).lower()
