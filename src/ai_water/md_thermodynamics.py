"""Equation-level screening calculations based on Malaguti et al. (2026).

This module intentionally does not derive outlet temperature differences or recovery:
those require the paper's supplementary derivation and a separately verified property
model. Inputs are explicit so callers cannot mistake the equations for a full MD simulator.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

J_PER_KWH = 3_600_000.0


@dataclass(frozen=True)
class MDRequirements:
    """Specific thermal/cooling requirements on a volumetric product-water basis."""

    stec_kwh_m3: float
    scr_kwh_m3: float


def _positive_finite(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and > 0")


def evaluate_requirements(
    *,
    configuration: int,
    delta_t_k: float,
    delta_t_h_in_k: float,
    delta_t_h_out_k: float,
    hvap_j_kg: float,
    vaporization_efficiency: float,
    density_kg_m3: float,
    delta_t_hx_k: float | None = None,
    c_hot_j_kg_k: float | None = None,
    c_cold_j_kg_k: float | None = None,
) -> MDRequirements:
    """Evaluate published STEC/SCR equations for a supplied outlet temperature difference.

    All temperature differences are in K (numerically equivalent to °C differences),
    hvap in J/kg, heat capacities in J/(kg K), and density in kg/m³.
    Returned values are kWh/m³ of distillate.

    delta_t_h_out_k must come from a separately validated calculation or a
    published benchmark; this function does not infer it from other inputs.
    """
    for name, value in (
        ("delta_t_k", delta_t_k),
        ("delta_t_h_in_k", delta_t_h_in_k),
        ("delta_t_h_out_k", delta_t_h_out_k),
        ("hvap_j_kg", hvap_j_kg),
        ("density_kg_m3", density_kg_m3),
    ):
        _positive_finite(name, value)
    if not isfinite(vaporization_efficiency) or not 0 < vaporization_efficiency <= 1:
        raise ValueError("vaporization_efficiency must be in (0, 1]")
    denominator = delta_t_k - delta_t_h_out_k
    if denominator <= 0:
        raise ValueError("delta_t_k must exceed delta_t_h_out_k")
    if delta_t_h_in_k >= delta_t_k:
        raise ValueError("delta_t_h_in_k must be smaller than delta_t_k")

    eta = vaporization_efficiency
    if configuration == 1:
        scr_j_kg = (hvap_j_kg / eta) * (
            (delta_t_k - delta_t_h_in_k) / denominator
        )
        stec_j_kg = (hvap_j_kg / eta) * (delta_t_k / denominator)
    elif configuration == 2:
        if delta_t_hx_k is None:
            raise ValueError("configuration 2 requires delta_t_hx_k")
        _positive_finite("delta_t_hx_k", delta_t_hx_k)
        scr_j_kg = (hvap_j_kg / eta) * (delta_t_hx_k / denominator)
        stec_j_kg = (hvap_j_kg / eta) * (
            (delta_t_h_in_k + delta_t_hx_k) / denominator
        )
    elif configuration == 3:
        if c_hot_j_kg_k is None or c_cold_j_kg_k is None:
            raise ValueError("configuration 3 requires hot- and cold-stream heat capacities")
        _positive_finite("c_hot_j_kg_k", c_hot_j_kg_k)
        _positive_finite("c_cold_j_kg_k", c_cold_j_kg_k)
        scr_j_kg = (
            hvap_j_kg * c_cold_j_kg_k / (eta * c_hot_j_kg_k)
        ) * (delta_t_h_out_k / denominator)
        stec_j_kg = (hvap_j_kg / eta) * (
            delta_t_h_in_k / denominator
        )
    else:
        raise ValueError("configuration must be 1, 2, or 3")

    # Convert J/kg distillate to kWh/m³ using the explicitly supplied product density.
    scale = density_kg_m3 / J_PER_KWH
    return MDRequirements(stec_kwh_m3=stec_j_kg * scale, scr_kwh_m3=scr_j_kg * scale)


def module_pumping_kwh_m3(
    *,
    pressure_drop_pa: float,
    single_pass_recovery: float,
    pump_efficiency: float,
) -> float:
    """Return module pumping energy in kWh/m³ product from deltaP/(R * eta_pump).

    Pressure is in Pa (= J/m³); recovery and pump efficiency are dimensionless.
    """
    _positive_finite("pressure_drop_pa", pressure_drop_pa)
    if not isfinite(single_pass_recovery) or not 0 < single_pass_recovery <= 1:
        raise ValueError("single_pass_recovery must be in (0, 1]")
    if not isfinite(pump_efficiency) or not 0 < pump_efficiency <= 1:
        raise ValueError("pump_efficiency must be in (0, 1]")
    return pressure_drop_pa / (
        single_pass_recovery * pump_efficiency * J_PER_KWH
    )
