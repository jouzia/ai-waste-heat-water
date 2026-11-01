"""Run a higher-resolution Sobol convergence check on scenario-only model outputs.

The sampled ranges are illustrative, not calibrated uncertainty distributions.
The analysis is a numerical sensitivity diagnostic, not physical validation.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import platform
import sys
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from ai_water.engine import simulate
from ai_water.global_sensitivity import sobol_uniform

SCENARIO_SCRIPT = Path(__file__).resolve().with_name("run_scenario_uncertainty_study.py")
SPEC = importlib.util.spec_from_file_location("scenario_uncertainty_module", SCENARIO_SCRIPT)
if SPEC is None or SPEC.loader is None:
    raise ImportError(f"Cannot load scenario definitions from {SCENARIO_SCRIPT}")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

BOUNDS = MODULE.SCENARIO_BOUNDS
BASE_SCENARIO = MODULE.base_scenario
SCENARIO_FROM_VECTOR = MODULE.scenario_from_vector
SIZES = (4096, 8192)
SEED = 20261023
OUTPUTS = ("net_consumption_change_l", "freshwater_produced_l")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(output_dir: Path) -> dict[str, object]:
    base = BASE_SCENARIO()
    names = tuple(BOUNDS)
    all_rows: list[dict[str, object]] = []
    output_summaries: dict[str, object] = {}

    for output_name in OUTPUTS:
        by_size: dict[int, dict[str, object]] = {}
        for size in SIZES:
            def evaluate(values: np.ndarray, field: str = output_name) -> float:
                scenario = SCENARIO_FROM_VECTOR(base, names, values)
                result = simulate(scenario)
                value = float(getattr(result, field))
                if not math.isfinite(value):
                    raise ValueError(f"Non-finite {field} for sample {values.tolist()}")
                return value

            result = sobol_uniform(
                evaluate,
                BOUNDS,
                sample_size=size,
                seed=SEED,
            )
            by_size[size] = {
                item.parameter: {
                    "first_order": item.first_order,
                    "total_effect": item.total_effect,
                }
                for item in result.indices
            }
            for item in result.indices:
                all_rows.append(
                    {
                        "output": output_name,
                        "sample_size_per_matrix": size,
                        "seed": SEED,
                        "output_variance": result.output_variance,
                        "parameter": item.parameter,
                        "first_order": item.first_order,
                        "total_effect": item.total_effect,
                        "range_low": BOUNDS[item.parameter][0],
                        "range_high": BOUNDS[item.parameter][1],
                    }
                )

        low, high = SIZES
        rank_low = {
            name: rank
            for rank, (name, _) in enumerate(
                sorted(by_size[low].items(), key=lambda pair: pair[1]["total_effect"], reverse=True),
                start=1,
            )
        }
        rank_high = {
            name: rank
            for rank, (name, _) in enumerate(
                sorted(by_size[high].items(), key=lambda pair: pair[1]["total_effect"], reverse=True),
                start=1,
            )
        }
        parameter_diagnostics = {}
        for name in names:
            left = by_size[low][name]
            right = by_size[high][name]
            parameter_diagnostics[name] = {
                "first_order_abs_delta": abs(left["first_order"] - right["first_order"]),
                "total_effect_abs_delta": abs(left["total_effect"] - right["total_effect"]),
                "total_effect_rank_4096": rank_low[name],
                "total_effect_rank_8192": rank_high[name],
                "absolute_rank_shift": abs(rank_low[name] - rank_high[name]),
            }
        output_summaries[output_name] = {
            "sample_sizes_per_matrix": list(SIZES),
            "seed": SEED,
            "top_5_total_effect_at_4096": [
                name for name, _ in sorted(
                    by_size[low].items(), key=lambda pair: pair[1]["total_effect"], reverse=True
                )[:5]
            ],
            "top_5_total_effect_at_8192": [
                name for name, _ in sorted(
                    by_size[high].items(), key=lambda pair: pair[1]["total_effect"], reverse=True
                )[:5]
            ],
            "parameter_diagnostics": parameter_diagnostics,
            "max_first_order_abs_delta": max(
                row["first_order_abs_delta"] for row in parameter_diagnostics.values()
            ),
            "max_total_effect_abs_delta": max(
                row["total_effect_abs_delta"] for row in parameter_diagnostics.values()
            ),
            "max_absolute_rank_shift": max(
                row["absolute_rank_shift"] for row in parameter_diagnostics.values()
            ),
        }

    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / "sobol_convergence_4096_8192.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(all_rows[0]))
        writer.writeheader()
        writer.writerows(all_rows)

    summary = {
        "study_id": "SOBOL-SCENARIO-CONVERGENCE-4096-8192-2026-10-14",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "python_version": platform.python_version(),
        "git_sha": __import__("os").environ.get("GITHUB_SHA", "local-unknown"),
        "source_script": str(SCENARIO_SCRIPT.name),
        "seed": SEED,
        "sample_sizes_per_matrix": list(SIZES),
        "parameter_count": len(names),
        "evaluation_count_per_output": sum(size * (len(names) + 2) for size in SIZES),
        "bounds": {
            name: {"low": values[0], "high": values[1], "interpretation": "illustrative scenario range"}
            for name, values in BOUNDS.items()
        },
        "outputs": output_summaries,
        "interpretation": (
            "Higher-resolution nested Sobol sequence comparison. Reported indices are conditional "
            "on independent uniform scenario ranges and the current unvalidated model. A stable "
            "ranking is not proof of physical validity or empirically calibrated uncertainty."
        ),
        "claim_limits": [
            "Scenario ranges are illustrative rather than measurement-backed uncertainty distributions.",
            "The base MD model has not passed empirical or independent held-out validation.",
            "Sobol indices are bound- and model-dependent and assume independent inputs.",
            "No index is clipped to [0, 1]; estimator artifacts remain visible.",
            "Numerical ranking stability does not establish a real-world probability of net-water benefit.",
        ],
    }
    summary_path = output_dir / "sobol_convergence_4096_8192_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    manifest = {
        "summary_file": summary_path.name,
        "csv_file": csv_path.name,
        "sha256": {
            summary_path.name: sha256_file(summary_path),
            csv_path.name: sha256_file(csv_path),
        },
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/sobol_convergence"))
    args = parser.parse_args()
    summary = run(args.output_dir)
    print(json.dumps({
        output: {
            "max_total_effect_abs_delta": details["max_total_effect_abs_delta"],
            "max_absolute_rank_shift": details["max_absolute_rank_shift"],
            "top_5_total_effect_at_8192": details["top_5_total_effect_at_8192"],
        }
        for output, details in summary["outputs"].items()
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
