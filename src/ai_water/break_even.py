"""Break-even and Pareto analysis primitives."""

from __future__ import annotations

import numpy as np


def break_even_linear(x: np.ndarray, y: np.ndarray) -> float | None:
    """Return the first linear-interpolated zero crossing, if one exists."""
    x_values = np.asarray(x, dtype=float)
    y_values = np.asarray(y, dtype=float)
    if (
        x_values.ndim != 1
        or y_values.ndim != 1
        or x_values.size != y_values.size
        or x_values.size < 2
    ):
        raise ValueError("x and y must be equal-length 1-D arrays with >= 2 values")
    if not np.all(np.isfinite(x_values)) or not np.all(np.isfinite(y_values)):
        raise ValueError("x and y must be finite")

    order = np.argsort(x_values)
    x_values = x_values[order]
    y_values = y_values[order]
    for index in range(len(x_values) - 1):
        if y_values[index] == 0:
            return float(x_values[index])
        if y_values[index] * y_values[index + 1] < 0:
            return float(
                x_values[index]
                - y_values[index]
                * (x_values[index + 1] - x_values[index])
                / (y_values[index + 1] - y_values[index])
            )
    if y_values[-1] == 0:
        return float(x_values[-1])
    return None


def pareto_mask(values: np.ndarray, *, minimize: tuple[bool, ...]) -> np.ndarray:
    """Return True for nondominated rows under mixed minimize/maximize objectives."""
    objectives = np.asarray(values, dtype=float)
    if objectives.ndim != 2 or objectives.shape[1] != len(minimize):
        raise ValueError("values must be 2-D and match minimize")
    if objectives.shape[0] == 0 or not np.all(np.isfinite(objectives)):
        raise ValueError("values must contain at least one finite row")

    oriented = objectives.copy()
    for column, is_minimized in enumerate(minimize):
        if not is_minimized:
            oriented[:, column] *= -1.0

    nondominated = np.ones(len(oriented), dtype=bool)
    for index, candidate in enumerate(oriented):
        # A row is dominated when another row is no worse in every objective
        # and strictly better in at least one. Mark the candidate itself false;
        # never mark the rows that dominate it.
        dominates_candidate = np.all(oriented <= candidate, axis=1) & np.any(
            oriented < candidate, axis=1
        )
        if np.any(dominates_candidate):
            nondominated[index] = False
    return nondominated
