import pytest
from pathlib import Path

from config_manager.models import ConfigEntry


@pytest.fixture
def sample_entries() -> list[ConfigEntry]:
    return [
        {"name": "development", "debug": True, "port": 8000, "host": "127.0.0.1"},
        {"name": "production", "debug": False, "port": 443, "host": "example.com"},
    ]


@pytest.fixture
def sample_files(tmp_path: Path) -> dict[str, Path]:
    from config_manager.handlers import CsvHandler, JsonHandler, XmlHandler

    entries: list[ConfigEntry] = [
        {
            "name": "development",
            "debug": True,
            "port": 8000,
            "host": "127.0.0.1",
        },
        {
            "name": "production",
            "debug": False,
            "port": 443,
            "host": "example.com",
        },
    ]
    paths = {
        "json": tmp_path / "config.json",
        "csv": tmp_path / "config.csv",
        "xml": tmp_path / "config.xml",
    }
    JsonHandler().write(paths["json"], entries)
    CsvHandler().write(paths["csv"], entries)
    XmlHandler().write(paths["xml"], entries)
    return paths
