"""Reduced-order membrane-distillation thermal accounting.

This module deliberately separates:
1. useful vaporization duty,
2. conductive heat leak through the membrane,
3. the supplied hot-side thermal duty,
4. the corresponding cold-side duty.

It is a screening layer, not a channel-resolved CFD model. The conductive
term requires membrane-specific thickness and thermal conductivity; if those
are not supplied, the caller must not silently invent them.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class MDThermalResult:
    latent_duty_kwh_th: float
    conductive_heat_leak_kwh_th: float
    hot_side_duty_kwh_th: float
    cold_side_duty_kwh_th: float

def account_for_membrane_heat(
    *,
    water_kg: float,
    latent_heat_kwh_th_per_kg: float,
    membrane_area_m2: float,
    interface_delta_t_k: float,
    membrane_thermal_conductivity_w_m_k: float | None = None,
    membrane_thickness_m: float | None = None,
    duration_h: float,
) -> MDThermalResult:
    if water_kg < 0 or latent_heat_kwh_th_per_kg <= 0:
        raise ValueError("water_kg must be non-negative and latent heat must be positive")
    if membrane_area_m2 <= 0 or duration_h <= 0:
        raise ValueError("area and duration must be positive")
    if interface_delta_t_k < 0:
        raise ValueError("interface temperature difference cannot be negative")

    latent = water_kg * latent_heat_kwh_th_per_kg

    supplied_geometry = (
        membrane_thermal_conductivity_w_m_k is not None
        or membrane_thickness_m is not None
    )
    if supplied_geometry and (
        membrane_thermal_conductivity_w_m_k is None
        or membrane_thickness_m is None
    ):
        raise ValueError("membrane conductivity and thickness must be supplied together")
    if membrane_thermal_conductivity_w_m_k is not None:
        if membrane_thermal_conductivity_w_m_k < 0 or membrane_thickness_m <= 0:
            raise ValueError("membrane conductivity must be non-negative and thickness positive")
        conductive = (
            membrane_thermal_conductivity_w_m_k
            / membrane_thickness_m
            * interface_delta_t_k
            * membrane_area_m2
            * duration_h
            / 1000.0
        )
        # W -> kW, then multiply by h.
    else:
        conductive = 0.0

    return MDThermalResult(
        latent_duty_kwh_th=latent,
        conductive_heat_leak_kwh_th=conductive,
        hot_side_duty_kwh_th=latent + conductive,
        cold_side_duty_kwh_th=latent + conductive,
    )
