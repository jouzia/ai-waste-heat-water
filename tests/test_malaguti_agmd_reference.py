from __future__ import annotations

import pytest

from ai_water.malaguti_agmd_reference import solve_agmd_reference

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
        vaporization_efficiency=0.6973894314192178,
        delta_t_c=91.75565385125267,
        delta_t_h_in_c=6.56277877653812,
        cold_inlet_c=11.463104474916047,
        cp_hot_j_kg_k=4431.63491923573,
        cp_cold_j_kg_k=3184.019355313946,
        cp_distillate_j_kg_k=4180.0,
        latent_heat_j_kg=2456547.51341516,
    )
    assert result.delta_t_h_out_c > 6.56277877653812
    assert result.recovery_fraction > 0.0


def test_optional_outlet_upper_bound_is_enforced_when_supplied():
    with pytest.raises(ValueError, match="exactly one"):
        solve_agmd_reference(
            vaporization_efficiency=0.6973894314192178,
            delta_t_c=91.75565385125267,
            delta_t_h_in_c=6.56277877653812,
            cold_inlet_c=11.463104474916047,
            cp_hot_j_kg_k=4431.63491923573,
            cp_cold_j_kg_k=3184.019355313946,
            cp_distillate_j_kg_k=4180.0,
            latent_heat_j_kg=2456547.51341516,
            maximum_delta_t_h_out_c=6.56277877653812,
        )

