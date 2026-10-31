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
def test_solver_residuals_and_physical_domain(eta, delta_t, expected_recovery):
    result = solve_agmd_reference(
        vaporization_efficiency=eta,
        delta_t_c=delta_t,
        **PROVISIONAL_PROPERTIES,
    )
    assert result.recovery_fraction == pytest.approx(expected_recovery, abs=1e-9)
    assert 0.0 < result.recovery_fraction < 0.1
    assert 0.5 <= result.delta_t_h_out_c <= PROVISIONAL_PROPERTIES["delta_t_h_in_c"]
    assert result.equation_s2_residual == pytest.approx(0.0, abs=1e-10)
    assert result.equation_s8_residual_w_per_kg_k == pytest.approx(0.0, abs=1e-6)


def test_rejects_inlet_difference_not_below_overall_difference():
    with pytest.raises(ValueError, match="smaller"):
        solve_agmd_reference(
            vaporization_efficiency=0.5,
            delta_t_c=5.0,
            **PROVISIONAL_PROPERTIES,
        )


def test_outlet_difference_can_exceed_inlet_without_optional_policy_cap():
    result = solve_agmd_reference(
        vaporization_efficiency=0.7480277753658483,
        delta_t_c=44.1125971862735,
        delta_t_h_in_c=4.4198898005722835,
        cold_inlet_c=20.0,
        cp_hot_j_kg_k=4023.7871741005165,
        cp_cold_j_kg_k=3575.9758914073695,
        cp_distillate_j_kg_k=4180.0,
        latent_heat_j_kg=2467075.614008491,
    )
    assert result.delta_t_h_out_c > 4.4198898005722835
    assert result.recovery_fraction > 0.0


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
        )


def test_real_polynomial_roots_returns_one_exact_repeated_root():
    # Exact synthetic quadratic (x - 2)^2. This tests multiplicity handling
    # directly without claiming the coefficients are a seawater operating case.
    roots = _real_polynomial_roots(Polynomial([4.0, -4.0, 1.0]))
    assert roots == pytest.approx([2.0], abs=1e-14)
