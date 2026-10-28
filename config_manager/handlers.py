"""Readers and writers for JSON, CSV, and XML configuration files."""

import csv
import json
import xml.etree.ElementTree as ET
from collections.abc import Iterator
from pathlib import Path
from typing import Protocol

from config_manager.models import ConfigEntry, validate_entries, validate_entry


class FormatHandler(Protocol):
    """Common interface that every format handler must provide."""

    def read(self, path: Path) -> list[ConfigEntry]: ...
    def write(self, path: Path, entries: list[ConfigEntry]) -> None: ...


class JsonHandler:
    def read(self, path: Path) -> list[ConfigEntry]:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, dict) or not isinstance(data.get("configs"), list):
            raise TypeError("JSON must contain a 'configs' list.")
        return validate_entries(data["configs"])

    def write(self, path: Path, entries: list[ConfigEntry]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump({"configs": entries}, file, indent=2)


class CsvHandler:
    def read_rows(self, path: Path) -> Iterator[ConfigEntry]:
        """Yield validated CSV rows one at a time."""
        with path.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            expected = {"name", "debug", "port", "host"}
            if reader.fieldnames is None or not expected.issubset(reader.fieldnames):
                raise ValueError("CSV must have name, debug, port, and host columns.")
            for row in reader:
                yield validate_entry(dict(row))

    def read(self, path: Path) -> list[ConfigEntry]:
        return list(self.read_rows(path))

    def write(self, path: Path, entries: list[ConfigEntry]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = ["name", "debug", "port", "host"]
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(entries)


class XmlHandler:
    def read_rows(self, path: Path) -> Iterator[ConfigEntry]:
        """Yield XML config entries as their end tags are encountered."""
        for _, element in ET.iterparse(path, events=("end",)):
            if element.tag != "config":
                continue
            values = {child.tag: child.text or "" for child in element}
            yield validate_entry(dict(values))
            element.clear()

    def read(self, path: Path) -> list[ConfigEntry]:
        return list(self.read_rows(path))

    def write(self, path: Path, entries: list[ConfigEntry]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        root = ET.Element("configs")
        for entry in entries:
            config = ET.SubElement(root, "config")
            for field in ("name", "debug", "port", "host"):
                child = ET.SubElement(config, field)
                child.text = (
                    str(entry[field]).lower()
                    if isinstance(entry[field], bool)
                    else str(entry[field])
                )
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(path, encoding="unicode", xml_declaration=True)


def handler_for(path: Path) -> FormatHandler:
    """Choose a handler from the file extension."""
    handlers: dict[str, FormatHandler] = {
        ".json": JsonHandler(),
        ".csv": CsvHandler(),
        ".xml": XmlHandler(),
    }
    try:
        return handlers[path.suffix.lower()]
    except KeyError as error:
        raise ValueError(f"Unsupported file format: {path.suffix}") from error
