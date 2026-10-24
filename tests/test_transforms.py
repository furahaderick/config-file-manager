from config_manager.models import ConfigEntry
from config_manager.transforms import normalize_names, valid_entries


def test_normalize_names_strips_whitespace(sample_entries: list[ConfigEntry]) -> None:
    entries: list[ConfigEntry] = [
        {**sample_entries[0], "name": " dev ", "host": " localhost "}
    ]

    result = normalize_names(entries)

    assert result[0]["name"] == "dev"
    assert result[0]["host"] == "localhost"


def test_normalize_names_keeps_other_values(sample_entries):
    assert normalize_names(sample_entries)[0]["port"] == 8000


def test_valid_entries_keeps_valid_values(sample_entries):
    assert valid_entries(sample_entries) == sample_entries


def test_valid_entries_skips_invalid_values():
    rows = [
        {"name": "dev", "debug": True, "port": 8000, "host": "localhost"},
        {"name": "", "debug": True, "port": 8000, "host": "localhost"},
    ]
    assert len(valid_entries(rows)) == 1


def test_valid_entries_returns_empty_for_all_invalid():
    assert not valid_entries([{"name": ""}])
