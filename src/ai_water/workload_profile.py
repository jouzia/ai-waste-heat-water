"""Time-resolved workload and recoverable-heat accounting.

This module is intentionally separate from the lumped scenario engine. It
integrates a declared workload trace without claiming that IT power is a
measured waste-heat stream; the IT-electricity-to-heat equivalence remains a
first-order approximation.
"""
from dataclasses import dataclass
from collections.abc import Iterable

from pydantic import BaseModel, Field


class WorkloadInterval(BaseModel):
    """Piecewise-constant workload interval; energy is power times duration."""

    duration_h: float = Field(gt=0)
    it_power_kw: float = Field(ge=0)
    recoverable_heat_fraction: float = Field(ge=0, le=1, default=0.8)
    source_temperature_c: float


class WorkloadProfileFactors(BaseModel):
    recovery_efficiency: float = Field(ge=0, le=1, default=0.5)
    heat_exchanger_effectiveness: float = Field(ge=0, le=1, default=0.8)
    usable_heat_fraction: float = Field(ge=0, le=1, default=1.0)
    minimum_source_temperature_c: float = 0.0


@dataclass(frozen=True)
class WorkloadProfileResult:
    duration_h: float
    it_energy_kwh: float
    heat_generated_kwh_th: float
    raw_recoverable_heat_kwh_th: float
    usable_recoverable_heat_kwh_th: float
    thermally_eligible_duration_h: float
    heat_availability_fraction: float
    heat_weighted_source_temperature_c: float | None


def integrate_workload_profile(
    intervals: Iterable[WorkloadInterval],
    factors: WorkloadProfileFactors,
) -> WorkloadProfileResult:
    """Integrate workload intervals and apply recovery factors per interval.

    Heat below the declared source-temperature threshold is excluded from
    usable recovery, but remains in total IT energy and generated heat.
    """
    samples = list(intervals)
    if not samples:
        raise ValueError("workload profile must contain at least one interval")

    total_duration = sum(item.duration_h for item in samples)
    it_energy = sum(item.it_power_kw * item.duration_h for item in samples)
    heat_generated = it_energy
    raw_recoverable = sum(
        item.it_power_kw
        * item.duration_h
        * item.recoverable_heat_fraction
        * factors.recovery_efficiency
        * factors.heat_exchanger_effectiveness
        * factors.usable_heat_fraction
        for item in samples
    )

    eligible = [
        item
        for item in samples
        if item.source_temperature_c >= factors.minimum_source_temperature_c
    ]
    eligible_duration = sum(item.duration_h for item in eligible)
    usable_heat = sum(
        item.it_power_kw
        * item.duration_h
        * item.recoverable_heat_fraction
        * factors.recovery_efficiency
        * factors.heat_exchanger_effectiveness
        * factors.usable_heat_fraction
        for item in eligible
    )
    weighted_heat = sum(
        item.source_temperature_c
        * item.it_power_kw
        * item.duration_h
        * item.recoverable_heat_fraction
        * factors.recovery_efficiency
        * factors.heat_exchanger_effectiveness
        * factors.usable_heat_fraction
        for item in eligible
    )

    return WorkloadProfileResult(
        duration_h=total_duration,
        it_energy_kwh=it_energy,
        heat_generated_kwh_th=heat_generated,
        raw_recoverable_heat_kwh_th=raw_recoverable,
        usable_recoverable_heat_kwh_th=usable_heat,
        thermally_eligible_duration_h=eligible_duration,
        heat_availability_fraction=(
            eligible_duration / total_duration if total_duration > 0 else 0.0
        ),
        heat_weighted_source_temperature_c=(
            weighted_heat / usable_heat if usable_heat > 0 else None
        ),
    )
