"""Standalone numerical reference for Malaguti et al. (2026), AGMD configuration 3.

This module solves supplementary equations S2 and S8 with explicit property inputs.
It does not select or silently infer property values; source-matched Sharqawy inputs
must be supplied by the caller before this is treated as a paper reproduction.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

import numpy as np


@dataclass(frozen=True)
class AGMDReferenceResult:
    """Solution to the configuration-3 balance equations."""

    delta_t_h_out_c: float
    recovery_fraction: float
    distillate_outlet_c: float
    equation_s2_residual: float
    equation_s8_residual_w_per_kg_k: float


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
) -> AGMDReferenceResult:
    """Solve S2/S8 for AGMD using caller-supplied properties and SI units.

    Temperatures are in °C and temperature differences in K/°C differences.
    Heat capacities are in J/(kg K); latent heat is in J/kg. The supplementary
    equations assume constant heat capacities along each stream and estimate
    distillate outlet temperature as (T_h,in + T_c,in + delta_T_h,out) / 2.

    The supplement's printed constraint sets delta_T_h,in = 0.5 °C, but its
    prose and the main article state that delta_T_h,in is fixed at 5 °C and
    delta_T_h,out >= 0.5 °C. This function does not hard-code delta_T_h,in;
    callers must choose and document the case being evaluated.
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
    if minimum_delta_t_h_out_c > delta_t_h_in_c:
        raise ValueError("minimum outlet difference cannot exceed inlet difference")

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
    for root in balance.roots():
        if abs(float(root.imag)) > 1e-8:
            continue
        delta_t_h_out = float(root.real)
        recovery_value = recovery_per_kelvin * (delta_t_c - delta_t_h_out)
        if (
            minimum_delta_t_h_out_c - 1e-9 <= delta_t_h_out <= delta_t_h_in_c + 1e-9
            and 0.0 < recovery_value <= 1.0
        ):
            candidates.append((delta_t_h_out, recovery_value))

    if len(candidates) != 1:
        raise ValueError(
            "Expected exactly one physically admissible real root; "
            f"found {len(candidates)}. Check property inputs and source assumptions."
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
