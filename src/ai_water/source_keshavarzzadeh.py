"""Explicit Keshavarzzadeh (2020) source-model equations.

These functions are kept separate from the project's current preferred
thermodynamic pathway. They exist solely to reproduce the published model
form without silently replacing it with newer correlations.
"""
import math


def source_water_activity_from_molar_nacl(x: float) -> float:
    """Eq. (6)-(7) multiplier gamma_w(1-X) used by the source."""
    if not 0 <= x < 1:
        raise ValueError("molar solute fraction must be in [0,1)")
    gamma_w = 1.0 - 0.5 * x - 10.0 * x**2
    return gamma_w * (1.0 - x)


def source_saturation_pressure_pa(temperature_c: float) -> float:
    """Eq. (8), with temperature supplied in Celsius as in the paper."""
    temperature_k = temperature_c + 273.15
    if not 273.0 <= temperature_k <= 373.0:
        raise ValueError("source Antoine correlation is stated for 273-373 K")
    return math.exp(23.1964 - 3816.44 / (temperature_k - 46.13))


def source_membrane_flux_coefficient(
    *,
    temperature_k: float,
    pore_radius_m: float,
    thickness_m: float,
    porosity: float,
    tortuosity: float,
    atmospheric_pressure_pa: float = 101325.0,
) -> float:
    """Eq. (2) membrane flux coefficient B from the published model."""
    if temperature_k <= 0 or pore_radius_m <= 0 or thickness_m <= 0:
        raise ValueError("temperature, pore radius, and thickness must be positive")
    if not 0 < porosity <= 1 or tortuosity <= 0 or atmospheric_pressure_pa <= 0:
        raise ValueError("invalid membrane or pressure parameters")
    r = 8.314462618
    mw = 0.01801528
    pd = 1.895e-5 * temperature_k**2.072
    molecular_term = (
        (2.0 / 3.0)
        * math.sqrt(8.0 * r * temperature_k / (math.pi * mw))
        * pore_radius_m**3
    )
    diffusion_term = (pd / atmospheric_pressure_pa) * pore_radius_m**2
    resistance = (1.0 / molecular_term) + (1.0 / diffusion_term)
    return (
        math.pi
        / (r * temperature_k)
        * porosity
        / (tortuosity * thickness_m)
        / resistance
    )


def source_membrane_conductivity_w_m_k(
    *,
    temperature_k: float,
    porosity: float,
) -> float:
    """Eq. (19)-(21), with the source's temperature-dependent conductivities."""
    if not 273.0 <= temperature_k <= 373.0:
        raise ValueError("source conductivity correlations are stated for 273-373 K")
    if not 0 <= porosity <= 1:
        raise ValueError("porosity must be in [0,1]")
    k_s = 0.087 + 6.0e-4 * temperature_k
    k_v = 2.72e-3 + 5.71e-5 * temperature_k
    return porosity * k_v + (1.0 - porosity) * k_s
