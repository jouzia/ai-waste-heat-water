"""Extract reproducible observations from the registered open MD datasets.

This utility never invents observations. It requires locally downloaded source
workbooks, records SHA-256 hashes, inventories sheets, and writes a manifest
before any researcher-selected extraction is performed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory_workbook(path: Path) -> dict:
    sheets = pd.ExcelFile(path, engine="xlrd").sheet_names
    return {
        "path": str(path),
        "filename": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "sheets": sheets,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    files = sorted(
        p for p in args.input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in {".xls", ".xlsx"}
    )
    if not files:
        raise SystemExit("No Excel workbooks found; extraction cannot proceed.")

    records = []
    for path in files:
        records.append(inventory_workbook(path))

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
