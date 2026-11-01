"""Audit nonmonotonicity in source-labelled Ali et al. (2020) mw series.

This is a measurement-quality diagnostic, not a semantic inference. It preserves
source units and row locators and never rewrites raw mass values as cumulative
distillate mass. A nonmonotonic series may reflect measurement noise, reset
behavior, or another source-specific convention; the script does not decide which.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections.abc import Sequence
from datetime import UTC, datetime
from itertools import pairwise
from pathlib import Path

SOURCE_DOI = "10.1371/journal.pone.0230207"


def finite_float(value: object) -> float | None:
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def summarize_series(values: Sequence[float]) -> dict[str, object]:
    """Summarize signed steps without smoothing or assuming cumulative semantics."""
    if len(values) < 2:
        raise ValueError("At least two finite raw readings are required")
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Raw readings must be finite numbers")
    steps = [right - left for left, right in pairwise(values)]
    negative = [step for step in steps if step < 0.0]
    net_change = values[-1] - values[0]
    total_negative_variation = -sum(negative)
    return {
        "n_readings": len(values),
        "start_raw_reading_kg": values[0],
        "end_raw_reading_kg": values[-1],
        "minimum_raw_reading_kg": min(values),
        "maximum_raw_reading_kg": max(values),
        "net_change_raw_kg": net_change,
        "negative_step_count": len(negative),
        "negative_step_fraction": len(negative) / len(steps),
        "total_negative_variation_kg": total_negative_variation,
        "negative_variation_as_pct_of_positive_net_change": (
            100.0 * total_negative_variation / net_change if net_change > 0.0 else None
        ),
        "largest_negative_step_magnitude_kg": -min(negative) if negative else 0.0,
        "largest_drop_as_pct_of_positive_net_change": (
            100.0 * (-min(negative)) / net_change
            if negative and net_change > 0.0
            else None
        ),
        "monotonic_non_decreasing": not negative,
        "interpretation": "raw-series diagnostic only; mw semantics not inferred",
    }


def audit_workbooks(input_dir: Path, output_dir: Path) -> dict[str, object]:
    try:
        from openpyxl import load_workbook
    except ImportError as exc:
        raise RuntimeError("Install openpyxl>=3.1.2 to inspect source XLSX files") from exc

    output_dir.mkdir(parents=True, exist_ok=True)
    summaries: list[dict[str, object]] = []
    for workbook_path in sorted(input_dir.glob("S*_Data.xlsx")):
        digest = hashlib.sha256(workbook_path.read_bytes()).hexdigest()
        workbook = load_workbook(workbook_path, read_only=True, data_only=True)
        for sheet in workbook.worksheets:
            header_index = None
            header_values: tuple[object, ...] = ()
            for index, row in enumerate(sheet.iter_rows(min_row=1, max_row=min(5, sheet.max_row or 5), values_only=True)):
                if row and str(row[0]).strip().lower() == "time":
                    header_index = index
                    header_values = row
                    break
            if header_index is None:
                continue
            headers = ["" if value is None else str(value).strip().lower() for value in header_values]
            time_index = next((i for i, value in enumerate(headers) if value.startswith("time")), None)
            mass_index = next((i for i, value in enumerate(headers) if value.startswith("mw")), None)
            if time_index is None or mass_index is None:
                continue

            times: list[float] = []
            values: list[float] = []
            excel_rows: list[int] = []
            for row_index, row in enumerate(
                sheet.iter_rows(min_row=header_index + 2, values_only=True),
                start=header_index + 2,
            ):
                time_value = finite_float(row[time_index] if time_index < len(row) else None)
                mass_value = finite_float(row[mass_index] if mass_index < len(row) else None)
                if time_value is None or mass_value is None:
                    continue
                times.append(time_value)
                values.append(mass_value)
                excel_rows.append(row_index)
            if len(values) < 2:
                continue
            record = summarize_series(values)
            record.update(
                {
                    "source_doi": SOURCE_DOI,
                    "source_workbook": workbook_path.name,
                    "source_sha256": digest,
                    "worksheet": sheet.title,
                    "raw_time_header": str(header_values[time_index]),
                    "raw_mass_header": str(header_values[mass_index]),
                    "time_unit": "not inferred",
                    "first_excel_row_1based": excel_rows[0],
                    "last_excel_row_1based": excel_rows[-1],
                    "time_start_raw": times[0],
                    "time_end_raw": times[-1],
                    "time_strictly_increasing": all(
                        right > left for left, right in pairwise(times)
                    ),
                }
            )
            summaries.append(record)
        workbook.close()

    if not summaries:
        raise ValueError(f"No timed mw worksheets found in {input_dir}")

    fields = list(summaries[0])
    csv_path = output_dir / "ali_2020_mw_series_quality_audit.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summaries)

    nonmonotonic = [row for row in summaries if not row["monotonic_non_decreasing"]]
    manifest: dict[str, object] = {
        "source_doi": SOURCE_DOI,
        "source_url": "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230207",
        "license": "CC BY 4.0",
        "audited_at_utc": datetime.now(UTC).isoformat(),
        "workbook_count": len({row["source_workbook"] for row in summaries}),
        "timed_mw_worksheet_count": len(summaries),
        "nonmonotonic_worksheet_count": len(nonmonotonic),
        "monotonic_worksheet_count": len(summaries) - len(nonmonotonic),
        "output_csv": csv_path.name,
        "output_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        "interpretation": (
            "The audit quantifies raw-series behavior only. It does not determine "
            "whether mw is cumulative collected mass, a balance reading with noise, "
            "or another measured quantity. No smoothing, isotonic correction, reset "
            "repair, unit conversion, or model comparison is performed."
        ),
        "rows": summaries,
    }
    manifest_path = output_dir / "ali_2020_mw_series_quality_audit_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=Path("data/raw/ali_2020"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/ali_2020_exports"))
    args = parser.parse_args()
    result = audit_workbooks(args.input_dir, args.output_dir)
    print(
        f"Audited {result['timed_mw_worksheet_count']} timed mw worksheets; "
        f"{result['nonmonotonic_worksheet_count']} are nonmonotonic. "
        "Raw readings remain unmodified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
