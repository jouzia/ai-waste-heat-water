"""Extract source-linked row-level observations from the GDR Villa 3M XLS workbook.

Only raw time-series measurements are exported. The Theoretical worksheet is
intentionally excluded. The output is a derived, provenance-linked ledger, not
an assertion that all sensor channels are physically valid.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SOURCE_DOI = "10.15121/1452747"
SOURCE_PAGE = "https://gdr.openei.org/submissions/1016"
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"
WORKBOOK_NAME = "3M 0.2 Micron Plate and Frame Countercurrent DCMD.xls"
EXPECTED_SOURCE_SHA256 = "5b80da45f991a8572a8a77372535cf0ba3dc40eb46a3c32c58e09e9d608dd8bb"
EXPECTED_LEDGER_ROWS = 631
CONDITION_SHEETS = tuple(
    f"{cold}-{hot}" for cold in (20, 30) for hot in (40, 45, 50, 55, 60, 65)
)
COLUMN_MAP = {
    "excel_date_serial": 0,
    "time_fraction_of_day": 1,
    "runtime_hr": 2,
    "iteration": 3,
    "alarm_flag_raw": 4,
    "feed_volume_l_raw": 5,
    "distillate_volume_l": 6,
    "feed_flowrate_high_lpm_raw": 15,
    "distillate_flowrate_high_lpm_raw": 16,
    "feed_flowrate_low_lpm_raw": 17,
    "distillate_flowrate_low_lpm_raw": 18,
    "feed_inlet_temperature_c": 21,
    "distillate_inlet_temperature_c": 22,
    "feed_outlet_temperature_c": 23,
    "distillate_outlet_temperature_c": 24,
}
OUTPUT_FIELDS = [
    "observation_id",
    "source_doi",
    "workbook_filename",
    "source_file_sha256",
    "worksheet_name",
    "excel_row_1based",
    *COLUMN_MAP.keys(),
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_source_checksum(actual_sha256: str) -> None:
    """Fail closed if the public workbook bytes differ from the audited source."""
    if actual_sha256.lower() != EXPECTED_SOURCE_SHA256:
        raise ValueError(
            "Source workbook SHA-256 changed; audit the new source version before "
            f"extracting observations (got {actual_sha256})."
        )


def _finite_number(value: Any) -> float | None:
    if isinstance(value, (int, float)) and math.isfinite(float(value)):
        return float(value)
    return None


def _raw_value(sheet: Any, row: int, column: int) -> str | float | int:
    value = sheet.cell_value(row, column)
    if isinstance(value, (int, float)):
        if math.isfinite(float(value)):
            return value
        return str(value)
    return str(value).strip()


def extract_sheet_rows(
    sheet: Any, *, workbook_filename: str, source_sha256: str
) -> list[dict[str, object]]:
    """Extract contiguous numeric runtime/cumulative-volume observations."""
    if sheet.name not in CONDITION_SHEETS:
        return []

    rows: list[dict[str, object]] = []
    started = False
    for row in range(3, sheet.nrows):
        runtime = _finite_number(sheet.cell_value(row, COLUMN_MAP["runtime_hr"]))
        volume = _finite_number(sheet.cell_value(row, COLUMN_MAP["distillate_volume_l"]))
        if runtime is None or volume is None:
            if started:
                break
            continue
        started = True
        record: dict[str, object] = {
            "observation_id": f"VILLA3M-{sheet.name}-row{row + 1}",
            "source_doi": SOURCE_DOI,
            "workbook_filename": workbook_filename,
            "source_file_sha256": source_sha256,
            "worksheet_name": sheet.name,
            "excel_row_1based": row + 1,
        }
        for field, column in COLUMN_MAP.items():
            record[field] = _raw_value(sheet, row, column)
        rows.append(record)
    return rows


def extract_ledger(
    input_path: Path, output_path: Path, manifest_path: Path
) -> dict[str, object]:
    try:
        import xlrd
    except ImportError as exc:
        raise RuntimeError(
            'Install legacy XLS support with: python -m pip install "xlrd>=2.0.1"'
        ) from exc

    workbook = xlrd.open_workbook(str(input_path), on_demand=True)
    required = {"Specifications", "Theoretical", *CONDITION_SHEETS}
    missing = sorted(required.difference(workbook.sheet_names()))
    if missing:
        raise ValueError(f"Workbook missing required sheets: {missing}")

    source_sha = sha256_file(input_path)
    validate_source_checksum(source_sha)
    records: list[dict[str, object]] = []
    counts: dict[str, int] = {}
    for sheet_name in CONDITION_SHEETS:
        sheet = workbook.sheet_by_name(sheet_name)
        sheet_records = extract_sheet_rows(
            sheet, workbook_filename=input_path.name, source_sha256=source_sha
        )
        records.extend(sheet_records)
        counts[sheet_name] = len(sheet_records)
    workbook.release_resources()

    if len(records) != EXPECTED_LEDGER_ROWS:
        raise ValueError(
            f"Expected {EXPECTED_LEDGER_ROWS} source rows for the audited workbook, "
            f"found {len(records)}."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(records)

    manifest = {
        "source_doi": SOURCE_DOI,
        "source_page": SOURCE_PAGE,
        "license": "CC BY 4.0",
        "license_url": LICENSE_URL,
        "retrieved_workbook_filename": input_path.name,
        "source_file_size_bytes": input_path.stat().st_size,
        "source_file_sha256": source_sha,
        "extracted_at_utc": datetime.now(UTC).isoformat(),
        "output_csv": output_path.name,
        "output_row_count": len(records),
        "row_count_matches_audited_source": len(records) == EXPECTED_LEDGER_ROWS,
        "source_checksum_matches_audited_version": source_sha == EXPECTED_SOURCE_SHA256,
        "row_count_by_worksheet": counts,
        "selected_worksheets": list(CONDITION_SHEETS),
        "excluded_worksheet": "Theoretical",
        "source_columns": COLUMN_MAP,
        "transformation_policy": [
            "Runtime and cumulative distillate volume must be numeric and finite.",
            "Extraction stops at the first nonnumeric runtime/volume row after the trace begins, matching the flux-summary extractor.",
            "All retained measurements remain in their source units; no unit conversion is performed.",
            "Raw non-finite/sensor values in auxiliary flow channels are preserved as text, not repaired or interpreted.",
            "Each row retains worksheet name and one-based Excel row locator.",
        ],
        "scope_warning": (
            "These are extracted workbook observations, not independently replicated "
            "measurements. Temperature and flow channels may be inconsistent; review "
            "the workbook audit before using them as model boundary conditions."
        ),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/gdr_villa_2018") / WORKBOOK_NAME,
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/gdr_villa_exports/observation_ledger.csv"),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("artifacts/gdr_villa_exports/observation_ledger_manifest.json"),
    )
    args = parser.parse_args()
    manifest = extract_ledger(args.input, args.output, args.manifest)
    print(f"Exported {manifest['output_row_count']} observations to {args.output}")
    print(f"Source SHA-256: {manifest['source_file_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
