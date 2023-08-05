from typing import Iterable


class CollectorType(type):

    # it is a staticmethod
    def __new__(
        collectorType: type, new_cls_name: str, new_cls_bases: tuple, class_definition_dict: dict,
    ):
        new_cls = super().__new__(collectorType, new_cls_name, new_cls_bases, class_definition_dict)
        return new_cls  # __init__()

    # called before __new__ return automatically
    def __init__(new_cls: type, new_cls_name: str, new_cls_bases: tuple, new_cls_dict: dict):
        super().__init__(new_cls_name, new_cls_bases, new_cls_dict)
        new_cls._objects = set()
        original_init = new_cls.__init__

        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            new_cls._objects.add(self)

        new_cls.__init__ = new_init

    def __iter__(new_cls) -> Iterable:
        return iter(new_cls._objects)

    def clear(new_cls):
        new_cls._objects.clear()

    def __getitem__(new_cls, item):
        for i in new_cls:
            if item == i:
                return i
        raise IndexError(f"object with index ({item}) not found")

    def __len__(new_cls):
        return len(new_cls._objects)
