from ai_water.md import flux_kg_m2_h, interface_temperatures, saturation_pressure_bar, vapor_pressure_driving_force_bar

def test_saturation_pressure_increases_with_temperature():
    assert saturation_pressure_bar(60) > saturation_pressure_bar(40)

def test_interface_temperatures_reduce_bulk_delta():
    hot, cold = interface_temperatures(70, 25, 0.7)
    assert hot < 70
    assert cold > 25
    assert hot > cold

def test_activity_reduces_vapor_pressure_driving_force():
    pure = vapor_pressure_driving_force_bar(60, 25, 1.0)
    saline = vapor_pressure_driving_force_bar(60, 25, 0.9)
    assert saline < pure

def test_flux_increases_with_permeance():
    low = flux_kg_m2_h(60, 25, 1.0)
    high = flux_kg_m2_h(60, 25, 2.0)
    assert high == 2 * low

def test_outside_nist_range_is_rejected():
    try:
        saturation_pressure_bar(20)
    except ValueError:
        pass
    else:
        raise AssertionError("expected unsupported temperature range")
