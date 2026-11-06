import pytest

import ai_water.md_channel_countercurrent as countercurrent
from ai_water.channel_transport import concentration_polarization_coefficient
from ai_water.md_channel import ChannelConfig
from ai_water.md_channel_countercurrent import simulate_countercurrent_dcmd_channel


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
        "salt_mass_transfer_coefficient_m_s": 1e-4,
        "solvent_density_kg_m3": 1020.0,
    }
    values.update(overrides)
    return ChannelConfig(**values)


def test_countercurrent_cpc_is_consistent_with_final_cell_flux():
    result = simulate_countercurrent_dcmd_channel(
        config=_config(),
        feed_in_temperature_c=60.0,
        permeate_in_temperature_c=25.0,
    )

    for cell in result.cells:
        expected_cpc = concentration_polarization_coefficient(
            flux_kg_m2_s=cell.flux_kg_m2_h / 3600.0,
            mass_transfer_coefficient_m_s=1e-4,
            solvent_density_kg_m3=1020.0,
        )
        assert cell.concentration_polarization_coefficient == pytest.approx(
            expected_cpc, rel=1e-10
        )
        assert cell.interface_salinity_g_kg == pytest.approx(
            cell.feed_salinity_g_kg * expected_cpc, rel=1e-10
        )
        assert cell.interface_salinity_g_kg >= cell.feed_salinity_g_kg


def test_countercurrent_cpc_requires_positive_density():
    with pytest.raises(ValueError, match="solvent density"):
        simulate_countercurrent_dcmd_channel(
            config=_config(solvent_density_kg_m3=None),
            feed_in_temperature_c=60.0,
            permeate_in_temperature_c=25.0,
        )


def test_countercurrent_cpc_requires_positive_mass_transfer_coefficient():
    with pytest.raises(ValueError, match="mass-transfer coefficient"):
        simulate_countercurrent_dcmd_channel(
            config=_config(salt_mass_transfer_coefficient_m_s=0.0),
            feed_in_temperature_c=60.0,
            permeate_in_temperature_c=25.0,
        )


def test_countercurrent_solver_requires_positive_iteration_controls():
    with pytest.raises(ValueError, match="iteration limit"):
        simulate_countercurrent_dcmd_channel(
            config=_config(),
            feed_in_temperature_c=60.0,
            permeate_in_temperature_c=25.0,
            max_iterations=0,
        )
    with pytest.raises(ValueError, match="iteration limit"):
        simulate_countercurrent_dcmd_channel(
            config=_config(),
            feed_in_temperature_c=60.0,
            permeate_in_temperature_c=25.0,
            tolerance_c=0.0,
        )


def test_countercurrent_cpc_raises_if_inner_closure_does_not_converge(monkeypatch):
    calls = 0

    def oscillating_interfaces(**kwargs):
        nonlocal calls
        calls += 1
        flux = 1.0 if calls % 2 else 2.0
        return 50.0, 30.0, flux

    monkeypatch.setattr(countercurrent, "_cell_interfaces", oscillating_interfaces)

    with pytest.raises(
        RuntimeError,
        match="CPC/membrane-flux closure did not converge",
    ):
        simulate_countercurrent_dcmd_channel(
            config=_config(cells=1),
            feed_in_temperature_c=60.0,
            permeate_in_temperature_c=25.0,
        )
