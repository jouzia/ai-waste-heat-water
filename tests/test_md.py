from ai_water.md import (
    flux_kg_m2_h,
    interface_temperatures,
    mean_single_pass_salinity_g_kg,
    saturation_pressure_bar,
    vapor_pressure_driving_force_bar,
)


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
        saturation_pressure_bar(90)
    except ValueError:
        pass
    else:
        raise AssertionError("expected unsupported temperature range")


def test_single_pass_mean_salinity_increases_with_recovery():
    mean_0 = mean_single_pass_salinity_g_kg(35, 0.0)
    mean_20 = mean_single_pass_salinity_g_kg(35, 0.2)
    assert mean_0 == 35
    assert mean_20 > 35


def test_single_pass_mean_salinity_remains_below_concentrate_salinity():
    from ai_water.md import concentrate_salinity_g_kg

    mean_20 = mean_single_pass_salinity_g_kg(35, 0.2)
    concentrate = concentrate_salinity_g_kg(35, 0.2)
    assert 35 < mean_20 < concentrate


def test_iapws_seawater_activity_is_below_unity_and_salinity_reduces_it():
    from ai_water.md import seawater_water_activity

    fresh = seawater_water_activity(60, 0)
    seawater = seawater_water_activity(60, 35)
    assert 0 < seawater < 1
    assert abs(fresh - 1.0) < 1e-8
    assert seawater < fresh


def test_iapws_seawater_activity_rejects_out_of_range_salinity():
    from ai_water.md import seawater_water_activity

    try:
        seawater_water_activity(60, 121)
    except ValueError:
        pass
    else:
        raise AssertionError("expected IAPWS-08 salinity validation")
