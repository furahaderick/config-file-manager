"""Small functional transformations used by the manager."""

from collections.abc import Iterable
from config_manager.models import ConfigEntry, validate_entry


def normalize_names(entries: Iterable[ConfigEntry]) -> list[ConfigEntry]:
    """Return entries with whitespace removed from names and hosts."""
    return list(
        map(
            lambda entry: {
                **entry,
                "name": entry["name"].strip(),
                "host": entry["host"].strip(),
            },
            entries,
        )
    )


def valid_entries(entries: Iterable[dict[str, object]]) -> list[ConfigEntry]:
    """Keep entries that pass validation; invalid entries are skipped."""

    def is_valid(entry: dict[str, object]) -> bool:
        try:
            validate_entry(entry)
            return True
        except (ValueError, TypeError):
            return False

    return list(map(validate_entry, filter(is_valid, entries)))
