"""Decision-analysis primitives for break-even and Pareto studies.

These utilities do not assign empirical parameter values. They operate on
caller-supplied model evaluations so study assumptions remain explicit.
"""
from collections.abc import Callable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class BreakEvenBracket:
    """A sampled parameter interval containing a zero crossing."""

    low: float
    high: float
    low_value: float
    high_value: float


@dataclass(frozen=True)
class BreakEvenResult:
    """Bisection result for a declared monotone scalar response."""

    parameter: float
    value: float
    iterations: int
    bracket: BreakEvenBracket


def find_sign_change_brackets(
    parameter_values: Sequence[float],
    values: Sequence[float],
) -> tuple[BreakEvenBracket, ...]:
    """Return adjacent sampled intervals whose response changes sign."""
    if len(parameter_values) != len(values) or len(parameter_values) < 2:
        raise ValueError("parameter_values and values must have equal length >= 2")
    if any(
        parameter_values[index] >= parameter_values[index + 1]
        for index in range(len(parameter_values) - 1)
    ):
        raise ValueError("parameter_values must be strictly increasing")

    brackets = []
    for low, high, low_value, high_value in zip(
        parameter_values[:-1],
        parameter_values[1:],
        values[:-1],
        values[1:],
        strict=True,
    ):
        if low_value == 0:
            brackets.append(BreakEvenBracket(low, low, low_value, low_value))
        elif low_value * high_value < 0:
            brackets.append(BreakEvenBracket(low, high, low_value, high_value))
        elif high_value == 0:
            brackets.append(BreakEvenBracket(high, high, high_value, high_value))
    return tuple(brackets)


def bisect_break_even(
    evaluator: Callable[[float], float],
    bracket: BreakEvenBracket,
    *,
    tolerance: float = 1e-6,
    max_iterations: int = 100,
) -> BreakEvenResult:
    """Bisect a declared sign-changing bracket without assuming its units."""
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")
    if max_iterations < 1:
        raise ValueError("max_iterations must be positive")
    if bracket.low == bracket.high:
        return BreakEvenResult(
            parameter=bracket.low,
            value=bracket.low_value,
            iterations=0,
            bracket=bracket,
        )

    low, high = bracket.low, bracket.high
    low_value, high_value = bracket.low_value, bracket.high_value
    if low_value * high_value >= 0:
        raise ValueError("bracket must contain a strict sign change")

    for iteration in range(1, max_iterations + 1):
        mid = (low + high) / 2
        mid_value = evaluator(mid)
        if abs(mid_value) <= tolerance or (high - low) / 2 <= tolerance:
            return BreakEvenResult(mid, mid_value, iteration, bracket)
        if low_value * mid_value < 0:
            high, high_value = mid, mid_value
        else:
            low, low_value = mid, mid_value

    mid = (low + high) / 2
    return BreakEvenResult(mid, evaluator(mid), max_iterations, bracket)


def pareto_mask(
    objectives: Sequence[Sequence[float]],
    *,
    minimize: Sequence[bool] | None = None,
) -> tuple[bool, ...]:
    """Mark non-dominated rows for a multi-objective minimization problem."""
    if not objectives:
        return ()
    width = len(objectives[0])
    if width == 0 or any(len(row) != width for row in objectives):
        raise ValueError("objectives must be a non-empty rectangular matrix")
    directions = tuple(minimize) if minimize is not None else (True,) * width
    if len(directions) != width:
        raise ValueError("minimize must match the objective count")

    normalized = [
        tuple(value if directions[j] else -value for j, value in enumerate(row))
        for row in objectives
    ]
    mask = []
    for index, candidate in enumerate(normalized):
        dominated = any(
            other != candidate
            and all(a <= b for a, b in zip(other, candidate, strict=True))
            and any(a < b for a, b in zip(other, candidate, strict=True))
            for other in normalized
        )
        mask.append(not dominated)
    return tuple(mask)
