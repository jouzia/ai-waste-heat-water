"""Run a Villa-area deterministic sensitivity sweep on the screening model.

The area is based on the workbook's nominal 0.23088 m² membrane area.
Area multipliers and crossed conductivity values are illustrative stress tests,
not empirically estimated uncertainty distributions or independent validation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path

from ai_water.engine import simulate
from run_break_even_failure_envelope import (
    MEMBRANE_THERMAL_CONDUCTIVITY_W_M_K,
    make_scenario,
)

VILLA_NOMINAL_AREA_M2 = 0.23088
AREA_MULTIPLIERS = (0.8, 0.9, 1.0, 1.1, 1.2)
# Fixed reference settings are held constant to isolate area/conductivity effects.
REFERENCE = {
    "recoverable_heat_fraction": 0.5,
    "tpc": 0.8,
    "permeance": 15.0,
    "grid_water_factor": 0.5,
    "cooling_water_intensity": 0.2,
    "incremental_facility_electricity_kwh": 10.0,
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for multiplier in AREA_MULTIPLIERS:
        area = VILLA_NOMINAL_AREA_M2 * multiplier
        for conductivity in MEMBRANE_THERMAL_CONDUCTIVITY_W_M_K:
            full = simulate(make_scenario(
                **REFERENCE,
                area_m2=area,
                membrane_thermal_conductivity_w_m_k=conductivity,
                displacement_fraction=1.0,
            ))
            produced = full.freshwater_produced_l
            additional = full.additional_water_consumption_l
            threshold = additional / produced if produced > 0 else None
            if produced <= 0:
                failure_class = "no_freshwater_production"
            elif threshold is not None and threshold > 1.0:
                failure_class = "break_even_impossible_at_full_displacement"
            else:
                failure_class = "break_even_possible_with_sufficient_displacement"
            rows.append({
                "villa_nominal_membrane_area_m2": VILLA_NOMINAL_AREA_M2,
                "area_multiplier": multiplier,
                "membrane_area_m2": area,
                "membrane_thermal_conductivity_w_m_k": conductivity,
                **REFERENCE,
                "freshwater_produced_l": produced,
                "additional_water_consumption_l": additional,
                "break_even_displacement_fraction": "" if threshold is None else threshold,
                "net_consumption_change_at_full_displacement_l": full.net_consumption_change_l,
                "heat_limited": full.heat_limited,
                "failure_class": failure_class,
            })
    csv_path = output_dir / "villa_area_sensitivity.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    manifest = {
        "experiment_id": "VILLA-AREA-SENSITIVITY-2026-10-23",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "git_sha": os.environ.get("GITHUB_SHA", "local-unknown"),
        "row_count": len(rows),
        "nominal_area_m2": VILLA_NOMINAL_AREA_M2,
        "area_multipliers": list(AREA_MULTIPLIERS),
        "conductivity_values_w_m_k": list(MEMBRANE_THERMAL_CONDUCTIVITY_W_M_K),
        "fixed_reference_parameters": REFERENCE,
        "interpretation": (
            "Deterministic screening sensitivity only; multipliers are illustrative, "
            "not empirical uncertainty distributions. Not independent validation."
        ),
        "files": {csv_path.name: sha256_file(csv_path)},
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/villa_area_sensitivity"))
    args = parser.parse_args()
    manifest = run(args.output_dir)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
