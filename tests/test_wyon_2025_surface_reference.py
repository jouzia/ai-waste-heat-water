import pytest

from ai_water.wyon_2025_surface_reference import (
    solve_wyon_membrane_surfaces,
    wyon_convective_heat_transfer_coefficient_w_m2_k,
    wyon_mass_transfer_coefficient_kg_m2_s_pa,
    wyon_nusselt_number,
    wyon_pure_water_vapour_pressure_pa,
    wyon_tortuosity,
)


@pytest.mark.parametrize(
    ("temperature_c", "expected_kpa"),
    [(40, 7.76733644), (60, 21.05325909), (80, 50.22266550), (100, 107.80480593)],
)
def test_wyon_vapour_pressure_matches_transcribed_equation(temperature_c, expected_kpa):
    assert wyon_pure_water_vapour_pressure_pa(temperature_c) / 1000 == pytest.approx(
        expected_kpa, rel=1e-8
    )


def test_wyon_tortuosity_matches_equation_16():
    assert wyon_tortuosity(0.89) == pytest.approx((2 - 0.89) ** 2 / 0.89)


def test_wyon_mass_transfer_coefficient_is_positive_and_finite():
    value = wyon_mass_transfer_coefficient_kg_m2_s_pa(
        mean_membrane_temperature_k=323.15,
        pore_radius_m=0.225e-6,
        membrane_thickness_m=77e-6,
        porosity=0.89,
    )
    temperature_k = 323.15
    pore_radius_m = 0.225e-6
    membrane_thickness_m = 77e-6
    porosity = 0.89
    tau = (2.0 - porosity) ** 2 / porosity
    vapour_pressure_pa = wyon_pure_water_vapour_pressure_pa(temperature_k - 273.15)
    air_pressure_pa = 100000.0 - vapour_pressure_pa
    diffusion_pressure_product = 1.895e-5 * temperature_k**2.072
    knudsen = (
        (2.0 * pore_radius_m * porosity)
        / (3.0 * tau * membrane_thickness_m)
        * (8.0 * 0.01801528 / (3.141592653589793 * 8.314462618 * temperature_k)) ** 0.5
    )
    molecular = (
        porosity
        * 0.01801528
        * diffusion_pressure_product
        / (tau * membrane_thickness_m * 8.314462618 * temperature_k * air_pressure_pa)
    )
    expected = 1.0 / (1.0 / knudsen + 1.0 / molecular)
    assert value == pytest.approx(expected, rel=1e-12)
    assert value > 0
    assert value < min(knudsen, molecular)


def test_wyon_nusselt_and_film_coefficient():
    nu = wyon_nusselt_number(
        reynolds=12000,
        prandtl=6.0,
        hydraulic_diameter_m=0.004,
        channel_length_m=0.5,
    )
    alpha = wyon_convective_heat_transfer_coefficient_w_m2_k(
        nusselt=nu,
        fluid_thermal_conductivity_w_m_k=0.6,
        hydraulic_diameter_m=0.004,
    )
    expected_nu = 0.023 * (1.0 + 6.0 * 0.004 / 0.5) * 12000**0.8 * 6.0 ** (1.0 / 3.0)
    assert nu == pytest.approx(expected_nu)
    assert alpha == pytest.approx(expected_nu * 0.6 / 0.004)


def test_coupled_surface_solver_closes_heat_flux_and_keeps_interfaces_ordered():
    result = solve_wyon_membrane_surfaces(
        feed_bulk_temperature_c=60,
        permeate_bulk_temperature_c=25,
        feed_heat_transfer_coefficient_w_m2_k=5000,
        permeate_heat_transfer_coefficient_w_m2_k=5000,
        membrane_thermal_conductivity_w_m_k=0.031,
        membrane_thickness_m=77e-6,
        pore_radius_m=0.225e-6,
        porosity=0.89,
    )
    assert 25 < result.permeate_interface_temperature_c
    assert result.permeate_interface_temperature_c < result.feed_interface_temperature_c
    assert result.feed_interface_temperature_c < 60
    assert result.mass_flux_kg_m2_s > 0
    assert result.membrane_mass_transfer_coefficient_kg_m2_s_pa > 0
    assert result.feed_convective_heat_flux_w_m2 == pytest.approx(
        result.permeate_convective_heat_flux_w_m2, abs=1e-6
    )
    assert result.heat_flux_w_m2 == pytest.approx(
        result.latent_heat_flux_w_m2 + result.conductive_heat_flux_w_m2, abs=1e-6
    )
    assert abs(result.energy_balance_residual_w_m2) <= 1e-7


def test_surface_solver_handles_invalid_zero_flux_endpoint_with_unequal_films():
    result = solve_wyon_membrane_surfaces(
        feed_bulk_temperature_c=100,
        permeate_bulk_temperature_c=96,
        feed_heat_transfer_coefficient_w_m2_k=2000,
        permeate_heat_transfer_coefficient_w_m2_k=8000,
        membrane_thermal_conductivity_w_m_k=0.031,
        membrane_thickness_m=77e-6,
        pore_radius_m=0.225e-6,
        porosity=0.89,
    )
    interface_mean_k = (
        0.5 * (result.feed_interface_temperature_c + result.permeate_interface_temperature_c)
        + 273.15
    )
    assert result.mean_membrane_temperature_k == pytest.approx(interface_mean_k)
    assert result.membrane_mass_transfer_coefficient_kg_m2_s_pa == pytest.approx(
        wyon_mass_transfer_coefficient_kg_m2_s_pa(
            mean_membrane_temperature_k=interface_mean_k,
            pore_radius_m=0.225e-6,
            membrane_thickness_m=77e-6,
            porosity=0.89,
        )
    )
    assert result.energy_balance_residual_w_m2 == pytest.approx(0.0, abs=1e-7)


def test_surface_solver_rejects_nonpositive_temperature_driving_force():
    with pytest.raises(ValueError, match="feed bulk temperature"):
        solve_wyon_membrane_surfaces(
            feed_bulk_temperature_c=25,
            permeate_bulk_temperature_c=60,
            feed_heat_transfer_coefficient_w_m2_k=5000,
            permeate_heat_transfer_coefficient_w_m2_k=5000,
            membrane_thermal_conductivity_w_m_k=0.031,
            membrane_thickness_m=77e-6,
            pore_radius_m=0.225e-6,
            porosity=0.89,
        )



@pytest.mark.parametrize(
    ("feed_temperature_c", "permeate_temperature_c", "invalid_name"),
    [
        (-1.0, -5.0, "feed_bulk_temperature_c"),
        (101.0, 25.0, "feed_bulk_temperature_c"),
        (60.0, -0.1, "permeate_bulk_temperature_c"),
    ],
)
def test_surface_solver_rejects_bulk_temperatures_outside_vapour_pressure_domain(
    feed_temperature_c, permeate_temperature_c, invalid_name
):
    with pytest.raises(ValueError, match=invalid_name):
        solve_wyon_membrane_surfaces(
            feed_bulk_temperature_c=feed_temperature_c,
            permeate_bulk_temperature_c=permeate_temperature_c,
            feed_heat_transfer_coefficient_w_m2_k=5000,
            permeate_heat_transfer_coefficient_w_m2_k=5000,
            membrane_thermal_conductivity_w_m_k=0.031,
            membrane_thickness_m=77e-6,
            pore_radius_m=0.225e-6,
            porosity=0.89,
        )
