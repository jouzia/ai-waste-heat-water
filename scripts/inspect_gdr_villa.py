"""Inspect GDR Villa et al. (2018) XLS workbooks without treating sheets as observations."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

SOURCE_DOI = "10.15121/1452747"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_workbook(path: Path, xlrd_module) -> dict[str, object]:
    workbook = xlrd_module.open_workbook(str(path), on_demand=True)
    sheets = []
    for sheet in workbook.sheets():
        preview = [
            [sheet.cell_value(row, col) for col in range(min(sheet.ncols, 12))]
            for row in range(min(sheet.nrows, 6))
        ]
        sheets.append(
            {
                "name": sheet.name,
                "rows": sheet.nrows,
                "columns": sheet.ncols,
                "preview_first_rows_first_12_columns": preview,
                "interpretation": (
                    "calculated_or_mixed_values_review_required"
                    if sheet.name.strip().lower() == "theoretical"
                    else "sheet_type_not_automatically_classified"
                ),
            }
        )
    workbook.release_resources()
    return {
        "filename": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "sheets": sheets,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/raw/gdr_villa_2018"),
        help="Directory containing downloaded GDR .xls files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/provenance/gdr_villa_workbook_inspection.json"),
        help="Output JSON metadata and limited cell previews.",
    )
    args = parser.parse_args()

    try:
        import xlrd
    except ImportError:
        parser.error('Install workbook support with: python -m pip install -e ".[analysis]"')

    files = sorted(args.input_dir.glob("*.xls"))
    if not files:
        parser.error(f"No .xls files found in {args.input_dir}")

    manifest = {
        "source_doi": SOURCE_DOI,
        "inspected_at_utc": datetime.now(UTC).isoformat(),
        "files": [inspect_workbook(path, xlrd) for path in files],
        "scope_note": (
            "Metadata and limited previews only. Verify sheet type and units against "
            "the GDR source page; do not treat Theoretical-sheet calculations as raw "
            "measurements or use previews as extracted observations."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Inspected {len(files)} workbook(s): {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
