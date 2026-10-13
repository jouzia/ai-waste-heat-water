"""Run an unfitted source-trace check on Ali et al. (2020) measured inputs."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import median

import numpy as np

from ai_water.ali_dynamic_model import (
    PUBLISHED_FLOS_LUMPED,
    AliDynamicConfig,
    simulate_lumped_transient,
)


def read_trace(path: Path, workbook: str, worksheet: str) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = [
            row
            for row in csv.DictReader(stream)
            if row["workbook_filename"] == workbook
            and row["worksheet_name"] == worksheet
            and row["row_status"] == "complete_time_series_row"
        ]
    rows.sort(key=lambda row: float(row["time_min"]))
    if len(rows) < 3:
        raise ValueError(f"Expected at least 3 complete observations, got {len(rows)}")
    times = [float(row["time_min"]) for row in rows]
    if np.any(np.diff(times) <= 0):
        raise ValueError("Source trace time values must be strictly increasing")
    return rows


def error_metrics(predicted: np.ndarray, observed: np.ndarray) -> dict[str, float]:
    residual = predicted - observed
    return {
        "mae": float(np.mean(np.abs(residual))),
        "rmse": float(np.sqrt(np.mean(residual**2))),
        "bias": float(np.mean(residual)),
    }


def run_case(
    rows: list[dict[str, str]],
    *,
    correction: float,
    case_id: str,
) -> dict[str, object]:
    time_min = np.asarray([float(row["time_min"]) for row in rows])
    hot_in = np.asarray([float(row["hot_inlet_temperature_c"]) for row in rows])
    cold_in = np.asarray([float(row["cold_inlet_temperature_c"]) for row in rows])
    hot_out_observed = np.asarray([float(row["hot_outlet_temperature_c"]) for row in rows])
    cold_out_observed = np.asarray([float(row["cold_outlet_temperature_c"]) for row in rows])
    mass_observed = np.asarray(
        [float(row["cumulative_distillate_mass_kg"]) for row in rows]
    )
    first = rows[0]
    flow = float(first["nominal_flow_l_h"])
    result: dict[str, object] = {
        "case_id": case_id,
        "status": "not_run",
        "heat_loss_correction": correction,
        "rows": len(rows),
        "flow_l_h": flow,
        "target_hot_inlet_c": float(first["hot_inlet_target_c"]),
        "start_time_min": float(time_min[0]),
        "end_time_min": float(time_min[-1]),
        "median_sample_interval_s": median(np.diff(time_min).tolist()) * 60.0,
        "measured_hot_inlet_start_c": float(hot_in[0]),
        "measured_hot_inlet_end_c": float(hot_in[-1]),
        "measured_cold_inlet_min_c": float(np.min(cold_in)),
        "measured_cold_inlet_max_c": float(np.max(cold_in)),
        "measured_hot_outlet_start_c": float(hot_out_observed[0]),
        "measured_cold_outlet_start_c": float(cold_out_observed[0]),
        "measured_mass_start_kg": float(mass_observed[0]),
        "measured_mass_end_kg": float(mass_observed[-1]),
        "error": "",
        "metrics": None,
    }
    try:
        predicted = simulate_lumped_transient(
            time_min=time_min,
            hot_inlet_c=hot_in,
            cold_inlet_c=cold_in,
            nominal_flow_l_h=flow,
            heat_loss_correction=correction,
            initial_hot_outlet_c=float(hot_out_observed[0]),
            initial_cold_outlet_c=float(cold_out_observed[0]),
            initial_accumulated_mass_kg=float(mass_observed[0]),
            config=AliDynamicConfig(),
        )
        result["status"] = "completed_unfitted_comparison"
        result["metrics"] = {
            "hot_outlet_temperature_c": error_metrics(
                predicted.hot_outlet_c, hot_out_observed
            ),
            "cold_outlet_temperature_c": error_metrics(
                predicted.cold_outlet_c, cold_out_observed
            ),
            "accumulated_distillate_mass_kg": error_metrics(
                predicted.accumulated_mass_kg, mass_observed
            ),
            "predicted_mass_end_kg": float(predicted.accumulated_mass_kg[-1]),
            "predicted_mass_rate_end_kg_h": float(predicted.mass_rate_kg_h[-1]),
            "predicted_flux_end_kg_m2_h": float(predicted.membrane_flux_kg_m2_h[-1]),
        }
    except (RuntimeError, ValueError, ArithmeticError) as exc:
        result["status"] = "rejected_or_failed"
        result["error"] = f"{type(exc).__name__}: {exc}"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ledger",
        type=Path,
        default=Path("artifacts/ali_2020_exports/ali_2020_transient_observation_ledger.csv"),
    )
    parser.add_argument("--workbook", default="S2_Data.xlsx")
    parser.add_argument("--worksheet", default="50")
    parser.add_argument(
        "--output-dir", type=Path, default=Path("artifacts/ali_source_trace_validation")
    )
    args = parser.parse_args()
    rows = read_trace(args.ledger, args.workbook, args.worksheet)
    if not all(
        math.isfinite(float(row[field]))
        for row in rows
        for field in (
            "time_min",
            "hot_inlet_temperature_c",
            "hot_outlet_temperature_c",
            "cold_inlet_temperature_c",
            "cold_outlet_temperature_c",
            "cumulative_distillate_mass_kg",
        )
    ):
        raise ValueError("Selected source trace contains non-finite required values")

    flow = int(float(rows[0]["nominal_flow_l_h"]))
    cases = [
        run_case(rows, correction=0.0, case_id="unfitted_no_correction"),
        run_case(
            rows,
            correction=PUBLISHED_FLOS_LUMPED[flow],
            case_id="published_source_correction_not_refitted",
        ),
    ]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "source": {
            "citation": "Ali, Orfi & Najib (2020), PLOS ONE 15(3):e0230207",
            "doi": "10.1371/journal.pone.0230207",
            "license": "CC BY 4.0",
            "workbook": args.workbook,
            "worksheet": args.worksheet,
            "trace_rows": len(rows),
            "input_ledger": str(args.ledger),
            "initial_outlets_from_measurement": True,
            "measured_input_histories_used": True,
        },
        "purpose": "Unfitted source-reconstruction diagnostic, not independent validation",
        "cases": cases,
        "interpretation_rules": [
            "Do not tune parameters on this trace and report it as held-out validation.",
            "The published heat-loss correction is a separate source-reproduction case, not a newly estimated physical heat-loss coefficient.",
            "Any physical-admissibility rejection is a failed model case, not a missing result.",
            "The source trace includes warm-up; measured input and initial outlet temperatures are used rather than an artificial instantaneous 60 C step.",
        ],
    }
    json_path = args.output_dir / "ali_source_trace_validation.json"
    json_path.write_text(json.dumps(report, indent=2, allow_nan=False), encoding="utf-8")
    csv_path = args.output_dir / "ali_source_trace_validation_cases.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["case_id", "status", "heat_loss_correction", "rows", "error", "metrics"],
        )
        writer.writeheader()
        for case in cases:
            writer.writerow(
                {
                    **{key: case.get(key) for key in writer.fieldnames if key not in {"error", "metrics"}},
                    "error": case["error"],
                    "metrics": json.dumps(case["metrics"], allow_nan=False),
                }
            )
    for case in cases:
        print(
            f"{case['case_id']}: {case['status']}; "
            f"error={case['error']}; metrics={json.dumps(case['metrics'], allow_nan=False)}"
        )


if __name__ == "__main__":
    main()
