import pytest

from ai_water.source_keshavarzzadeh import (
    source_mole_fraction_from_molarity,
    source_water_activity_from_molar_nacl,
    source_water_activity_from_mole_fraction,
)


def test_source_activity_accepts_molarity_via_explicit_mole_fraction_conversion():
    x = source_mole_fraction_from_molarity(1.67)
    from_molarity = source_water_activity_from_molar_nacl(1.67)
    from_fraction = source_water_activity_from_mole_fraction(x)

    assert 0 < x < 0.1
    assert from_molarity == pytest.approx(from_fraction)
    assert 0 < from_molarity < 1
