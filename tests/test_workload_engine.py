import pytest

from ai_water.models import (
    AuxiliaryLoads,
    Cooling,
    HeatRecovery,
    MembraneDistillation,
    Scenario,
    WaterFactors,
    Workload,
)
from ai_water.workload_engine import simulate_workload_profile
from ai_water.workload_profile import WorkloadInterval, WorkloadProfileFactors


def scenario():
    return Scenario(
        workload=Workload(it_power_kw=100, duration_h=1, recoverable_heat_fraction=1),
        cooling=Cooling(),
        recovery=HeatRecovery(
            recovery_efficiency=1,
            heat_exchanger_effectiveness=1,
            source_temperature_c=70,
            cold_side_temperature_c=25,
        ),
        md=MembraneDistillation(
            flux_kg_m2_h=1,
            membrane_area_m2=1,
            thermal_energy_kwh_th_per_kg=1,
        ),
        auxiliary=AuxiliaryLoads(),
        water=WaterFactors(avoided_freshwater_consumption_l=2.0),
    )


def test_piecewise_profile_changes_heat_available_to_md():
    result = simulate_workload_profile(
        scenario(),
        [
            WorkloadInterval(
                duration_h=1,
                it_power_kw=100,
                recoverable_heat_fraction=1,
                source_temperature_c=70,
            ),
            WorkloadInterval(
                duration_h=1,
                it_power_kw=100,
                recoverable_heat_fraction=1,
                source_temperature_c=35,
            ),
        ],
        WorkloadProfileFactors(
            recovery_efficiency=1,
            heat_exchanger_effectiveness=1,
            usable_heat_fraction=1,
            minimum_source_temperature_c=50,
        ),
    )

    assert result.duration_h == pytest.approx(2)
    assert result.thermally_eligible_duration_h == pytest.approx(1)
    assert result.heat_availability_fraction == pytest.approx(0.5)
    assert result.result.it_energy_kwh == pytest.approx(200)
    assert result.result.freshwater_produced_l == pytest.approx(1)
    assert result.result.avoided_freshwater_consumption_l == pytest.approx(2)
    assert result.result.net_consumption_change_l == pytest.approx(-1)


def test_profile_avoided_water_is_counted_once():
    result = simulate_workload_profile(
        scenario(),
        [
            WorkloadInterval(
                duration_h=1,
                it_power_kw=100,
                recoverable_heat_fraction=1,
                source_temperature_c=70,
            ),
            WorkloadInterval(
                duration_h=1,
                it_power_kw=100,
                recoverable_heat_fraction=1,
                source_temperature_c=70,
            ),
        ],
        WorkloadProfileFactors(
            recovery_efficiency=1,
            heat_exchanger_effectiveness=1,
            usable_heat_fraction=1,
        ),
    )

    assert result.result.avoided_freshwater_consumption_l == pytest.approx(2)
    assert result.result.net_freshwater_benefit_l == pytest.approx(0)
