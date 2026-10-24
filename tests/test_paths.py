import pytest

from config_manager.paths import discover_configs, file_details


def test_discovery_finds_supported_files(sample_files, tmp_path):
    found = discover_configs(tmp_path)
    assert set(found) == set(sample_files.values())


def test_discovery_can_search_recursively(tmp_path):
    nested = tmp_path / "nested"
    nested.mkdir()
    (nested / "other.json").write_text('{"configs": []}', encoding="utf-8")
    assert nested / "other.json" in discover_configs(tmp_path, recursive=True)


def test_discovery_ignores_unsupported_extensions(tmp_path):
    (tmp_path / "notes.txt").write_text("hello", encoding="utf-8")
    assert discover_configs(tmp_path) == []


def test_file_details_returns_size(sample_files):
    details = file_details(sample_files["json"])
    size_bytes = details["size_bytes"]

    assert isinstance(size_bytes, int)
    assert size_bytes > 0

    assert details["path"] == sample_files["json"]


def test_file_details_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        file_details(tmp_path / "missing.json")


def test_file_details_rejects_directory(tmp_path):
    with pytest.raises(ValueError, match="Not a file"):
        file_details(tmp_path)
