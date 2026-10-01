"""Global sensitivity analysis for independent uniform input ranges.

This implements a Saltelli covariance first-order estimator and a Jansen total-effect estimator.
The bounds are scenario ranges supplied by the researcher, not empirical
probability distributions unless separately justified.
"""
from dataclasses import dataclass
from math import log2

import numpy as np
from scipy.stats import qmc


@dataclass(frozen=True)
class SobolIndex:
    parameter: str
    first_order: float
    total_effect: float


@dataclass(frozen=True)
class SobolResult:
    sample_size_per_matrix: int
    seed: int
    output_variance: float
    indices: tuple[SobolIndex, ...]


def sobol_uniform(
    evaluate,
    bounds: dict[str, tuple[float, float]],
    *,
    sample_size: int,
    seed: int,
) -> SobolResult:
    """Estimate first-order/total-effect indices for independent uniform inputs.

    sample_size must be a power of two for the Sobol low-discrepancy sequence.
    The evaluate callback receives a one-dimensional array in bounds-key order.
    Invalid/non-finite model outputs are errors, not silently dropped samples.
    """
    if not bounds:
        raise ValueError("at least one parameter bound is required")
    if sample_size < 2 or sample_size & (sample_size - 1):
        raise ValueError("sample_size must be a power of two and at least 2")

    names = tuple(bounds)
    lower = np.asarray([bounds[name][0] for name in names], dtype=float)
    upper = np.asarray([bounds[name][1] for name in names], dtype=float)
    if not np.all(np.isfinite(lower)) or not np.all(np.isfinite(upper)):
        raise ValueError("bounds must be finite")
    if np.any(upper <= lower):
        raise ValueError("each upper bound must exceed its lower bound")

    dimension = len(names)
    exponent = int(log2(sample_size))
    # Generate A and B as disjoint coordinate blocks from one scrambled
    # 2d-dimensional Sobol design; separate same-dimension scrambles can have
    # undesirable finite-sample cross-correlation for covariance estimators.
    unit = qmc.Sobol(d=2 * dimension, scramble=True, seed=seed).random_base2(
        exponent
    )
    unit_a = unit[:, :dimension]
    unit_b = unit[:, dimension:]
    a = lower + unit_a * (upper - lower)
    b = lower + unit_b * (upper - lower)

    def evaluate_matrix(matrix: np.ndarray) -> np.ndarray:
        outputs = np.asarray([evaluate(row) for row in matrix], dtype=float)
        if outputs.shape != (sample_size,) or not np.all(np.isfinite(outputs)):
            raise ValueError("model returned non-finite or incorrectly shaped outputs")
        return outputs

    ya = evaluate_matrix(a)
    yb = evaluate_matrix(b)
    variance = float(np.var(np.concatenate((ya, yb)), ddof=1))
    if variance <= np.finfo(float).eps:
        raise ValueError("output variance is too small to estimate Sobol indices")

    indices = []
    for i, name in enumerate(names):
        hybrid = a.copy()
        hybrid[:, i] = b[:, i]
        y_hybrid = evaluate_matrix(hybrid)
        # Covariance of f(B) and f(A with B_i) isolates the variance
        # contribution shared through input i without subtracting the finite-
        # sample covariance between the independent A and B designs.
        first = float(np.cov(yb, y_hybrid, ddof=1)[0, 1]) / variance
        total = float(np.mean((ya - y_hybrid) ** 2)) / (2.0 * variance)
        indices.append(
            SobolIndex(
                parameter=name,
                first_order=first,
                total_effect=total,
            )
        )

    return SobolResult(
        sample_size_per_matrix=sample_size,
        seed=seed,
        output_variance=variance,
        indices=tuple(indices),
    )
