from dataclasses import replace

import pytest

from ai_water.md_channel import ChannelConfig
from ai_water.md_channel_countercurrent import simulate_countercurrent_dcmd_channel


def _config():
    return ChannelConfig(
        membrane_area_m2=10,
        membrane_permeance_kg_m2_h_bar=0.8,
        latent_heat_kwh_th_per_kg=0.65,
        membrane_thermal_conductivity_w_m_k=0.05,
        membrane_thickness_m=100e-6,
        feed_heat_transfer_coefficient_w_m2_k=1000,
        permeate_heat_transfer_coefficient_w_m2_k=1000,
        feed_mass_flow_kg_h=10_000,
        permeate_mass_flow_kg_h=10_000,
        feed_salinity_g_kg=0,
        duration_h=1,
        cells=20,
    )


def test_countercurrent_solver_converges_and_preserves_temperature_direction():
    result = simulate_countercurrent_dcmd_channel(
        config=_config(),
        feed_in_temperature_c=60,
        permeate_in_temperature_c=25,
    )
    assert result.freshwater_produced_kg > 0
    assert result.feed_out_temperature_c < 60
    assert result.permeate_out_temperature_c > 25
    assert all(c.feed_interface_temperature_c < c.feed_bulk_temperature_c for c in result.cells)
    assert all(c.permeate_interface_temperature_c > c.permeate_bulk_temperature_c for c in result.cells)


def test_countercurrent_boundary_temperatures_are_at_opposite_ends():
    result = simulate_countercurrent_dcmd_channel(
        config=_config(),
        feed_in_temperature_c=70,
        permeate_in_temperature_c=20,
    )
    assert result.cells[0].feed_bulk_temperature_c == pytest.approx(70)
    assert result.cells[-1].permeate_bulk_temperature_c == pytest.approx(20)
    assert result.feed_out_temperature_c > 20


def test_countercurrent_result_is_not_claimed_as_literature_validation():
    # This is a software invariant: the solver is an implementation capability,
    # not evidence that any external experimental benchmark has been reproduced.
    result = simulate_countercurrent_dcmd_channel(
        config=_config(),
        feed_in_temperature_c=60,
        permeate_in_temperature_c=25,
    )
    assert result.freshwater_produced_kg > 0


def test_countercurrent_bulk_temperatures_are_invariant_to_reporting_duration():
    short = simulate_countercurrent_dcmd_channel(
        config=_config(),
        feed_in_temperature_c=60,
        permeate_in_temperature_c=25,
    )
    long = simulate_countercurrent_dcmd_channel(
        config=replace(_config(), duration_h=3.0),
        feed_in_temperature_c=60,
        permeate_in_temperature_c=25,
    )

    assert long.feed_out_temperature_c == pytest.approx(short.feed_out_temperature_c)
    assert long.permeate_out_temperature_c == pytest.approx(short.permeate_out_temperature_c)
    assert long.feed_out_mass_kg_h == pytest.approx(short.feed_out_mass_kg_h)
    assert long.permeate_out_mass_kg_h == pytest.approx(short.permeate_out_mass_kg_h)
    assert long.freshwater_produced_kg == pytest.approx(
        3.0 * short.freshwater_produced_kg
    )
    assert long.hot_side_thermal_demand_kwh_th == pytest.approx(
        3.0 * short.hot_side_thermal_demand_kwh_th
    )


def test_countercurrent_feed_permeate_and_salt_mass_balances_close():
    config = replace(_config(), feed_salinity_g_kg=35.0)
    result = simulate_countercurrent_dcmd_channel(
        config=config,
        feed_in_temperature_c=60,
        permeate_in_temperature_c=25,
    )

    cell_area = config.membrane_area_m2 / config.cells
    product_rate = sum(cell.flux_kg_m2_h * cell_area for cell in result.cells)
    salt_mass_flow_in = config.feed_mass_flow_kg_h * config.feed_salinity_g_kg / 1000.0

    assert result.freshwater_produced_kg == pytest.approx(
        product_rate * config.duration_h, rel=1e-9
    )
    assert result.feed_out_mass_kg_h == pytest.approx(
        config.feed_mass_flow_kg_h - product_rate, rel=1e-9
    )
    assert result.permeate_out_mass_kg_h == pytest.approx(
        config.permeate_mass_flow_kg_h + product_rate, rel=1e-9
    )
    assert (
        result.feed_out_mass_kg_h * result.concentrate_salinity_g_kg / 1000.0
    ) == pytest.approx(salt_mass_flow_in, rel=1e-9)

    cumulative_product_rate = 0.0
    for cell in result.cells:
        expected_inlet_salinity = (
            salt_mass_flow_in
            / (config.feed_mass_flow_kg_h - cumulative_product_rate)
            * 1000.0
        )
        assert cell.feed_salinity_g_kg == pytest.approx(
            expected_inlet_salinity, rel=1e-9
        )
        cumulative_product_rate += cell.flux_kg_m2_h * cell_area


def test_countercurrent_cell_interface_energy_balances_close():
    config = _config()
    result = simulate_countercurrent_dcmd_channel(
        config=config,
        feed_in_temperature_c=60,
        permeate_in_temperature_c=25,
    )

    cell_area = config.membrane_area_m2 / config.cells
    for cell in result.cells:
        q_feed_kw = (
            config.feed_heat_transfer_coefficient_w_m2_k
            * (cell.feed_bulk_temperature_c - cell.feed_interface_temperature_c)
            * cell_area / 1000.0
        )
        q_permeate_kw = (
            config.permeate_heat_transfer_coefficient_w_m2_k
            * (cell.permeate_interface_temperature_c - cell.permeate_bulk_temperature_c)
            * cell_area / 1000.0
        )
        q_membrane_kw = (
            cell.membrane_latent_heat_kw + cell.membrane_conductive_heat_kw
        )

        assert cell.feed_heat_kw == pytest.approx(q_feed_kw, rel=1e-7, abs=1e-9)
        assert q_permeate_kw == pytest.approx(q_feed_kw, rel=1e-7, abs=1e-9)
        assert q_membrane_kw == pytest.approx(q_feed_kw, rel=1e-7, abs=1e-9)

    expected_integrated_feed_duty = (
        sum(cell.feed_heat_kw for cell in result.cells) * config.duration_h
    )
    assert result.hot_side_thermal_demand_kwh_th == pytest.approx(
        expected_integrated_feed_duty, rel=1e-7, abs=1e-9
    )
    assert result.hot_side_thermal_demand_kwh_th == pytest.approx(
        result.latent_duty_kwh_th + result.conductive_heat_leak_kwh_th,
        rel=1e-7,
        abs=1e-9,
    )
