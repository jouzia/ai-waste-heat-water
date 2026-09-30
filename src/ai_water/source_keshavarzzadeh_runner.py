"""Source-compatible axial runner scaffold for Keshavarzzadeh et al. (2020).

This module deliberately separates source reproduction from the modern generic
channel model. It implements the source membrane transport and local thermal
conductivity equations, while requiring explicit thermodynamic/enthalpy inputs
for the axial balance. It must not be used as experimental validation until
source operating conditions and primary observations are frozen.
"""

from dataclasses import dataclass
import math

from .source_keshavarzzadeh import (
    source_membrane_conductivity_w_m_k,
    source_membrane_flux_coefficient,
    source_water_activity_from_molar_nacl,
    source_saturation_pressure_pa,
)


@dataclass(frozen=True)
class SourceRunnerConfig:
    membrane_thickness_m: float
    pore_radius_m: float
    porosity: float
    tortuosity: float
    channel_area_m2: float
    membrane_area_m2: float
    cells: int
    pressure_pa: float = 101325.0
    source_pd_exponent: float = 2.072


def source_vapor_pressure_pa(
    *,
    temperature_c: float,
    nacl_molarity_mol_l: float,
) -> float:
    """Source Eq. 7: activity-adjusted feed vapor pressure."""
    if nacl_molarity_mol_l < 0:
        raise ValueError("NaCl molarity must be non-negative")
    activity = source_water_activity_from_molar_nacl(nacl_molarity_mol_l)
    return activity * source_saturation_pressure_pa(temperature_c)


def source_pure_vapor_pressure_pa(*, temperature_c: float) -> float:
    """Source Eq. 5: pure-water saturation pressure."""
    return source_saturation_pressure_pa(temperature_c)


def source_membrane_flux_kg_m2_s(
    *,
    feed_interface_temperature_c: float,
    permeate_interface_temperature_c: float,
    feed_nacl_molarity_mol_l: float,
    config: SourceRunnerConfig,
) -> float:
    """Evaluate source Eq. 1 using source Eq. 2 membrane coefficient."""
    tf_k = feed_interface_temperature_c + 273.15
    tp_k = permeate_interface_temperature_c + 273.15
    if tf_k <= 0 or tp_k <= 0:
        raise ValueError("interface temperatures must be above absolute zero")
    membrane_k = 0.5 * (tf_k + tp_k)
    coefficient = source_membrane_flux_coefficient(
        temperature_k=membrane_k,
        pore_radius_m=config.pore_radius_m,
        thickness_m=config.membrane_thickness_m,
        porosity=config.porosity,
        tortuosity=config.tortuosity,
        pressure_pa=config.pressure_pa,
    )
    dp_pa = (
        source_vapor_pressure_pa(
            temperature_c=feed_interface_temperature_c,
            nacl_molarity_mol_l=feed_nacl_molarity_mol_l,
        )
        - source_pure_vapor_pressure_pa(temperature_c=permeate_interface_temperature_c)
    )
    return max(0.0, coefficient * dp_pa)


def source_membrane_conductivity(
    *,
    membrane_temperature_c: float,
    porosity: float,
) -> float:
    """Source Eqs. 19-21; conductivity in W m-1 K-1."""
    return source_membrane_conductivity_w_m_k(
        temperature_k=membrane_temperature_c + 273.15,
        porosity=porosity,
    )


def validate_source_config(config: SourceRunnerConfig) -> None:
    """Validate only source-runner geometry and numerical controls."""
    if config.membrane_thickness_m <= 0:
        raise ValueError("membrane thickness must be positive")
    if config.pore_radius_m <= 0:
        raise ValueError("pore radius must be positive")
    if not 0 < config.porosity <= 1:
        raise ValueError("porosity must be in (0,1]")
    if config.tortuosity <= 0:
        raise ValueError("tortuosity must be positive")
    if config.channel_area_m2 <= 0 or config.membrane_area_m2 <= 0:
        raise ValueError("areas must be positive")
    if config.cells <= 0:
        raise ValueError("cells must be positive")
    if config.pressure_pa <= 0:
        raise ValueError("pressure must be positive")


def source_cell_area(config: SourceRunnerConfig) -> float:
    validate_source_config(config)
    return config.membrane_area_m2 / config.cells
