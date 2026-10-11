"""Recreate the GDR 3M condition-level flux summary from the source XLS workbook."""

from __future__ import annotations

import argparse
import csv
import hashlib
import math
from pathlib import Path


CONDITION_SHEETS = {
    f"{cold}-{hot}" for cold in (20, 30) for hot in (40, 45, 50, 55, 60, 65)
}
FIELDS = [
    "condition_id",
    "workbook_filename",
    "worksheet_name",
    "excel_first_data_row",
    "excel_last_data_row",
    "n_timepoints",
    "n_alarm_flags",
    "runtime_start_h",
    "runtime_end_h",
    "runtime_span_h",
    "distillate_volume_start_l",
    "distillate_volume_end_l",
    "distillate_volume_change_l",
    "derived_flux_l_m2_h",
    "hac_slope_se_l_m2_h",
    "hac_approx95_low_l_m2_h",
    "hac_approx95_high_l_m2_h",
    "ols_r_squared",
    "residual_rmse_l",
    "hac_lag",
    "feed_inlet_mean_c",
    "distillate_inlet_mean_c",
    "feed_outlet_mean_c",
    "distillate_outlet_mean_c",
    "theoretical_sheet_flux_crosscheck_l_m2_h",
    "difference_vs_theoretical_crosscheck_l_m2_h",
    "source_file_sha256",
]


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(float(value))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fit_volume_slope(
    times: list[float], volumes: list[float]
) -> tuple[float, float, float, float, int]:
    """Return slope, HAC SE, R², residual RMSE, and Newey-West lag."""
    n = len(times)
    if n < 4:
        raise ValueError("At least four time points are required for a slope estimate.")

    xbar = sum(times) / n
    ybar = sum(volumes) / n
    centered_x = [value - xbar for value in times]
    sxx = sum(value * value for value in centered_x)
    if sxx <= 0:
        raise ValueError("Runtime values have no variation.")

    slope = sum(
        x * (y - ybar) for x, y in zip(centered_x, volumes, strict=True)
    ) / sxx
    intercept = ybar - slope * xbar
    residuals = [
        y - (intercept + slope * x)
        for x, y in zip(times, volumes, strict=True)
    ]
    sse = sum(value * value for value in residuals)
    sst = sum((value - ybar) ** 2 for value in volumes)
    r_squared = 1.0 - sse / sst if sst > 0 else 1.0
    rmse = math.sqrt(sse / n)

    lag = max(1, math.floor(4 * (n / 100.0) ** (2.0 / 9.0)))
    lag = min(lag, n - 2)
    hac_numerator = sum(
        centered_x[i] ** 2 * residuals[i] ** 2 for i in range(n)
    )
    for offset in range(1, lag + 1):
        bartlett_weight = 1.0 - offset / (lag + 1)
        autocovariance = sum(
            centered_x[i]
            * centered_x[i - offset]
            * residuals[i]
            * residuals[i - offset]
            for i in range(offset, n)
        )
        hac_numerator += 2.0 * bartlett_weight * autocovariance
    variance = max(0.0, hac_numerator / (sxx * sxx))
    return slope, math.sqrt(variance), r_squared, rmse, lag


