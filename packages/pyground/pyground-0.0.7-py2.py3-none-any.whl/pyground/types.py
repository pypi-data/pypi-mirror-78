from dataclasses import dataclass
from typing import Collection

from .ascii import tree


def astype(obj_or_cls) -> type:
    """
    If `obj_or_cls` is already a type, just return that, otherwise call type(...)
    """
    if isinstance(obj_or_cls, type):
        return obj_or_cls
    return type(obj_or_cls)


def fullname(obj_or_cls) -> str:
    """
    Coerce `obj_or_cls` to its type and return its __qualname__,
    prefixed (dot-separated) with its __module__, if available.
    """
    cls = astype(obj_or_cls)
    qualname = cls.__qualname__
    if module := cls.__module__:
        return f"{module}.{qualname}"
    return qualname


@dataclass
class Hierarchy:
    klass: type
    bases: Collection["Hierarchy"]

    @classmethod
    def build(cls, obj_or_cls):
        klass = astype(obj_or_cls)
        bases = [cls.build(base) for base in klass.__bases__ if base is not object]
        return Hierarchy(klass, bases)

    def __str__(self) -> str:
        return tree(
            self,
            lambda hierarchy: fullname(hierarchy.klass),
            lambda hierarchy: hierarchy.bases,
        )
