"""Lumped Wyon DCMD module outlet balances (Eqs. 18-20).

This layer takes a converged local surface solution and closes one-pass feed
and permeate mass/enthalpy balances over a specified membrane area. It is a
well-mixed/lumped module approximation, not an axial finite-volume model.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .wyon_2025_enthalpy import (
    wyon_specific_enthalpy_j_kg,
    wyon_temperature_from_specific_enthalpy_c,
)
from .wyon_2025_fluid_properties import wyon_fluid_properties
from .wyon_2025_coupled_channel_surface import WyonCoupledChannelSurfaceResult


@dataclass(frozen=True)
class WyonModuleOutletResult:
    """One-pass module outlet states and conservation diagnostics."""

    feed_outlet_temperature_c: float
    permeate_outlet_temperature_c: float
    feed_outlet_salinity_sr_g_kg: float
    feed_inlet_mass_flow_kg_s: float
    feed_outlet_mass_flow_kg_s: float
    permeate_inlet_mass_flow_kg_s: float
    permeate_outlet_mass_flow_kg_s: float
    transferred_water_mass_flow_kg_s: float
    heat_transfer_rate_w: float
    feed_heat_loss_w: float
    permeate_heat_gain_w: float
    energy_balance_residual_w: float
    feed_salt_mass_flow_kg_s: float
    salt_mass_balance_residual_kg_s: float
    feed_inlet_volumetric_flow_m3_s: float
    feed_outlet_volumetric_flow_m3_s: float
    feed_inlet_salt_concentration_kg_m3: float
    feed_outlet_salt_concentration_kg_m3: float
    equation_20_salt_balance_residual_kg_s: float


def _positive_finite(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def solve_wyon_lumped_module_outlets(
    *,
    surface_result: WyonCoupledChannelSurfaceResult,
    feed_inlet_temperature_c: float,
    permeate_inlet_temperature_c: float,
    feed_salinity_sr_g_kg: float,
    feed_velocity_m_s: float,
    permeate_velocity_m_s: float,
    channel_width_m: float,
    channel_height_m: float,
    membrane_area_m2: float,
) -> WyonModuleOutletResult:
    """Solve one-pass mass and enthalpy outlet states from Wyon Eqs. (18)-(20).

    Inlet mass flow rates follow Eq. (19): m_dot = v * A_channel * rho.
    The water transferred through the membrane is J * A_membrane. Feed mass
    decreases by this amount; permeate mass increases by the same amount.
    Salt mass is conserved, so feed outlet salinity is computed on a kg/kg
    mass-fraction basis for Appendix A11.

    Eq. (20) is then checked in its dimensionally consistent volumetric form:
        Q_in * C_s,in = Q_out * C_s,out
    where Q is volumetric flow (m3/s) and C_s is salt concentration (kg/m3).
    Since C_s = rho * w_s, this is algebraically equivalent to
    m_dot_in * w_s,in = m_dot_out * w_s,out. Appendix A11's S in kg/kg is
    therefore not passed directly as the volumetric concentration in Eq. (20).
    """
    for name, value in (
        ("feed_inlet_temperature_c", feed_inlet_temperature_c),
        ("permeate_inlet_temperature_c", permeate_inlet_temperature_c),
        ("feed_salinity_sr_g_kg", feed_salinity_sr_g_kg),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    _positive_finite("feed_velocity_m_s", feed_velocity_m_s)
    _positive_finite("permeate_velocity_m_s", permeate_velocity_m_s)
    _positive_finite("channel_width_m", channel_width_m)
    _positive_finite("channel_height_m", channel_height_m)
    _positive_finite("membrane_area_m2", membrane_area_m2)

    if not 0.0 <= feed_salinity_sr_g_kg <= 160.0:
        raise ValueError("feed_salinity_sr_g_kg must be in [0, 160] g/kg")
    if not 0.0 <= permeate_inlet_temperature_c <= 100.0:
        raise ValueError("permeate inlet temperature must be in [0, 100] C")
    if not 0.0 <= feed_inlet_temperature_c <= 100.0:
        raise ValueError("feed inlet temperature must be in [0, 100] C")
    if feed_inlet_temperature_c <= permeate_inlet_temperature_c:
        raise ValueError("feed inlet temperature must exceed permeate inlet temperature")

    channel_cross_section_m2 = channel_width_m * channel_height_m
    feed_inlet_properties = wyon_fluid_properties(
        feed_inlet_temperature_c, feed_salinity_sr_g_kg
    )
    permeate_inlet_properties = wyon_fluid_properties(
        permeate_inlet_temperature_c, 0.0
    )

    feed_inlet_mass_flow = (
        feed_velocity_m_s
        * channel_cross_section_m2
        * feed_inlet_properties.density_kg_m3
    )
    permeate_inlet_mass_flow = (
        permeate_velocity_m_s
        * channel_cross_section_m2
        * permeate_inlet_properties.density_kg_m3
    )
    transferred_water_mass_flow = (
        surface_result.surface.mass_flux_kg_m2_s * membrane_area_m2
    )
    if not isfinite(transferred_water_mass_flow) or transferred_water_mass_flow < 0.0:
        raise ValueError("surface mass flux must be finite and non-negative")

    feed_outlet_mass_flow = feed_inlet_mass_flow - transferred_water_mass_flow
    permeate_outlet_mass_flow = (
        permeate_inlet_mass_flow + transferred_water_mass_flow
    )
    if feed_outlet_mass_flow <= 0.0:
        raise ValueError("membrane water transfer exhausts the feed mass flow")

    feed_salinity_mass_fraction_in = feed_salinity_sr_g_kg / 1000.0
    feed_salt_mass_flow = (
        feed_inlet_mass_flow * feed_salinity_mass_fraction_in
    )
    feed_salinity_mass_fraction_out = (
        feed_salt_mass_flow / feed_outlet_mass_flow
    )
    feed_salinity_sr_g_kg_out = (
        feed_salinity_mass_fraction_out * 1000.0
    )
    if feed_salinity_sr_g_kg_out > 160.0:
        raise ValueError(
            "feed outlet salinity exceeds the implemented Wyon Appendix A range"
        )

    heat_transfer_rate = (
        surface_result.surface.heat_flux_w_m2 * membrane_area_m2
    )
    feed_enthalpy_in = wyon_specific_enthalpy_j_kg(
        feed_inlet_temperature_c, feed_salinity_sr_g_kg
    )
    permeate_enthalpy_in = wyon_specific_enthalpy_j_kg(
        permeate_inlet_temperature_c, 0.0
    )
    feed_enthalpy_out = (
        feed_inlet_mass_flow * feed_enthalpy_in - heat_transfer_rate
    ) / feed_outlet_mass_flow
    permeate_enthalpy_out = (
        permeate_inlet_mass_flow * permeate_enthalpy_in + heat_transfer_rate
    ) / permeate_outlet_mass_flow

    feed_outlet_temperature = wyon_temperature_from_specific_enthalpy_c(
        feed_enthalpy_out, feed_salinity_sr_g_kg_out
    )
    permeate_outlet_temperature = wyon_temperature_from_specific_enthalpy_c(
        permeate_enthalpy_out, 0.0
    )

    feed_outlet_properties = wyon_fluid_properties(
        feed_outlet_temperature, feed_salinity_sr_g_kg_out
    )
    feed_inlet_volumetric_flow = (
        feed_inlet_mass_flow / feed_inlet_properties.density_kg_m3
    )
    feed_outlet_volumetric_flow = (
        feed_outlet_mass_flow / feed_outlet_properties.density_kg_m3
    )
    feed_salt_concentration_in = (
        feed_inlet_properties.density_kg_m3
        * feed_salinity_mass_fraction_in
    )
    feed_salt_concentration_out = (
        feed_outlet_properties.density_kg_m3
        * feed_salinity_mass_fraction_out
    )

    feed_heat_loss = (
        feed_inlet_mass_flow * feed_enthalpy_in
        - feed_outlet_mass_flow * feed_enthalpy_out
    )
    permeate_heat_gain = (
        permeate_outlet_mass_flow * permeate_enthalpy_out
        - permeate_inlet_mass_flow * permeate_enthalpy_in
    )
    energy_balance_residual = max(
        abs(feed_heat_loss - heat_transfer_rate),
        abs(permeate_heat_gain - heat_transfer_rate),
    )
    salt_mass_balance_residual = abs(
        feed_salt_mass_flow
        - feed_outlet_mass_flow * feed_salinity_mass_fraction_out
    )
    equation_20_residual = abs(
        feed_inlet_volumetric_flow * feed_salt_concentration_in
        - feed_outlet_volumetric_flow * feed_salt_concentration_out
    )

    return WyonModuleOutletResult(
        feed_outlet_temperature_c=feed_outlet_temperature,
        permeate_outlet_temperature_c=permeate_outlet_temperature,
        feed_outlet_salinity_sr_g_kg=feed_salinity_sr_g_kg_out,
        feed_inlet_mass_flow_kg_s=feed_inlet_mass_flow,
        feed_outlet_mass_flow_kg_s=feed_outlet_mass_flow,
        permeate_inlet_mass_flow_kg_s=permeate_inlet_mass_flow,
        permeate_outlet_mass_flow_kg_s=permeate_outlet_mass_flow,
        transferred_water_mass_flow_kg_s=transferred_water_mass_flow,
        heat_transfer_rate_w=heat_transfer_rate,
        feed_heat_loss_w=feed_heat_loss,
        permeate_heat_gain_w=permeate_heat_gain,
        energy_balance_residual_w=energy_balance_residual,
        feed_salt_mass_flow_kg_s=feed_salt_mass_flow,
        salt_mass_balance_residual_kg_s=salt_mass_balance_residual,
        feed_inlet_volumetric_flow_m3_s=feed_inlet_volumetric_flow,
        feed_outlet_volumetric_flow_m3_s=feed_outlet_volumetric_flow,
        feed_inlet_salt_concentration_kg_m3=feed_salt_concentration_in,
        feed_outlet_salt_concentration_kg_m3=feed_salt_concentration_out,
        equation_20_salt_balance_residual_kg_s=equation_20_residual,
    )
