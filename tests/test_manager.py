import pytest

from config_manager.manager import convert_config, read_config, write_config
from config_manager.transaction import ConfigTransaction


def test_read_config_uses_extension(sample_files, sample_entries):
    assert read_config(sample_files["json"]) == sample_entries


def test_write_config_creates_destination_parent(tmp_path, sample_entries):
    destination = tmp_path / "new" / "settings.json"
    write_config(destination, sample_entries)
    assert destination.exists()


def test_convert_json_to_csv(sample_files, tmp_path, sample_entries):
    destination = tmp_path / "converted.csv"
    convert_config(sample_files["json"], destination)
    from config_manager.manager import read_config

    assert read_config(destination) == sample_entries


def test_convert_csv_to_xml(sample_files, tmp_path, sample_entries):
    destination = tmp_path / "converted.xml"
    convert_config(sample_files["csv"], destination)
    assert read_config(destination) == sample_entries


def test_transaction_restores_original_after_error(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("original", encoding="utf-8")
    with pytest.raises(RuntimeError), ConfigTransaction(path):
        path.write_text("changed", encoding="utf-8")
        raise RuntimeError("simulate failure")
    assert path.read_text(encoding="utf-8") == "original"
    assert path.with_suffix(".json.bak").exists()


def test_transaction_keeps_changes_on_success(tmp_path):
    path = tmp_path / "config.json"
    path.write_text("original", encoding="utf-8")
    with ConfigTransaction(path):
        path.write_text("changed", encoding="utf-8")
    assert path.read_text(encoding="utf-8") == "changed"
