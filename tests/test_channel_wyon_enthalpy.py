from dataclasses import replace

import pytest

from ai_water.channel_enthalpy import advance_wyon_stream_enthalpy
from ai_water.md_channel import ChannelConfig, simulate_dcmd_channel
from ai_water.md_channel_countercurrent import simulate_countercurrent_dcmd_channel
from ai_water.wyon_2025_enthalpy import wyon_specific_enthalpy_j_kg


def _config(**overrides):
    values = {
        "membrane_area_m2": 2.0,
        "membrane_permeance_kg_m2_h_bar": 0.5,
        "latent_heat_kwh_th_per_kg": 0.65,
        "membrane_thermal_conductivity_w_m_k": 0.05,
        "membrane_thickness_m": 100e-6,
        "feed_heat_transfer_coefficient_w_m2_k": 1000.0,
        "permeate_heat_transfer_coefficient_w_m2_k": 1000.0,
        "feed_mass_flow_kg_h": 1000.0,
        "permeate_mass_flow_kg_h": 1000.0,
        "feed_salinity_g_kg": 35.0,
        "duration_h": 1.0,
        "cells": 5,
        "energy_balance_mode": "wyon_enthalpy",
    }
    values.update(overrides)
    return ChannelConfig(**values)


def _assert_cell_enthalpy_closure(result):
    for cell in result.cells:
        assert cell.feed_enthalpy_balance_residual_w is not None
        assert cell.permeate_enthalpy_balance_residual_w is not None
        assert cell.combined_enthalpy_balance_residual_w is not None
        assert abs(cell.feed_enthalpy_balance_residual_w) < 1e-8
        assert abs(cell.permeate_enthalpy_balance_residual_w) < 1e-8
        assert abs(cell.combined_enthalpy_balance_residual_w) < 1e-8


def test_wyon_stream_enthalpy_step_recovers_constant_mass_zero_flux_conduction():
    step = advance_wyon_stream_enthalpy(
        inlet_temperature_c=60.0,
        inlet_mass_flow_kg_h=1000.0,
        outlet_mass_flow_kg_h=1000.0,
        heat_transfer_w=100.0,
        salinity_in_g_kg=35.0,
        salinity_out_g_kg=35.0,
        direction="feed",
    )
    assert step.outlet_temperature_c < 60.0
    assert step.residual_w == pytest.approx(0.0, abs=1e-10)


def test_wyon_stream_enthalpy_step_rejects_invalid_mass_and_direction():
    with pytest.raises(ValueError, match="mass flow rates"):
        advance_wyon_stream_enthalpy(
            inlet_temperature_c=60.0,
            inlet_mass_flow_kg_h=1000.0,
            outlet_mass_flow_kg_h=0.0,
            heat_transfer_w=100.0,
            salinity_in_g_kg=35.0,
            salinity_out_g_kg=35.0,
            direction="feed",
        )
    with pytest.raises(ValueError, match="direction"):
        advance_wyon_stream_enthalpy(
            inlet_temperature_c=60.0,
            inlet_mass_flow_kg_h=1000.0,
            outlet_mass_flow_kg_h=1000.0,
            heat_transfer_w=100.0,
            salinity_in_g_kg=35.0,
            salinity_out_g_kg=35.0,
            direction="both",
        )


def test_co_current_wyon_enthalpy_mode_closes_each_cell_and_module_balances():
    result = simulate_dcmd_channel(
        config=_config(flow_arrangement="co_current"),
        feed_in_temperature_c=60.0,
        permeate_in_temperature_c=25.0,
    )
    _assert_cell_enthalpy_closure(result)
    assert result.freshwater_produced_kg > 0.0
    assert result.feed_out_mass_kg_h < 1000.0
    assert result.permeate_out_mass_kg_h > 1000.0
    assert result.feed_out_temperature_c < 60.0
    assert result.permeate_out_temperature_c > 25.0
    assert result.feed_out_mass_kg_h * result.concentrate_salinity_g_kg / 1000.0 == pytest.approx(
        35.0, rel=1e-8
    )


