"""Cooling-architecture scenario definitions.

Values are intentionally supplied by the caller. This module provides the
scenario taxonomy and validation, not universal WUE or efficiency defaults.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

CoolingArchitecture = Literal[
    "air_cooled",
    "evaporative",
    "direct_liquid",
    "rear_door_heat_exchanger",
    "hybrid",
    "immersion",
]


@dataclass(frozen=True)
class CoolingScenario:
    architecture: CoolingArchitecture
    cooling_water_l_per_kwh_facility: float
    incremental_electricity_kwh_per_kwh_it: float
    heat_rejection_fraction: float
    heat_recovery_fraction: float

    def __post_init__(self) -> None:
        if self.cooling_water_l_per_kwh_facility < 0:
            raise ValueError("cooling water intensity must be non-negative")
        if self.incremental_electricity_kwh_per_kwh_it < 0:
            raise ValueError("incremental electricity intensity must be non-negative")
        if not 0 <= self.heat_rejection_fraction <= 1:
            raise ValueError("heat rejection fraction must be in [0, 1]")
        if not 0 <= self.heat_recovery_fraction <= 1:
            raise ValueError("heat recovery fraction must be in [0, 1]")
    @property
    def non_recovered_heat_fraction(self) -> float:
        return 1.0 - self.heat_recovery_fraction

    def cooling_water_consumption_l(self, facility_energy_kwh: float) -> float:
        if facility_energy_kwh < 0:
            raise ValueError("facility energy must be non-negative")
        return facility_energy_kwh * self.cooling_water_l_per_kwh_facility


def validate_scenario_set(scenarios: list[CoolingScenario]) -> None:
    """Require architecture diversity before a comparative study is run."""
    names = {s.architecture for s in scenarios}
    if len(names) < 2:
        raise ValueError("comparative cooling study requires at least two architectures")
