import math

import pytest

from ai_water.nayar_2016_vapour_pressure import (
    nayar_natural_seawater_vapour_pressure_pa,
    nayar_pure_water_vapour_pressure_pa,
)


@pytest.mark.parametrize(
    ("temperature_c", "expected_pa"),
    [
        (0.0, 611.8710397),
        (20.0, 2341.216993),
        (40.0, 7390.799274),
        (60.0, 19962.94809),
        (80.0, 47455.94515),
        (100.0, 101511.2377),
    ],
)
def test_nayar_pure_water_reference_values(temperature_c, expected_pa):
    assert nayar_pure_water_vapour_pressure_pa(temperature_c) == pytest.approx(
        expected_pa, rel=2e-8
    )


def test_nayar_natural_seawater_salinity_factor_at_38_g_kg():
    pure = nayar_pure_water_vapour_pressure_pa(60.0)
    seawater = nayar_natural_seawater_vapour_pressure_pa(60.0, 38.0)
    expected_ratio = math.exp(-4.58180e-4 * 38.0 - 2.04430e-6 * 38.0**2)
    assert expected_ratio == pytest.approx(0.9798431127144791, rel=1e-12)
    assert seawater / pure == pytest.approx(expected_ratio, rel=1e-12)
    assert seawater == pytest.approx(19560.55719, rel=1e-8)


def test_nayar_zero_salinity_reduces_to_pure_water():
    for temperature_c in (0.0, 40.0, 100.0, 180.0):
        assert nayar_natural_seawater_vapour_pressure_pa(
            temperature_c, 0.0
        ) == pytest.approx(nayar_pure_water_vapour_pressure_pa(temperature_c))


@pytest.mark.parametrize("temperature_c", [-0.01, 180.01, float("nan"), float("inf")])
def test_nayar_rejects_temperature_outside_validity_domain(temperature_c):
    with pytest.raises(ValueError):
        nayar_pure_water_vapour_pressure_pa(temperature_c)


@pytest.mark.parametrize("salinity", [-0.01, 160.01, float("nan"), float("inf")])
def test_nayar_rejects_salinity_outside_validity_domain(salinity):
    with pytest.raises(ValueError):
        nayar_natural_seawater_vapour_pressure_pa(40.0, salinity)
