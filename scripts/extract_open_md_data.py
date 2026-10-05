"""Extract reproducible observations from the registered open MD datasets.

This utility never invents observations. It requires locally downloaded source
workbooks, records SHA-256 hashes, inventories sheets, and writes a manifest
before any researcher-selected extraction is performed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _xlsx_sheet_names(path: Path) -> list[str]:
    """Read worksheet names from an XLSX package without loading cell data."""
    with zipfile.ZipFile(path) as archive:
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    namespace = {"main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    return [
        sheet.attrib["name"]
        for sheet in workbook.findall("main:sheets/main:sheet", namespace)
    ]


def inventory_workbook(path: Path) -> dict:
    suffix = path.suffix.lower()
    if suffix == ".xlsx":
        sheets = _xlsx_sheet_names(path)
        inventory_status = "sheet_names_extracted"
    else:
        # Legacy XLS parsing is intentionally deferred to the analysis environment
        # where xlrd is installed; never report unknown sheets as extracted.
        sheets = []
        inventory_status = "legacy_xls_sheet_inventory_deferred"
    return {
        "path": str(path),
        "filename": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "format": suffix.lstrip("."),
        "inventory_status": inventory_status,
        "sheets": sheets,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    files = sorted(
        p
        for p in args.input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in {".xls", ".xlsx"}
    )
    if not files:
        raise SystemExit("No Excel workbooks found; extraction cannot proceed.")

    records = [inventory_workbook(path) for path in files]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "purpose": "source-file inventory before observation extraction",
                "files": records,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Inventoried {len(records)} workbook(s): {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
