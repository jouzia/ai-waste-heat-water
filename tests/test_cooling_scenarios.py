import pytest

from ai_water.cooling_scenarios import CoolingScenario, validate_scenario_set


def make(name: str) -> CoolingScenario:
    return CoolingScenario(
        architecture=name,
        cooling_water_l_per_kwh_facility=0.2,
        incremental_electricity_kwh_per_kwh_it=0.05,
        heat_rejection_fraction=0.4,
        heat_recovery_fraction=0.6,
    )


def test_cooling_water_accounting():
    assert make("air_cooled").cooling_water_consumption_l(100.0) == pytest.approx(20.0)


def test_comparative_set_requires_diversity():
    with pytest.raises(ValueError):
        validate_scenario_set([make("air_cooled")])
    validate_scenario_set([make("air_cooled"), make("evaporative")])


def test_fraction_validation():
    with pytest.raises(ValueError):
        CoolingScenario("air_cooled", 0.0, 0.0, 1.2, 0.0)
