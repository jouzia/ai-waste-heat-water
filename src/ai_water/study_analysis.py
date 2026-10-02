"""Study-level analysis utilities for reproducible uncertainty results.

These functions consume already-generated model records. They do not assign
empirical distributions and they never turn scenario ranges into real-world
probabilities.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil

import numpy as np


@dataclass(frozen=True)
class Summary:
    n: int
    median: float
    p05: float
    p95: float
    probability_negative: float
    probability_positive: float


@dataclass(frozen=True)
class ConvergencePoint:
    sample_count: int
    median: float
    p05: float
    p95: float
    probability_negative: float


def summarize_net_water(values: np.ndarray | list[float]) -> Summary:
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x)):
        raise ValueError("values must be a non-empty finite 1-D array")
    return Summary(
        n=int(x.size),
        median=float(np.median(x)),
        p05=float(np.quantile(x, 0.05)),
        p95=float(np.quantile(x, 0.95)),
        probability_negative=float(np.mean(x < 0.0)),
        probability_positive=float(np.mean(x > 0.0)),
    )


def convergence_curve(
    values: np.ndarray | list[float],
    *,
    sample_counts: tuple[int, ...] = (1000, 2500, 5000, 10000),
) -> tuple[ConvergencePoint, ...]:
    """Compute deterministic prefix convergence diagnostics.

    Prefixes are used intentionally so convergence can be inspected without
    re-sampling. Each requested count must be <= len(values).
    """
    x = np.asarray(values, dtype=float)
    if x.ndim != 1 or x.size == 0 or not np.all(np.isfinite(x)):
        raise ValueError("values must be a non-empty finite 1-D array")
    counts = tuple(sorted(set(sample_counts)))
    if not counts or any(n <= 0 or n > x.size for n in counts):
        raise ValueError("sample counts must be positive and within values")
    return tuple(
        ConvergencePoint(
            sample_count=n,
            median=float(np.median(x[:n])),
            p05=float(np.quantile(x[:n], 0.05)),
            p95=float(np.quantile(x[:n], 0.95)),
            probability_negative=float(np.mean(x[:n] < 0.0)),
        )
        for n in counts
    )


def sign_change_interval(
    x: np.ndarray | list[float],
    y: np.ndarray | list[float],
) -> tuple[float, float] | None:
    """Return the first bracket containing a sign change in y versus x."""
    xx = np.asarray(x, dtype=float)
    yy = np.asarray(y, dtype=float)
    if xx.ndim != 1 or yy.ndim != 1 or xx.size != yy.size or xx.size < 2:
        raise ValueError("x and y must be equal-length 1-D arrays with >=2 points")
    if not np.all(np.isfinite(xx)) or not np.all(np.isfinite(yy)):
        raise ValueError("x and y must be finite")
    order = np.argsort(xx)
    xx, yy = xx[order], yy[order]
    for i in range(xx.size - 1):
        if yy[i] == 0.0:
            return float(xx[i]), float(xx[i])
        if yy[i] * yy[i + 1] < 0.0:
            return float(xx[i]), float(xx[i + 1])
    return None


def required_sample_count(
    *,
    current_count: int,
    target_relative_change: float = 0.01,
) -> int:
    """Conservative planning aid for repeated Monte Carlo convergence runs.

    This does not claim a statistical stopping theorem. It simply provides a
    reproducible geometric progression target for study planning.
    """
    if current_count <= 0:
        raise ValueError("current_count must be positive")
    if not 0.0 < target_relative_change < 1.0:
        raise ValueError("target_relative_change must be in (0, 1)")
    multiplier = ceil(1.0 / target_relative_change)
    return current_count * max(multiplier, 2)
