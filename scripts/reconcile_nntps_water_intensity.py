"""Reconcile reported NNTPS water volumes and process-water intensities.

This is an evidence-consistency calculation only. It does not create or approve
a water factor because the source period and water-source boundary are unresolved.
"""

import json

NET_GENERATION_MU = {
    "2020-21": 3176.32,
    "2021-22": 5758.70,
}
REPORTED_PROCESS_INTENSITY_L_PER_KWH = {
    "2020-21": 0.111,
    "2021-22": 0.069,
}
PROCESS_VOLUME_M3_AS_PRINTED_PER_DAY = 32712.46
COOLING_VOLUME_M3_AS_PRINTED_PER_DAY = 1165.15
DOMESTIC_VOLUME_M3_AS_PRINTED_PER_DAY = 5597.12
DAYS_PER_YEAR = 365
DAYS_PER_MONTH_FOR_ALTERNATIVE = 30


def implied_monthly_volume_m3(
    net_generation_mu: float,
    process_intensity_l_per_kwh: float,
) -> float:
    """Return the monthly process volume implied by an annual intensity."""
    annual_kwh = net_generation_mu * 1_000_000
    annual_volume_m3 = process_intensity_l_per_kwh * annual_kwh / 1_000
    return annual_volume_m3 / 12


def intensity_from_daily_volume_l_per_kwh(
    volume_m3_per_day: float,
    net_generation_mu: float,
) -> float:
    """Convert a literal daily volume to intensity using annual net generation."""
    daily_kwh = net_generation_mu * 1_000_000 / DAYS_PER_YEAR
    return volume_m3_per_day * 1_000 / daily_kwh


def intensity_from_30_day_total_l_per_kwh(
    volume_m3_per_30_days: float,
    net_generation_mu: float,
) -> float:
    """Treat the printed volume as a 30-day total and calculate its intensity."""
    daily_kwh = net_generation_mu * 1_000_000 / DAYS_PER_YEAR
    period_kwh = daily_kwh * DAYS_PER_MONTH_FOR_ALTERNATIVE
    return volume_m3_per_30_days * 1_000 / period_kwh


def daily_volume_implied_by_intensity_m3(
    process_intensity_l_per_kwh: float,
    net_generation_mu: float,
) -> float:
    """Return the average daily volume implied by an annual intensity."""
    daily_kwh = net_generation_mu * 1_000_000 / DAYS_PER_YEAR
    return process_intensity_l_per_kwh * daily_kwh / 1_000


def build_reconciliation() -> dict[str, object]:
    """Build both competing interpretations without selecting either one."""
    net_generation = NET_GENERATION_MU["2021-22"]
    daily_process_intensity = intensity_from_daily_volume_l_per_kwh(
        PROCESS_VOLUME_M3_AS_PRINTED_PER_DAY,
        net_generation,
    )
    thirty_day_intensity = intensity_from_30_day_total_l_per_kwh(
        PROCESS_VOLUME_M3_AS_PRINTED_PER_DAY,
        net_generation,
    )
    reported_intensity = REPORTED_PROCESS_INTENSITY_L_PER_KWH["2021-22"]
    implied_monthly = implied_monthly_volume_m3(
        net_generation,
        reported_intensity,
    )
    daily_volume_from_30_day_total = (
        PROCESS_VOLUME_M3_AS_PRINTED_PER_DAY / DAYS_PER_MONTH_FOR_ALTERNATIVE
    )
    daily_volume_from_reported_intensity = daily_volume_implied_by_intensity_m3(
        reported_intensity,
        net_generation,
    )
    total_daily_volume = (
        PROCESS_VOLUME_M3_AS_PRINTED_PER_DAY
        + COOLING_VOLUME_M3_AS_PRINTED_PER_DAY
        + DOMESTIC_VOLUME_M3_AS_PRINTED_PER_DAY
    )
    total_daily_intensity = intensity_from_daily_volume_l_per_kwh(
        total_daily_volume,
        net_generation,
    )

    return {
        "status": "PROVISIONAL_RECONCILIATION_ONLY",
        "net_generation_mu": NET_GENERATION_MU,
        "reported_process_intensity_l_per_kwh": (
            REPORTED_PROCESS_INTENSITY_L_PER_KWH
        ),
        "fy2020_21_implied_monthly_process_volume_m3": (
            implied_monthly_volume_m3(
                NET_GENERATION_MU["2020-21"],
                REPORTED_PROCESS_INTENSITY_L_PER_KWH["2020-21"],
            )
        ),
        "fy2021_22_reported_process_volume_m3_as_printed": (
            PROCESS_VOLUME_M3_AS_PRINTED_PER_DAY
        ),
        "fy2021_22_implied_monthly_process_volume_from_0_069_m3": (
            implied_monthly
        ),
        "reported_volume_divided_by_implied_monthly_volume": (
            PROCESS_VOLUME_M3_AS_PRINTED_PER_DAY / implied_monthly
        ),
        "process_intensity_if_volume_is_daily_l_per_kwh": (
            daily_process_intensity
        ),
        "process_intensity_if_volume_is_30_day_total_l_per_kwh": (
            thirty_day_intensity
        ),
        "daily_process_volume_if_30_day_total_m3": daily_volume_from_30_day_total,
        "daily_process_volume_implied_by_reported_0_069_m3": (
            daily_volume_from_reported_intensity
        ),
        "daily_volume_ratio_30_day_total_to_reported_intensity": (
            daily_volume_from_30_day_total / daily_volume_from_reported_intensity
        ),
        "process_to_reported_intensity_ratio_if_daily": (
            daily_process_intensity
            / REPORTED_PROCESS_INTENSITY_L_PER_KWH["2021-22"]
        ),
        "all_three_volumes_m3_per_day_if_literal": total_daily_volume,
        "all_three_category_intensity_if_daily_l_per_kwh": (
            total_daily_intensity
        ),
        "interpretation": (
            "The 30-day-total interpretation closely reproduces 0.069, "
            "but the source labels the volume m3/day. The daily interpretation "
            "is about 30 times larger. Source period and FW/NFW composition "
            "must be confirmed before either value is used."
        ),
        "factor_ledger_disposition": "EXCLUDED_PENDING_SOURCE_RECONCILIATION",
    }


def main() -> None:
    print(json.dumps(build_reconciliation(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
