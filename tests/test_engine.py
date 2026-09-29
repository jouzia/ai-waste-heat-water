from ai_water.engine import simulate
from ai_water.models import AuxiliaryLoads, Cooling, HeatRecovery, MembraneDistillation, Scenario, WaterFactors, Workload


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
        water=WaterFactors(),
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
    assert result.freshwater_produced_l == 0.5


def test_distillate_is_not_automatically_avoided_consumption():
    result = simulate(scenario())
    assert result.freshwater_produced_l == 1.0
    assert result.avoided_freshwater_consumption_l == 0.0
    assert result.net_consumption_change_l == 0.0
    assert result.net_freshwater_benefit_l == 0.0


def test_declared_counterfactual_drives_net_water_response():
    s = scenario()
    s.water.avoided_freshwater_consumption_l = 0.8
    result = simulate(s)
    assert result.net_consumption_change_l == -0.8
    assert result.net_freshwater_benefit_l == 0.8


def test_baseline_facility_electricity_is_not_incremental_water_burden():
    s = scenario()
    s.water.grid_water_l_per_kwh = 1.0
    result = simulate(s)
    assert result.indirect_water_consumption_l == 0.0
