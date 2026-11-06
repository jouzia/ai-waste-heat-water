import pytest

from ai_water.wyon_2025_enthalpy import (
    wyon_pure_water_specific_enthalpy_j_kg,
    wyon_seawater_specific_enthalpy_j_kg,
    wyon_specific_enthalpy_j_kg,
    wyon_temperature_from_specific_enthalpy_c,
)


def test_wyon_pure_water_enthalpy_reference():
    assert wyon_pure_water_specific_enthalpy_j_kg(20.0) == pytest.approx(84000.755)


def test_wyon_seawater_enthalpy_reference():
    assert wyon_seawater_specific_enthalpy_j_kg(20.0, 38.0) == pytest.approx(79461.11443936)


def test_wyon_enthalpy_inverse_round_trip():
    h = wyon_specific_enthalpy_j_kg(60.0, 38.0)
    t = wyon_temperature_from_specific_enthalpy_c(h, 38.0)
    assert t == pytest.approx(60.0, abs=1e-8)
