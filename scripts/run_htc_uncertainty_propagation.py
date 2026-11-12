"""Deterministic HTC uncertainty propagation for the DCMD channel model.

The independent uniform factor grid is a scenario stress test, not an empirical
probability distribution. Each case is evaluated at 80 cells, the finest mesh
used in the completed convergence audit.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

from ai_water.md_channel import ChannelConfig
from ai_water.md_channel_countercurrent import simulate_countercurrent_dcmd_channel

TEMPERATURES_C = (40.0, 50.0, 60.0, 70.0)
SALINITIES_G_KG = (15.0, 35.0, 38.0)
FACTORS = (0.5, 0.75, 1.0, 1.25, 1.5)
MODES = ("sensible_cp", "wyon_enthalpy")
BASE_HTC_W_M2_K = 500.0
CELLS = 80
PERMEATE_IN_C = 20.0
FIXED = {
    "membrane_area_m2": 0.23088,
    "membrane_permeance_kg_m2_h_bar": 100.0,
    "latent_heat_kwh_th_per_kg": 0.67,
    "membrane_thermal_conductivity_w_m_k": 0.0551,
    "membrane_thickness_m": 110e-6,
    "feed_mass_flow_kg_h": 600.0,
    "permeate_mass_flow_kg_h": 600.0,
    "feed_cp_kj_kg_k": 4.18,
    "permeate_cp_kj_kg_k": 4.18,
    "duration_h": 1.0,
    "flow_arrangement": "counter_current",
}
OUTPUTS = (
    "feed_out_temperature_c",
    "permeate_out_temperature_c",
    "freshwater_produced_kg",
    "hot_side_thermal_demand_kwh_th",
    "latent_duty_kwh_th",
    "conductive_heat_leak_kwh_th",
)
CASES = tuple(
    (t, s) for t in TEMPERATURES_C for s in SALINITIES_G_KG
)
GRID = tuple(itertools.product(CASES, MODES, FACTORS, FACTORS))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def solve(temp: float, salinity: float, mode: str, feed_factor: float, permeate_factor: float):
    config = ChannelConfig(
        **FIXED,
        cells=CELLS,
        feed_salinity_g_kg=salinity,
        energy_balance_mode=mode,
        feed_heat_transfer_coefficient_w_m2_k=BASE_HTC_W_M2_K * feed_factor,
        permeate_heat_transfer_coefficient_w_m2_k=BASE_HTC_W_M2_K * permeate_factor,
    )
    return simulate_countercurrent_dcmd_channel(
        config=config,
        feed_in_temperature_c=temp,
        permeate_in_temperature_c=PERMEATE_IN_C,
    )


def run(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    baseline = {}
    for (temp, salinity), mode, ff, pf in GRID:
        result = solve(temp, salinity, mode, ff, pf)
        key = (temp, salinity, mode)
        values = {name: float(getattr(result, name)) for name in OUTPUTS}
        if ff == 1.0 and pf == 1.0:
            baseline[key] = values
        rows.append({
            "case_id": f"T{int(temp)}_S{int(salinity)}",
            "feed_in_temperature_c": temp,
            "permeate_in_temperature_c": PERMEATE_IN_C,
            "feed_reference_salinity_g_kg": salinity,
            "energy_balance_mode": mode,
            "cells": CELLS,
            "feed_htc_factor": ff,
            "permeate_htc_factor": pf,
            "feed_htc_w_m2_k": BASE_HTC_W_M2_K * ff,
            "permeate_htc_w_m2_k": BASE_HTC_W_M2_K * pf,
            **values,
            "solver_status": "success",
        })
    expected = len(CASES) * len(MODES) * len(FACTORS) ** 2
    if len(rows) != expected or len(baseline) != len(CASES) * len(MODES):
        raise RuntimeError("incomplete uncertainty grid or missing baseline")
    for row in rows:
        key = (row["feed_in_temperature_c"], row["feed_reference_salinity_g_kg"], row["energy_balance_mode"])
        ref = baseline[key]
        for name in OUTPUTS:
            value, base = float(row[name]), ref[name]
            row[f"{name}_delta_vs_nominal"] = value - base
            row[f"{name}_relative_delta_vs_nominal_pct"] = (
                "" if name.endswith("_temperature_c") or base == 0
                else (value / base - 1.0) * 100.0
            )
        if not all(math.isfinite(float(row[name])) for name in OUTPUTS):
            raise RuntimeError(f"non-finite output for {row['case_id']}")

    csv_path = output_dir / "htc_uncertainty_propagation.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = []
    for mode in MODES:
        subset = [r for r in rows if r["energy_balance_mode"] == mode]
        item = {"energy_balance_mode": mode, "scenario_count": len(subset)}
        for name in OUTPUTS:
            deltas = [float(r[f"{name}_delta_vs_nominal"]) for r in subset]
            rel = [float(r[f"{name}_relative_delta_vs_nominal_pct"]) for r in subset
                   if r[f"{name}_relative_delta_vs_nominal_pct"] != ""]
            item[f"{name}_min_delta"] = min(deltas)
            item[f"{name}_max_delta"] = max(deltas)
            if rel:
                item[f"{name}_min_relative_delta_pct"] = min(rel)
                item[f"{name}_max_relative_delta_pct"] = max(rel)
        summary.append(item)
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "experiment_id": "DCMD-HTC-UNCERTAINTY-PROPAGATION-2026-11-07",
        "row_count": len(rows),
        "operating_point_count": len(CASES),
        "modes": list(MODES),
        "htc_factors_each_side": list(FACTORS),
        "nominal_htc_w_m2_k": BASE_HTC_W_M2_K,
        "cells": CELLS,
        "reference_note": "80 cells is the finest mesh in the completed numerical mesh study, not exact truth.",
        "design": "Full factorial independent feed/permeate HTC factor grid; only HTC factors vary within each paired operating-point/mode block.",
        "interpretation_limits": [
            "Factors 0.5 to 1.5 are deliberately illustrative stress-test bounds, not sourced uncertainty distributions.",
            "The grid is not a probability distribution; scenario fractions are not probabilities.",
            "Feed and permeate HTC factors are varied independently as a diagnostic design; physical correlation between them is not represented.",
            "This propagates HTC uncertainty through the reduced-order channel model, not through an independently validated hydrodynamic correlation.",
            "No empirical calibration or experimental validation is implied.",
            "Temperature changes are absolute degrees Celsius; no percentage change is computed for Celsius values.",
        ],
        "files": {csv_path.name: sha256(csv_path), summary_path.name: sha256(summary_path)},
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/htc_uncertainty"))
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
