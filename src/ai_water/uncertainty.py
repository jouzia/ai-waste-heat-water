"""Uncertainty sampling primitives for the research framework.

These utilities intentionally contain no default empirical distributions. A
published analysis must supply source-linked distribution parameters externally.
"""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class DistributionSpec:
    name: str
    parameters: tuple[float, ...]


def sample_distribution(
    spec: DistributionSpec,
    *,
    size: int,
    rng: np.random.Generator,
) -> np.ndarray:
    if size <= 0:
        raise ValueError("sample size must be positive")
    if spec.name == "uniform":
        low, high = spec.parameters
        if high < low:
            raise ValueError("uniform high must be >= low")
        return rng.uniform(low, high, size)
    if spec.name == "normal":
        mean, sd = spec.parameters
        if sd < 0:
            raise ValueError("normal standard deviation must be non-negative")
        return rng.normal(mean, sd, size)
    if spec.name == "lognormal":
        mean_log, sd_log = spec.parameters
        if sd_log < 0:
            raise ValueError("lognormal log-scale standard deviation must be non-negative")
        return rng.lognormal(mean_log, sd_log, size)
    raise ValueError(f"unsupported distribution: {spec.name}")


def probability_negative(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        raise ValueError("values cannot be empty")
    return float(np.mean(values < 0))


def summarize(values: np.ndarray) -> dict[str, float]:
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        raise ValueError("values cannot be empty")
    return {
        "n": float(values.size),
        "mean": float(np.mean(values)),
        "median": float(np.median(values)),
        "p05": float(np.quantile(values, 0.05)),
        "p95": float(np.quantile(values, 0.95)),
        "probability_negative": probability_negative(values),
    }
