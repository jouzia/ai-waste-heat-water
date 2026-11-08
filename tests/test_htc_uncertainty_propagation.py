from ai_water.md_channel import _cell_interfaces
from scripts.run_htc_uncertainty_propagation import (
    BASE_HTC_W_M2_K,
    CELLS,
    FACTORS,
    GRID,
    MODES,
    OUTPUTS,
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


def test_interface_solver_keeps_interfaces_between_bulk_streams():
    feed_interface, permeate_interface, flux = _cell_interfaces(
        feed_bulk_c=70.0,
        permeate_bulk_c=20.0,
        feed_h=750.0,
        permeate_h=250.0,
        membrane_k=0.0551,
        membrane_thickness_m=110e-6,
        latent_heat_kwh_per_kg=0.67,
        permeance=100.0,
        water_activity=0.98,
    )
    assert 20.0 <= permeate_interface <= feed_interface <= 70.0
    assert flux >= 0.0
