import numpy as np
import pytest

from ai_water.study_analysis import (
    convergence_curve,
    sign_change_interval,
    summarize_net_water,
)


def test_net_water_summary():
    result = summarize_net_water(np.array([-2.0, -1.0, 0.0, 1.0, 3.0]))
    assert result.n == 5
    assert result.median == 0.0
    assert result.probability_negative == pytest.approx(0.4)
    assert result.probability_positive == pytest.approx(0.4)


def test_convergence_uses_prefixes():
    result = convergence_curve(np.arange(-5.0, 5.0), sample_counts=(4, 8))
    assert [item.sample_count for item in result] == [4, 8]
    assert result[0].median == pytest.approx(-3.5)


def test_sign_change_interval():
    assert sign_change_interval([0.0, 1.0, 2.0], [2.0, -1.0, -2.0]) == (0.0, 1.0)
    assert sign_change_interval([0.0, 1.0], [1.0, 2.0]) is None


def test_invalid_summary_rejected():
    with pytest.raises(ValueError):
        summarize_net_water([1.0, np.nan])
