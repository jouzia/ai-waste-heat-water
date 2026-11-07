"""Mesh-convergence study for paired DCMD bulk-stream energy-balance modes.

The study changes only the finite-volume cell count. It is a numerical
resolution assessment, not an experimental benchmark or validation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

from ai_water.md_channel import ChannelConfig
from ai_water.md_channel_countercurrent import simulate_countercurrent_dcmd_channel
from ai_water.wyon_2025_enthalpy import wyon_specific_enthalpy_j_kg

CELL_COUNTS = (10, 20, 40, 80)
CASES = (
    {"case_id": "T60_S35", "feed_temperature_c": 60.0, "salinity_g_kg": 35.0},
    {"case_id": "T70_S38", "feed_temperature_c": 70.0, "salinity_g_kg": 38.0},
)
PERMEATE_IN_TEMPERATURE_C = 20.0
DURATION_H = 1.0
MODES = ("sensible_cp", "wyon_enthalpy")
METRICS = (
    "feed_out_temperature_c",
    "permeate_out_temperature_c",
    "freshwater_produced_kg",
    "feed_out_mass_kg_h",
    "permeate_out_mass_kg_h",
    "concentrate_salinity_g_kg",
    "hot_side_thermal_demand_kwh_th",
    "latent_duty_kwh_th",
    "conductive_heat_leak_kwh_th",
)
TEMPERATURE_METRICS = {"feed_out_temperature_c", "permeate_out_temperature_c"}

FIXED_CONFIG = {
    "membrane_area_m2": 0.23088,
    "membrane_permeance_kg_m2_h_bar": 100.0,
    "latent_heat_kwh_th_per_kg": 0.67,
    "membrane_thermal_conductivity_w_m_k": 0.0551,
    "membrane_thickness_m": 110e-6,
    "feed_heat_transfer_coefficient_w_m2_k": 500.0,
    "permeate_heat_transfer_coefficient_w_m2_k": 500.0,
    "feed_mass_flow_kg_h": 600.0,
    "permeate_mass_flow_kg_h": 600.0,
    "feed_cp_kj_kg_k": 4.18,
    "permeate_cp_kj_kg_k": 4.18,
    "duration_h": DURATION_H,
    "flow_arrangement": "counter_current",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _global_wyon_enthalpy_residual_w(result, feed_temperature_c: float,
                                      feed_salinity_g_kg: float) -> float:
    inlet = (
        FIXED_CONFIG["feed_mass_flow_kg_h"]
        * wyon_specific_enthalpy_j_kg(feed_temperature_c, feed_salinity_g_kg)
        + FIXED_CONFIG["permeate_mass_flow_kg_h"]
        * wyon_specific_enthalpy_j_kg(PERMEATE_IN_TEMPERATURE_C, 0.0)
    )
    outlet = (
        result.feed_out_mass_kg_h
        * wyon_specific_enthalpy_j_kg(
            result.feed_out_temperature_c, result.concentrate_salinity_g_kg
        )
        + result.permeate_out_mass_kg_h
        * wyon_specific_enthalpy_j_kg(result.permeate_out_temperature_c, 0.0)
    )
    return (outlet - inlet) / 3600.0


def _solve(case: dict[str, object], cells: int, mode: str):
    config = ChannelConfig(
        **FIXED_CONFIG,
        cells=cells,
        feed_salinity_g_kg=float(case["salinity_g_kg"]),
        energy_balance_mode=mode,
    )
    return simulate_countercurrent_dcmd_channel(
        config=config,
        feed_in_temperature_c=float(case["feed_temperature_c"]),
        permeate_in_temperature_c=PERMEATE_IN_TEMPERATURE_C,
    )


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    results_by_key = {}
    rows: list[dict[str, object]] = []

    for case in CASES:
        for mode in MODES:
            for cells in CELL_COUNTS:
                result = _solve(case, cells, mode)
                results_by_key[(case["case_id"], mode, cells)] = result
                row: dict[str, object] = {
                    "case_id": case["case_id"],
                    "feed_in_temperature_c": case["feed_temperature_c"],
                    "permeate_in_temperature_c": PERMEATE_IN_TEMPERATURE_C,
                    "feed_reference_salinity_g_kg": case["salinity_g_kg"],
                    "energy_balance_mode": mode,
                    "cells": cells,
                    "duration_h": DURATION_H,
                }
                for metric in METRICS:
                    row[metric] = getattr(result, metric)
                row["global_wyon_enthalpy_residual_w"] = (
                    _global_wyon_enthalpy_residual_w(
                        result, float(case["feed_temperature_c"]),
                        float(case["salinity_g_kg"])
                    )
                )
                cell_residuals = [
                    abs(cell.combined_enthalpy_balance_residual_w)
                    for cell in result.cells
                    if cell.combined_enthalpy_balance_residual_w is not None
                ]
                row["max_abs_combined_cell_residual_w"] = (
                    max(cell_residuals) if cell_residuals else ""
                )
                rows.append(row)

    # Compare every mesh to the 80-cell result for the same case and mode.
    for row in rows:
        reference = results_by_key[(row["case_id"], row["energy_balance_mode"], 80)]
        for metric in METRICS:
            value = float(row[metric])
            reference_value = float(getattr(reference, metric))
            row[f"{metric}_delta_vs_80"] = value - reference_value
            row[f"{metric}_relative_delta_vs_80_pct"] = (
                "" if metric in TEMPERATURE_METRICS or reference_value == 0
                else (value / reference_value - 1.0) * 100.0
            )

    for row in rows:
        for key, value in row.items():
            if isinstance(value, float) and not math.isfinite(value):
                raise RuntimeError(f"non-finite result in {row['case_id']}:{key}")
    expected_rows = len(CASES) * len(MODES) * len(CELL_COUNTS)
    if len(rows) != expected_rows:
        raise RuntimeError(f"expected {expected_rows} rows, got {len(rows)}")

    csv_path = output_dir / "enthalpy_mesh_convergence.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    # Summarize the 10/20/40-cell deviations from the 80-cell reference.
    summary = []
    for case in CASES:
        for mode in MODES:
            reference = results_by_key[(case["case_id"], mode, 80)]
            for cells in CELL_COUNTS[:-1]:
                result = results_by_key[(case["case_id"], mode, cells)]
                item = {
                    "case_id": case["case_id"],
                    "energy_balance_mode": mode,
                    "cells": cells,
                    "reference_cells": 80,
                }
                for metric in METRICS:
                    delta = float(getattr(result, metric)) - float(getattr(reference, metric))
                    item[f"{metric}_absolute_delta_vs_80"] = delta
                    item[f"{metric}_relative_delta_vs_80_pct"] = (
                        "" if metric in TEMPERATURE_METRICS
                        or float(getattr(reference, metric)) == 0
                        else delta / float(getattr(reference, metric)) * 100.0
                    )
                summary.append(item)

    summary_path = output_dir / "mesh_convergence_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "experiment_id": "DCMD-ENTHALPY-MESH-CONVERGENCE-2026-11-07",
        "row_count": len(rows),
        "cell_counts": list(CELL_COUNTS),
        "cases": list(CASES),
        "modes": list(MODES),
        "permeate_in_temperature_c": PERMEATE_IN_TEMPERATURE_C,
        "fixed_config": FIXED_CONFIG,
        "reference_mesh_cells": 80,
        "comparison": "Each 10/20/40-cell solution is compared with the 80-cell solution for the same operating point and energy-balance mode.",
        "limitations": [
            "The 80-cell result is a finest-mesh reference, not an exact solution or experimentally validated truth.",
            "This study assesses spatial discretization sensitivity only; it does not validate constitutive correlations, heat-transfer coefficients, membrane parameters, or the Wyon enthalpy convention.",
            "The same fixed physical inputs and boundary conditions are used at every mesh; only the number of finite-volume cells changes.",
            "Temperature errors are reported as absolute degrees Celsius only; percentages of Celsius temperatures are omitted.",
            "The post-hoc Wyon enthalpy residual is a model-form diagnostic, not independent experimental error.",
        ],
        "files": {
            csv_path.name: _sha256(csv_path),
            summary_path.name: _sha256(summary_path),
        },
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir", type=Path,
        default=Path("artifacts/enthalpy_mesh_convergence"),
    )
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
