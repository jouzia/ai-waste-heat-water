"""Check Monte Carlo numerical convergence across independent seeds and a larger run.

All distributions are illustrative scenario ranges from the existing study script.
Passing this audit establishes numerical stability under those assumptions only;
it does not validate the model or make scenario fractions real-world probabilities.
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

from ai_water.monte_carlo import run_monte_carlo
from ai_water.uncertainty import DistributionSpec
from scripts.run_scenario_uncertainty_study import SCENARIO_BOUNDS, base_scenario

DESIGNS = (
    (20261013, 20_000),
    (20261014, 20_000),
    (20261015, 20_000),
    (20261016, 50_000),
)
P05_RELATIVE_TOLERANCE = 0.05
SIGN_PROBABILITY_ABSOLUTE_TOLERANCE = 0.005
P95_NET_RELATIVE_TOLERANCE = 0.02
P95_FRESHWATER_ABSOLUTE_TOLERANCE_L = 0.5


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def summarize(values: list[float]) -> dict[str, float]:
    array = np.asarray(values, dtype=float)
    return {
        "p05": float(np.quantile(array, 0.05)),
        "median": float(np.quantile(array, 0.50)),
        "p95": float(np.quantile(array, 0.95)),
    }


def run(output_dir: Path) -> dict[str, object]:
    base = base_scenario()
    distributions = {
        name: DistributionSpec("uniform", bounds)
        for name, bounds in SCENARIO_BOUNDS.items()
    }
    summaries: list[dict[str, object]] = []
    sample_records: list[dict[str, object]] = []
    for seed, sample_size in DESIGNS:
        result = run_monte_carlo(
            base,
            distributions,
            sample_size=sample_size,
            seed=seed,
        )
        if result.failed_samples:
            raise RuntimeError(
                f"Seed {seed} had {result.failed_samples} invalid draws; "
                "convergence cannot be judged by silently dropping them."
            )
        net = [float(row["net_consumption_change_l"]) for row in result.records]
        freshwater = [float(row["freshwater_produced_l"]) for row in result.records]
        summary = {
            "seed": seed,
            "requested_samples": result.requested_samples,
            "successful_samples": result.successful_samples,
            "failed_samples": result.failed_samples,
            "net_consumption_change_l": summarize(net),
            "negative_net_fraction": float(np.mean(np.asarray(net) < 0.0)),
            "positive_net_fraction": float(np.mean(np.asarray(net) > 0.0)),
            "freshwater_produced_l": summarize(freshwater),
            "zero_freshwater_fraction": float(np.mean(np.asarray(freshwater) == 0.0)),
        }
        summaries.append(summary)
        sample_records.append({
            "seed": seed,
            "sample_size": sample_size,
            "net_p05_l": summary["net_consumption_change_l"]["p05"],
            "net_median_l": summary["net_consumption_change_l"]["median"],
            "net_p95_l": summary["net_consumption_change_l"]["p95"],
            "negative_net_fraction": summary["negative_net_fraction"],
            "freshwater_p95_l": summary["freshwater_produced_l"]["p95"],
            "zero_freshwater_fraction": summary["zero_freshwater_fraction"],
        })

    replicates = summaries[:3]
    large = summaries[3]
    p05_values = [float(x["net_consumption_change_l"]["p05"]) for x in replicates]
    p95_values = [float(x["net_consumption_change_l"]["p95"]) for x in replicates]
    sign_values = [float(x["negative_net_fraction"]) for x in replicates]
    freshwater_p95 = [float(x["freshwater_produced_l"]["p95"]) for x in replicates]
    large_p05 = float(large["net_consumption_change_l"]["p05"])
    large_p95 = float(large["net_consumption_change_l"]["p95"])
    large_sign = float(large["negative_net_fraction"])
    large_freshwater_p95 = float(large["freshwater_produced_l"]["p95"])

    p05_reference = float(np.median(p05_values))
    p95_reference = float(np.median(p95_values))
    p05_relative_spread = (
        (max(p05_values + [large_p05]) - min(p05_values + [large_p05]))
        / max(abs(p05_reference), 1e-12)
    )
    p95_relative_spread = (
        (max(p95_values + [large_p95]) - min(p95_values + [large_p95]))
        / max(abs(p95_reference), 1e-12)
    )
    sign_spread = max(sign_values + [large_sign]) - min(sign_values + [large_sign])
    freshwater_p95_spread = (
        max(freshwater_p95 + [large_freshwater_p95])
        - min(freshwater_p95 + [large_freshwater_p95])
    )
    checks = {
        "net_p05_relative_spread_within_tolerance": p05_relative_spread <= P05_RELATIVE_TOLERANCE,
        "negative_sign_probability_spread_within_tolerance": sign_spread <= SIGN_PROBABILITY_ABSOLUTE_TOLERANCE,
        "net_p95_relative_spread_within_tolerance": p95_relative_spread <= P95_NET_RELATIVE_TOLERANCE,
        "freshwater_p95_absolute_spread_within_tolerance": freshwater_p95_spread <= P95_FRESHWATER_ABSOLUTE_TOLERANCE_L,
    }
    summary: dict[str, object] = {
        "study_id": "SCENARIO-MC-INDEPENDENT-SEED-CONVERGENCE-2026-10-13",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "python_version": platform.python_version(),
        "input_interpretation": "illustrative independent-uniform scenario ranges; not empirical probability distributions",
        "designs": [{"seed": seed, "sample_size": n} for seed, n in DESIGNS],
        "acceptance_tolerances": {
            "net_p05_relative_spread": P05_RELATIVE_TOLERANCE,
            "negative_sign_probability_absolute_spread": SIGN_PROBABILITY_ABSOLUTE_TOLERANCE,
            "net_p95_relative_spread": P95_NET_RELATIVE_TOLERANCE,
            "freshwater_p95_absolute_spread_l": P95_FRESHWATER_ABSOLUTE_TOLERANCE_L,
        },
        "per_run_summaries": summaries,
        "spread_diagnostics": {
            "net_p05_relative_spread": p05_relative_spread,
            "negative_sign_probability_absolute_spread": sign_spread,
            "net_p95_relative_spread": p95_relative_spread,
            "freshwater_p95_absolute_spread_l": freshwater_p95_spread,
        },
        "acceptance_checks": checks,
        "numerically_converged_under_declared_scenario_ranges": all(checks.values()),
        "claim_limits": [
            "A pass means numerical Monte Carlo estimates are stable under the chosen illustrative scenario ranges.",
            "It does not establish empirically calibrated uncertainty, model validity, or real-world probability of net water benefit.",
            "Sobol freshwater-output convergence is a separate question and remains governed by its own diagnostics.",
        ],
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "independent_seed_monte_carlo_summary.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(sample_records[0]))
        writer.writeheader()
        writer.writerows(sample_records)
    summary_path = output_dir / "independent_seed_monte_carlo_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest = {
        "summary_sha256": sha256_file(summary_path),
        "csv_sha256": sha256_file(output_dir / "independent_seed_monte_carlo_summary.csv"),
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary["spread_diagnostics"], indent=2))
    print("Numerically converged under declared scenario ranges:", summary["numerically_converged_under_declared_scenario_ranges"])
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/monte_carlo_convergence"),
    )
    args = parser.parse_args()
    run(args.output_dir)


if __name__ == "__main__":
    main()
