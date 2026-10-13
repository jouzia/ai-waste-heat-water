import numpy as np
import pytest

from ai_water.break_even import break_even_linear, pareto_mask


def test_break_even_interpolates_first_crossing() -> None:
    assert break_even_linear(np.array([0.0, 2.0]), np.array([-1.0, 1.0])) == pytest.approx(1.0)


def test_break_even_returns_none_without_crossing() -> None:
    assert break_even_linear(np.array([0.0, 1.0, 2.0]), np.array([1.0, 2.0, 3.0])) is None


def test_break_even_validates_finite_equal_length_vectors() -> None:
    with pytest.raises(ValueError, match="equal-length"):
        break_even_linear(np.array([1.0]), np.array([1.0, 2.0]))
    with pytest.raises(ValueError, match="finite"):
        break_even_linear(np.array([0.0, 1.0]), np.array([0.0, np.nan]))


def test_pareto_mask_marks_dominated_row_not_its_dominator() -> None:
    values = np.array(
        [
            [1.0, 2.0],
            [2.0, 1.0],
            [3.0, 3.0],
            [1.0, 2.0],
        ]
    )
    assert pareto_mask(values, minimize=(True, True)).tolist() == [
        True, True, False, True
    ]


def test_pareto_mask_supports_mixed_minimize_and_maximize_objectives() -> None:
    values = np.array(
        [
            [1.0, 5.0, 10.0],
            [2.0, 4.0, 11.0],
            [3.0, 6.0, 8.0],
            [4.0, 8.0, 4.0],
        ]
    )
    mask = pareto_mask(values, minimize=(True, True, False))
    assert mask.tolist() == [True, True, False, False]


def test_pareto_mask_rejects_empty_or_nonfinite_values() -> None:
    with pytest.raises(ValueError, match="at least one finite row"):
        pareto_mask(np.empty((0, 2)), minimize=(True, True))
    with pytest.raises(ValueError, match="at least one finite row"):
        pareto_mask(np.array([[1.0, np.inf]]), minimize=(True, True))
