"""Nayar et al. (2016) natural-seawater vapour-pressure correlations.

This is an alternative property formulation, not a replacement for Wyon's
historical Appendix A Eq. (A9) baseline. Salinity is Reference Salinity in
g/kg. Temperature is ITS-90 Celsius and is converted to kelvin for Eq. (6).

Source: Nayar et al. (2016), Desalination 390, 1-24, Eqs. (5)-(6),
DOI: 10.1016/j.desal.2016.02.024.
"""
from __future__ import annotations

from math import exp, isfinite, log


def _validate_temperature(temperature_c: float) -> None:
    if not isfinite(temperature_c) or not 0.0 <= temperature_c <= 180.0:
        raise ValueError("temperature_c must be finite and in [0, 180] C")


def nayar_pure_water_vapour_pressure_pa(temperature_c: float) -> float:
    """Nayar et al. (2016) Eq. (6), pure-water saturation pressure in Pa."""
    _validate_temperature(temperature_c)
    temperature_k = temperature_c + 273.15
    log_pressure = (
        -5800.0 / temperature_k
        + 1.3915
        - 4.8640e-2 * temperature_k
        + 4.1765e-5 * temperature_k**2
        - 1.4452e-8 * temperature_k**3
        + 6.5460 * log(temperature_k)
    )
    return exp(log_pressure)


def nayar_natural_seawater_vapour_pressure_pa(
    temperature_c: float, reference_salinity_g_kg: float
) -> float:
    """Nayar et al. (2016) Eq. (5), natural-seawater vapour pressure in Pa.

    The salinity argument is Reference Salinity in g/kg (not kg/kg, practical
    salinity, or NaCl concentration). Validity: 0-180 C and 0-160 g/kg.
    Nayar report a maximum uncertainty of +/-0.26% within the stated range.
    """
    _validate_temperature(temperature_c)
    if (
        not isfinite(reference_salinity_g_kg)
        or not 0.0 <= reference_salinity_g_kg <= 160.0
    ):
        raise ValueError("reference_salinity_g_kg must be finite and in [0, 160] g/kg")
    salinity = reference_salinity_g_kg
    salinity_factor = exp(
        -4.58180e-4 * salinity - 2.04430e-6 * salinity**2
    )
    return salinity_factor * nayar_pure_water_vapour_pressure_pa(temperature_c)
