from pathlib import Path
from typing import Iterator, List
import logging
import os
import plistlib

from xattr import xattr

from filesystemlib import walk

from .json import marshall
from .time import parse_timestamp  # also for marshall dispatch


PATH_PREDICATES = [
    ("absolute", Path.is_absolute),
    ("block_device", Path.is_block_device),
    ("char_device", Path.is_char_device),
    ("dir", Path.is_dir),
    ("fifo", Path.is_fifo),
    ("file", Path.is_file),
    ("mount", Path.is_mount),
    ("reserved", Path.is_reserved),
    ("socket", Path.is_socket),
    ("symlink", Path.is_symlink),
]


def path_types(path: Path) -> Iterator[str]:
    for name, predicate in PATH_PREDICATES:
        if predicate(path):
            yield name


COLOR_MAPPING = [
    "None",  # 0
    "Gray",  # 1
    "Green",  # 2
    "Purple",  # 3
    "Blue",  # 4
    "Yellow",  # 5
    "Red",  # 6
    "Orange",  # 7
]
FINDER_INFO = "com.apple.FinderInfo"
METADATA_ITEM_USER_TAGS = "com.apple.metadata:_kMDItemUserTags"


def read_tags(path: Path) -> Iterator[str]:
    """
    Read color names and/or other tags from a file's extended attributes.
    """
    attrs = xattr(path)
    if METADATA_ITEM_USER_TAGS in attrs:
        metadata_item_user_tags: bytes = attrs.get(METADATA_ITEM_USER_TAGS)
        for item in plistlib.loads(metadata_item_user_tags):
            if "\n" in item:
                color, _number = item.split("\n")
                # assert COLOR_MAPPING[int(_number)] == color
                yield color
            else:
                yield item
    # FINDER_INFO only supports a single color, and seems to be whatever (color) tag was
    # most recently set (unless tags were added to a file with a pre-Mavericks tag?)
    if FINDER_INFO in attrs:
        finder_info: bytes = attrs.get(FINDER_INFO)
        # color resides in 10th byte
        color_byte = finder_info[9]
        # select bits 2 through 4 (where rightmost is bit 1) by
        # first dropping the lowest bit then ANDing with 0b111 (= 7)
        color_value = (color_byte >> 1) & 7
        yield COLOR_MAPPING[color_value]


@marshall.register
def marshall_stat_result(sr: os.stat_result, **options) -> dict:
    return marshall(
        {
            "mode": f"{sr.st_mode:o}",  # TODO: truncate?
            "ino": sr.st_ino,
            "dev": sr.st_dev,
            # "nlink": sr.st_nlink,
            "uid": sr.st_uid,  # TODO: convert to name?
            "gid": sr.st_gid,  # TODO: convert to name?
            "size": sr.st_size,
            "atime": parse_timestamp(sr.st_atime),
            "mtime": parse_timestamp(sr.st_mtime),
            "ctime": parse_timestamp(sr.st_ctime),
            "btime": parse_timestamp(sr.st_birthtime),
        },
        **options,
    )


@marshall.register
def marshall_path(path: Path, *, root: Path = None, **options) -> dict:
    return marshall(
        {
            "path": str(path.relative_to(root) if root else path),
            "type": "|".join(sorted(set(path_types(path)) - {"absolute"})),
            "stat": path.stat(),
        },
        **options,
    )


if __name__ == "__main__":
    # Use like:
    #   python -m pyground.filesystem /path/to/a /path/to/b
    import shutil
    import sys

    import click

    from . import jsonl

    @click.command()
    @click.argument("roots", type=click.Path(exists=True), nargs=-1)
    @click.option("-v", "--verbose", count=True, help="Increase logging verbosity.")
    @click.option("--relative", is_flag=True, help="Use relative paths.")
    @click.option("--sort", is_flag=True, help="Sort by filename within directories.")
    def main(
        roots: List[str] = (),
        verbose: int = 0,
        relative: bool = False,
        sort: bool = False,
    ):
        """
        Recurse filesystem starting at each ROOT, serializing nodes into JSON.

        Every node has these fields:
          path: string (POSIX path)
          type: string (|-separated list of types like "dir", "file", "mount")
          stat: object (stat results, with timestamps in ISO-8601)

        Additionally, the node for each ROOT has these fields:
          root: boolean (always true)
          disk_total_bytes: number (total bytes on the disk containing ROOT)
          disk_used_bytes: number (used bytes)
          disk_free_bytes: number (available bytes)
        (note that used + free ≠ total if there are blocks that are free,
        but not available to unprivileged processes)
        """
        logging_level = logging.INFO - (verbose * 10)
        logging_format = "%(asctime)14s %(levelname)-7s %(name)s - %(message)s"
        logging.basicConfig(format=logging_format, level=logging_level)
        logging.debug(
            "Set logging level to %s [%d]",
            logging.getLevelName(logging_level),
            logging_level,
        )
        logger = logging.getLogger("pyground-filesystem")
        logger.debug("Listing files in %d roots", len(roots))

        sortkey = lambda path: path.as_posix().casefold() if sort else None

        for root in roots:
            root = Path(root)
            if not relative:
                root = root.resolve()
            logger.debug("Descending into %s", root)
            marshall_root = root if relative else None
            nodes: Iterator[dict] = (
                marshall(path, root=marshall_root, timespec="seconds")
                for path in walk(root, sortkey=sortkey)
            )
            # peel off the first node, which is the root
            root_node = next(nodes)
            # update root node with capacity and usage
            usage = shutil.disk_usage(root)
            root_node.update(
                root=True,
                disk_total_bytes=usage.total,
                disk_used_bytes=usage.used,
                disk_free_bytes=usage.free,
            )
            jsonl.dump([root_node], sys.stdout)
            # continue with the rest of the nodes as-is
            jsonl.dump(nodes, sys.stdout)

    main()
