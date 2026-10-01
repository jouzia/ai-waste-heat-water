import numpy as np
import pytest

from ai_water.global_sensitivity import sobol_uniform


def test_sobol_indices_recover_additive_linear_variance_shares():
    result = sobol_uniform(
        lambda x: x[0] + 2.0 * x[1],
        {"x1": (0.0, 1.0), "x2": (0.0, 1.0)},
        sample_size=4096,
        seed=123,
    )
    indices = {item.parameter: item for item in result.indices}
    assert indices["x1"].first_order == pytest.approx(0.2, abs=0.04)
    assert indices["x2"].first_order == pytest.approx(0.8, abs=0.04)
    assert indices["x1"].total_effect == pytest.approx(0.2, abs=0.04)
    assert indices["x2"].total_effect == pytest.approx(0.8, abs=0.04)


def test_sobol_rejects_non_power_of_two_sample_size():
    with pytest.raises(ValueError, match="power of two"):
        sobol_uniform(lambda x: float(x[0]), {"x": (0.0, 1.0)}, sample_size=100, seed=1)


def test_sobol_rejects_nonfinite_model_outputs():
    def invalid(_):
        return np.nan

    with pytest.raises(ValueError, match="non-finite"):
        sobol_uniform(invalid, {"x": (0.0, 1.0)}, sample_size=8, seed=1)
