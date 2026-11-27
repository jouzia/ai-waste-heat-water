"""Summarize Tamil Nadu's reported state-wise generation mix.

The output is a generation-side dataset summary, not a Tamil Nadu electricity
consumption mix or a water-intensity factor.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "geography"
    / "tamil_nadu_generation_mix_2020_21_to_2025_26.csv"
)


def load_generation_rows() -> list[dict[str, str]]:
    """Load the source-transcribed generation mix CSV."""
    with DATA_PATH.open(encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def summarize_generation_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    """Calculate total and non-hydro generation shares for each period."""
    summaries = []

    for row in rows:
        grand_total = float(row["grand_total_mu"])
        thermal = float(row["total_thermal_mu"])
        nuclear = float(row["nuclear_mu"])
        renewable = float(row["total_renewable_mu"])
        small_hydro = float(row["small_hydro_mu"])
        large_hydro = float(row["large_hydro_mu"])
        nonhydro_total = grand_total - small_hydro - large_hydro
        nonhydro_renewable = renewable - small_hydro - large_hydro
        coverage_months = int(row["coverage_months"])

        summaries.append(
            {
                "period": row["period"],
                "coverage_months": coverage_months,
                "period_complete": coverage_months == 12,
                "grand_total_mu": grand_total,
                "thermal_mu": thermal,
                "nuclear_mu": nuclear,
                "renewable_mu": renewable,
                "small_hydro_mu": small_hydro,
                "large_hydro_mu": large_hydro,
                "nonhydro_renewable_mu": nonhydro_renewable,
                "thermal_share_pct": thermal / grand_total * 100,
                "nuclear_share_pct": nuclear / grand_total * 100,
                "renewable_share_pct": renewable / grand_total * 100,
                "nonhydro_total_mu": nonhydro_total,
                "thermal_share_nonhydro_pct": thermal / nonhydro_total * 100,
                "nuclear_share_nonhydro_pct": nuclear / nonhydro_total * 100,
                "renewable_share_nonhydro_pct": (
                    nonhydro_renewable / nonhydro_total * 100
                ),
            }
        )

    return summaries


def build_report() -> dict[str, object]:
    """Build a machine-readable summary while preserving scope limitations."""
    return {
        "status": "GENERATION_MIX_ONLY_NOT_CONSUMPTION_MIX",
        "source_id": "RS-AU4143-ANNEXURE-I-2026",
        "unit": "MU (million kWh)",
        "periods": summarize_generation_rows(load_generation_rows()),
        "scope_note": (
            "State-wise generation located in Tamil Nadu. Thermal, nuclear, "
            "and large-hydro generation is reported for stations >=25 MW. "
            "Renewable totals include small and large hydro. This is not the "
            "electricity-consumption mix; central-station firm allocations "
            "to other states are documented separately."
        ),
        "water_factor_disposition": (
            "No water factor is calculated or added to the factor ledger."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = json.dumps(build_report(), indent=2, sort_keys=True)
    if args.output is not None:
        args.output.write_text(report + "\n", encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()
