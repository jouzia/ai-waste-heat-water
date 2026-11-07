"""Controlled sensible-cp versus Wyon-enthalpy DCMD channel sweep.

This is a model-form sensitivity experiment, not a literature benchmark.
Both modes use identical geometry, transport inputs, boundary conditions,
salinity, mesh, and solver tolerances; only the bulk-stream energy update
changes.
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

FEED_TEMPERATURES_C = (40.0, 50.0, 60.0, 70.0)
FEED_SALINITIES_SR_G_KG = (15.0, 35.0, 38.0)
PERMEATE_IN_TEMPERATURE_C = 20.0
DURATION_H = 1.0
CELLS = 20

# A fixed, explicit numerical scenario adapted from the repository's
# counter-current grid-test scale. It is not represented as Wyon Table 6 data.
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
    "cells": CELLS,
    "flow_arrangement": "counter_current",
}

MODES = ("sensible_cp", "wyon_enthalpy")
OUTPUT_METRICS = (
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


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _global_wyon_enthalpy_residual_w(result, feed_temperature_c: float,
                                      feed_salinity_g_kg: float) -> float:
    """Post-hoc common-datum stream enthalpy residual, in W."""
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


def _solve(feed_temperature_c: float, salinity: float, mode: str):
    config = ChannelConfig(
        **FIXED_CONFIG,
        feed_salinity_g_kg=salinity,
        energy_balance_mode=mode,
    )
    return simulate_countercurrent_dcmd_channel(
        config=config,
        feed_in_temperature_c=feed_temperature_c,
        permeate_in_temperature_c=PERMEATE_IN_TEMPERATURE_C,
    )


def _relative_change_pct(value: float, reference: float) -> float | str:
    if reference == 0:
        return ""
    return (value / reference - 1.0) * 100.0


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []

    for feed_temperature_c in FEED_TEMPERATURES_C:
        for salinity in FEED_SALINITIES_SR_G_KG:
            results = {
                mode: _solve(feed_temperature_c, salinity, mode)
                for mode in MODES
            }
            row: dict[str, object] = {
                "case_id": f"T{int(feed_temperature_c)}_S{int(salinity)}",
                "feed_in_temperature_c": feed_temperature_c,
                "permeate_in_temperature_c": PERMEATE_IN_TEMPERATURE_C,
                "feed_reference_salinity_g_kg": salinity,
                "duration_h": DURATION_H,
                "cells": CELLS,
            }
            for mode, result in results.items():
                for metric in OUTPUT_METRICS:
                    row[f"{mode}_{metric}"] = getattr(result, metric)
                row[f"{mode}_global_wyon_enthalpy_residual_w"] = (
                    _global_wyon_enthalpy_residual_w(
                        result, feed_temperature_c, salinity
                    )
                )
                cell_residuals = [
                    abs(cell.combined_enthalpy_balance_residual_w)
                    for cell in result.cells
                    if cell.combined_enthalpy_balance_residual_w is not None
                ]
                row[f"{mode}_max_abs_combined_cell_residual_w"] = (
                    max(cell_residuals) if cell_residuals else ""
                )
                row[f"{mode}_max_abs_feed_cell_residual_w"] = max(
                    (abs(cell.feed_enthalpy_balance_residual_w)
                     for cell in result.cells
                     if cell.feed_enthalpy_balance_residual_w is not None),
                    default="",
                )
                row[f"{mode}_max_abs_permeate_cell_residual_w"] = max(
                    (abs(cell.permeate_enthalpy_balance_residual_w)
                     for cell in result.cells
                     if cell.permeate_enthalpy_balance_residual_w is not None),
                    default="",
                )

            for metric in OUTPUT_METRICS:
                sensible = getattr(results["sensible_cp"], metric)
                enthalpy = getattr(results["wyon_enthalpy"], metric)
                row[f"wyon_minus_sensible_{metric}_delta"] = enthalpy - sensible
                row[f"wyon_vs_sensible_{metric}_change_pct"] = (
                    "" if metric in {"feed_out_temperature_c", "permeate_out_temperature_c"}
                    else _relative_change_pct(enthalpy, sensible)
                )
            rows.append(row)

    # Refuse to publish incomplete or non-finite comparisons.
    for row in rows:
        for key, value in row.items():
            if isinstance(value, float) and not math.isfinite(value):
                raise RuntimeError(f"non-finite result in {row['case_id']}:{key}")
    if len(rows) != len(FEED_TEMPERATURES_C) * len(FEED_SALINITIES_SR_G_KG):
        raise RuntimeError("temperature-salinity matrix is incomplete")

    csv_path = output_dir / "sensible_vs_wyon_enthalpy_sweep.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    manifest: dict[str, object] = {
        "experiment_id": "SENSIBLE-VS-WYON-ENTHALPY-COUNTERCURRENT-2026-11-07",
        "row_count": len(rows),
        "feed_temperatures_c": list(FEED_TEMPERATURES_C),
        "feed_reference_salinity_g_kg": list(FEED_SALINITIES_SR_G_KG),
        "permeate_in_temperature_c": PERMEATE_IN_TEMPERATURE_C,
        "fixed_config": FIXED_CONFIG,
        "comparison": {
            "baseline": "sensible_cp: existing constant-cp bulk-stream update",
            "alternative": "wyon_enthalpy: opt-in mass-weighted Wyon Appendix A stream enthalpy update",
            "changed_dimension": "energy_balance_mode only",
            "solver": "separate counter-current finite-volume solver",
        },
        "diagnostics": {
            "global_wyon_enthalpy_residual_w": (
                "Post-hoc common-datum Wyon enthalpy-flow residual for both modes; "
                "a diagnostic comparison, not an independent experimental error."
            ),
            "cell_residuals": (
                "Algebraic residuals emitted by the Wyon enthalpy mode; blank for "
                "the sensible-cp baseline."
            ),
        },
        "limitations": [
            "The fixed scenario is an explicit numerical sensitivity case, not a reproduction of Wyon Table 6 or an experimental benchmark.",
            "The Wyon mode applies the Wyon Eq. (18) net-stream-enthalpy convention cellwise; this sweep does not validate that convention against independent axial measurements.",
            "Only the bulk-stream energy update changes; the local membrane interface closure, latent-heat input, transport coefficients, mesh, and boundary conditions are held fixed.",
            "The post-hoc global Wyon enthalpy residual is a model-form diagnostic and must not be described as experimental validation.",
        ],
        "files": {csv_path.name: _sha256(csv_path)},
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/sensible_vs_wyon_enthalpy_sweep"),
    )
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
