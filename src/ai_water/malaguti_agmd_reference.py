"""Standalone numerical reference for Malaguti et al. (2026), AGMD configuration 3.

This module solves supplementary equations S2 and S8 with explicit property inputs.
It does not select or silently infer property values; source-matched Sharqawy inputs
must be supplied by the caller before this is treated as a paper reproduction.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import copysign, isfinite, sqrt

import numpy as np


@dataclass(frozen=True)
class AGMDReferenceResult:
    """Solution to the configuration-3 balance equations."""

    delta_t_h_out_c: float
    recovery_fraction: float
    distillate_outlet_c: float
    equation_s2_residual: float
    equation_s8_residual_w_per_kg_k: float


def _real_polynomial_roots(polynomial: np.polynomial.Polynomial) -> list[float]:
    """Return distinct real roots, treating a roundoff-level zero discriminant robustly."""
    coefficients = np.asarray(polynomial.coef, dtype=float)
    degree = len(coefficients) - 1
    if degree == 0:
        return []
    if degree == 1:
        return [-float(coefficients[0] / coefficients[1])]
    if degree != 2:
        raise ValueError("AGMD balance is expected to be at most quadratic")

    constant, linear, quadratic = coefficients
    discriminant = linear * linear - 4.0 * quadratic * constant
    scale = linear * linear + abs(4.0 * quadratic * constant)
    tolerance = 64.0 * np.finfo(float).eps * scale

    if abs(discriminant) <= tolerance:
        return [-float(linear / (2.0 * quadratic))]
    if discriminant < 0.0:
        return []

    sqrt_discriminant = sqrt(discriminant)
    q = -0.5 * (linear + copysign(sqrt_discriminant, linear))
    if q == 0.0:
        return [-float(linear / (2.0 * quadratic))]
    return [float(q / quadratic), float(constant / q)]


def solve_agmd_reference(
    *,
    vaporization_efficiency: float,
    delta_t_c: float,
    delta_t_h_in_c: float,
    cold_inlet_c: float,
    cp_hot_j_kg_k: float,
    cp_cold_j_kg_k: float,
    cp_distillate_j_kg_k: float,
    latent_heat_j_kg: float,
    minimum_delta_t_h_out_c: float = 0.5,
    maximum_delta_t_h_out_c: float | None = None,
) -> AGMDReferenceResult:
    """Solve S2/S8 using caller-supplied properties and algebraic constraints.

    Temperatures are in °C and temperature differences in K/°C differences.
    Heat capacities are in J/(kg K); latent heat is in J/kg. The supplementary
    equations assume constant heat capacities along each stream and estimate
    distillate outlet temperature as (T_h,in + T_c,in + delta_T_h,out) / 2.

    The supplement's printed constraint sets delta_T_h,in = 0.5 °C, but its
    prose and the main article state that delta_T_h,in is fixed at 5 °C and
    delta_T_h,out >= 0.5 °C. This function does not hard-code delta_T_h,in;
    callers must choose and document the case being evaluated.

    Root admissibility here is limited to the supplied algebraic bounds and
    0 < recovery <= 1. Passing this filter is not physical validation of the
    assumed properties, operating state, or the paper's experimental regime.
    """
    values = {
        "vaporization_efficiency": vaporization_efficiency,
        "delta_t_c": delta_t_c,
        "delta_t_h_in_c": delta_t_h_in_c,
        "cold_inlet_c": cold_inlet_c,
        "cp_hot_j_kg_k": cp_hot_j_kg_k,
        "cp_cold_j_kg_k": cp_cold_j_kg_k,
        "cp_distillate_j_kg_k": cp_distillate_j_kg_k,
        "latent_heat_j_kg": latent_heat_j_kg,
        "minimum_delta_t_h_out_c": minimum_delta_t_h_out_c,
    }
    for name, value in values.items():
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if maximum_delta_t_h_out_c is not None and not isfinite(maximum_delta_t_h_out_c):
        raise ValueError("maximum_delta_t_h_out_c must be finite when supplied")
    if not 0 < vaporization_efficiency <= 1:
        raise ValueError("vaporization_efficiency must be in (0, 1]")
    for name in (
        "delta_t_c",
        "delta_t_h_in_c",
        "cp_hot_j_kg_k",
        "cp_cold_j_kg_k",
        "cp_distillate_j_kg_k",
        "latent_heat_j_kg",
        "minimum_delta_t_h_out_c",
    ):
        if values[name] <= 0:
            raise ValueError(f"{name} must be > 0")
    if delta_t_h_in_c >= delta_t_c:
        raise ValueError("delta_t_h_in_c must be smaller than delta_t_c")
    if maximum_delta_t_h_out_c is not None:
        if maximum_delta_t_h_out_c <= 0:
            raise ValueError("maximum_delta_t_h_out_c must be > 0")
        if maximum_delta_t_h_out_c < minimum_delta_t_h_out_c:
            raise ValueError("maximum outlet difference cannot be below the minimum")

    hot_inlet_c = cold_inlet_c + delta_t_c
    # From S2: R = eta * c_h * (delta_T - delta_T_h,out) / h_vap.
    recovery_per_kelvin = (
        vaporization_efficiency * cp_hot_j_kg_k / latent_heat_j_kg
    )
    x = np.polynomial.Polynomial([0.0, 1.0])
    recovery = recovery_per_kelvin * (delta_t_c - x)
    distillate_outlet = (
        hot_inlet_c + cold_inlet_c + x
    ) / 2.0

    # S8 rearranged to residual = 0, retaining the source equation's signs.
    balance = (
        (recovery - 1.0) * cp_hot_j_kg_k * (x + cold_inlet_c)
        - recovery * cp_distillate_j_kg_k * distillate_outlet
        - hot_inlet_c * (cp_cold_j_kg_k - cp_hot_j_kg_k)
        + cp_cold_j_kg_k * (delta_t_h_in_c + cold_inlet_c)
    )
    candidates: list[tuple[float, float]] = []
    for delta_t_h_out in _real_polynomial_roots(balance):
        recovery_value = recovery_per_kelvin * (delta_t_c - delta_t_h_out)
        if (
            minimum_delta_t_h_out_c - 1e-9 <= delta_t_h_out
            and (maximum_delta_t_h_out_c is None or delta_t_h_out <= maximum_delta_t_h_out_c + 1e-9)
            and 0.0 < recovery_value <= 1.0
        ):
            candidates.append((delta_t_h_out, recovery_value))

    if len(candidates) != 1:
        raise ValueError(
            "Expected exactly one model-admissible real root under the supplied "
            f"constraints; found {len(candidates)}. Check property inputs and source assumptions."
        )

    delta_t_h_out, recovery_value = candidates[0]
    distillate_outlet_value = (
        hot_inlet_c + cold_inlet_c + delta_t_h_out
    ) / 2.0
    s2_residual = (
        vaporization_efficiency
        - recovery_value * latent_heat_j_kg
        / (cp_hot_j_kg_k * (delta_t_c - delta_t_h_out))
    )
    s8_residual = (
        (recovery_value - 1.0)
        * cp_hot_j_kg_k
        * (delta_t_h_out + cold_inlet_c)
        - recovery_value * cp_distillate_j_kg_k * distillate_outlet_value
        - hot_inlet_c * (cp_cold_j_kg_k - cp_hot_j_kg_k)
        + cp_cold_j_kg_k * (delta_t_h_in_c + cold_inlet_c)
    )
    return AGMDReferenceResult(
        delta_t_h_out_c=delta_t_h_out,
        recovery_fraction=recovery_value,
        distillate_outlet_c=distillate_outlet_value,
        equation_s2_residual=s2_residual,
        equation_s8_residual_w_per_kg_k=s8_residual,
    )
