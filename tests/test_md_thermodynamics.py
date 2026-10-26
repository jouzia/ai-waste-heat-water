import pytest

from ai_water.md_thermodynamics import evaluate_requirements, module_pumping_kwh_m3


BASE = {
    "delta_t_k": 30.0,
    "delta_t_h_in_k": 5.0,
    "delta_t_h_out_k": 0.5,
    "hvap_j_kg": 2_400_000.0,
    "vaporization_efficiency": 0.5,
    "density_kg_m3": 1000.0,
}


def test_configuration_one_matches_direct_equation_calculation():
    result = evaluate_requirements(configuration=1, **BASE)
    # Independently expanded from Eq. (1), using J/kg -> kWh/m³.
    scale = 1000.0 / 3_600_000.0
    expected_stec = (
        (2_400_000.0 / 0.5) * (30.0 / (30.0 - 0.5)) * scale
    )
    expected_scr = (
        (2_400_000.0 / 0.5) * ((30.0 - 5.0) / (30.0 - 0.5)) * scale
    )
    assert result.stec_kwh_m3 == pytest.approx(expected_stec)
    assert result.scr_kwh_m3 == pytest.approx(expected_scr)


def test_configuration_two_matches_direct_equation_calculation():
    result = evaluate_requirements(configuration=2, delta_t_hx_k=5.0, **BASE)
    scale = 1000.0 / 3_600_000.0
    expected_stec = (
        (2_400_000.0 / 0.5) * ((5.0 + 5.0) / (30.0 - 0.5)) * scale
    )
    expected_scr = (
        (2_400_000.0 / 0.5) * (5.0 / (30.0 - 0.5)) * scale
    )
    assert result.stec_kwh_m3 == pytest.approx(expected_stec)
    assert result.scr_kwh_m3 == pytest.approx(expected_scr)


def test_configuration_three_matches_direct_equation_calculation():
    result = evaluate_requirements(
        configuration=3,
        c_hot_j_kg_k=4000.0,
        c_cold_j_kg_k=4180.0,
        **BASE,
    )
    scale = 1000.0 / 3_600_000.0
    expected_stec = (
        (2_400_000.0 / 0.5) * (5.0 / (30.0 - 0.5)) * scale
    )
    expected_scr = (
        (2_400_000.0 * 4180.0 / (0.5 * 4000.0))
        * (0.5 / (30.0 - 0.5))
        * scale
    )
    assert result.stec_kwh_m3 == pytest.approx(expected_stec)
    assert result.scr_kwh_m3 == pytest.approx(expected_scr)


def test_configuration_two_requires_heat_exchanger_pinch():
    with pytest.raises(ValueError, match="delta_t_hx_k"):
        evaluate_requirements(configuration=2, **BASE)


def test_configuration_three_requires_heat_capacities():
    with pytest.raises(ValueError, match="heat capacities"):
        evaluate_requirements(configuration=3, **BASE)


@pytest.mark.parametrize(
    "updates",
    [
        {"vaporization_efficiency": 0.0},
        {"vaporization_efficiency": 1.1},
        {"delta_t_k": 0.0},
        {"delta_t_h_out_k": 30.0},
        {"delta_t_h_out_k": 6.0},
        {"delta_t_h_in_k": 30.0},
    ],
)
def test_rejects_invalid_thermodynamic_inputs(updates):
    args = BASE | updates
    with pytest.raises(ValueError):
        evaluate_requirements(configuration=1, **args)


def test_pumping_energy_matches_published_expression_and_unit_conversion():
    # 300 mbar = 30,000 Pa; R=0.03 and eta=0.75 -> 0.37037037 kWh/m³.
    value = module_pumping_kwh_m3(
        pressure_drop_pa=30_000.0,
        single_pass_recovery=0.03,
        pump_efficiency=0.75,
    )
    expected = 30_000.0 / (0.03 * 0.75 * 3_600_000.0)
    assert value == pytest.approx(expected)
    assert value == pytest.approx(0.37037037, rel=1e-7)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"pressure_drop_pa": 0.0, "single_pass_recovery": 0.03, "pump_efficiency": 0.75},
        {"pressure_drop_pa": 30000.0, "single_pass_recovery": 0.0, "pump_efficiency": 0.75},
        {"pressure_drop_pa": 30000.0, "single_pass_recovery": 0.03, "pump_efficiency": 0.0},
    ],
)
def test_pumping_rejects_nonphysical_inputs(kwargs):
    with pytest.raises(ValueError):
        module_pumping_kwh_m3(**kwargs)
