import pytest

from ai_water.md import saturation_pressure_bar, vapor_pressure_driving_force_bar

def test_water_vapor_pressure_increases_with_temperature():
    assert saturation_pressure_bar(60.0) > saturation_pressure_bar(40.0)

def test_driving_force_is_positive_for_hotter_feed():
    assert vapor_pressure_driving_force_bar(60.0, 25.0) > 0.0

def test_outside_validated_range_is_rejected():
    with pytest.raises(ValueError):
        saturation_pressure_bar(20.0)
