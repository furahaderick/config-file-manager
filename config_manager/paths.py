"""Path utilities and configuration-file discovery."""

from pathlib import Path

SUPPORTED_SUFFIXES = {".json", ".csv", ".xml"}


def discover_configs(directory: Path, recursive: bool = False) -> list[Path]:
    """Find supported config files in a directory."""
    pattern = "**/*" if recursive else "*"
    return sorted(
        path
        for path in directory.glob(pattern)
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def file_details(path: Path) -> dict[str, object]:
    """Return basic file information after checking that the file exists."""
    if not path.exists():
        raise FileNotFoundError(path)
    if not path.is_file():
        raise ValueError(f"Not a file: {path}")
    stat = path.stat()
    return {
        "path": path,
        "size_bytes": stat.st_size,
        "modified_time": stat.st_mtime,
        "readable": path.stat().st_mode & 0o444 != 0,
        "writable": path.stat().st_mode & 0o222 != 0,
    }
