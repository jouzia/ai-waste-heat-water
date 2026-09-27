"""Channel-side heat/mass-transfer correlations and concentration polarization.

The functions here are deliberately correlation-selectable. Correlations are
not universal MD physics: published CFD/experimental work shows geometry and
downstream development can materially affect polarization. Each correlation
must therefore be reported with its source and applicability range.
"""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class ChannelProperties:
    density_kg_m3: float
    viscosity_pa_s: float
    thermal_conductivity_w_m_k: float
    heat_capacity_j_kg_k: float
    diffusivity_m2_s: float


@dataclass(frozen=True)
class ChannelDimensionless:
    reynolds: float
    prandtl: float
    schmidt: float
    nusselt: float
    sherwood: float


def dimensionless_numbers(
    *,
    velocity_m_s: float,
    hydraulic_diameter_m: float,
    properties: ChannelProperties,
) -> tuple[float, float, float]:
    if velocity_m_s <= 0 or hydraulic_diameter_m <= 0:
        raise ValueError("velocity and hydraulic diameter must be positive")
    if min(
        properties.density_kg_m3,
        properties.viscosity_pa_s,
        properties.thermal_conductivity_w_m_k,
        properties.heat_capacity_j_kg_k,
        properties.diffusivity_m2_s,
    ) <= 0:
        raise ValueError("channel properties must be positive")
    re = properties.density_kg_m3 * velocity_m_s * hydraulic_diameter_m / properties.viscosity_pa_s
    pr = (
        properties.heat_capacity_j_kg_k
        * properties.viscosity_pa_s
        / properties.thermal_conductivity_w_m_k
    )
    sc = properties.viscosity_pa_s / (
        properties.density_kg_m3 * properties.diffusivity_m2_s
    )
    return re, pr, sc


def graetz_leveque_nusselt(
    reynolds: float,
    prandtl: float,
    hydraulic_diameter_m: float,
    channel_length_m: float,
) -> float:
    """Laminar developing-flow correlation: Nu = 1.86(Re Pr Dh/L)^(1/3)."""
    if min(reynolds, prandtl, hydraulic_diameter_m, channel_length_m) <= 0:
        raise ValueError("correlation inputs must be positive")
    return 1.86 * (reynolds * prandtl * hydraulic_diameter_m / channel_length_m) ** (1.0 / 3.0)


def graetz_leveque_sherwood(
    reynolds: float,
    schmidt: float,
    hydraulic_diameter_m: float,
    channel_length_m: float,
) -> float:
    """Laminar developing-flow correlation: Sh = 1.86(Re Sc Dh/L)^(1/3)."""
    if min(reynolds, schmidt, hydraulic_diameter_m, channel_length_m) <= 0:
        raise ValueError("correlation inputs must be positive")
    return 1.86 * (reynolds * schmidt * hydraulic_diameter_m / channel_length_m) ** (1.0 / 3.0)


def watertap_nusselt(reynolds: float, prandtl: float) -> float:
    """WaterTAP MD 0-D correlation: Nu = 0.2 Re^0.57 Pr^0.4."""
    if reynolds <= 0 or prandtl <= 0:
        raise ValueError("Reynolds and Prandtl numbers must be positive")
    return 0.2 * reynolds**0.57 * prandtl**0.4


def heat_transfer_coefficient(
    *,
    nusselt: float,
    thermal_conductivity_w_m_k: float,
    hydraulic_diameter_m: float,
) -> float:
    if nusselt <= 0 or thermal_conductivity_w_m_k <= 0 or hydraulic_diameter_m <= 0:
        raise ValueError("heat-transfer inputs must be positive")
    return nusselt * thermal_conductivity_w_m_k / hydraulic_diameter_m


def mass_transfer_coefficient(
    *,
    sherwood: float,
    diffusivity_m2_s: float,
    hydraulic_diameter_m: float,
) -> float:
    if sherwood <= 0 or diffusivity_m2_s <= 0 or hydraulic_diameter_m <= 0:
        raise ValueError("mass-transfer inputs must be positive")
    return sherwood * diffusivity_m2_s / hydraulic_diameter_m


def concentration_polarization_coefficient(
    *,
    flux_kg_m2_s: float,
    mass_transfer_coefficient_m_s: float,
    solvent_density_kg_m3: float,
) -> float:
    """CPC = C_interface/C_bulk under the common exponential boundary-layer model."""
    if flux_kg_m2_s < 0:
        raise ValueError("flux cannot be negative")
    if mass_transfer_coefficient_m_s <= 0 or solvent_density_kg_m3 <= 0:
        raise ValueError("mass-transfer coefficient and density must be positive")
    return math.exp(flux_kg_m2_s / (mass_transfer_coefficient_m_s * solvent_density_kg_m3))


def interface_salinity_g_kg(
    bulk_salinity_g_kg: float,
    cpc: float,
) -> float:
    if bulk_salinity_g_kg < 0 or cpc < 1:
        raise ValueError("bulk salinity must be non-negative and CPC must be >= 1")
    return bulk_salinity_g_kg * cpc


def tpc_from_interfaces(
    feed_bulk_c: float,
    permeate_bulk_c: float,
    feed_interface_c: float,
    permeate_interface_c: float,
) -> float:
    bulk_delta = feed_bulk_c - permeate_bulk_c
    if bulk_delta <= 0:
        raise ValueError("feed bulk temperature must exceed permeate bulk temperature")
    return (feed_interface_c - permeate_interface_c) / bulk_delta
