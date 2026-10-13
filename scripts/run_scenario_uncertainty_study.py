"""Run explicitly illustrative Monte Carlo and Sobol scenario analysis.

All ranges below are scenario assumptions, not empirical distributions. This
script is intended to test the uncertainty pipeline and map conditional
break-even behavior; its outputs are not predictions for a real data centre.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ai_water.engine import simulate
from ai_water.global_sensitivity import sobol_uniform
from ai_water.models import (
    AuxiliaryLoads,
    Cooling,
    HeatRecovery,
    MembraneDistillation,
    Scenario,
    WaterFactors,
    Workload,
)
from ai_water.monte_carlo import run_monte_carlo
from ai_water.study_analysis import convergence_curve, summarize_net_water
from ai_water.uncertainty import DistributionSpec

SEED = 20261013
MC_SAMPLES = 10000
SOBOL_SIZES = (512, 2048)

# Broad engineering scenario ranges, intentionally not labelled empirical.
# Each range must be replaced or narrowed using a source/measurement prior
# before any publication-grade probabilistic interpretation.
SCENARIO_BOUNDS: dict[str, tuple[float, float]] = {
    "workload.it_power_kw": (50.0, 200.0),
    "workload.recoverable_heat_fraction": (0.2, 0.9),
    "recovery.recovery_efficiency": (0.3, 0.8),
    "recovery.heat_exchanger_effectiveness": (0.5, 0.95),
    "md.membrane_permeance_kg_m2_h_bar": (5.0, 25.0),
    "md.temperature_polarization_coefficient": (0.6, 1.0),
    "md.feed_salinity_g_kg": (0.0, 35.0),
    "md.thermal_energy_kwh_th_per_kg": (0.06, 0.2),
    "cooling.cooling_heat_penalty_fraction": (0.0, 0.3),
    "cooling.incremental_facility_electricity_kwh": (0.0, 20.0),
    "cooling.cooling_water_consumption_l_per_kwh_facility": (0.0, 1.0),
    "cooling.md_cooling_to_heating_ratio": (0.0, 1.0),
    "cooling.md_cooling_electricity_kwh_per_kwh_th": (0.0, 0.1),
    "cooling.md_cooling_water_l_per_kwh_th": (0.0, 0.5),
    "water.grid_water_l_per_kwh": (0.0, 2.0),
    "water.freshwater_displacement_fraction": (0.0, 1.0),
}


def base_scenario() -> Scenario:
    return Scenario(
        workload=Workload(
            it_power_kw=100.0,
            duration_h=1.0,
            recoverable_heat_fraction=0.8,
        ),
        cooling=Cooling(
            facility_overhead_fraction=0.3,
            incremental_facility_electricity_kwh=5.0,
            cooling_water_consumption_l_per_kwh_facility=0.2,
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
            membrane_area_m2=10.0,
            membrane_permeance_kg_m2_h_bar=15.0,
            flux_kg_m2_h=None,
            thermal_energy_kwh_th_per_kg=0.1,
            latent_heat_kwh_th_per_kg=0.65,
            membrane_thermal_conductivity_w_m_k=0.03,
            membrane_thickness_m=0.0002,
            feed_recovery_fraction=0.2,
            feed_salinity_g_kg=5.0,
            use_iapws_seawater=True,
            temperature_polarization_coefficient=0.8,
        ),
        auxiliary=AuxiliaryLoads(
            pump_kwh_per_m3=0.4,
            pretreatment_kwh_per_m3=0.1,
            other_kwh_per_m3=0.0,
        ),
        water=WaterFactors(
            grid_water_l_per_kwh=0.5,
            freshwater_displacement_fraction=0.5,
        ),
    )


def set_nested(data: dict, path: str, value: float) -> None:
    target = data
    parts = path.split(".")
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = float(value)


def scenario_from_vector(base: Scenario, names: tuple[str, ...], values: np.ndarray) -> Scenario:
    data = base.model_dump()
    for name, value in zip(names, values, strict=True):
        set_nested(data, name, float(value))
    return Scenario.model_validate(data)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_csv(path: Path, records: list[dict[str, object]]) -> None:
    if not records:
        raise ValueError(f"refusing to write empty result: {path}")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    base = base_scenario()
    distributions = {
        name: DistributionSpec("uniform", bounds)
        for name, bounds in SCENARIO_BOUNDS.items()
    }
    mc = run_monte_carlo(
        base,
        distributions,
        sample_size=MC_SAMPLES,
        seed=SEED,
    )
    if mc.failed_samples:
        raise RuntimeError(
            f"Monte Carlo has {mc.failed_samples} invalid draws; investigate rather than suppress."
        )

    records: list[dict[str, object]] = []
    net_values: list[float] = []
    freshwater_values: list[float] = []
    break_even_values: list[float] = []
    for raw in mc.records:
        row: dict[str, object] = dict(raw)
        produced = raw["freshwater_produced_l"]
        additional = raw["additional_water_consumption_l"]
        row["break_even_displacement_fraction"] = (
            additional / produced if produced > 0 else math.inf
        )
        records.append(row)
        net_values.append(raw["net_consumption_change_l"])
        freshwater_values.append(produced)
        if produced > 0:
            break_even_values.append(additional / produced)

    write_csv(output_dir / "monte_carlo_samples.csv", records)
    net_summary = summarize_net_water(net_values)
    convergence = [
        point.__dict__
        for point in convergence_curve(
            net_values, sample_counts=(1000, 2500, 5000, 10000)
        )
    ]
    write_csv(output_dir / "monte_carlo_convergence.csv", convergence)

    base_dump = base.model_dump()
    names = tuple(SCENARIO_BOUNDS)
    sobol_runs: dict[str, list[dict[str, object]]] = {}
    sobol_results: dict[str, dict[str, object]] = {}
    for output_name in ("net_consumption_change_l", "freshwater_produced_l"):
        sobol_runs[output_name] = []
        for sample_size in SOBOL_SIZES:
            def evaluate(values: np.ndarray, field: str = output_name) -> float:
                scenario = scenario_from_vector(base, names, values)
                result = simulate(scenario)
                return float(getattr(result, field))

            result = sobol_uniform(
                evaluate,
                SCENARIO_BOUNDS,
                sample_size=sample_size,
                seed=SEED,
            )
            rows = [
                {
                    "output": output_name,
                    "sample_size_per_matrix": result.sample_size_per_matrix,
                    "seed": result.seed,
                    "output_variance": result.output_variance,
                    "parameter": item.parameter,
                    "first_order": item.first_order,
                    "total_effect": item.total_effect,
                    "range_low": SCENARIO_BOUNDS[item.parameter][0],
                    "range_high": SCENARIO_BOUNDS[item.parameter][1],
                }
                for item in result.indices
            ]
            sobol_runs[output_name].extend(rows)
        sobol_results[output_name] = {
            "sample_sizes_per_matrix": list(SOBOL_SIZES),
            "index_change_512_to_2048": {
                parameter: {
                    "first_order_abs_delta": abs(
                        next(
                            r["first_order"] for r in sobol_runs[output_name]
                            if r["parameter"] == parameter and r["sample_size_per_matrix"] == 512
                        )
                        - next(
                            r["first_order"] for r in sobol_runs[output_name]
                            if r["parameter"] == parameter and r["sample_size_per_matrix"] == 2048
                        )
                    ),
                    "total_effect_abs_delta": abs(
                        next(
                            r["total_effect"] for r in sobol_runs[output_name]
                            if r["parameter"] == parameter and r["sample_size_per_matrix"] == 512
                        )
                        - next(
                            r["total_effect"] for r in sobol_runs[output_name]
                            if r["parameter"] == parameter and r["sample_size_per_matrix"] == 2048
                        )
                    ),
                }
                for parameter in names
            },
        }
    write_csv(output_dir / "sobol_indices.csv", [
        row for output_name in sobol_runs for row in sobol_runs[output_name]
    ])

    summary: dict[str, object] = {
        "experiment_id": "SCENARIO-UNCERTAINTY-2026-10-13",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "python_version": platform.python_version(),
        "seed": SEED,
        "git_sha": __import__("os").environ.get("GITHUB_SHA", "local-unknown"),
        "monte_carlo": {
            "requested_samples": mc.requested_samples,
            "successful_samples": mc.successful_samples,
            "failed_samples": mc.failed_samples,
            "net_consumption_change_l": net_summary.__dict__,
            "freshwater_produced_l": {
                "median": float(np.median(freshwater_values)),
                "p05": float(np.quantile(freshwater_values, 0.05)),
                "p95": float(np.quantile(freshwater_values, 0.95)),
            },
            "break_even_displacement_fraction": {
                "median": float(np.median(break_even_values)),
                "p05": float(np.quantile(break_even_values, 0.05)),
                "p95": float(np.quantile(break_even_values, 0.95)),
                "fraction_above_one": float(np.mean(np.asarray(break_even_values) > 1.0)),
            },
            "convergence": convergence,
        },
        "sobol": sobol_results,
        "bounds": {
            name: {"low": bounds[0], "high": bounds[1], "interpretation": "illustrative scenario range, not empirical distribution"}
            for name, bounds in SCENARIO_BOUNDS.items()
        },
        "claim_limits": [
            "All input ranges are illustrative scenario assumptions, not empirically calibrated probability distributions.",
            "Sign probabilities are conditional on this model, these ranges, and the declared freshwater-displacement counterfactual; they are not real-world probabilities.",
            "The model has not passed empirical MD validation or held-out validation.",
            "Sobol analysis assumes independent uniform inputs and is bound-dependent.",
            "The fixed one-hour scenario is not a time-resolved data-centre workload or a dynamic MD model.",
        ],
    }
    summary_path = output_dir / "scenario_uncertainty_summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "summary_file": summary_path.name,
        "samples_file": "monte_carlo_samples.csv",
        "convergence_file": "monte_carlo_convergence.csv",
        "sobol_file": "sobol_indices.csv",
        "sha256": {
            name: sha256_file(output_dir / name)
            for name in (
                summary_path.name,
                "monte_carlo_samples.csv",
                "monte_carlo_convergence.csv",
                "sobol_indices.csv",
            )
        },
        "status": "scenario_analysis_only_not_validation",
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/scenario_uncertainty"))
    args = parser.parse_args()
    summary = run(args.output_dir)
    print(json.dumps({
        "experiment_id": summary["experiment_id"],
        "mc_samples": summary["monte_carlo"]["successful_samples"],
        "net_water_summary": summary["monte_carlo"]["net_consumption_change_l"],
        "artifact_dir": str(args.output_dir),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
