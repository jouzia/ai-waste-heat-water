"""Couple a time-varying workload trace to the reduced-order MD engine.

The coupling is intentionally piecewise-constant: each workload interval is
simulated independently with its declared source temperature and IT power,
then additive water/energy quantities are aggregated. This is a study
integration layer, not a transient CFD or plant controller model.
"""
from dataclasses import dataclass
from typing import Iterable

from .engine import simulate
from .models import HeatRecovery, Result, Scenario, Workload
from .workload_profile import WorkloadInterval, WorkloadProfileFactors


@dataclass(frozen=True)
class WorkloadCoupledResult:
    """Aggregate result plus trace-level diagnostics."""

    result: Result
    interval_results: tuple[Result, ...]
    duration_h: float
    thermally_eligible_duration_h: float
    heat_availability_fraction: float
    heat_weighted_source_temperature_c: float | None


def simulate_workload_profile(
    scenario: Scenario,
    intervals: Iterable[WorkloadInterval],
    factors: WorkloadProfileFactors,
) -> WorkloadCoupledResult:
    """Run the reduced-order engine once per workload interval.

    The scenario's avoided-freshwater value is interpreted as a profile-level
    counterfactual and is applied once after interval aggregation. The supplied
    profile factors control heat recovery for every eligible interval.
    """
    samples = tuple(intervals)
    if not samples:
        raise ValueError("workload profile must contain at least one interval")

    interval_results: list[Result] = []
    for interval in samples:
        eligible = (
            interval.source_temperature_c >= factors.minimum_source_temperature_c
            and interval.it_power_kw > 0
            and interval.recoverable_heat_fraction > 0
        )
        recoverable_fraction = interval.recoverable_heat_fraction if eligible else 0.0
        interval_scenario = scenario.model_copy(
            update={
                "workload": Workload(
                    it_power_kw=interval.it_power_kw,
                    duration_h=interval.duration_h,
                    recoverable_heat_fraction=recoverable_fraction,
                ),
                "recovery": HeatRecovery(
                    recovery_efficiency=factors.recovery_efficiency,
                    heat_exchanger_effectiveness=factors.heat_exchanger_effectiveness,
                    usable_heat_fraction=factors.usable_heat_fraction,
                    source_temperature_c=interval.source_temperature_c,
                    cold_side_temperature_c=scenario.recovery.cold_side_temperature_c,
                ),
                "water": scenario.water.model_copy(
                    update={"avoided_freshwater_consumption_l": 0.0}
                ),
            }
        )
        interval_results.append(simulate(interval_scenario))

    total_duration = sum(item.duration_h for item in samples)
    eligible_duration = sum(
        item.duration_h
        for item in samples
        if (
            item.source_temperature_c >= factors.minimum_source_temperature_c
            and item.it_power_kw > 0
            and item.recoverable_heat_fraction > 0
        )
    )

    additive_fields = (
        "it_energy_kwh",
        "facility_energy_kwh",
        "heat_generated_kwh_th",
        "recoverable_heat_kwh_th",
        "md_thermal_demand_kwh_th",
        "md_latent_demand_kwh_th",
        "md_conductive_heat_leak_kwh_th",
        "md_cooling_demand_kwh_th",
        "md_cooling_electricity_kwh",
        "md_cooling_water_l",
        "freshwater_produced_l",
        "feed_water_withdrawal_l",
        "concentrate_discharge_l",
        "direct_cooling_consumption_l",
        "pumping_electricity_kwh",
        "auxiliary_electricity_kwh",
        "indirect_water_consumption_l",
        "additional_water_consumption_l",
    )
    values = {
        field: sum(getattr(item, field) for item in interval_results)
        for field in additive_fields
    }

    weighted_heat = sum(
        item.source_temperature_c
        * item.it_power_kw
        * item.duration_h
        * item.recoverable_heat_fraction
        * factors.recovery_efficiency
        * factors.heat_exchanger_effectiveness
        * factors.usable_heat_fraction
        for item in samples
        if (
            item.source_temperature_c >= factors.minimum_source_temperature_c
            and item.it_power_kw > 0
            and item.recoverable_heat_fraction > 0
        )
    )
    usable_heat = sum(
        item.it_power_kw
        * item.duration_h
        * item.recoverable_heat_fraction
        * factors.recovery_efficiency
        * factors.heat_exchanger_effectiveness
        * factors.usable_heat_fraction
        for item in samples
        if (
            item.source_temperature_c >= factors.minimum_source_temperature_c
            and item.it_power_kw > 0
            and item.recoverable_heat_fraction > 0
        )
    )

    avoided = scenario.water.avoided_freshwater_consumption_l
    aggregate = Result(
        **values,
        concentrate_salinity_g_kg=(
            sum(
                item.concentrate_salinity_g_kg * item.concentrate_discharge_l
                for item in interval_results
            )
            / values["concentrate_discharge_l"]
            if values["concentrate_discharge_l"] > 0
            else 0.0
        ),
        avoided_freshwater_consumption_l=avoided,
        net_consumption_change_l=values["additional_water_consumption_l"] - avoided,
        net_freshwater_benefit_l=avoided - values["additional_water_consumption_l"],
        heat_limited=any(item.heat_limited for item in interval_results),
    )

    return WorkloadCoupledResult(
        result=aggregate,
        interval_results=tuple(interval_results),
        duration_h=total_duration,
        thermally_eligible_duration_h=eligible_duration,
        heat_availability_fraction=eligible_duration / total_duration,
        heat_weighted_source_temperature_c=(
            weighted_heat / usable_heat if usable_heat > 0 else None
        ),
    )
