from __future__ import annotations

import pytest
from numpy.polynomial import Polynomial

from ai_water.malaguti_agmd_reference import (
    _real_polynomial_roots,
    solve_agmd_reference,
)

# Provisional numerical smoke-test inputs only; NOT verified Sharqawy outputs.
# The cold channel is saline water in AGMD, not pure distillate water.
PROVISIONAL_PROPERTIES = {
    "cp_hot_j_kg_k": 4000.0,
    "cp_cold_j_kg_k": 4000.0,
    "cp_distillate_j_kg_k": 4180.0,
    "latent_heat_j_kg": 2_400_000.0,
    "delta_t_h_in_c": 5.0,
    "cold_inlet_c": 20.0,
}


@pytest.mark.parametrize(
    ("eta", "delta_t", "expected_recovery"),
    [
        (0.5, 30.0, 0.0210851568),
        (0.5, 50.0, 0.0383010174),
        (0.7, 30.0, 0.0296647349),
        (0.7, 50.0, 0.0540961566),
    ],
)
def test_solver_residuals_and_model_admissibility(eta, delta_t, expected_recovery):
    result = solve_agmd_reference(
        vaporization_efficiency=eta,
        delta_t_c=delta_t,
        **PROVISIONAL_PROPERTIES,
    )
    assert result.recovery_fraction == pytest.approx(expected_recovery, abs=1e-9)
    assert 0.0 < result.recovery_fraction < 0.1
    assert result.delta_t_h_out_c >= 0.5
    assert result.equation_s2_residual == pytest.approx(0.0, abs=1e-10)
    assert result.equation_s8_residual_w_per_kg_k == pytest.approx(0.0, abs=1e-6)


def test_rejects_inlet_difference_not_below_overall_difference():
    with pytest.raises(ValueError, match="smaller"):
        solve_agmd_reference(
            vaporization_efficiency=0.5,
            delta_t_c=5.0,
            **PROVISIONAL_PROPERTIES,
        )


def test_outlet_difference_above_inlet_is_admissible_only_in_algebraic_mode():
    result = solve_agmd_reference(
        vaporization_efficiency=0.7480277753658483,
        delta_t_c=44.1125971862735,
        delta_t_h_in_c=4.4198898005722835,
        cold_inlet_c=20.0,
        cp_hot_j_kg_k=4023.7871741005165,
        cp_cold_j_kg_k=3575.9758914073695,
        cp_distillate_j_kg_k=4180.0,
        latent_heat_j_kg=2467075.614008491,
        enforce_config3_terminal_order=False,
    )
    assert result.delta_t_h_out_c > 4.4198898005722835
    assert result.recovery_fraction > 0.0


def test_paper_config3_domain_rejects_outlet_difference_above_inlet():
    # Same synthetic root as the algebraic-mode test; paper-domain terminal
    # ordering excludes it. This is not a seawater-property validation case.
    with pytest.raises(ValueError, match="found 0"):
        solve_agmd_reference(
            vaporization_efficiency=0.7480277753658483,
            delta_t_c=44.1125971862735,
            delta_t_h_in_c=4.4198898005722835,
            cold_inlet_c=20.0,
            cp_hot_j_kg_k=4023.7871741005165,
            cp_cold_j_kg_k=3575.9758914073695,
            cp_distillate_j_kg_k=4180.0,
            latent_heat_j_kg=2467075.614008491,
        )


def test_optional_outlet_upper_bound_is_enforced_when_supplied():
    with pytest.raises(ValueError, match="exactly one"):
        solve_agmd_reference(
            vaporization_efficiency=0.7480277753658483,
            delta_t_c=44.1125971862735,
            delta_t_h_in_c=4.4198898005722835,
            cold_inlet_c=20.0,
            cp_hot_j_kg_k=4023.7871741005165,
            cp_cold_j_kg_k=3575.9758914073695,
            cp_distillate_j_kg_k=4180.0,
            latent_heat_j_kg=2467075.614008491,
            maximum_delta_t_h_out_c=4.4198898005722835,
            enforce_config3_terminal_order=False,
        )


def test_solver_reports_zero_admissible_roots():
    # Synthetic algebraic stress case, not a seawater-property scenario.
    with pytest.raises(ValueError, match="found 0"):
        solve_agmd_reference(
            vaporization_efficiency=0.5185918434982489,
            delta_t_c=38.73108980068479,
            delta_t_h_in_c=4.885763869707903,
            cold_inlet_c=26.987148929512614,
            cp_hot_j_kg_k=3699.8278157839345,
            cp_cold_j_kg_k=4486.426816194942,
            cp_distillate_j_kg_k=4180.0,
            latent_heat_j_kg=2128002.144351397,
            enforce_config3_terminal_order=False,
        )


def test_solver_rejects_multiple_admissible_roots():
    # Deliberately adversarial coefficients exercise ambiguity handling only.
    # These values are not claimed to represent seawater or the paper's regime.
    with pytest.raises(ValueError, match="found 2"):
        solve_agmd_reference(
            vaporization_efficiency=0.7134154568880409,
            delta_t_c=81.35000948376,
            delta_t_h_in_c=62.95142695184112,
            cold_inlet_c=50.192339608335175,
            cp_hot_j_kg_k=5142.442031919776,
            cp_cold_j_kg_k=4668.8795856819725,
            cp_distillate_j_kg_k=6357.43391115901,
            latent_heat_j_kg=275894.7824005884,
            enforce_config3_terminal_order=False,
        )


def test_real_polynomial_roots_returns_one_exact_repeated_root():
    # Exact synthetic quadratic (x - 2)^2. This tests multiplicity handling
    # directly without claiming the coefficients are a seawater operating case.
    roots = _real_polynomial_roots(Polynomial([4.0, -4.0, 1.0]))
    assert roots == pytest.approx([2.0], abs=1e-14)


@pytest.mark.parametrize("coefficient_scale", [1e-200, 1.0, 1e200])
def test_real_polynomial_roots_are_invariant_to_coefficient_scale(coefficient_scale):
    # The polynomial has roots 1 and 2; scaling every coefficient must not
    # change the roots or turn a distinct-root case into a repeated root.
    polynomial = Polynomial(
        [2.0 * coefficient_scale, -3.0 * coefficient_scale, coefficient_scale]
    )
    roots = sorted(_real_polynomial_roots(polynomial))
    assert roots == pytest.approx([1.0, 2.0], abs=1e-12)


def test_real_polynomial_roots_reject_nonfinite_coefficients():
    with pytest.raises(ValueError, match="finite"):
        _real_polynomial_roots(Polynomial([1.0, float("inf"), 1.0]))
