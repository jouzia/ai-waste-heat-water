import pytest

from ai_water.wyon_2025_coupled_channel_surface import (
    solve_wyon_coupled_channel_surface,
)
from ai_water.wyon_2025_module_outlets import solve_wyon_lumped_module_outlets


def _coupled_surface():
    return solve_wyon_coupled_channel_surface(
        feed_bulk_temperature_c=60.0,
        permeate_bulk_temperature_c=25.0,
        feed_velocity_m_s=1.85,
        permeate_velocity_m_s=2.92,
        hydraulic_diameter_m=0.003,
        channel_length_m=0.1,
        feed_salinity_sr_g_kg=38.0,
        membrane_thermal_conductivity_w_m_k=0.031,
        membrane_thickness_m=77e-6,
        pore_radius_m=0.225e-6,
        porosity=0.89,
    )


def _module_outlets(**overrides):
    parameters = {
        "surface_result": _coupled_surface(),
        "feed_inlet_temperature_c": 60.0,
        "permeate_inlet_temperature_c": 25.0,
        "feed_salinity_sr_g_kg": 38.0,
        "feed_velocity_m_s": 1.85,
        "permeate_velocity_m_s": 2.92,
        "channel_width_m": 0.05,
        "channel_height_m": 0.005,
        "membrane_area_m2": 0.1,
    }
    parameters.update(overrides)
    return solve_wyon_lumped_module_outlets(**parameters)


def test_wyon_module_outlet_balances_conserve_water_and_salt():
    result = _module_outlets()

    assert result.feed_outlet_mass_flow_kg_s == pytest.approx(
        result.feed_inlet_mass_flow_kg_s
        - result.transferred_water_mass_flow_kg_s,
        abs=1e-12,
    )
    assert result.permeate_outlet_mass_flow_kg_s == pytest.approx(
        result.permeate_inlet_mass_flow_kg_s
        + result.transferred_water_mass_flow_kg_s,
        abs=1e-12,
    )
    assert result.salt_mass_balance_residual_kg_s <= 1e-12
    assert result.equation_20_salt_balance_residual_kg_s <= 1e-12


def test_wyon_module_outlet_balances_close_both_enthalpy_rates():
    result = _module_outlets()

    assert result.feed_outlet_temperature_c < 60.0
    assert result.permeate_outlet_temperature_c > 25.0
    assert result.feed_heat_loss_w == pytest.approx(
        result.heat_transfer_rate_w, abs=1e-8
    )
    assert result.permeate_heat_gain_w == pytest.approx(
        result.heat_transfer_rate_w, abs=1e-8
    )
    assert result.energy_balance_residual_w <= 1e-8


def test_wyon_module_outlet_salinity_increases_when_water_is_removed():
    result = _module_outlets()
    assert result.feed_outlet_salinity_sr_g_kg > 38.0
    assert result.feed_outlet_salinity_sr_g_kg < 40.0


def test_wyon_module_outlet_rejects_water_transfer_that_exhausts_feed_flow():
    with pytest.raises(ValueError, match="exhausts the feed mass flow"):
        _module_outlets(membrane_area_m2=1e6)


@pytest.mark.parametrize(
    "invalid",
    [
        {"channel_width_m": 0.0},
        {"channel_height_m": -0.005},
        {"membrane_area_m2": 0.0},
        {"feed_velocity_m_s": 0.0},
        {"permeate_velocity_m_s": -1.0},
    ],
)
def test_wyon_module_outlet_validates_geometry_and_flow_inputs(invalid):
    with pytest.raises(ValueError):
        _module_outlets(**invalid)
