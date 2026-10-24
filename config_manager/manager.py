"""High-level operations built from the format handlers."""

from pathlib import Path

from config_manager.handlers import handler_for
from config_manager.models import ConfigEntry
from config_manager.paths import discover_configs, file_details
from config_manager.transforms import normalize_names


def read_config(path: Path) -> list[ConfigEntry]:
    return handler_for(path).read(path)


def write_config(path: Path, entries: list[ConfigEntry]) -> None:
    handler_for(path).write(path, entries)


def convert_config(source: Path, destination: Path) -> None:
    """Read one supported format and write the same data in another format."""
    entries = read_config(source)
    write_config(destination, normalize_names(entries))


def list_configs(directory: Path, recursive: bool = False) -> list[Path]:
    return discover_configs(directory, recursive)


def inspect_config_file(path: Path) -> dict[str, object]:
    return file_details(path)
