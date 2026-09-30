import numpy as np
import pytest

from ai_water.engine import simulate
from ai_water.hydraulics import pumping_from_pressure_drop
from ai_water.thermal import exergy_efficiency, heat_exergy_kwh
from ai_water.md import (
    flux_kg_m2_h,
    interface_temperatures,
    saturation_pressure_bar,
    vapor_pressure_driving_force_bar,
)
from ai_water.md_channel import ChannelConfig, simulate_dcmd_channel
from ai_water.md_thermal import account_for_membrane_heat
from ai_water.models import (
    AuxiliaryLoads,
    Cooling,
    HeatRecovery,
    MembraneDistillation,
    Scenario,
    WaterFactors,
    Workload,
)
from ai_water.uncertainty import (
    DistributionSpec,
    probability_negative,
    sample_distribution,
    summarize,
)


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
        water=WaterFactors(avoided_freshwater_consumption_l=1.0),
    )
    r = simulate(s)
    assert r.md_cooling_demand_kwh_th == 0.8
    assert r.md_cooling_electricity_kwh == 0.4
    assert r.md_cooling_water_l == 1.6
    assert r.direct_cooling_consumption_l == 1.6
    assert r.net_consumption_change_l == pytest.approx(0.6)
    assert r.net_freshwater_benefit_l == pytest.approx(-0.6)


def test_heat_limit_keeps_fixed_membrane_conduction():
    s = Scenario(
        workload=Workload(it_power_kw=1, duration_h=1, recoverable_heat_fraction=1),
        cooling=Cooling(),
        recovery=HeatRecovery(
            recovery_efficiency=1,
            heat_exchanger_effectiveness=1,
            source_temperature_c=70,
            cold_side_temperature_c=25,
        ),
        md=MembraneDistillation(
            membrane_area_m2=1,
            membrane_permeance_kg_m2_h_bar=1,
            thermal_energy_kwh_th_per_kg=1,
            latent_heat_kwh_th_per_kg=0.65,
            membrane_thermal_conductivity_w_m_k=0.2,
            membrane_thickness_m=100e-6,
            feed_recovery_fraction=0.1,
        ),
    )
    r = simulate(s)
    assert r.heat_limited is True
    assert r.md_conductive_heat_leak_kwh_th > 0
    assert r.md_thermal_demand_kwh_th > r.recoverable_heat_kwh_th
    assert r.freshwater_produced_l == 0.0
    assert r.concentrate_salinity_g_kg == 0.0



def test_one_dimensional_dcmd_channel_resolves_interface_temperatures_and_axial_cooling():
    result = simulate_dcmd_channel(
        config=ChannelConfig(
            membrane_area_m2=10,
            membrane_permeance_kg_m2_h_bar=1.0,
            latent_heat_kwh_th_per_kg=0.65,
            membrane_thermal_conductivity_w_m_k=0.05,
            membrane_thickness_m=100e-6,
            feed_heat_transfer_coefficient_w_m2_k=1000,
            permeate_heat_transfer_coefficient_w_m2_k=1000,
            feed_mass_flow_kg_h=10_000,
            permeate_mass_flow_kg_h=10_000,
            feed_salinity_g_kg=0,
            duration_h=1,
            cells=10,
        ),
        feed_in_temperature_c=60,
        permeate_in_temperature_c=25,
    )
    assert len(result.cells) == 10
    assert result.freshwater_produced_kg > 0
    assert result.feed_out_temperature_c < 60
    assert result.permeate_out_temperature_c > 25
    assert result.conductive_heat_leak_kwh_th > 0
    assert all(c.feed_interface_temperature_c < c.feed_bulk_temperature_c for c in result.cells)
    assert all(c.permeate_interface_temperature_c > c.permeate_bulk_temperature_c for c in result.cells)


def test_one_dimensional_channel_concentrates_saline_feed():
    result = simulate_dcmd_channel(
        config=ChannelConfig(
            membrane_area_m2=2,
            membrane_permeance_kg_m2_h_bar=0.5,
            latent_heat_kwh_th_per_kg=0.65,
            membrane_thermal_conductivity_w_m_k=0.05,
            membrane_thickness_m=100e-6,
            feed_heat_transfer_coefficient_w_m2_k=1000,
            permeate_heat_transfer_coefficient_w_m2_k=1000,
            feed_mass_flow_kg_h=1000,
            permeate_mass_flow_kg_h=1000,
            feed_salinity_g_kg=35,
            duration_h=1,
            cells=5,
        ),
        feed_in_temperature_c=60,
        permeate_in_temperature_c=25,
    )
    assert result.freshwater_produced_kg > 0
    assert result.concentrate_salinity_g_kg > 35
from ai_water.channel_transport import (
    ChannelProperties,
    concentration_polarization_coefficient,
    dimensionless_numbers,
    graetz_leveque_nusselt,
    graetz_leveque_sherwood,
    heat_transfer_coefficient,
    interface_salinity_g_kg,
    mass_transfer_coefficient,
    tpc_from_interfaces,
    watertap_nusselt,
)


