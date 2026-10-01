from ai_water.engine import simulate
from ai_water.models import (
    AuxiliaryLoads,
    Cooling,
    HeatRecovery,
    MembraneDistillation,
    Scenario,
    WaterFactors,
    Workload,
)


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
        water=WaterFactors(avoided_freshwater_consumption_l=1.0),
    )


def test_energy_to_heat_is_explicit_and_recoverable():
    result = simulate(scenario())
    assert result.it_energy_kwh == 100
    assert result.heat_generated_kwh_th == 100
    assert result.recoverable_heat_kwh_th == 100


def test_heat_limiting_reduces_production():
    s = scenario()
    s.recovery.recovery_efficiency = 0.005
    result = simulate(s)
    assert result.heat_limited is True
    # 0.5 kWh_th is available and the configured effective duty is
    # 1 kWh_th per kg, so production is limited to 0.5 kg = 0.5 L.
    assert result.freshwater_produced_l == 0.5


def test_net_consumption_sign_is_explicit():
    result = simulate(scenario())
    assert result.net_consumption_change_l == -1.0
    assert result.net_freshwater_benefit_l == 1.0



def test_incremental_cooling_water_excludes_baseline_facility_load():
    s = scenario()
    s.cooling = Cooling(
        facility_overhead_fraction=0.3,
        incremental_facility_electricity_kwh=3.0,
        cooling_water_consumption_l_per_kwh_facility=2.0,
    )
    result = simulate(s)
    assert result.facility_energy_kwh == 130.0
    # Only 3 kWh of incremental facility electricity is attributable to
    # the intervention; baseline facility cooling is in the counterfactual.
    assert result.direct_cooling_consumption_l == 6.0
    assert result.additional_water_consumption_l == 6.0
