from scripts.run_htc_uncertainty_propagation import (
    BASE_HTC_W_M2_K, CELLS, FACTORS, GRID, MODES, OUTPUTS, run,
)


def test_design_is_complete_and_symmetric():
    assert len(FACTORS) == 5
    assert FACTORS[2] == 1.0
    assert len(GRID) == 12 * 2 * 25
    assert CELLS == 80
    assert BASE_HTC_W_M2_K == 500.0
    assert set(MODES) == {"sensible_cp", "wyon_enthalpy"}
    assert "feed_out_temperature_c" in OUTPUTS


def test_temperature_percentages_are_not_reported():
    assert all(name.endswith("_temperature_c") for name in OUTPUTS if "temperature" in name)