def extract_summary(input_path: Path, output_path: Path) -> list[dict[str, object]]:
    try:
        import xlrd
    except ImportError as exc:
        raise RuntimeError(
            'Install legacy XLS support with: python -m pip install "xlrd>=2.0.1"'
        ) from exc

    workbook = xlrd.open_workbook(str(input_path), on_demand=True)
    if "Specifications" not in workbook.sheet_names() or "Theoretical" not in workbook.sheet_names():
        raise ValueError("Workbook is missing the audited Specifications/Theoretical sheets.")

    specs = workbook.sheet_by_name("Specifications")
    area_m2 = None
    for row in range(specs.nrows):
        if str(specs.cell_value(row, 0)).strip().lower() == "membrane surface area":
            area_value = specs.cell_value(row, 1)
            if is_number(area_value) and str(specs.cell_value(row, 2)).strip() == "m^2":
                area_m2 = float(area_value)
                break
    if area_m2 is None or area_m2 <= 0:
        raise ValueError("Could not read a positive membrane area from Specifications.")

    theoretical = workbook.sheet_by_name("Theoretical")
    summary_fluxes: dict[str, float] = {}
    # The worksheet repeats condition labels in later calculation blocks.
    # Restrict this cross-check to the first 12-row summary table only.
    for row in range(3, min(theoretical.nrows, 3 + len(CONDITION_SHEETS))):
        key = str(theoretical.cell_value(row, 0)).strip()
        value = theoretical.cell_value(row, 13) if theoretical.ncols > 13 else None
        if key in CONDITION_SHEETS and is_number(value):
            summary_fluxes[key] = float(value)

    file_hash = sha256_file(input_path)
    records: list[dict[str, object]] = []
    for sheet in workbook.sheets():
        condition = sheet.name.strip()
        if condition not in CONDITION_SHEETS:
            continue
        expected_headers = {
            2: "Runtime (hr)",
            6: "MD Distillate Volume [L]",
            21: "MD Feed Temperature (MD,I) [C]",
            22: "MD Distillate Temperature (MD,I) [C]",
            23: "MD Feed Temperature (MD,O) [C]",
            24: "MD Distillate Temperature (MD,O) [C]",
        }
        for column, expected in expected_headers.items():
            actual = str(sheet.cell_value(2, column)).strip()
            if actual != expected:
                raise ValueError(
                    f"{condition}: column {column + 1} expected {expected!r}, got {actual!r}"
                )

        rows: list[tuple[int, float, float, float, list[float]]] = []
        started = False
        for row in range(3, sheet.nrows):
            runtime = sheet.cell_value(row, 2)
            volume = sheet.cell_value(row, 6)
            if not (is_number(runtime) and is_number(volume)):
                if started:
                    break
                continue
            started = True
            alarm = sheet.cell_value(row, 4)
            temperatures = [
                float(sheet.cell_value(row, column))
                if is_number(sheet.cell_value(row, column))
                else math.nan
                for column in (21, 22, 23, 24)
            ]
            rows.append(
                (
                    row + 1,
                    float(runtime),
                    float(volume),
                    float(alarm) if is_number(alarm) else 0.0,
                    temperatures,
                )
            )

        if len(rows) < 4:
            raise ValueError(f"{condition}: fewer than four time-series rows found.")

        excel_rows = [item[0] for item in rows]
        times = [item[1] for item in rows]
        volumes = [item[2] for item in rows]
        alarms = [item[3] for item in rows]
        slope, slope_se, r_squared, rmse, lag = fit_volume_slope(times, volumes)
        flux = slope / area_m2
        flux_se = slope_se / area_m2
        temperature_means = []
        for index in range(4):
            values = [item[4][index] for item in rows if math.isfinite(item[4][index])]
            temperature_means.append(sum(values) / len(values) if values else math.nan)

        theoretical_flux = summary_fluxes.get(condition, math.nan)
        records.append(
            {
                "condition_id": condition,
                "workbook_filename": input_path.name,
                "worksheet_name": condition,
                "excel_first_data_row": min(excel_rows),
                "excel_last_data_row": max(excel_rows),
                "n_timepoints": len(rows),
                "n_alarm_flags": sum(value != 0 for value in alarms),
                "runtime_start_h": round(times[0], 6),
                "runtime_end_h": round(times[-1], 6),
                "runtime_span_h": round(times[-1] - times[0], 6),
                "distillate_volume_start_l": round(volumes[0], 6),
                "distillate_volume_end_l": round(volumes[-1], 6),
                "distillate_volume_change_l": round(volumes[-1] - volumes[0], 6),
                "derived_flux_l_m2_h": round(flux, 8),
                "hac_slope_se_l_m2_h": round(flux_se, 8),
                "hac_approx95_low_l_m2_h": round(flux - 1.96 * flux_se, 8),
                "hac_approx95_high_l_m2_h": round(flux + 1.96 * flux_se, 8),
                "ols_r_squared": round(r_squared, 8),
                "residual_rmse_l": round(rmse, 8),
                "hac_lag": lag,
                "feed_inlet_mean_c": round(temperature_means[0], 6),
                "distillate_inlet_mean_c": round(temperature_means[1], 6),
                "feed_outlet_mean_c": round(temperature_means[2], 6),
                "distillate_outlet_mean_c": round(temperature_means[3], 6),
                "theoretical_sheet_flux_crosscheck_l_m2_h": round(theoretical_flux, 8),
                "difference_vs_theoretical_crosscheck_l_m2_h": round(flux - theoretical_flux, 8),
                "source_file_sha256": file_hash,
            }
        )

    workbook.release_resources()
    records.sort(key=lambda record: str(record["condition_id"]))
    if {record["condition_id"] for record in records} != CONDITION_SHEETS:
        missing = sorted(CONDITION_SHEETS - {str(record["condition_id"]) for record in records})
        raise ValueError(f"Missing condition sheets: {missing}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/gdr_villa_2018/3M 0.2 Micron Plate and Frame Countercurrent DCMD.xls"),
        help="Downloaded source workbook.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("04_experiments/literature_benchmarks/MD-OEDI-VILLA-2018_3M_flux_summary.csv"),
        help="Output condition-level flux summary CSV.",
    )
    args = parser.parse_args()
    try:
        records = extract_summary(args.input, args.output)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.error(str(exc))
    print(f"Wrote {len(records)} condition summaries to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
