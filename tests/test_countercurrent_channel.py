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
    assert result.feed_out_temperature_c > result.permeate_in_temperature_c


def test_countercurrent_result_is_not_claimed_as_literature_validation():
    # This is a software invariant: the solver is an implementation capability,
    # not evidence that any external experimental benchmark has been reproduced.
    result = simulate_countercurrent_dcmd_channel(
        config=_config(),
        feed_in_temperature_c=60,
        permeate_in_temperature_c=25,
    )
    assert result.freshwater_produced_kg > 0