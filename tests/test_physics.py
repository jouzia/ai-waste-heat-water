from ai_water.engine import simulate
from ai_water.hydraulics import pumping_from_pressure_drop
from ai_water.models import (
    AuxiliaryLoads,
    Cooling,
    HeatRecovery,
    MembraneDistillation,
    Scenario,
    WaterFactors,
    Workload,
)
from ai_water.md import (
    flux_kg_m2_h,
    interface_temperatures,
    saturation_pressure_bar,
    vapor_pressure_driving_force_bar,
)
from ai_water.md_thermal import account_for_membrane_heat


def test_saturation_pressure_increases_with_temperature():
    assert saturation_pressure_bar(40) < saturation_pressure_bar(60)


def test_interface_temperatures_reduce_bulk_delta():
    hot_i, cold_i = interface_temperatures(70, 25, 0.8)
    assert cold_i > 25
    assert hot_i < 70
    assert hot_i > cold_i


def test_activity_reduces_vapor_pressure_driving_force():
    pure = vapor_pressure_driving_force_bar(60, 30, 1.0)
    saline = vapor_pressure_driving_force_bar(60, 30, 0.9)
    assert saline < pure


def test_flux_scales_with_permeance():
    base = flux_kg_m2_h(60, 30, 1.0)
    doubled = flux_kg_m2_h(60, 30, 2.0)
    assert doubled == 2 * base


def test_thermal_accounting_separates_latent_and_conductive_heat():
    r = account_for_membrane_heat(
        water_kg=10,
        latent_heat_kwh_th_per_kg=0.65,
        membrane_area_m2=5,
        interface_delta_t_k=20,
        membrane_thermal_conductivity_w_m_k=0.2,
        membrane_thickness_m=100e-6,
        duration_h=1,
    )
    assert r.latent_duty_kwh_th == 6.5
    assert r.conductive_heat_leak_kwh_th > 0
    assert r.hot_side_duty_kwh_th > r.latent_duty_kwh_th


def test_pumping_pressure_drop_route():
    r = pumping_from_pressure_drop(
        distillate_l=1000,
        duration_h=1,
        recovery_fraction=0.05,
        pressure_drop_bar=0.3,
        pump_efficiency=0.7,
    )
    assert r.feed_flow_m3_h == 20
    assert r.electrical_power_kw > 0
    assert r.specific_electricity_kwh_m3 > 0


def test_cooling_burden_reaches_water_accounting():
    s = Scenario(
        workload=Workload(it_power_kw=100, duration_h=1, recoverable_heat_fraction=1),
        cooling=Cooling(
            md_cooling_to_heating_ratio=0.8,
            md_cooling_electricity_kwh_per_kwh_th=0.5,
            md_cooling_water_l_per_kwh_th=2,
        ),
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
    r = simulate(s)
    assert r.md_cooling_demand_kwh_th == 0.8
    assert r.md_cooling_electricity_kwh == 0.4
    assert r.md_cooling_water_l == 1.6
    assert r.direct_cooling_consumption_l == 1.6
