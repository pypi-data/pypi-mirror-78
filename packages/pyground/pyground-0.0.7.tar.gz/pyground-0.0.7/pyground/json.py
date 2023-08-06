"""
This module primarily defines a singledispatch function, `marshall`, and several
implementations for Python's primitive data structures that operate recursively.

It's named "marshall" rather than "serialize" because at this stage it's not yet
converting the data structure to a byte stream, but only from complex data structures
to more primitive types.

dict -> dict, marshalling keys and values
list -> list, marshalling each item
tuple -> tuple, marshalling each item
set -> list, sorting and marshalling each item
frozenset -> tuple, sorting and marshalling each item
"""
from functools import singledispatch
from typing import Any


@singledispatch
def marshall(value: Any, **options) -> Any:
    """
    Convert `value` into a JSON-friendly structure.
    """
    return value


@marshall.register
def marshall_dict(mapping: dict, **options) -> dict:
    return {
        marshall(key, **options): marshall(value, **options)
        for key, value in mapping.items()
    }


@marshall.register
def marshall_list(items: list, **options) -> list:
    return [marshall(item, **options) for item in items]


@marshall.register
def marshall_tuple(items: tuple, **options) -> tuple:
    return tuple(marshall(item, **options) for item in items)


@marshall.register
def marshall_set(items: set, **options) -> list:
    return [marshall(item, **options) for item in sorted(items)]


@marshall.register
def marshall_frozenset(items: frozenset, **options) -> tuple:
    return tuple(marshall(item, **options) for item in sorted(items))
