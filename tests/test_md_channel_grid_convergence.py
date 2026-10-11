import pytest

from ai_water.md_channel import ChannelConfig, simulate_dcmd_channel


def _countercurrent_config(cells: int) -> ChannelConfig:
    return ChannelConfig(
        membrane_area_m2=0.23088,
        membrane_permeance_kg_m2_h_bar=100.0,
        latent_heat_kwh_th_per_kg=0.67,
        membrane_thermal_conductivity_w_m_k=0.0551,
        membrane_thickness_m=110e-6,
        feed_heat_transfer_coefficient_w_m2_k=500.0,
        permeate_heat_transfer_coefficient_w_m2_k=500.0,
        feed_mass_flow_kg_h=60.0,
        permeate_mass_flow_kg_h=60.0,
        feed_cp_kj_kg_k=4.18,
        permeate_cp_kj_kg_k=4.18,
        feed_salinity_g_kg=4.0,
        water_activity_override=0.9981,
        cells=cells,
        duration_h=1.0,
        flow_arrangement="counter_current",
    )


def test_countercurrent_solver_converges_at_32_cells() -> None:
    config = _countercurrent_config(cells=32)

    result = simulate_dcmd_channel(
        config=config,
        feed_in_temperature_c=40.6,
        permeate_in_temperature_c=19.9,
    )

    assert len(result.cells) == 32
    assert result.freshwater_produced_kg > 0
    assert result.feed_out_mass_kg_h < config.feed_mass_flow_kg_h
    assert (
        config.feed_mass_flow_kg_h - result.feed_out_mass_kg_h
    ) == pytest.approx(result.freshwater_produced_kg, rel=1e-6, abs=1e-8)


def test_countercurrent_energy_balance_closes_at_32_cells() -> None:
    config = _countercurrent_config(cells=32)

    result = simulate_dcmd_channel(
        config=config,
        feed_in_temperature_c=40.6,
        permeate_in_temperature_c=19.9,
    )

    accounted_heat = result.latent_duty_kwh_th + result.conductive_heat_leak_kwh_th
    assert result.hot_side_thermal_demand_kwh_th == pytest.approx(
        accounted_heat, rel=1e-6, abs=1e-8
    )
