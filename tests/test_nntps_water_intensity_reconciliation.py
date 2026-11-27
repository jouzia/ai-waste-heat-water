"""Regression tests for the provisional NNTPS water reconciliation."""

import pytest

from scripts.reconcile_nntps_water_intensity import (
    build_reconciliation,
    daily_volume_implied_by_intensity_m3,
    implied_monthly_volume_m3,
    intensity_from_30_day_total_l_per_kwh,
    intensity_from_daily_volume_l_per_kwh,
)


def test_literal_daily_volume_implies_about_2_073_l_per_kwh() -> None:
    value = intensity_from_daily_volume_l_per_kwh(32712.46, 5758.70)
    assert value == pytest.approx(2.07339294, rel=1e-7)


def test_thirty_day_total_reproduces_reported_0_069() -> None:
    value = intensity_from_30_day_total_l_per_kwh(32712.46, 5758.70)
    assert value == pytest.approx(0.06911310, rel=1e-7)


def test_two_year_reported_intensities_imply_similar_monthly_volumes() -> None:
    fy2020_21 = implied_monthly_volume_m3(3176.32, 0.111)
    fy2021_22 = implied_monthly_volume_m3(5758.70, 0.069)

    assert fy2020_21 == pytest.approx(29380.96)
    assert fy2021_22 == pytest.approx(33112.525)



def test_thirty_day_volume_matches_reported_intensity_daily_volume() -> None:
    volume_from_30_day_total = 32712.46 / 30
    volume_from_intensity = daily_volume_implied_by_intensity_m3(0.069, 5758.70)

    assert volume_from_intensity == pytest.approx(1088.63096, rel=1e-7)
    assert volume_from_30_day_total / volume_from_intensity == pytest.approx(
        1.0016391, rel=1e-6
    )


def test_reconciliation_keeps_factor_excluded() -> None:
    result = build_reconciliation()

    assert result["status"] == "PROVISIONAL_RECONCILIATION_ONLY"
    assert (
        result["factor_ledger_disposition"]
        == "EXCLUDED_PENDING_SOURCE_RECONCILIATION"
    )
    assert result["process_to_reported_intensity_ratio_if_daily"] == pytest.approx(
        30.049173, rel=1e-6
    )
