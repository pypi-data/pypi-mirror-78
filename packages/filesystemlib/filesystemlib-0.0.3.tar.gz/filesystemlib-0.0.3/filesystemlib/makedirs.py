import logging
import os

from .internal import DRY_RUN_PREFIX, Pathable

logger = logging.getLogger(__name__)


def makedirs(path: Pathable, mode: int = 0o777, *, dry_run: bool = False) -> Pathable:
    """
    Make directory at `path` if it doesn't already exist, including any missing parent
    directories.
    """
    if os.path.exists(path) and os.path.isdir(path):
        return path
    logger.info(
        "%sMaking directory %r", DRY_RUN_PREFIX if dry_run else "", os.fspath(path)
    )
    if not dry_run:
        os.makedirs(path, mode=mode)
    return path
