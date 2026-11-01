"""Explicit property correlations transcribed from Sharqawy et al. (2010).

This module does not choose the AGMD stream evaluation temperatures or salinity.
Callers must supply ITS-90 temperature and reference-composition salinity (S_R).
The Jamieson seawater heat-capacity fit internally requires IPTS-68 temperature
and practical salinity (S_P), converted using Sharqawy et al. Eqs. (3) and (4).

Source: Sharqawy, Lienhard V & Zubair (2010), Desalination and Water Treatment
16, 354-380, DOI 10.5004/dwt.2010.1079; Eqs. (3), (4), (9), (37), and (54),
and Table 11 Eq. (51). The 2011 erratum to Eq. (6) is unrelated to these fits.
"""

from __future__ import annotations

from math import isfinite


def _finite(name: str, value: float) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def its90_to_ipts68_kelvin(temperature_its90_k: float) -> float:
    """Convert ITS-90 absolute temperature to IPTS-68 (Sharqawy Eq. 4)."""
    _finite("temperature_its90_k", temperature_its90_k)
    return (temperature_its90_k - 0.00025 * 273.15) / (1.0 - 0.00025)


def reference_to_practical_salinity_g_kg(salinity_sr_g_kg: float) -> float:
    """Convert reference-composition salinity S_R to practical salinity S_P (Eq. 3)."""
    _finite("salinity_sr_g_kg", salinity_sr_g_kg)
    if not 0.0 <= salinity_sr_g_kg <= 180.0:
        raise ValueError("salinity_sr_g_kg must be in [0, 180] g/kg")
    return salinity_sr_g_kg / 1.00472


def jamieson_seawater_cp_j_kg_k(
    temperature_its90_c: float, salinity_sr_g_kg: float
) -> float:
    """Return seawater cp from Sharqawy Eq. (9), converted to J/(kg K).

    Eq. (9) uses T_68 in kelvin and S_P in g/kg. The recommended range is
    273.15 < T_68 < 453.15 K and 0 < S_P < 180 g/kg. No extrapolation is done.
    """
    _finite("temperature_its90_c", temperature_its90_c)
    t68_k = its90_to_ipts68_kelvin(temperature_its90_c + 273.15)
    sp = reference_to_practical_salinity_g_kg(salinity_sr_g_kg)
    if not 273.15 < t68_k < 453.15:
        raise ValueError("Eq. (9) requires 273.15 < T_68 < 453.15 K")
    if not 0.0 < sp < 180.0:
        raise ValueError("Eq. (9) requires 0 < S_P < 180 g/kg")

    a = 5.328 - 9.76e-2 * sp + 4.04e-4 * sp**2
    b = -6.913e-3 + 7.351e-4 * sp - 3.15e-6 * sp**2
    c = 9.6e-6 - 1.927e-6 * sp + 8.23e-9 * sp**2
    d = 2.5e-9 + 1.666e-9 * sp - 7.125e-12 * sp**2
    return 1000.0 * (a + b * t68_k + c * t68_k**2 + d * t68_k**3)


def pure_water_cp_j_kg_k(
    temperature_its90_c: float, pressure_mpa: float = 0.1
) -> float:
    """Return pure-water cp from Sharqawy Table 11 Eq. (51), in J/(kg K).

    The pressure argument is in MPa. The default is 0.1 MPa, the atmospheric
    pressure convention used for the paper's pure-water property table.
    """
    _finite("temperature_its90_c", temperature_its90_c)
    _finite("pressure_mpa", pressure_mpa)
    t = temperature_its90_c
    p = pressure_mpa
    if not 0.0 <= t <= 374.0:
        raise ValueError("Eq. (51) requires 0 <= temperature <= 374 C")
    if not 0.1 < p < 100.0:
        raise ValueError("Eq. (51) requires 0.1 < pressure < 100 MPa")
    a1, a2, a3, a4 = 4.193, -2.273e-4, 2.369e-6, 1.670e-10
    a5, a6, a7 = -3.978e-3, 3.229e-5, -1.073e-9
    a8, a9, a10 = 1.913e-5, -4.176e-7, 2.306e-9
    cp_kj_kg_k = (
        a1 + a2*t + a3*t**2 + a4*t**4
        + a5*p + a6*p*t + a7*p*t**3
        + a8*p**2 + a9*p**2*t + a10*p**2*t**2
    )
    return 1000.0 * cp_kj_kg_k


def pure_water_latent_heat_j_kg(temperature_its90_c: float) -> float:
    """Return pure-water latent heat from Sharqawy Table 11 Eq. (54), J/kg."""
    _finite("temperature_its90_c", temperature_its90_c)
    t = temperature_its90_c
    if not 0.0 <= t <= 200.0:
        raise ValueError("Eq. (54) requires 0 <= temperature <= 200 C")
    return (
        2.501e6 - 2.369e3*t + 2.678e-1*t**2
        - 8.103e-3*t**3 - 2.079e-5*t**4
    )


def seawater_latent_heat_j_kg(
    temperature_its90_c: float, salinity_sr_g_kg: float
) -> float:
    """Return seawater-basis latent heat using Sharqawy Eq. (37), J/kg.

    Eq. (37) multiplies pure-water latent heat by (1 - S_R/1000), converting
    from per kg evaporated water to per kg total saline solution.
    """
    _finite("salinity_sr_g_kg", salinity_sr_g_kg)
    if not 0.0 <= salinity_sr_g_kg <= 1000.0:
        raise ValueError("salinity_sr_g_kg must be in [0, 1000] g/kg")
    return pure_water_latent_heat_j_kg(temperature_its90_c) * (
        1.0 - salinity_sr_g_kg / 1000.0
    )
