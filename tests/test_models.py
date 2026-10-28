import pytest

from config_manager.models import validate_entries, validate_entry


def test_valid_entry(sample_entries):
    assert validate_entry(sample_entries[0]) == sample_entries[0]


def test_debug_string_is_converted_to_boolean():
    entry = {"name": "dev", "debug": "false", "port": "8000", "host": "localhost"}
    result = validate_entry(dict(entry))
    assert result["debug"] is False
    assert result["port"] == 8000


def test_missing_field_is_rejected():
    with pytest.raises(ValueError, match="Missing required fields"):
        validate_entry({"name": "dev"})


def test_invalid_port_is_rejected():
    with pytest.raises(ValueError, match="integer"):
        validate_entry(
            {"name": "dev", "debug": True, "port": "abc", "host": "localhost"}
        )


def test_port_out_of_range_is_rejected():
    with pytest.raises(ValueError, match="between"):
        validate_entry(
            {"name": "dev", "debug": True, "port": 70000, "host": "localhost"}
        )


def test_empty_name_is_rejected():
    with pytest.raises(ValueError, match="name"):
        validate_entry({"name": " ", "debug": True, "port": 80, "host": "localhost"})


def test_validate_entries_handles_multiple_rows(sample_entries):
    assert validate_entries(sample_entries) == sample_entries
