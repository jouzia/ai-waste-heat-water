"""Membrane-distillation transport primitives.

The first implementation uses the standard pressure-difference formulation
J = C_m * (p_v,hot - p_v,cold). C_m remains an explicit calibrated or
literature-derived parameter; it is not inferred from an arbitrary membrane.

Pure-water saturation pressure uses NIST Chemistry WebBook Antoine
coefficients. Salinity/activity corrections are intentionally not applied
here and must be added before this is used for saline-feed prediction.
"""
_ANTOINE = (
    (304.0, 333.0, 5.20389, 1733.926, -39.485),
    (334.0, 363.0, 5.0768, 1659.793, -45.854),
)

def saturation_pressure_bar(temperature_c: float) -> float:
    """Return pure-water saturation pressure in bar for the supported range."""
    temperature_k = temperature_c + 273.15
    for lower, upper, a, b, c in _ANTOINE:
        if lower <= temperature_k <= upper:
            return 10.0 ** (a - b / (temperature_k + c))
    raise ValueError("temperature is outside the implemented NIST Antoine ranges (304-363 K)")

def vapor_pressure_driving_force_bar(hot_c: float, cold_c: float) -> float:
    """Pure-water vapor-pressure difference across an idealized MD interface."""
    return saturation_pressure_bar(hot_c) - saturation_pressure_bar(cold_c)

def flux_kg_m2_h(hot_c: float, cold_c: float, membrane_permeance_kg_m2_h_bar: float) -> float:
    """Compute idealized pure-water MD flux from pressure driving force."""
    if membrane_permeance_kg_m2_h_bar < 0:
        raise ValueError("membrane permeance must be non-negative")
    return max(0.0, membrane_permeance_kg_m2_h_bar * vapor_pressure_driving_force_bar(hot_c, cold_c))
