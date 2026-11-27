"""Regression tests for the provisional NNTPS water reconciliation."""

import json
import math
from pathlib import Path
import subprocess
import sys


def run_reconciliation() -> dict[str, object]:
    """Run the standalone audit script and parse its JSON result."""
    repository_root = Path(__file__).resolve().parents[1]
    script_path = repository_root / "scripts" / "reconcile_nntps_water_intensity.py"
    result = subprocess.run(
        [sys.executable, str(script_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_literal_daily_volume_implies_about_2_073_l_per_kwh() -> None:
    result = run_reconciliation()
    value = result["process_intensity_if_volume_is_daily_l_per_kwh"]

    assert math.isclose(value, 2.07339294, rel_tol=1e-7)


def test_thirty_day_total_reproduces_reported_0_069() -> None:
    result = run_reconciliation()
    value = result["process_intensity_if_volume_is_30_day_total_l_per_kwh"]

    assert math.isclose(value, 0.06911310, rel_tol=1e-7)


def test_two_year_reported_intensities_imply_similar_monthly_volumes() -> None:
    result = run_reconciliation()

    assert math.isclose(
        result["fy2020_21_implied_monthly_process_volume_m3"],
        29380.96,
        rel_tol=1e-7,
    )
    assert math.isclose(
        result["fy2021_22_implied_monthly_process_volume_from_0_069_m3"],
        33112.525,
        rel_tol=1e-7,
    )


def test_thirty_day_volume_matches_reported_intensity_daily_volume() -> None:
    result = run_reconciliation()
    ratio = result["daily_volume_ratio_30_day_total_to_reported_intensity"]

    assert math.isclose(ratio, 1.0016391, rel_tol=1e-6)


def test_reconciliation_keeps_factor_excluded() -> None:
    result = run_reconciliation()

    assert result["status"] == "PROVISIONAL_RECONCILIATION_ONLY"
    assert (
        result["factor_ledger_disposition"]
        == "EXCLUDED_PENDING_SOURCE_RECONCILIATION"
    )
