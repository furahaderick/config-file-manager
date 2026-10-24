"""Shared data types and basic schema validation."""

from typing import TypedDict


class ConfigEntry(TypedDict):
    name: str
    debug: bool
    port: int
    host: str


def validate_entry(entry: dict[str, object]) -> ConfigEntry:
    """Validate one configuration entry and return normalized values."""
    required = {"name", "debug", "port", "host"}
    missing = required - entry.keys()
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(sorted(missing))}")

    name = str(entry["name"]).strip()
    host = str(entry["host"]).strip()
    if not name:
        raise ValueError("Field 'name' cannot be empty.")
    if not host:
        raise ValueError("Field 'host' cannot be empty.")

    raw_debug = entry["debug"]
    if isinstance(raw_debug, bool):
        debug = raw_debug
    elif str(raw_debug).strip().lower() in {"true", "1", "yes"}:
        debug = True
    elif str(raw_debug).strip().lower() in {"false", "0", "no"}:
        debug = False
    else:
        raise ValueError("Field 'debug' must be true or false.")

    raw_port = entry["port"]
    if not isinstance(raw_port, (int, str)):
        raise ValueError("Field 'port' must be an integer.")

    try:
        port = int(raw_port)
    except (TypeError, ValueError) as error:
        raise ValueError("Field 'port' must be an integer.") from error

    if not 1 <= port <= 65535:
        raise ValueError("Field 'port' must be between 1 and 65535.")

    return {"name": name, "debug": debug, "port": port, "host": host}


def validate_entries(entries: list[dict[str, object]]) -> list[ConfigEntry]:
    """Validate a list of entries."""
    return [validate_entry(entry) for entry in entries]
