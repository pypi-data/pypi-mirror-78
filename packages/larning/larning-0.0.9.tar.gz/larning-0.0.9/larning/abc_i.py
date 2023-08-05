from abc import ABC, abstractmethod


def del_abstractmethod(cls: type, method_name: str):
    if "__abstractmethods__" in cls.__dict__.keys():
        setattr(
            cls, "__abstractmethods__", frozenset([i for i in cls.__dict__["__abstractmethods__"] if i != method_name]),
        )


class ContextManager(ABC):
    @abstractmethod
    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...


class Namable(ABC):
    @property
    @abstractmethod
    def name(self):
        ...

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, name: str):
        return self.name == name


class Printable(ABC):
    @abstractmethod
    def __str__(self):
        ...
