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



@pytest.mark.parametrize(
    (
        "feed_temperature_c",
        "pore_radius_m",
        "expected_mass_flux_kg_m2_h",
        "expected_heat_flux_w_m2",
    ),
    [
        (40.0, 0.11e-6, 6.0426300, 10299.6821),
        (40.0, 0.22e-6, 7.4243725, 11235.3444),
        (50.0, 0.11e-6, 12.0651391, 17548.3973),
        (50.0, 0.22e-6, 14.8692193, 19457.9955),
        (60.0, 0.11e-6, 21.3128114, 27055.9146),
        (60.0, 0.22e-6, 26.3387134, 30496.8995),
        (70.0, 0.11e-6, 35.0343195, 39710.0022),
        (70.0, 0.22e-6, 43.4031388, 45469.1116),
    ],
)
def test_initial_pvdf_setup_pore_radius_interpretation_sensitivity(
    feed_temperature_c,
    pore_radius_m,
    expected_mass_flux_kg_m2_h,
    expected_heat_flux_w_m2,
):
    result = _solve_coupled_case(
        feed_bulk_temperature_c=feed_temperature_c,
        permeate_bulk_temperature_c=20.0,
        feed_velocity_m_s=1.85,
        permeate_velocity_m_s=2.92,
        hydraulic_diameter_m=0.003,
        channel_length_m=0.1,
        feed_salinity_sr_g_kg=38.0,
        membrane_thermal_conductivity_w_m_k=0.041,
        membrane_thickness_m=126e-6,
        pore_radius_m=pore_radius_m,
        porosity=0.75,
    )
    assert result.fixed_point_residual_c <= 1e-8
    assert result.surface.mass_flux_kg_m2_h == pytest.approx(
        expected_mass_flux_kg_m2_h, rel=1e-5
    )
    assert result.surface.heat_flux_w_m2 == pytest.approx(
        expected_heat_flux_w_m2, rel=1e-5
    )


@pytest.mark.parametrize(
    (
        "feed_temperature_c",
        "expected_heat_flux_15g_kg",
        "expected_heat_flux_35g_kg",
        "expected_mass_flux_15g_kg_h",
        "expected_mass_flux_35g_kg_h",
    ),
    [
        (40.0, 10311.3304, 10301.2477, 6.0513386, 6.0438003),
        (50.0, 17572.5629, 17551.6324, 12.0869743, 12.0680616),
        (60.0, 27102.5556, 27062.1381, 21.3609056, 21.3192275),
        (70.0, 39796.8952, 39721.5670, 35.1323803, 35.0473682),
    ],
)
def test_wyon_pure_water_vapour_baseline_has_weak_salinity_sensitivity(
    feed_temperature_c,
    expected_heat_flux_15g_kg,
    expected_heat_flux_35g_kg,
    expected_mass_flux_15g_kg_h,
    expected_mass_flux_35g_kg_h,
):
    common = {
        "feed_bulk_temperature_c": feed_temperature_c,
        "permeate_bulk_temperature_c": 20.0,
        "feed_velocity_m_s": 1.85,
        "permeate_velocity_m_s": 2.92,
        "hydraulic_diameter_m": 0.003,
        "channel_length_m": 0.1,
        "membrane_thermal_conductivity_w_m_k": 0.041,
        "membrane_thickness_m": 126e-6,
        "pore_radius_m": 0.11e-6,
        "porosity": 0.75,
    }
    lower_salinity = solve_wyon_coupled_channel_surface(
        **common, feed_salinity_sr_g_kg=15.0
    )
    high_salinity = solve_wyon_coupled_channel_surface(
        **common, feed_salinity_sr_g_kg=35.0
    )
    assert lower_salinity.surface.heat_flux_w_m2 == pytest.approx(
        expected_heat_flux_15g_kg, rel=1e-5
    )
    assert high_salinity.surface.heat_flux_w_m2 == pytest.approx(
        expected_heat_flux_35g_kg, rel=1e-5
    )
    assert lower_salinity.surface.mass_flux_kg_m2_h == pytest.approx(
        expected_mass_flux_15g_kg_h, rel=1e-5
    )
    assert high_salinity.surface.mass_flux_kg_m2_h == pytest.approx(
        expected_mass_flux_35g_kg_h, rel=1e-5
    )
    heat_flux_change = abs(
        high_salinity.surface.heat_flux_w_m2
        / lower_salinity.surface.heat_flux_w_m2
        - 1.0
    )
    mass_flux_change = abs(
        high_salinity.surface.mass_flux_kg_m2_h
        / lower_salinity.surface.mass_flux_kg_m2_h
        - 1.0
    )
    assert heat_flux_change < 0.005
    assert mass_flux_change < 0.005



def test_nayar_mode_reduces_flux_with_increasing_feed_salinity():
    common = {
        "feed_bulk_temperature_c": 60.0,
        "permeate_bulk_temperature_c": 20.0,
        "feed_velocity_m_s": 1.85,
        "permeate_velocity_m_s": 2.92,
        "hydraulic_diameter_m": 0.003,
        "channel_length_m": 0.1,
        "membrane_thermal_conductivity_w_m_k": 0.041,
        "membrane_thickness_m": 126e-6,
        "pore_radius_m": 0.11e-6,
        "porosity": 0.75,
        "vapour_pressure_model": "nayar_2016",
    }
    lower_salinity = solve_wyon_coupled_channel_surface(
        **common, feed_salinity_sr_g_kg=15.0
    )
    seawater_salinity = solve_wyon_coupled_channel_surface(
        **common, feed_salinity_sr_g_kg=38.0
    )
    assert lower_salinity.surface.mass_flux_kg_m2_h > (
        seawater_salinity.surface.mass_flux_kg_m2_h
    )
    assert lower_salinity.surface.heat_flux_w_m2 > (
        seawater_salinity.surface.heat_flux_w_m2
    )
    assert seawater_salinity.surface.vapour_pressure_feed_pa < (
        lower_salinity.surface.vapour_pressure_feed_pa
    )
    assert seawater_salinity.surface.energy_balance_residual_w_m2 == pytest.approx(
        0.0, abs=1e-7
    )


def test_nayar_mode_requires_explicit_feed_salinity_in_surface_solver():
    from ai_water.wyon_2025_surface_reference import solve_wyon_membrane_surfaces

    with pytest.raises(ValueError, match="feed_salinity_sr_g_kg is required"):
        solve_wyon_membrane_surfaces(
            feed_bulk_temperature_c=60.0,
            permeate_bulk_temperature_c=20.0,
            feed_heat_transfer_coefficient_w_m2_k=5000.0,
            permeate_heat_transfer_coefficient_w_m2_k=5000.0,
            membrane_thermal_conductivity_w_m_k=0.041,
            membrane_thickness_m=126e-6,
            pore_radius_m=0.11e-6,
            porosity=0.75,
            vapour_pressure_model="nayar_2016",
        )
