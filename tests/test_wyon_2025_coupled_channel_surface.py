import pytest

from ai_water.wyon_2025_coupled_channel_surface import (
    solve_wyon_coupled_channel_surface,
)


def _solve_coupled_case(**overrides):
    parameters = {
        "feed_bulk_temperature_c": 60.0,
        "permeate_bulk_temperature_c": 25.0,
        "feed_velocity_m_s": 1.85,
        "permeate_velocity_m_s": 2.92,
        "hydraulic_diameter_m": 0.003,
        "channel_length_m": 0.1,
        "feed_salinity_sr_g_kg": 38.0,
        "membrane_thermal_conductivity_w_m_k": 0.031,
        "membrane_thickness_m": 77e-6,
        "pore_radius_m": 0.225e-6,
        "porosity": 0.89,
    }
    parameters.update(overrides)
    return solve_wyon_coupled_channel_surface(**parameters)


def test_coupled_wyon_surface_solver_converges_on_local_mean_fluid_temperatures():
    result = _solve_coupled_case()

    expected_feed_mean = 0.5 * (
        60.0 + result.surface.feed_interface_temperature_c
    )
    expected_permeate_mean = 0.5 * (
        25.0 + result.surface.permeate_interface_temperature_c
    )
    assert result.iterations > 1
    assert result.fixed_point_residual_c <= 1e-8
    assert result.feed_mean_fluid_temperature_c == pytest.approx(
        expected_feed_mean, abs=1e-8
    )
    assert result.permeate_mean_fluid_temperature_c == pytest.approx(
        expected_permeate_mean, abs=1e-8
    )


def test_coupled_wyon_surface_solver_closes_energy_balance():
    result = _solve_coupled_case()
    surface = result.surface

    assert surface.feed_interface_temperature_c > surface.permeate_interface_temperature_c
    assert surface.mass_flux_kg_m2_s > 0
    assert surface.energy_balance_residual_w_m2 == pytest.approx(0.0, abs=1e-7)
    assert surface.feed_convective_heat_flux_w_m2 == pytest.approx(
        surface.permeate_convective_heat_flux_w_m2, abs=1e-6
    )
    assert surface.heat_flux_w_m2 == pytest.approx(
        surface.latent_heat_flux_w_m2 + surface.conductive_heat_flux_w_m2,
        abs=1e-6,
    )


def test_coupled_wyon_surface_solver_reports_nonconvergence():
    with pytest.raises(RuntimeError, match="did not converge"):
        _solve_coupled_case(max_iterations=1)


@pytest.mark.parametrize(
    ("relaxation", "temperature_tolerance_c", "max_iterations"),
    [(0.0, 1e-8, 100), (1.1, 1e-8, 100), (0.5, 0.0, 100), (0.5, 1e-8, 0)],
)
def test_coupled_wyon_surface_solver_validates_iteration_controls(
    relaxation, temperature_tolerance_c, max_iterations
):
    with pytest.raises(ValueError):
        _solve_coupled_case(
            relaxation=relaxation,
            temperature_tolerance_c=temperature_tolerance_c,
            max_iterations=max_iterations,
        )
