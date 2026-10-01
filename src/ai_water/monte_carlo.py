"""Reproducible Monte Carlo scenario runner.

Distribution choices and parameters must be supplied by the caller and linked
to literature, measurement data, or an explicitly labelled scenario assumption.
Invalid draws are counted, not silently clipped.
"""
from dataclasses import dataclass

import numpy as np
from pydantic import ValidationError

from .engine import simulate
from .models import Scenario
from .uncertainty import DistributionSpec, sample_distribution


@dataclass(frozen=True)
class MonteCarloResult:
    seed: int
    requested_samples: int
    successful_samples: int
    failed_samples: int
    records: tuple[dict[str, float], ...]


def _set_nested_value(data: dict, path: str, value: float) -> None:
    parts = path.split(".")
    target = data
    for part in parts[:-1]:
        if part not in target or not isinstance(target[part], dict):
            raise ValueError(f"unknown scenario parameter path: {path}")
        target = target[part]
    if parts[-1] not in target:
        raise ValueError(f"unknown scenario parameter path: {path}")
    target[parts[-1]] = float(value)


def run_monte_carlo(
    base_scenario: Scenario,
    distributions: dict[str, DistributionSpec],
    *,
    sample_size: int,
    seed: int,
) -> MonteCarloResult:
    """Sample declared scenario parameters and simulate each valid draw.

    Each record contains sample index, sampled parameters, and key water/energy
    outputs. The function does not assign empirical distributions or replace
    invalid draws with clipped values.
    """
    if sample_size <= 0:
        raise ValueError("sample_size must be positive")
    if not distributions:
        raise ValueError("at least one source-linked distribution is required")

    rng = np.random.default_rng(seed)
    sampled = {
        path: sample_distribution(spec, size=sample_size, rng=rng)
        for path, spec in distributions.items()
    }
    base_data = base_scenario.model_dump()
    # Validate parameter paths before sampling so a misspelled path cannot be
    # silently counted as a failed Monte Carlo draw.
    for path in distributions:
        probe = {
            key: (value.copy() if isinstance(value, dict) else value)
            for key, value in base_data.items()
        }
        _set_nested_value(probe, path, 0.0)
    records: list[dict[str, float]] = []
    failures = 0

    for index in range(sample_size):
        data = {
            key: (value.copy() if isinstance(value, dict) else value)
            for key, value in base_data.items()
        }
        sampled_values = {
            path: float(values[index]) for path, values in sampled.items()
        }
        try:
            for path, value in sampled_values.items():
                _set_nested_value(data, path, value)
            scenario = Scenario.model_validate(data)
            result = simulate(scenario)
        except (ValueError, ValidationError, OverflowError, ZeroDivisionError):
            failures += 1
            continue

        record = {
            "sample_index": float(index),
            **sampled_values,
            "it_energy_kwh": result.it_energy_kwh,
            "recoverable_heat_kwh_th": result.recoverable_heat_kwh_th,
            "freshwater_produced_l": result.freshwater_produced_l,
            "additional_water_consumption_l": result.additional_water_consumption_l,
            "avoided_freshwater_consumption_l": result.avoided_freshwater_consumption_l,
            "net_consumption_change_l": result.net_consumption_change_l,
        }
        records.append(record)

    return MonteCarloResult(
        seed=seed,
        requested_samples=sample_size,
        successful_samples=len(records),
        failed_samples=failures,
        records=tuple(records),
    )
