"""A simple file transaction that restores the original on failure."""

import shutil
from pathlib import Path
from types import TracebackType
from typing import Self


class ConfigTransaction:
    """Make a backup on entry and restore it if the block raises an error."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.backup_path = path.with_suffix(path.suffix + ".bak")

    def __enter__(self) -> Self:
        if not self.path.exists():
            raise FileNotFoundError(self.path)
        shutil.copy2(self.path, self.backup_path)
        return self

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ):
        if exception_type is not None:
            shutil.copy2(self.backup_path, self.path)
        return False
