from termcolor import colored

line_length = 225


def red(s: str) -> str:
    return colored(s, color="red")


def green(s: str) -> str:
    return colored(s, color="green")


def blue(s: str) -> str:
    return colored(s, color="blue")


def on_white(s: str) -> str:
    return colored(s, on_color="on_white")


def var(s: str) -> str:
    return f"<@{s}@>"
