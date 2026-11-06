import pytest

from ai_water.wyon_2025_fluid_properties import (
    pure_water_density_kg_m3,
    pure_water_dynamic_viscosity_pa_s,
    pure_water_thermal_conductivity_w_m_k,
    seawater_density_kg_m3,
    seawater_dynamic_viscosity_pa_s,
    seawater_thermal_conductivity_w_m_k,
    wyon_channel_heat_transfer,
    wyon_fluid_properties,
)


def test_pure_water_appendix_properties_at_20_c():
    properties = wyon_fluid_properties(20.0, 0.0)
    assert properties.heat_capacity_j_kg_k == pytest.approx(4189.09, abs=0.1)
    assert properties.thermal_conductivity_w_m_k == pytest.approx(0.598464, rel=1e-5)
    assert properties.density_kg_m3 == pytest.approx(998.0298, rel=1e-6)
    assert properties.dynamic_viscosity_pa_s == pytest.approx(1.001762e-3, rel=1e-5)


def test_seawater_appendix_properties_at_20_c_and_38_g_kg():
    properties = wyon_fluid_properties(20.0, 38.0)
    assert properties.heat_capacity_j_kg_k == pytest.approx(3984.447, abs=0.1)
    assert properties.thermal_conductivity_w_m_k == pytest.approx(0.601510, rel=1e-5)
    assert properties.density_kg_m3 == pytest.approx(1026.702, rel=1e-6)
    assert properties.dynamic_viscosity_pa_s == pytest.approx(1.083806e-3, rel=1e-5)


def test_water_property_functions_preserve_expected_ordering():
    assert pure_water_density_kg_m3(20.0) < seawater_density_kg_m3(20.0, 38.0)
    assert pure_water_dynamic_viscosity_pa_s(20.0) < seawater_dynamic_viscosity_pa_s(20.0, 38.0)
    assert pure_water_thermal_conductivity_w_m_k(20.0) < seawater_thermal_conductivity_w_m_k(20.0, 38.0)


def test_wyon_feed_channel_transfer_example_at_30_c():
    result = wyon_channel_heat_transfer(
        velocity_m_s=1.85,
        hydraulic_diameter_m=0.003,
        channel_length_m=0.1,
        temperature_its90_c=30.0,
        salinity_sr_g_kg=38.0,
    )
    assert result.reynolds == pytest.approx(6554.50, rel=1e-4)
    assert result.prandtl == pytest.approx(5.61752, rel=1e-4)
    assert result.nusselt == pytest.approx(54.5368, rel=1e-4)
    assert result.heat_transfer_coefficient_w_m2_k == pytest.approx(11186.34, rel=1e-4)


def test_wyon_permeate_channel_transfer_example_at_30_c():
    result = wyon_channel_heat_transfer(
        velocity_m_s=2.92,
        hydraulic_diameter_m=0.003,
        channel_length_m=0.1,
        temperature_its90_c=30.0,
        salinity_sr_g_kg=0.0,
    )
    assert result.reynolds == pytest.approx(10938.11, rel=1e-4)
    assert result.prandtl == pytest.approx(5.42530, rel=1e-4)
    assert result.nusselt == pytest.approx(81.2029, rel=1e-4)
    assert result.heat_transfer_coefficient_w_m2_k == pytest.approx(16660.25, rel=1e-4)


@pytest.mark.parametrize(
    ("temperature_c", "salinity_g_kg"),
    [(-0.1, 38.0), (100.1, 38.0), (30.0, -0.1), (30.0, 160.1)],
)
def test_wyon_fluid_properties_reject_out_of_scope_inputs(temperature_c, salinity_g_kg):
    with pytest.raises(ValueError):
        wyon_fluid_properties(temperature_c, salinity_g_kg)



@pytest.mark.parametrize(
    ("temperature_c", "salinity_g_kg"),
    [(15.0, 38.0), (30.0, 5.0), (30.0, 151.0)],
)
def test_wyon_seawater_properties_enforce_source_correlation_ranges(
    temperature_c, salinity_g_kg
):
    with pytest.raises(ValueError):
        wyon_fluid_properties(temperature_c, salinity_g_kg)
