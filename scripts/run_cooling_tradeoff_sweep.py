"""Run a reproducible, explicitly illustrative cooling/water/energy/carbon trade-off sweep.

All architecture factors and grid intensities are scenario assumptions, not
empirical measurements. The sweep is a decision-space demonstration, not a
forecast or validation of any real facility.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ai_water.break_even import pareto_mask
from ai_water.cooling_scenarios import CoolingScenario, validate_scenario_set
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

# Hypothetical scenario parameters for comparing architectures. These values
# are intentionally not represented as source-backed performance factors.
ARCHITECTURES = (
    {
        "architecture": "air_cooled",
        "cooling_water_l_per_kwh_facility": 0.0,
        "incremental_electricity_kwh_per_kwh_it": 0.08,
        "heat_rejection_fraction": 0.8,
        "heat_recovery_fraction": 0.2,
        "md_cooling_to_heating_ratio": 0.8,
        "md_cooling_electricity_kwh_per_kwh_th": 0.05,
        "md_cooling_water_l_per_kwh_th": 0.0,
    },
    {
        "architecture": "evaporative",
        "cooling_water_l_per_kwh_facility": 1.0,
        "incremental_electricity_kwh_per_kwh_it": 0.03,
        "heat_rejection_fraction": 0.8,
        "heat_recovery_fraction": 0.2,
        "md_cooling_to_heating_ratio": 0.8,
        "md_cooling_electricity_kwh_per_kwh_th": 0.03,
        "md_cooling_water_l_per_kwh_th": 0.1,
    },
    {
        "architecture": "direct_liquid",
        "cooling_water_l_per_kwh_facility": 0.05,
        "incremental_electricity_kwh_per_kwh_it": 0.025,
        "heat_rejection_fraction": 0.5,
        "heat_recovery_fraction": 0.5,
        "md_cooling_to_heating_ratio": 0.6,
        "md_cooling_electricity_kwh_per_kwh_th": 0.04,
        "md_cooling_water_l_per_kwh_th": 0.02,
    },
    {
        "architecture": "rear_door_heat_exchanger",
        "cooling_water_l_per_kwh_facility": 0.02,
        "incremental_electricity_kwh_per_kwh_it": 0.03,
        "heat_rejection_fraction": 0.3,
        "heat_recovery_fraction": 0.7,
        "md_cooling_to_heating_ratio": 0.4,
        "md_cooling_electricity_kwh_per_kwh_th": 0.03,
        "md_cooling_water_l_per_kwh_th": 0.01,
    },
    {
        "architecture": "hybrid",
        "cooling_water_l_per_kwh_facility": 0.3,
        "incremental_electricity_kwh_per_kwh_it": 0.04,
        "heat_rejection_fraction": 0.4,
        "heat_recovery_fraction": 0.6,
        "md_cooling_to_heating_ratio": 0.5,
        "md_cooling_electricity_kwh_per_kwh_th": 0.04,
        "md_cooling_water_l_per_kwh_th": 0.05,
    },
    {
        "architecture": "immersion",
        "cooling_water_l_per_kwh_facility": 0.01,
        "incremental_electricity_kwh_per_kwh_it": 0.02,
        "heat_rejection_fraction": 0.2,
        "heat_recovery_fraction": 0.8,
        "md_cooling_to_heating_ratio": 0.3,
        "md_cooling_electricity_kwh_per_kwh_th": 0.02,
        "md_cooling_water_l_per_kwh_th": 0.01,
    },
)
AREAS_M2 = (2.0, 5.0, 10.0, 20.0)
DISPLACEMENT_FRACTIONS = (0.0, 0.25, 0.5, 0.75, 1.0)
GRID_WATER_FACTORS_L_KWH = (0.1, 0.5, 1.0, 2.0)
GRID_CARBON_FACTORS_KG_KWH = (0.05, 0.4, 0.8)


def make_base(
    architecture: dict[str, float | str],
    *,
    area_m2: float,
    displacement_fraction: float,
    grid_water_factor: float,
    grid_carbon_factor: float,
) -> tuple[Scenario, float]:
    workload = Workload(
        it_power_kw=100.0,
        duration_h=1.0,
        recoverable_heat_fraction=0.8,
    )
    it_energy = workload.it_power_kw * workload.duration_h
    cooling = Cooling(
        facility_overhead_fraction=0.3,
        incremental_facility_electricity_kwh=(
            it_energy * float(architecture["incremental_electricity_kwh_per_kwh_it"])
        ),
        cooling_water_consumption_l_per_kwh_facility=float(
            architecture["cooling_water_l_per_kwh_facility"]
        ),
        cooling_heat_penalty_fraction=0.0,
        md_cooling_to_heating_ratio=float(architecture["md_cooling_to_heating_ratio"]),
        md_cooling_electricity_kwh_per_kwh_th=float(
            architecture["md_cooling_electricity_kwh_per_kwh_th"]
        ),
        md_cooling_water_l_per_kwh_th=float(
            architecture["md_cooling_water_l_per_kwh_th"]
        ),
    )
    recovery = HeatRecovery(
        recovery_efficiency=0.5,
        heat_exchanger_effectiveness=0.8,
        usable_heat_fraction=float(architecture["heat_recovery_fraction"]),
        source_temperature_c=70.0,
        cold_side_temperature_c=25.0,
    )
    md = MembraneDistillation(
        membrane_area_m2=area_m2,
        membrane_permeance_kg_m2_h_bar=15.0,
        flux_kg_m2_h=None,
        thermal_energy_kwh_th_per_kg=0.1,
        latent_heat_kwh_th_per_kg=0.65,
        membrane_thermal_conductivity_w_m_k=0.03,
        membrane_thickness_m=0.0002,
        feed_recovery_fraction=0.2,
        feed_salinity_g_kg=5.0,
        water_activity=0.995,
        use_iapws_seawater=False,
        temperature_polarization_coefficient=0.8,
    )
    scenario = Scenario(
        workload=workload,
        cooling=cooling,
        recovery=recovery,
        md=md,
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
    return scenario, grid_carbon_factor


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    cooling_scenarios = [
        CoolingScenario(
            architecture=str(item["architecture"]),
            cooling_water_l_per_kwh_facility=float(item["cooling_water_l_per_kwh_facility"]),
            incremental_electricity_kwh_per_kwh_it=float(item["incremental_electricity_kwh_per_kwh_it"]),
            heat_rejection_fraction=float(item["heat_rejection_fraction"]),
            heat_recovery_fraction=float(item["heat_recovery_fraction"]),
        )
        for item in ARCHITECTURES
    ]
    validate_scenario_set(cooling_scenarios)

    records: list[dict[str, object]] = []
    for architecture in ARCHITECTURES:
        for area in AREAS_M2:
            for displacement in DISPLACEMENT_FRACTIONS:
                for water_factor in GRID_WATER_FACTORS_L_KWH:
                    for carbon_factor in GRID_CARBON_FACTORS_KG_KWH:
                        scenario, carbon_intensity = make_base(
                            architecture,
                            area_m2=area,
                            displacement_fraction=displacement,
                            grid_water_factor=water_factor,
                            grid_carbon_factor=carbon_factor,
                        )
                        result = simulate(scenario)
                        incremental_electricity = (
                            scenario.cooling.incremental_facility_electricity_kwh
                            + result.auxiliary_electricity_kwh
                        )
                        row = {
                            "architecture": architecture["architecture"],
                            "area_m2": area,
                            "freshwater_displacement_fraction": displacement,
                            "grid_water_l_per_kwh": water_factor,
                            "grid_carbon_kg_co2e_per_kwh": carbon_intensity,
                            "cooling_water_l_per_kwh_facility": architecture["cooling_water_l_per_kwh_facility"],
                            "incremental_facility_electricity_kwh": scenario.cooling.incremental_facility_electricity_kwh,
                            "incremental_electricity_kwh": incremental_electricity,
                            "operational_emissions_kg_co2e": incremental_electricity * carbon_intensity,
                            "recoverable_heat_kwh_th": result.recoverable_heat_kwh_th,
                            "md_thermal_demand_kwh_th": result.md_thermal_demand_kwh_th,
                            "freshwater_produced_l": result.freshwater_produced_l,
                            "additional_water_consumption_l": result.additional_water_consumption_l,
                            "avoided_freshwater_consumption_l": result.avoided_freshwater_consumption_l,
                            "net_consumption_change_l": result.net_consumption_change_l,
                            "heat_limited": result.heat_limited,
                            "break_even_displacement_fraction": (
                                result.additional_water_consumption_l / result.freshwater_produced_l
                                if result.freshwater_produced_l > 0
                                else ""
                            ),
                        }
                        records.append(row)

    # Evaluate Pareto fronts separately at each grid-carbon factor so different
    # emissions intensities are not mixed in a single comparison set.
    for carbon_factor in GRID_CARBON_FACTORS_KG_KWH:
        subset_indices = [
            i for i, row in enumerate(records)
            if row["grid_carbon_kg_co2e_per_kwh"] == carbon_factor
        ]
        values = np.asarray(
            [
                [
                    float(records[i]["net_consumption_change_l"]),
                    float(records[i]["incremental_electricity_kwh"]),
                    float(records[i]["operational_emissions_kg_co2e"]),
                    float(records[i]["freshwater_produced_l"]),
                ]
                for i in subset_indices
            ],
            dtype=float,
        )
        mask = pareto_mask(values, minimize=(True, True, True, False))
        for index, is_pareto in zip(subset_indices, mask, strict=True):
            records[index]["pareto_optimal_within_grid_carbon_case"] = bool(is_pareto)

    path = output_dir / "cooling_water_energy_carbon_tradeoffs.csv"
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

    pareto_records = [row for row in records if row["pareto_optimal_within_grid_carbon_case"]]
    manifest: dict[str, object] = {
        "experiment_id": "COOLING-WATER-ENERGY-CARBON-SWEEP-2026-10-13",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "git_sha": __import__("os").environ.get("GITHUB_SHA", "local-unknown"),
        "scenario_count": len(records),
        "pareto_point_count": len(pareto_records),
        "architecture_count": len(ARCHITECTURES),
        "areas_m2": list(AREAS_M2),
        "freshwater_displacement_fractions": list(DISPLACEMENT_FRACTIONS),
        "grid_water_factors_l_per_kwh": list(GRID_WATER_FACTORS_L_KWH),
        "grid_carbon_factors_kg_co2e_per_kwh": list(GRID_CARBON_FACTORS_KG_KWH),
        "output_file": path.name,
        "output_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "assumption_policy": [
            "All cooling architecture factors and grid water/carbon factors are illustrative scenario assumptions, not empirically measured values.",
            "The carbon boundary includes only incremental electricity multiplied by the declared grid-carbon factor; embodied emissions, water-treatment emissions, equipment manufacture, and baseline IT electricity are excluded.",
            "Freshwater benefit counts only the declared fraction of distillate that demonstrably displaces freshwater consumption; this is not inferred from gross production.",
            "Pareto fronts are computed separately for each grid-carbon factor and minimize net water consumption, incremental electricity, and operational emissions while maximizing freshwater production.",
            "The MD model has not passed source-matched or held-out empirical validation; the results are decision-space exploration only.",
        ],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    with (output_dir / "pareto_front.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(pareto_records[0]))
        writer.writeheader()
        writer.writerows(pareto_records)
    manifest["pareto_front_sha256"] = hashlib.sha256(
        (output_dir / "pareto_front.csv").read_bytes()
    ).hexdigest()
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/cooling_tradeoffs"))
    args = parser.parse_args()
    manifest = run(args.output_dir)
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
