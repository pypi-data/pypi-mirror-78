from typing import Callable, Collection, Iterator, TypeVar
from operator import attrgetter

TREE_BRANCH_SPACER = "├── ", "│   "
TREE_BRANCH_SPACER_LAST = "└── ", "    "

Node = TypeVar("Node")


def render_tree(
    node: Node,
    valuegetter: Callable[[Node], str],
    childrengetter: Callable[[Node], Collection[Node]],
) -> Iterator[str]:
    yield valuegetter(node)
    children = childrengetter(node)
    last_i = len(children) - 1
    for i, child in enumerate(children):
        # for the last child, branch and spacer are different
        branch, spacer = TREE_BRANCH_SPACER_LAST if i == last_i else TREE_BRANCH_SPACER
        # prepend branch to the first child line, and spacer to any further lines
        head, *tail = render_tree(child, valuegetter, childrengetter)
        yield branch + head
        for line in tail:
            yield spacer + line


def tree(
    node: Node,
    valuegetter: Callable[[Node], str] = attrgetter("value"),
    childrengetter: Callable[[Node], Collection[Node]] = attrgetter("children"),
) -> str:
    """
    Format tree structure using box drawing characters, like tree(1).
    """
    return "\n".join(render_tree(node, valuegetter, childrengetter))
