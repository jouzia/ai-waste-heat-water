from __future__ import annotations

import pytest

from ai_water.sharqawy_2010 import (
    its90_to_ipts68_kelvin,
    jamieson_seawater_cp_j_kg_k,
    pure_water_cp_j_kg_k,
    pure_water_latent_heat_j_kg,
    reference_to_practical_salinity_g_kg,
    seawater_latent_heat_j_kg,
)


def test_temperature_scale_conversion_matches_sharqawy_eq4():
    t90_k = 293.15
    t68_k = its90_to_ipts68_kelvin(t90_k)
    assert t90_k == pytest.approx(t68_k - 0.00025 * (t68_k - 273.15))


def test_salinity_conversion_matches_sharqawy_eq3():
    assert reference_to_practical_salinity_g_kg(35.0) == pytest.approx(
        35.0 / 1.00472
    )


def test_jamieson_cp_is_finite_and_in_expected_physical_range():
    cp = jamieson_seawater_cp_j_kg_k(20.0, 35.0)
    assert 3900.0 < cp < 4200.0


def test_jamieson_cp_rejects_zero_salinity_outside_published_fit_range():
    with pytest.raises(ValueError, match="0 < S_P"):
        jamieson_seawater_cp_j_kg_k(20.0, 0.0)


def test_pure_water_cp_at_atmospheric_pressure_is_finite():
    cp = pure_water_cp_j_kg_k(20.0, pressure_mpa=0.101325)
    assert 4100.0 < cp < 4300.0


def test_pure_water_latent_heat_matches_eq54_scale():
    assert pure_water_latent_heat_j_kg(20.0) == pytest.approx(
        2.453e6, rel=0.01
    )


def test_seawater_latent_heat_is_solution_mass_basis():
    water_basis = pure_water_latent_heat_j_kg(60.0)
    seawater_basis = seawater_latent_heat_j_kg(60.0, 35.0)
    assert seawater_basis == pytest.approx(water_basis * 0.965)
    assert seawater_basis < water_basis


@pytest.mark.parametrize(
    ("temperature", "salinity"),
    [(-0.1, 35.0), (20.0, -1.0), (20.0, 181.0), (200.1, 35.0)],
)
def test_property_correlations_reject_out_of_range_inputs(temperature, salinity):
    with pytest.raises(ValueError):
        jamieson_seawater_cp_j_kg_k(temperature, salinity)
