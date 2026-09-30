import pytest

from ai_water.source_keshavarzzadeh_runner import (
    SourceRunnerConfig,
    source_cell_area,
    source_membrane_conductivity,
    source_membrane_flux_kg_m2_s,
    source_pure_vapor_pressure_pa,
    source_vapor_pressure_pa,
)


def config():
    return SourceRunnerConfig(
        membrane_thickness_m=60e-6,
        pore_radius_m=0.1e-6,
        porosity=0.8,
        tortuosity=1.25,
        channel_area_m2=0.00315,
        membrane_area_m2=0.00337,
        cells=20,
    )


def test_source_flux_is_positive_for_hot_pure_feed():
    c = config()
    flux = source_membrane_flux_kg_m2_s(
        feed_interface_temperature_c=55,
        permeate_interface_temperature_c=30,
        feed_nacl_molarity_mol_l=0,
        config=c,
    )
    assert flux > 0


def test_source_salt_activity_reduces_feed_vapor_pressure():
    pure = source_pure_vapor_pressure_pa(55)
    saline = source_vapor_pressure_pa(
        temperature_c=55,
        nacl_molarity_mol_l=1.0,
    )
    assert 0 < saline < pure


def test_source_membrane_conductivity_is_positive():
    assert source_membrane_conductivity(membrane_temperature_c=55, porosity=0.8) > 0


def test_source_cell_area_matches_total_area():
    c = config()
    assert source_cell_area(c) == pytest.approx(0.00337 / 20)


def test_source_countercurrent_runner_conserves_total_water_transfer():
    from ai_water.source_keshavarzzadeh_runner import run_source_countercurrent

    cfg = SourceRunnerConfig(
        membrane_thickness_m=60e-6,
        pore_radius_m=0.1e-6,
        porosity=0.8,
        tortuosity=1.25,
        channel_area_m2=3.15e-6,
        membrane_area_m2=0.00337,
        cells=8,
    )
    result = run_source_countercurrent(
        feed_inlet_temperature_c=60.0,
        permeate_inlet_temperature_c=30.0,
        feed_flow_m3_s=7e-6,
        permeate_flow_m3_s=7e-6,
        feed_salinity_mol_l=0.55,
        config=cfg,
    )
    assert result.total_distillate_kg_s > 0
    assert result.feed_outlet_mass_flow_kg_s < 1000.0 * 7e-6
    assert result.permeate_inlet_temperature_c == 30.0
