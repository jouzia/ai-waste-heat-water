"""Quantify spatial-grid and ODE-tolerance convergence on an unfitted Ali DCMD trace.

This checks numerical convergence only. It does not tune the model, resolve the
source workbook's raw mw semantics, or establish empirical validation.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ai_water.ali_dynamic_model import AliDynamicConfig, simulate_spatial_transient


def load_trace(path: Path, workbook: str, worksheet: str) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = [
            row for row in csv.DictReader(stream)
            if row["workbook_filename"] == workbook
            and row["worksheet_name"] == worksheet
            and row["row_status"] == "complete_time_series_row"
        ]
    rows.sort(key=lambda row: float(row["time_min"]))
    if len(rows) < 3:
        raise ValueError(f"Expected at least 3 complete rows; got {len(rows)}")
    times = np.asarray([float(row["time_min"]) for row in rows])
    if np.any(np.diff(times) <= 0):
        raise ValueError("Source trace times must be strictly increasing")
    return rows


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def error_metrics(values: np.ndarray) -> dict[str, float]:
    return {
        "mae": float(np.mean(np.abs(values))),
        "rmse": float(np.sqrt(np.mean(values**2))),
        "max_abs": float(np.max(np.abs(values))),
    }


def run(output_dir: Path, ledger: Path, workbook: str, worksheet: str) -> dict[str, object]:
    rows = load_trace(ledger, workbook, worksheet)
    time_min = np.asarray([float(row["time_min"]) for row in rows])
    hot_in = np.asarray([float(row["hot_inlet_temperature_c"]) for row in rows])
    cold_in = np.asarray([float(row["cold_inlet_temperature_c"]) for row in rows])
    hot_obs = np.asarray([float(row["hot_outlet_temperature_c"]) for row in rows])
    cold_obs = np.asarray([float(row["cold_outlet_temperature_c"]) for row in rows])
    flow = float(rows[0]["nominal_flow_l_h"])
    common = {
        "time_min": time_min,
        "hot_inlet_c": hot_in,
        "cold_inlet_c": cold_in,
        "nominal_flow_l_h": flow,
        "heat_loss_correction": 0.0,
        "initial_hot_outlet_c": float(hot_obs[0]),
        "initial_cold_outlet_c": float(cold_obs[0]),
        "initial_accumulated_mass_kg": 0.0,
    }
    # Grid refinement and ODE tolerance are varied independently enough to
    # reveal gross numerical instability without fitting to measured outputs.
    design = [
        (5, 1e-4),
        (10, 1e-4),
        (20, 1e-4),
        (10, 1e-6),
        (20, 1e-6),
    ]
    records: list[dict[str, object]] = []
    predictions: dict[tuple[int, float], object] = {}
    for n_cells, rtol in design:
        config = AliDynamicConfig(
            relative_tolerance=rtol,
            absolute_tolerance_temperature_k=rtol,
        )
        result = simulate_spatial_transient(
            **common,
            n_cells=n_cells,
            config=config,
        )
        if not result.solver_success:
            raise RuntimeError(
                f"Solver failed for n_cells={n_cells}, rtol={rtol}: "
                f"{result.solver_message}"
            )
        predictions[(n_cells, rtol)] = result
        records.append(
            {
                "n_cells": n_cells,
                "relative_tolerance": rtol,
                "absolute_temperature_tolerance_k": rtol,
                "rows": len(time_min),
                "hot_outlet_vs_measurement": json.dumps(
                    error_metrics(result.hot_outlet_c - hot_obs), sort_keys=True
                ),
                "cold_outlet_vs_measurement": json.dumps(
                    error_metrics(result.cold_outlet_c - cold_obs), sort_keys=True
                ),
                "minimum_hot_outlet_c": float(np.min(result.hot_outlet_c)),
                "minimum_cold_outlet_c": float(np.min(result.cold_outlet_c)),
                "minimum_mass_rate_kg_h": float(np.min(result.mass_rate_kg_h)),
                "mass_rate_nonnegative": bool(np.all(result.mass_rate_kg_h >= -1e-9)),
                "accumulated_mass_monotonic": bool(
                    np.all(np.diff(result.accumulated_mass_kg) >= -1e-9)
                ),
                "predicted_mass_end_kg_model_output_only": float(
                    result.accumulated_mass_kg[-1]
                ),
            }
        )

    reference = predictions[(20, 1e-6)]
    convergence: list[dict[str, object]] = []
    for (n_cells, rtol), result in predictions.items():
        convergence.append(
            {
                "n_cells": n_cells,
                "relative_tolerance": rtol,
                "reference_n_cells": 20,
                "reference_relative_tolerance": 1e-6,
                "hot_outlet_difference_from_reference_c": json.dumps(
                    error_metrics(result.hot_outlet_c - reference.hot_outlet_c),
                    sort_keys=True,
                ),
                "cold_outlet_difference_from_reference_c": json.dumps(
                    error_metrics(result.cold_outlet_c - reference.cold_outlet_c),
                    sort_keys=True,
                ),
                "mass_rate_difference_from_reference_kg_h": json.dumps(
                    error_metrics(result.mass_rate_kg_h - reference.mass_rate_kg_h),
                    sort_keys=True,
                ),
                "accumulated_mass_difference_from_reference_kg_model_only": json.dumps(
                    error_metrics(result.accumulated_mass_kg - reference.accumulated_mass_kg),
                    sort_keys=True,
                ),
            }
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    for name, data in (
        ("ali_spatial_grid_tolerance_metrics.csv", records),
        ("ali_spatial_grid_tolerance_convergence.csv", convergence),
    ):
        with (output_dir / name).open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)

    summary: dict[str, object] = {
        "source": {
            "citation": "Ali, Orfi & Najib (2020), PLOS ONE 15(3):e0230207",
            "doi": "10.1371/journal.pone.0230207",
            "workbook": workbook,
            "worksheet": worksheet,
            "rows": len(rows),
            "flow_l_h": flow,
            "source_ledger_sha256": sha256_file(ledger),
        },
        "purpose": "numerical grid/tolerance convergence only; not fitted or validated",
        "design": [
            {"n_cells": n, "relative_tolerance": tol, "absolute_temperature_tolerance_k": tol}
            for n, tol in design
        ],
        "reference": {"n_cells": 20, "relative_tolerance": 1e-6},
        "results": records,
        "convergence": convergence,
        "interpretation_limits": [
            "Measured outputs are used only for residual reporting, not parameter fitting.",
            "The raw mw field is excluded from comparisons because its cumulative-mass semantics remain unverified.",
            "Predicted accumulated mass is a model output only, not an observed mass comparison.",
            "A numerical convergence result does not establish source reconstruction, empirical validation, or net-water benefit.",
        ],
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "python_version": platform.python_version(),
    }
    (output_dir / "ali_spatial_grid_tolerance_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "source_ledger_sha256": sha256_file(ledger),
        "outputs": {
            name: sha256_file(output_dir / name)
            for name in (
                "ali_spatial_grid_tolerance_metrics.csv",
                "ali_spatial_grid_tolerance_convergence.csv",
                "ali_spatial_grid_tolerance_summary.json",
            )
        },
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return summary


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
        "--output-dir",
        type=Path,
        default=Path("artifacts/ali_spatial_convergence"),
    )
    args = parser.parse_args()
    summary = run(args.output_dir, args.ledger, args.workbook, args.worksheet)
    print(
        f"Completed {len(summary['results'])} grid/tolerance cases over "
        f"{summary['source']['rows']} measured temperature rows."
    )


if __name__ == "__main__":
    main()
