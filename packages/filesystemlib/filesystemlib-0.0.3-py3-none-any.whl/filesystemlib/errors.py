from errno import ENOENT, EEXIST
import os

from .internal import Pathable


def file_not_found(path: Pathable) -> FileNotFoundError:
    "Create proper FileNotFoundError instance"
    return FileNotFoundError(ENOENT, os.strerror(ENOENT), os.fspath(path))


def file_exists(path: Pathable) -> FileExistsError:
    "Create proper FileExistsError instance"
    return FileExistsError(EEXIST, os.strerror(EEXIST), os.fspath(path))
