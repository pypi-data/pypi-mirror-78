# pylint: disable=too-few-public-methods
from textwrap import dedent

from pyground.types import Hierarchy


class A:
    pass


class B:
    pass


class C(A):
    pass


class D(C, B):
    pass


def test_hierarchy():
    hierarchy = Hierarchy.build(D)

    assert str(hierarchy) == dedent(
        """\
        test_types.D
        ├── test_types.C
        │   └── test_types.A
        └── test_types.B
        """.rstrip()
    )
