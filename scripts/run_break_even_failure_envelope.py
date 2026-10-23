"""Compute a conditional break-even and failure envelope for the reduced-order system model.

All swept ranges are explicit screening assumptions, not empirical distributions.
The output is a scenario envelope only; no real-world probability or validation
claim is permitted until MD model validation and source-backed priors are complete.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from ai_water.engine import simulate
from ai_water.models import (
    AuxiliaryLoads,
    Cooling,
    HeatRecovery,
    MembraneDistillation,
    Scenario,
    WaterFactors,
    Workload,
)

RECOVERABLE_HEAT_FRACTIONS = (0.2, 0.5, 0.8, 1.0)
TPC_VALUES = (0.6, 0.8, 1.0)
PERMEANCE_VALUES = (5.0, 15.0, 25.0)
AREAS_M2 = (2.0, 5.0, 10.0, 20.0)
GRID_WATER_FACTORS = (0.1, 0.5, 1.0, 2.0)
COOLING_WATER_INTENSITIES = (0.0, 0.2, 1.0)
INCREMENTAL_FACILITY_ELECTRICITY_KWH = (2.0, 10.0, 20.0)
DISPLACEMENT_FRACTIONS = (0.0, 0.25, 0.5, 0.75, 1.0)
# Illustrative factor-of-two stress test, not a sourced material uncertainty range.
MEMBRANE_THERMAL_CONDUCTIVITY_W_M_K = (0.015, 0.03, 0.06)


def make_scenario(
    *,
    recoverable_heat_fraction: float,
    tpc: float,
    permeance: float,
    area_m2: float,
    membrane_thermal_conductivity_w_m_k: float,
    grid_water_factor: float,
    cooling_water_intensity: float,
    incremental_facility_electricity_kwh: float,
    displacement_fraction: float,
) -> Scenario:
    return Scenario(
        workload=Workload(
            it_power_kw=100.0,
            duration_h=1.0,
            recoverable_heat_fraction=recoverable_heat_fraction,
        ),
        cooling=Cooling(
            facility_overhead_fraction=0.3,
            incremental_facility_electricity_kwh=incremental_facility_electricity_kwh,
            cooling_water_consumption_l_per_kwh_facility=cooling_water_intensity,
            cooling_heat_penalty_fraction=0.1,
            md_cooling_to_heating_ratio=0.5,
            md_cooling_electricity_kwh_per_kwh_th=0.05,
            md_cooling_water_l_per_kwh_th=0.1,
        ),
        recovery=HeatRecovery(
            recovery_efficiency=0.5,
            heat_exchanger_effectiveness=0.8,
            usable_heat_fraction=1.0,
            source_temperature_c=70.0,
            cold_side_temperature_c=25.0,
        ),
        md=MembraneDistillation(
            membrane_area_m2=area_m2,
            membrane_permeance_kg_m2_h_bar=permeance,
            flux_kg_m2_h=None,
            thermal_energy_kwh_th_per_kg=0.1,
            latent_heat_kwh_th_per_kg=0.65,
            membrane_thermal_conductivity_w_m_k=membrane_thermal_conductivity_w_m_k,
            membrane_thickness_m=0.0002,
            feed_recovery_fraction=0.2,
            feed_salinity_g_kg=5.0,
            water_activity=0.995,
            use_iapws_seawater=False,
            temperature_polarization_coefficient=tpc,
        ),
        auxiliary=AuxiliaryLoads(
            pump_kwh_per_m3=0.4,
            pretreatment_kwh_per_m3=0.1,
            other_kwh_per_m3=0.0,
        ),
        water=WaterFactors(
            grid_water_l_per_kwh=grid_water_factor,
            freshwater_displacement_fraction=displacement_fraction,
        ),
    )


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, records: list[dict[str, object]]) -> None:
    if not records:
        raise ValueError(f"Cannot write empty result file: {path}")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    envelope: list[dict[str, object]] = []
    displacement_sweep: list[dict[str, object]] = []
    for conductivity in MEMBRANE_THERMAL_CONDUCTIVITY_W_M_K:
        for heat_fraction in RECOVERABLE_HEAT_FRACTIONS:
            for tpc in TPC_VALUES:
                for permeance in PERMEANCE_VALUES:
                    for area in AREAS_M2:
                        for grid_water in GRID_WATER_FACTORS:
                            for cooling_water in COOLING_WATER_INTENSITIES:
                                for incremental_electricity in INCREMENTAL_FACILITY_ELECTRICITY_KWH:
                                    # A single scenario at full displacement yields the
                                    # break-even threshold independently of the requested
                                    # displacement fraction.
                                    full = simulate(
                                        make_scenario(
                                            recoverable_heat_fraction=heat_fraction,
                                            tpc=tpc,
                                            permeance=permeance,
                                            area_m2=area,
                                            grid_water_factor=grid_water,
                                            cooling_water_intensity=cooling_water,
                                            incremental_facility_electricity_kwh=incremental_electricity,
                                            displacement_fraction=1.0,
                                        )
                                    )
                                    produced = full.freshwater_produced_l
                                    additional = full.additional_water_consumption_l
                                    threshold = additional / produced if produced > 0 else None
                                    if produced <= 0:
                                        failure_class = "no_freshwater_production"
                                    elif threshold is not None and threshold > 1.0:
                                        failure_class = "break_even_impossible_at_full_displacement"
                                    else:
                                        failure_class = "break_even_possible_with_sufficient_displacement"
                                    envelope.append(
                                        {
                                            "recoverable_heat_fraction": heat_fraction,
                                            "temperature_polarization_coefficient": tpc,
                                            "membrane_permeance_kg_m2_h_bar": permeance,
                                            "membrane_area_m2": area,
                                            "membrane_thermal_conductivity_w_m_k": conductivity,
                                            "grid_water_l_per_kwh": grid_water,
                                            "cooling_water_l_per_kwh_facility": cooling_water,
                                            "incremental_facility_electricity_kwh": incremental_electricity,
                                            "freshwater_produced_l": produced,
                                            "additional_water_consumption_l": additional,
                                            "break_even_displacement_fraction": "" if threshold is None else threshold,
                                            "net_consumption_change_at_full_displacement_l": full.net_consumption_change_l,
                                            "heat_limited": full.heat_limited,
                                            "failure_class": failure_class,
                                        }
                                    )
                                    for displacement in DISPLACEMENT_FRACTIONS:
                                        scenario = make_scenario(
                                            recoverable_heat_fraction=heat_fraction,
                                            tpc=tpc,
                                            permeance=permeance,
                                            area_m2=area,
                                            grid_water_factor=grid_water,
                                            cooling_water_intensity=cooling_water,
                                            incremental_facility_electricity_kwh=incremental_electricity,
                                            displacement_fraction=displacement,
                                        )
                                        result = simulate(scenario)
                                        displacement_sweep.append(
                                            {
                                                "recoverable_heat_fraction": heat_fraction,
                                                "temperature_polarization_coefficient": tpc,
                                                "membrane_permeance_kg_m2_h_bar": permeance,
                                                "membrane_area_m2": area,
                                                "grid_water_l_per_kwh": grid_water,
                                                "cooling_water_l_per_kwh_facility": cooling_water,
                                                "incremental_facility_electricity_kwh": incremental_electricity,
                                                "freshwater_displacement_fraction": displacement,
                                                "freshwater_produced_l": result.freshwater_produced_l,
                                                "additional_water_consumption_l": result.additional_water_consumption_l,
                                                "avoided_freshwater_consumption_l": result.avoided_freshwater_consumption_l,
                                                "net_consumption_change_l": result.net_consumption_change_l,
                                                "heat_limited": result.heat_limited,
                                                "failure_class": failure_class,
                                            }
                                        )

    envelope_path = output_dir / "break_even_failure_envelope.csv"
    sweep_path = output_dir / "net_water_by_displacement.csv"
    write_csv(envelope_path, envelope)
    write_csv(sweep_path, displacement_sweep)
    counts: dict[str, int] = {}
    for row in envelope:
        key = str(row["failure_class"])
        counts[key] = counts.get(key, 0) + 1
    manifest: dict[str, object] = {
        "experiment_id": "BREAK-EVEN-FAILURE-ENVELOPE-2026-10-13",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "git_sha": __import__("os").environ.get("GITHUB_SHA", "local-unknown"),
        "base_parameter_combinations": len(envelope),
        "membrane_conductivity_scenarios": len(MEMBRANE_THERMAL_CONDUCTIVITY_W_M_K),
        "displacement_sweep_rows": len(displacement_sweep),
        "failure_class_counts": counts,
        "ranges": {
            "recoverable_heat_fraction": list(RECOVERABLE_HEAT_FRACTIONS),
            "temperature_polarization_coefficient": list(TPC_VALUES),
            "membrane_permeance_kg_m2_h_bar": list(PERMEANCE_VALUES),
            "membrane_area_m2": list(AREAS_M2),
            "membrane_thermal_conductivity_w_m_k": list(MEMBRANE_THERMAL_CONDUCTIVITY_W_M_K),
            "grid_water_l_per_kwh": list(GRID_WATER_FACTORS),
            "cooling_water_l_per_kwh_facility": list(COOLING_WATER_INTENSITIES),
            "incremental_facility_electricity_kwh": list(INCREMENTAL_FACILITY_ELECTRICITY_KWH),
            "freshwater_displacement_fraction": list(DISPLACEMENT_FRACTIONS),
        },
        "files": {
            envelope_path.name: sha256_file(envelope_path),
            sweep_path.name: sha256_file(sweep_path),
        },
        "interpretation_limits": [
            "All ranges are illustrative screening assumptions, not empirical distributions.",
            "Membrane thermal conductivity uses an illustrative factor-of-two stress test (0.015, 0.03, 0.06 W m-1 K-1), not a sourced uncertainty distribution.",
            "The one-hour scenario, fixed water activity, and reduced-order MD model are not source-validated.",
            "Break-even threshold is additional water consumption divided by gross freshwater production; thresholds above one mean full displacement is insufficient under the stated boundary.",
            "No-production cases have no finite displacement break-even threshold.",
            "The envelope is conditional scenario mapping, not a probability estimate or a real-facility forecast.",
        ],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/break_even_envelope"))
    args = parser.parse_args()
    manifest = run(args.output_dir)
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
