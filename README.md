# Configuration File Manager

A Configuration File Manager for JSON, CSV, and XML formats.

## Requirements

- Python 3.12
- Poetry

## Setup

```bash
poetry install
poetry run pytest
```

## Folder structure

```text
config-file-manager/
├── config_manager/
│   ├── __init__.py
│   ├── cli.py
│   ├── handlers.py
│   ├── manager.py
│   ├── models.py
│   ├── paths.py
│   ├── transforms.py
│   └── transaction.py
├── examples/
│   ├── config.json
│   ├── config.csv
│   └── config.xml
├── tests/
│   ├── conftest.py
│   ├── test_handlers.py
│   ├── test_manager.py
│   ├── test_models.py
│   ├── test_paths.py
│   └── test_transforms.py
├── pyproject.toml
└── README.md
```

## Format support matrix

| Operation | JSON | CSV | XML |
|---|---:|---:|---:|
| Read | Yes | Yes | Yes |
| Write | Yes | Yes | Yes |
| Convert to/from another format | Yes | Yes | Yes |
| Incremental entry reader | No | Yes | Yes |

## Schema

Every configuration entry has four fields:

- `name`: non-empty string
- `debug`: boolean (`true` or `false`)
- `port`: integer from 1 through 65535
- `host`: non-empty string

JSON wraps entries in a top-level `configs` list. CSV stores one entry per row with a header. XML stores one entry in each `<config>` element.

## Examples

Convert JSON to CSV:

```bash
poetry run python -m config_manager.cli convert examples/config.json output/config.csv
```

Convert CSV to XML:

```bash
poetry run python -m config_manager.cli convert examples/config.csv output/config.xml
```

Print a config file:

```bash
poetry run python -m config_manager.cli show examples/config.json
```

Find config files in a directory:

```bash
poetry run python -m config_manager.cli list examples
poetry run python -m config_manager.cli list . --recursive
```

## Important design decisions

1. `Path` objects are used for filesystem paths.
2. Every format reads into the same list of dictionaries, validated as `ConfigEntry` values.
3. `FormatHandler` is a `Protocol`, so each handler has the same `read` and `write` methods without needing a shared base class.
4. CSV and XML provide generator methods (`read_rows`) that yield one validated entry at a time. The convenience `read` method loads the yielded entries into a list when the full result is needed.
5. `ConfigTransaction` creates a `.bak` backup and restores it if an exception escapes the `with` block. This is a simple learning example, not a fully crash-safe transaction.
6. `map` and `filter` demonstrate functional transformations without introducing a large abstraction.

## Memory comparison report

The CSV and XML `read_rows()` methods yield one entry at a time, so a caller can process entries without storing the complete result list. The normal `read()` method returns a list and therefore uses memory proportional to the number of entries.

For a simple comparison, create a large test file and compare peak memory with `tracemalloc`:

```python
import tracemalloc
from pathlib import Path
from config_manager.handlers import CsvHandler

path = Path("large.csv")

tracemalloc.start()
for entry in CsvHandler().read_rows(path):
    # Process each entry without keeping it in a list.
    pass
_, generator_peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

tracemalloc.start()
entries = CsvHandler().read(path)
_, list_peak = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("Generator peak bytes:", generator_peak)
print("List peak bytes:", list_peak)
```

No fixed memory numbers are claimed here because results depend on the file, Python build, and environment. The generator should generally use less memory when entries are processed and discarded one at a time.
