from pydantic import validate_arguments
from typing import Callable
from larning.abc import del_abstractmethod


@validate_arguments
def with_property(*property_names: str) -> Callable:
    def decorator(cls: type) -> type:
        for property_name in property_names:
            get_name, set_name, del_name, val_name = (
                property_name + "_getter",
                property_name + "_setter",
                property_name + "_deleter",
                "_" + property_name,
            )
            fget = cls.__dict__[get_name] if get_name in cls.__dict__.keys() else (lambda val_name: lambda self: getattr(self, val_name))(val_name)
            fset = cls.__dict__[set_name] if set_name in cls.__dict__.keys() else (lambda val_name: lambda self, x: setattr(self, val_name, x))(val_name)
            fdel = cls.__dict__[del_name] if del_name in cls.__dict__.keys() else (lambda val_name: lambda self: delattr(self, val_name))(val_name)
            setattr(cls, property_name, property(fget, fset, fdel))
            del_abstractmethod(cls, property_name)
        return cls

    return decorator
