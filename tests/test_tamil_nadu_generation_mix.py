"""Tests for the Tamil Nadu generation-mix transcription and summary."""

import json
import math
import subprocess
import sys
from pathlib import Path


def run_generation_summary() -> dict[str, object]:
    """Run the standalone summary script and parse its JSON output."""
    repository_root = Path(__file__).resolve().parents[1]
    script_path = repository_root / "scripts" / "summarize_tamil_nadu_generation_mix.py"
    result = subprocess.run(
        [sys.executable, str(script_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_generation_components_reconcile_to_source_totals() -> None:
    report = run_generation_summary()

    for period in report["periods"]:
        component_total = (
            period["thermal_mu"] + period["nuclear_mu"] + period["renewable_mu"]
        )
        assert math.isclose(
            component_total,
            period["grand_total_mu"],
            rel_tol=0,
            abs_tol=0.05,
        )


def test_fy2021_22_source_values_and_shares() -> None:
    report = run_generation_summary()
    period = next(
        item for item in report["periods"] if item["period"] == "2021-22"
    )

    assert period["grand_total_mu"] == 106081.37
    assert period["thermal_mu"] == 61182.76
    assert period["nuclear_mu"] == 15625.26
    assert period["renewable_mu"] == 29273.35
    assert math.isclose(period["thermal_share_pct"], 57.68, abs_tol=0.01)


def test_nonhydro_mix_excludes_small_and_large_hydro() -> None:
    report = run_generation_summary()
    period = next(
        item for item in report["periods"] if item["period"] == "2024-25"
    )

    assert period["nonhydro_total_mu"] == 125265.60
    assert math.isclose(
        period["thermal_share_nonhydro_pct"],
        59.25,
        abs_tol=0.01,
    )
    assert math.isclose(
        period["nuclear_share_nonhydro_pct"],
        13.96,
        abs_tol=0.01,
    )


def test_latest_period_is_marked_partial() -> None:
    report = run_generation_summary()
    period = report["periods"][-1]

    assert period["period"] == "2025-26_to_Feb2026"
    assert period["coverage_months"] == 11
    assert period["period_complete"] is False


def test_summary_does_not_claim_consumption_mix_or_water_factor() -> None:
    report = run_generation_summary()

    assert report["status"] == "GENERATION_MIX_ONLY_NOT_CONSUMPTION_MIX"
    assert "not the electricity-consumption mix" in report["scope_note"]
    assert "No water factor" in report["water_factor_disposition"]
