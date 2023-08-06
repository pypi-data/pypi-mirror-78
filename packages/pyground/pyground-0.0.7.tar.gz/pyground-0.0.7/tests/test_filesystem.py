from pathlib import Path

from pyground.filesystem import path_types


def test_path_types():
    file_path = Path(__file__)
    assert {"file"} <= set(path_types(file_path))

    dir_path = file_path.parent
    assert {"dir"} <= set(path_types(dir_path))

    root_path = Path("/")
    assert {"dir", "mount"} <= set(path_types(root_path))
