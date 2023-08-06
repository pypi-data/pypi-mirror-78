from typing import Collection
from dataclasses import dataclass
from textwrap import dedent

from pyground.ascii import tree


@dataclass
class Node:
    value: str
    children: Collection["Node"] = ()


def test_tree():
    node = Node("root", [Node("a", [Node("b"), Node("c")]), Node("d")])

    assert tree(node) == dedent(
        """\
        root
        ├── a
        │   ├── b
        │   └── c
        └── d
        """.rstrip()
    )
