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
    assert value > 0
    assert value < 1e-3


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
    assert nu > 0
    assert alpha > 0


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