def test_countercurrent_wyon_enthalpy_mode_closes_each_cell_and_module_balances():
    result = simulate_countercurrent_dcmd_channel(
        config=_config(),
        feed_in_temperature_c=60.0,
        permeate_in_temperature_c=25.0,
    )
    _assert_cell_enthalpy_closure(result)
    assert result.freshwater_produced_kg > 0.0
    assert result.feed_out_mass_kg_h < 1000.0
    assert result.permeate_out_mass_kg_h > 1000.0
    assert result.feed_out_temperature_c < 60.0
    assert result.permeate_out_temperature_c > 25.0


def test_main_countercurrent_wyon_enthalpy_mode_closes_each_cell():
    result = simulate_dcmd_channel(
        config=_config(flow_arrangement="counter_current"),
        feed_in_temperature_c=60.0,
        permeate_in_temperature_c=25.0,
    )
    _assert_cell_enthalpy_closure(result)


def test_wyon_enthalpy_mode_is_invariant_to_reporting_duration():
    base = _config()
    short = simulate_countercurrent_dcmd_channel(
        config=base,
        feed_in_temperature_c=60.0,
        permeate_in_temperature_c=25.0,
    )
    long = simulate_countercurrent_dcmd_channel(
        config=replace(base, duration_h=3.0),
        feed_in_temperature_c=60.0,
        permeate_in_temperature_c=25.0,
    )
    assert long.feed_out_temperature_c == pytest.approx(short.feed_out_temperature_c, abs=1e-8)
    assert long.permeate_out_temperature_c == pytest.approx(short.permeate_out_temperature_c, abs=1e-8)
    assert long.feed_out_mass_kg_h == pytest.approx(short.feed_out_mass_kg_h, rel=1e-8)
    assert long.permeate_out_mass_kg_h == pytest.approx(short.permeate_out_mass_kg_h, rel=1e-8)
    assert long.freshwater_produced_kg == pytest.approx(3.0 * short.freshwater_produced_kg, rel=1e-8)



def _assert_independent_global_enthalpy_identity(result):
    feed_h_in = wyon_specific_enthalpy_j_kg(60.0, 35.0)
    permeate_h_in = wyon_specific_enthalpy_j_kg(25.0, 0.0)
    feed_h_out = wyon_specific_enthalpy_j_kg(
        result.feed_out_temperature_c, result.concentrate_salinity_g_kg
    )
    permeate_h_out = wyon_specific_enthalpy_j_kg(
        result.permeate_out_temperature_c, 0.0
    )
    inlet_enthalpy_rate = 1000.0 * feed_h_in + 1000.0 * permeate_h_in
    outlet_enthalpy_rate = (
        result.feed_out_mass_kg_h * feed_h_out
        + result.permeate_out_mass_kg_h * permeate_h_out
    )
    assert outlet_enthalpy_rate == pytest.approx(
        inlet_enthalpy_rate, rel=1e-10, abs=1e-4
    )


def test_co_current_wyon_mode_satisfies_independent_module_enthalpy_identity():
    result = simulate_dcmd_channel(
        config=_config(flow_arrangement="co_current"),
        feed_in_temperature_c=60.0,
        permeate_in_temperature_c=25.0,
    )
    _assert_independent_global_enthalpy_identity(result)


def test_countercurrent_wyon_mode_satisfies_independent_module_enthalpy_identity():
    result = simulate_countercurrent_dcmd_channel(
        config=_config(),
        feed_in_temperature_c=60.0,
        permeate_in_temperature_c=25.0,
    )
    _assert_independent_global_enthalpy_identity(result)


def test_main_countercurrent_wyon_mode_satisfies_independent_module_enthalpy_identity():
    result = simulate_dcmd_channel(
        config=_config(flow_arrangement="counter_current"),
        feed_in_temperature_c=60.0,
        permeate_in_temperature_c=25.0,
    )
    _assert_independent_global_enthalpy_identity(result)
