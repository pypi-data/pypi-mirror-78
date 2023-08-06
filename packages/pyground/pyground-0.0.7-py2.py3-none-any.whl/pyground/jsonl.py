from typing import Any, Iterable, Iterator, List, Union
import json


def dump(items: Iterable[Any], fp, *, separators=(",", ":"), **kwargs):
    """
    Much like json.dump followed by writing a newline, but with two changes:
    * `indent` is forced to None
    * `separators` defaults to the more compact version, but can be overridden
    """
    for item in items:
        json.dump(item, fp, indent=None, separators=separators, **kwargs)
        fp.write("\n")


def dumps(items: Iterable[Any], *, separators=(",", ":"), **kwargs) -> str:
    return "".join(
        chunk
        for item in items
        for chunk in (
            json.dumps(item, indent=None, separators=separators, **kwargs),
            "\n",
        )
    )


def load(fp, **kwargs) -> Iterator[Any]:
    for line in fp:
        yield json.loads(line, **kwargs)


def loads(s: Union[str, bytes, bytearray], **kwargs) -> List[Any]:
    # TODO: maybe iterate over lines instead of non-lazy splitlines()
    # TODO: splitlines's "universal newlines" might be too permissive
    return [json.loads(line, **kwargs) for line in s.splitlines()]
