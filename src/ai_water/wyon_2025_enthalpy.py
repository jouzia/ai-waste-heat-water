"""Wyon (2025) Appendix A specific-enthalpy correlations.

The appendix labels salinity S in kg/kg and temperature t in Celsius.
Public functions accept reference salinity in g/kg and convert it to kg/kg.
Specific enthalpy is returned in J/kg, consistent with the cp correlations
and the module enthalpy-rate balance H = m_dot * h.
"""
from __future__ import annotations

from math import isfinite


def _validate_temperature(temperature_its90_c: float) -> None:
    if not isfinite(temperature_its90_c):
        raise ValueError("temperature_its90_c must be finite")
    if not 0.0 <= temperature_its90_c <= 100.0:
        raise ValueError("Wyon Appendix A enthalpy evaluation is restricted to 0-100 C")


def _salinity_mass_fraction(salinity_sr_g_kg: float) -> float:
    if not isfinite(salinity_sr_g_kg):
        raise ValueError("salinity_sr_g_kg must be finite")
    if not 0.0 <= salinity_sr_g_kg <= 160.0:
        raise ValueError("salinity_sr_g_kg must be in [0, 160] g/kg")
    return salinity_sr_g_kg / 1000.0


def wyon_pure_water_specific_enthalpy_j_kg(
    temperature_its90_c: float,
) -> float:
    """Wyon Appendix A Eq. (A12), pure-water specific enthalpy in J/kg."""
    _validate_temperature(temperature_its90_c)
    t = temperature_its90_c
    return 141.355 + 4202.07 * t - 0.535 * t**2 + 0.004 * t**3


def wyon_seawater_specific_enthalpy_j_kg(
    temperature_its90_c: float, salinity_sr_g_kg: float
) -> float:
    """Wyon Appendix A Eq. (A11), seawater specific enthalpy in J/kg."""
    _validate_temperature(temperature_its90_c)
    salinity = _salinity_mass_fraction(salinity_sr_g_kg)
    t = temperature_its90_c
    a1 = -2.348e4
    a2 = 3.152e5
    a3 = 2.803e6
    a4 = -1.446e7
    a5 = 7.826e3
    a6 = -4.417e1
    a7 = 2.139e-1
    a8 = -1.991e4
    a9 = 2.778e4
    a10 = 9.728e1
    salinity_correction = salinity * (
        a1
        + a2 * salinity
        + a3 * salinity**2
        + a4 * salinity**3
        + a5 * t
        + a6 * t**2
        + a7 * t**3
        + a8 * salinity * t
        + a9 * salinity**2 * t
        + a10 * salinity * t**2
    )
    return wyon_pure_water_specific_enthalpy_j_kg(t) - salinity_correction


def wyon_specific_enthalpy_j_kg(
    temperature_its90_c: float, salinity_sr_g_kg: float = 0.0
) -> float:
    """Dispatch to the Appendix A pure-water or seawater enthalpy fit."""
    if salinity_sr_g_kg == 0.0:
        return wyon_pure_water_specific_enthalpy_j_kg(temperature_its90_c)
    return wyon_seawater_specific_enthalpy_j_kg(
        temperature_its90_c, salinity_sr_g_kg
    )


def wyon_temperature_from_specific_enthalpy_c(
    specific_enthalpy_j_kg: float,
    salinity_sr_g_kg: float = 0.0,
    *,
    lower_temperature_c: float = 0.0,
    upper_temperature_c: float = 100.0,
    temperature_tolerance_c: float = 1e-10,
    max_iterations: int = 200,
) -> float:
    """Invert the Wyon Appendix A enthalpy fit by bracketed bisection.

    The inversion is restricted to the supported 0-100 C model domain and
    fails explicitly when the requested enthalpy is not bracketed.
    """
    if not isfinite(specific_enthalpy_j_kg):
        raise ValueError("specific_enthalpy_j_kg must be finite")
    _salinity_mass_fraction(salinity_sr_g_kg)
    if not (
        0.0 <= lower_temperature_c < upper_temperature_c <= 100.0
    ):
        raise ValueError("temperature bounds must satisfy 0 <= lower < upper <= 100 C")
    if not isfinite(temperature_tolerance_c) or temperature_tolerance_c <= 0.0:
        raise ValueError("temperature_tolerance_c must be finite and positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")

    def enthalpy_at(t: float) -> float:
        return wyon_specific_enthalpy_j_kg(t, salinity_sr_g_kg)

    low_h = enthalpy_at(lower_temperature_c)
    high_h = enthalpy_at(upper_temperature_c)
    if not low_h <= specific_enthalpy_j_kg <= high_h:
        raise ValueError(
            "specific_enthalpy_j_kg is outside the enthalpy range for the "
            "requested temperature bounds"
        )

    low = lower_temperature_c
    high = upper_temperature_c
    for _ in range(max_iterations):
        midpoint = 0.5 * (low + high)
        mid_h = enthalpy_at(midpoint)
        if abs(mid_h - specific_enthalpy_j_kg) <= 1e-8:
            return midpoint
        if high - low <= temperature_tolerance_c:
            return midpoint
        if mid_h < specific_enthalpy_j_kg:
            low = midpoint
        else:
            high = midpoint

    raise RuntimeError(
        "Wyon enthalpy inversion did not converge within "
        f"{max_iterations} iterations"
    )