def test_channel_correlations_and_polarization_are_physical():
    props = ChannelProperties(
        density_kg_m3=1000,
        viscosity_pa_s=0.001,
        thermal_conductivity_w_m_k=0.6,
        heat_capacity_j_kg_k=4180,
        diffusivity_m2_s=1.5e-9,
    )
    re, pr, sc = dimensionless_numbers(
        velocity_m_s=0.2,
        hydraulic_diameter_m=0.002,
        properties=props,
    )
    nu = graetz_leveque_nusselt(re, pr, 0.002, 1.0)
    sh = graetz_leveque_sherwood(re, sc, 0.002, 1.0)
    assert re > 0 and pr > 0 and sc > 0
    assert nu > 0 and sh > 0
    assert watertap_nusselt(re, pr) > 0
    h = heat_transfer_coefficient(
        nusselt=nu,
        thermal_conductivity_w_m_k=0.6,
        hydraulic_diameter_m=0.002,
    )
    k_m = mass_transfer_coefficient(
        sherwood=sh,
        diffusivity_m2_s=1.5e-9,
        hydraulic_diameter_m=0.002,
    )
    cpc = concentration_polarization_coefficient(
        flux_kg_m2_s=1e-4,
        mass_transfer_coefficient_m_s=k_m,
        solvent_density_kg_m3=1000,
    )
    assert h > 0 and k_m > 0 and cpc >= 1
    assert interface_salinity_g_kg(35, cpc) >= 35
    assert 0.0 < tpc_from_interfaces(60, 25, 55, 30) <= 1.0


def test_one_dimensional_channel_can_apply_concentration_polarization():
    result = simulate_dcmd_channel(
        config=ChannelConfig(
            membrane_area_m2=2,
            membrane_permeance_kg_m2_h_bar=0.5,
            latent_heat_kwh_th_per_kg=0.65,
            membrane_thermal_conductivity_w_m_k=0.05,
            membrane_thickness_m=100e-6,
            feed_heat_transfer_coefficient_w_m2_k=1000,
            permeate_heat_transfer_coefficient_w_m2_k=1000,
            feed_mass_flow_kg_h=1000,
            permeate_mass_flow_kg_h=1000,
            feed_salinity_g_kg=35,
            duration_h=1,
            cells=5,
            salt_mass_transfer_coefficient_m_s=1e-4,
            solvent_density_kg_m3=1020,
        ),
        feed_in_temperature_c=60,
        permeate_in_temperature_c=25,
    )
    assert result.freshwater_produced_kg > 0
    assert all(c.concentration_polarization_coefficient >= 1 for c in result.cells)
    assert all(c.interface_salinity_g_kg >= c.feed_salinity_g_kg for c in result.cells)



def test_uncertainty_sampling_is_reproducible_and_preserves_sign_probability():
    a = sample_distribution(
        DistributionSpec("uniform", (0.0, 1.0)),
        size=100,
        rng=np.random.default_rng(42),
    )
    b = sample_distribution(
        DistributionSpec("uniform", (0.0, 1.0)),
        size=100,
        rng=np.random.default_rng(42),
    )
    assert np.array_equal(a, b)
    values = np.array([-1.0, 0.0, 1.0, 2.0])
    assert probability_negative(values) == 0.25
    summary = summarize(values)
    assert summary["p05"] <= summary["median"] <= summary["p95"]


def test_counter_current_channel_uses_opposite_stream_boundary_direction():
    result = simulate_dcmd_channel(
        config=ChannelConfig(
            membrane_area_m2=2,
            membrane_permeance_kg_m2_h_bar=0.5,
            latent_heat_kwh_th_per_kg=0.65,
            membrane_thermal_conductivity_w_m_k=0.05,
            membrane_thickness_m=100e-6,
            feed_heat_transfer_coefficient_w_m2_k=1000,
            permeate_heat_transfer_coefficient_w_m2_k=1000,
            feed_mass_flow_kg_h=1000,
            permeate_mass_flow_kg_h=1000,
            feed_salinity_g_kg=0,
            duration_h=1,
            cells=8,
            flow_arrangement="counter_current",
        ),
        feed_in_temperature_c=60,
        permeate_in_temperature_c=25,
    )
    assert len(result.cells) == 8
    assert result.freshwater_produced_kg > 0
    assert result.feed_out_temperature_c < 60
    assert result.permeate_out_temperature_c > 25
    assert result.permeate_out_mass_kg_h > 1000
    assert result.cells[-1].permeate_bulk_temperature_c > result.cells[0].permeate_bulk_temperature_c


def test_heat_exergy_reflects_source_temperature_quality():
    low = heat_exergy_kwh(heat_kwh_th=100, source_temperature_c=50, ambient_temperature_c=25)
    high = heat_exergy_kwh(heat_kwh_th=100, source_temperature_c=90, ambient_temperature_c=25)
    assert high > low > 0
    assert heat_exergy_kwh(heat_kwh_th=100, source_temperature_c=25, ambient_temperature_c=25) == 0


def test_exergy_efficiency_is_bounded():
    value = exergy_efficiency(
        useful_heat_kwh_th=50,
        source_heat_kwh_th=100,
        source_temperature_c=80,
        ambient_temperature_c=25,
    )
    assert 0 < value <= 1
