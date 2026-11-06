"""Wyon (2025) Appendix A fluid-property correlations for the initial DCMD model.

This module transcribes the thesis's seawater and pure-water properties used
to calculate channel Reynolds, Prandtl, Nusselt, and film heat-transfer
coefficients. It preserves Wyon's historical correlation set; it does not
replace it with IAPWS-08 or the newer Nayar vapour-pressure formulation.

Salinity inputs use reference salinity S_R in g/kg. The appendix converts to
practical salinity S_P = S_R / 1.00472 where required. Temperatures supplied
by callers are ITS-90 Celsius; correlations requiring IPTS-68 are converted
using Sharqawy et al. (2010), Eq. (4).

Sources:
- Wyon (2025), Appendix A, Eqs. (A1)-(A8).
- Sharqawy, Lienhard & Zubair (2010), DOI 10.5004/dwt.2010.1079.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log10

from .sharqawy_2010 import (
    jamieson_seawater_cp_j_kg_k,
    pure_water_cp_j_kg_k,
    reference_to_practical_salinity_g_kg,
    its90_to_ipts68_kelvin,
)
from .wyon_2025_surface_reference import (
    wyon_convective_heat_transfer_coefficient_w_m2_k,
    wyon_nusselt_number,
)


@dataclass(frozen=True)
class WyonFluidProperties:
    """Bulk-fluid properties at one local mean temperature."""

    heat_capacity_j_kg_k: float
    thermal_conductivity_w_m_k: float
    density_kg_m3: float
    dynamic_viscosity_pa_s: float


@dataclass(frozen=True)
class WyonChannelTransfer:
    """Hydrodynamic and convective-transfer quantities for one channel."""

    properties: WyonFluidProperties
    reynolds: float
    prandtl: float
    nusselt: float
    heat_transfer_coefficient_w_m2_k: float


def _finite(name: str, value: float) -> None:
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def _validate_temperature_salinity(
    temperature_its90_c: float, salinity_sr_g_kg: float
) -> tuple[float, float]:
    _finite("temperature_its90_c", temperature_its90_c)
    _finite("salinity_sr_g_kg", salinity_sr_g_kg)
    if not 0.0 <= temperature_its90_c <= 100.0:
        raise ValueError("Wyon Appendix A property evaluation is restricted to 0-100 C")
    if not 0.0 <= salinity_sr_g_kg <= 160.0:
        raise ValueError("salinity_sr_g_kg must be in [0, 160] g/kg")
    t68_k = its90_to_ipts68_kelvin(temperature_its90_c + 273.15)
    t68_c = t68_k - 273.15
    sp = reference_to_practical_salinity_g_kg(salinity_sr_g_kg)
    return t68_c, sp


def pure_water_thermal_conductivity_w_m_k(temperature_its90_c: float) -> float:
    """Wyon Appendix A Eq. (A4), pure-water conductivity in W/(m K)."""
    _finite("temperature_its90_c", temperature_its90_c)
    if not 0.0 <= temperature_its90_c <= 100.0:
        raise ValueError("temperature_its90_c must be in [0, 100] C")
    temperature_k = temperature_its90_c + 273.15
    a = (0.80201, -0.25992, 0.10024, -0.032005)
    b = (-0.32, -5.7, -12.0, -15.0)
    return sum(ai * (temperature_k / 300.0) ** bi for ai, bi in zip(a, b))


def seawater_thermal_conductivity_w_m_k(
    temperature_its90_c: float, salinity_sr_g_kg: float
) -> float:
    """Wyon Appendix A Eq. (A3), seawater conductivity in W/(m K).

    The printed correlation returns mW/(m K); this function converts to W/(m K).
    """
    t68_c, sp = _validate_temperature_salinity(
        temperature_its90_c, salinity_sr_g_kg
    )
    t68_k = t68_c + 273.15
    log10_k_mw = (
        log10(240.0 + 0.0002 * sp)
        + 0.434
        * (2.3 - (343.5 + 0.037 * sp) / t68_k)
        * (1.0 - t68_k / (647.0 + 0.03 * sp)) ** 0.333
    )
    return 10.0**log10_k_mw / 1000.0


def pure_water_density_kg_m3(temperature_its90_c: float) -> float:
    """Wyon Appendix A Eq. (A6), pure-water density in kg/m3."""
    _finite("temperature_its90_c", temperature_its90_c)
    if not 0.0 <= temperature_its90_c <= 100.0:
        raise ValueError("temperature_its90_c must be in [0, 100] C")
    t = temperature_its90_c
    coefficients = (
        9.999e2,
        2.034e-2,
        -6.126e-3,
        2.261e-5,
        -4.657e-8,
    )
    return sum(coefficient * t**power for power, coefficient in enumerate(coefficients))


def seawater_density_kg_m3(
    temperature_its90_c: float, salinity_sr_g_kg: float
) -> float:
    """Wyon Appendix A Eq. (A5), seawater density in kg/m3."""
    t68_c, sp = _validate_temperature_salinity(
        temperature_its90_c, salinity_sr_g_kg
    )
    b = (2.0 * sp - 150.0) / 150.0
    g1, g2, g3 = 0.5, b, 2.0 * b**2 - 1.0
    a1 = 4.032 * g1 + 0.115 * g2 + 3.26e-4 * g3
    a2 = -0.108 * g1 + 1.571e-3 * g2 - 4.23e-4 * g3
    a3 = -0.012 * g1 + 1.74e-3 * g2 - 9.0e-6 * g3
    a4 = 6.92e-4 * g1 - 8.7e-5 * g2 - 5.3e-5 * g3
    a = (2.0 * t68_c - 200.0) / 160.0
    f1, f2 = 0.5, a
    f3, f4 = 2.0 * a**2 - 1.0, 4.0 * a**3 - 3.0 * a
    return 1000.0 * (a1 * f1 + a2 * f2 + a3 * f3 + a4 * f4)


def pure_water_dynamic_viscosity_pa_s(temperature_its90_c: float) -> float:
    """Wyon Appendix A Eq. (A8), pure-water dynamic viscosity in Pa s."""
    _finite("temperature_its90_c", temperature_its90_c)
    if 0.0 <= temperature_its90_c <= 100.0:
        t = temperature_its90_c
    else:
        raise ValueError("temperature_its90_c must be in [0, 100] C")
    denominator = 0.157 * (t + 64.993) ** 2 - 91.296
    if denominator <= 0:
        raise ArithmeticError("pure-water viscosity denominator must be positive")
    return 4.2844e-5 + 1.0 / denominator


def seawater_dynamic_viscosity_pa_s(
    temperature_its90_c: float, salinity_sr_g_kg: float
) -> float:
    """Wyon Appendix A Eq. (A7), seawater dynamic viscosity in Pa s."""
    _validate_temperature_salinity(temperature_its90_c, salinity_sr_g_kg)
    salinity_mass_fraction = salinity_sr_g_kg / 1000.0
    t = temperature_its90_c
    a = 1.541 + 1.998e-2 * t - 9.52e-5 * t**2
    b = 7.974 - 7.561e-2 * t + 4.724e-4 * t**2
    return pure_water_dynamic_viscosity_pa_s(t) * (
        1.0 + a * salinity_mass_fraction + b * salinity_mass_fraction**2
    )


def wyon_fluid_properties(
    temperature_its90_c: float, salinity_sr_g_kg: float
) -> WyonFluidProperties:
    """Return Wyon Appendix A cp, k, rho, and mu for seawater or pure water.

    A salinity of exactly zero selects the pure-water correlations. Nonzero
    salinity selects the seawater correlations. The heat-capacity functions
    are the corresponding A1/A2 fits already transcribed in sharqawy_2010.py.
    """
    _validate_temperature_salinity(temperature_its90_c, salinity_sr_g_kg)
    if salinity_sr_g_kg == 0.0:
        return WyonFluidProperties(
            heat_capacity_j_kg_k=pure_water_cp_j_kg_k(temperature_its90_c),
            thermal_conductivity_w_m_k=pure_water_thermal_conductivity_w_m_k(
                temperature_its90_c
            ),
            density_kg_m3=pure_water_density_kg_m3(temperature_its90_c),
            dynamic_viscosity_pa_s=pure_water_dynamic_viscosity_pa_s(
                temperature_its90_c
            ),
        )
    return WyonFluidProperties(
        heat_capacity_j_kg_k=jamieson_seawater_cp_j_kg_k(
            temperature_its90_c, salinity_sr_g_kg
        ),
        thermal_conductivity_w_m_k=seawater_thermal_conductivity_w_m_k(
            temperature_its90_c, salinity_sr_g_kg
        ),
        density_kg_m3=seawater_density_kg_m3(
            temperature_its90_c, salinity_sr_g_kg
        ),
        dynamic_viscosity_pa_s=seawater_dynamic_viscosity_pa_s(
            temperature_its90_c, salinity_sr_g_kg
        ),
    )


def wyon_channel_heat_transfer(
    *,
    velocity_m_s: float,
    hydraulic_diameter_m: float,
    channel_length_m: float,
    temperature_its90_c: float,
    salinity_sr_g_kg: float,
) -> WyonChannelTransfer:
    """Calculate Re, Pr, Nu, and alpha from Wyon's appendix properties.

    The caller must supply the local arithmetic-mean bulk/interface temperature.
    """
    for name, value in (
        ("velocity_m_s", velocity_m_s),
        ("hydraulic_diameter_m", hydraulic_diameter_m),
        ("channel_length_m", channel_length_m),
    ):
        _finite(name, value)
        if value <= 0.0:
            raise ValueError(f"{name} must be > 0")
    properties = wyon_fluid_properties(temperature_its90_c, salinity_sr_g_kg)
    reynolds = (
        velocity_m_s
        * hydraulic_diameter_m
        * properties.density_kg_m3
        / properties.dynamic_viscosity_pa_s
    )
    prandtl = (
        properties.dynamic_viscosity_pa_s
        * properties.heat_capacity_j_kg_k
        / properties.thermal_conductivity_w_m_k
    )
    nusselt = wyon_nusselt_number(
        reynolds=reynolds,
        prandtl=prandtl,
        hydraulic_diameter_m=hydraulic_diameter_m,
        channel_length_m=channel_length_m,
    )
    alpha = wyon_convective_heat_transfer_coefficient_w_m2_k(
        nusselt=nusselt,
        fluid_thermal_conductivity_w_m_k=properties.thermal_conductivity_w_m_k,
        hydraulic_diameter_m=hydraulic_diameter_m,
    )
    return WyonChannelTransfer(
        properties=properties,
        reynolds=reynolds,
        prandtl=prandtl,
        nusselt=nusselt,
        heat_transfer_coefficient_w_m2_k=alpha,
    )
