import pytest

from ai_water.decision_analysis import (
    BreakEvenBracket,
    bisect_break_even,
    find_sign_change_brackets,
    pareto_mask,
)


def test_find_sign_change_brackets():
    result = find_sign_change_brackets([0, 1, 2, 3], [2, 1, -1, -2])
    assert result == (BreakEvenBracket(1, 2, 1, -1),)


def test_bisect_break_even():
    result = bisect_break_even(
        lambda x: x - 2.5,
        BreakEvenBracket(2, 3, -0.5, 0.5),
        tolerance=1e-8,
    )
    assert result.parameter == pytest.approx(2.5, abs=1e-7)
    assert abs(result.value) <= 1e-7


def test_bisect_rejects_non_bracket():
    with pytest.raises(ValueError, match="strict sign change"):
        bisect_break_even(
            lambda x: x,
            BreakEvenBracket(0, 1, 1, 2),
        )


def test_pareto_mask_supports_minimize_and_maximize_objectives():
    result = pareto_mask(
        [(1, 5), (2, 4), (3, 3), (4, 6)],
        minimize=(True, False),
    )
    assert result == (True, True, True, False)
