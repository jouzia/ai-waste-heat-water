import pytest

from ai_water.source_keshavarzzadeh_runner import (
    SourceRunnerConfig,
    _water_density_kg_m3,
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
        channel_area_m2=3.15e-6,
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
    assert result.converged
    assert result.feed_outlet_mass_flow_kg_s < 1000.0 * 7e-6
    assert result.feed_outlet_mass_flow_kg_s == pytest.approx(
        _water_density_kg_m3(60.0) * 7e-6 - result.total_distillate_kg_s, rel=2e-3
    )
    assert result.permeate_inlet_temperature_c == 30.0
    assert result.permeate_outlet_mass_flow_kg_s == pytest.approx(
        _water_density_kg_m3(30.0) * 7e-6 + result.total_distillate_kg_s,
        rel=2e-3,
    )


def test_source_countercurrent_permeate_mass_decreases_in_feed_coordinate():
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
    assert len(result.cells) == cfg.cells
    assert all(
        result.cells[i + 1].permeate_mass_flow_kg_s
        < result.cells[i].permeate_mass_flow_kg_s
        for i in range(len(result.cells) - 1)
    )
    assert result.cells[0].permeate_mass_flow_kg_s > result.cells[-1].permeate_mass_flow_kg_s


@pytest.mark.parametrize("flow_m3_s", [7e-6, 11e-6])
@pytest.mark.parametrize("salinity_mol_l", [0.0, 0.55, 1.15, 1.67])
def test_source_runner_eight_case_numerical_smoke_matrix(flow_m3_s, salinity_mol_l):
    """Smoke-test all flow/salinity combinations, not a source-condition validation.

    The 60/30 C boundary temperatures are deliberately provisional software
    inputs. They must not be reported as the Figure 3 experimental conditions.
    """
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
        feed_flow_m3_s=flow_m3_s,
        permeate_flow_m3_s=flow_m3_s,
        feed_salinity_mol_l=salinity_mol_l,
        config=cfg,
    )
    assert result.converged
    assert result.total_distillate_kg_s >= 0
    assert result.feed_outlet_mass_flow_kg_s == pytest.approx(
        _water_density_kg_m3(60.0) * flow_m3_s - result.total_distillate_kg_s,
        rel=2e-3,
    )
    assert result.permeate_outlet_mass_flow_kg_s == pytest.approx(
        _water_density_kg_m3(30.0) * flow_m3_s + result.total_distillate_kg_s,
        rel=2e-3,
    )
