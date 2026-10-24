import json
import pytest

from config_manager.handlers import CsvHandler, JsonHandler, XmlHandler, handler_for


def test_json_round_trip(tmp_path, sample_entries):
    path = tmp_path / "settings.json"
    JsonHandler().write(path, sample_entries)
    assert JsonHandler().read(path) == sample_entries


def test_csv_round_trip(tmp_path, sample_entries):
    path = tmp_path / "settings.csv"
    CsvHandler().write(path, sample_entries)
    assert CsvHandler().read(path) == sample_entries


def test_xml_round_trip(tmp_path, sample_entries):
    path = tmp_path / "settings.xml"
    XmlHandler().write(path, sample_entries)
    assert XmlHandler().read(path) == sample_entries


def test_json_without_configs_list_is_rejected(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"wrong": []}), encoding="utf-8")
    with pytest.raises(ValueError, match="configs"):
        JsonHandler().read(path)


def test_csv_missing_column_is_rejected(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("name,port\ndev,8000\n", encoding="utf-8")
    with pytest.raises(ValueError, match="columns"):
        CsvHandler().read(path)


def test_csv_generator_yields_entries(sample_files):
    rows = CsvHandler().read_rows(sample_files["csv"])
    assert next(rows)["name"] == "development"


def test_xml_generator_yields_entries(sample_files):
    rows = XmlHandler().read_rows(sample_files["xml"])
    assert next(rows)["port"] == 8000


def test_handler_rejects_unknown_extension(tmp_path):
    with pytest.raises(ValueError, match="Unsupported"):
        handler_for(tmp_path / "settings.txt")
