"""Couple Wyon's local DCMD surface solver to Appendix A channel properties.

Wyon evaluates the channel properties at the arithmetic-mean temperature
between each stream's bulk and membrane-surface temperatures. Since those
surface temperatures depend on the film heat-transfer coefficients, this
module solves the resulting small fixed-point problem. It still represents
one local, steady membrane element, not a complete axial DCMD module.
"""
from __future__ import annotations

from dataclasses import dataclass

from .wyon_2025_fluid_properties import (
    WyonChannelTransfer,
    wyon_channel_heat_transfer,
)
from .wyon_2025_surface_reference import (
    VapourPressureModel,
    WyonSurfaceResult,
    solve_wyon_membrane_surfaces,
)


@dataclass(frozen=True)
class WyonCoupledChannelSurfaceResult:
    """Converged surface solution with the channel properties used to obtain it."""

    surface: WyonSurfaceResult
    feed_channel: WyonChannelTransfer
    permeate_channel: WyonChannelTransfer
    feed_mean_fluid_temperature_c: float
    permeate_mean_fluid_temperature_c: float
    fixed_point_residual_c: float
    iterations: int


def solve_wyon_coupled_channel_surface(
    *,
    feed_bulk_temperature_c: float,
    permeate_bulk_temperature_c: float,
    feed_velocity_m_s: float,
    permeate_velocity_m_s: float,
    hydraulic_diameter_m: float,
    channel_length_m: float,
    feed_salinity_sr_g_kg: float,
    membrane_thermal_conductivity_w_m_k: float,
    membrane_thickness_m: float,
    pore_radius_m: float,
    porosity: float,
    total_pore_pressure_pa: float = 100000.0,
    temperature_tolerance_c: float = 1e-8,
    relaxation: float = 0.5,
    max_iterations: int = 100,
    vapour_pressure_model: VapourPressureModel = "wyon_2025",
) -> WyonCoupledChannelSurfaceResult:
    """Solve Wyon surface temperatures and channel-film properties together.

    For each stream, fluid properties are evaluated at the arithmetic mean of
    its bulk and membrane-surface temperatures, as described in Wyon (2025),
    Section 3.2.2. The mean temperatures determine Re, Pr, Nu, and alpha;
    alpha determines the membrane-surface temperatures. A relaxed fixed-point
    iteration closes this dependency.

    Feed salinity and pore radius are explicit inputs. The default
    ``wyon_2025`` vapour-pressure mode preserves Wyon's pure-water convention.
    The opt-in ``nayar_2016`` mode uses Nayar's paired pure-water and natural-
    seawater correlations; it approximates feed-side membrane-interface and
    mean-pore salinity with the supplied bulk Reference Salinity. This is an
    explicit sensitivity assumption, not a concentration-polarization model.
    """
    if temperature_tolerance_c <= 0:
        raise ValueError("temperature_tolerance_c must be positive")
    if not 0.0 < relaxation <= 1.0:
        raise ValueError("relaxation must be in (0, 1]")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")

    feed_mean_c = feed_bulk_temperature_c
    permeate_mean_c = permeate_bulk_temperature_c
    residual_c = float("inf")

    for iteration in range(1, max_iterations + 1):
        feed_channel = wyon_channel_heat_transfer(
            velocity_m_s=feed_velocity_m_s,
            hydraulic_diameter_m=hydraulic_diameter_m,
            channel_length_m=channel_length_m,
            temperature_its90_c=feed_mean_c,
            salinity_sr_g_kg=feed_salinity_sr_g_kg,
        )
        permeate_channel = wyon_channel_heat_transfer(
            velocity_m_s=permeate_velocity_m_s,
            hydraulic_diameter_m=hydraulic_diameter_m,
            channel_length_m=channel_length_m,
            temperature_its90_c=permeate_mean_c,
            salinity_sr_g_kg=0.0,
        )
        surface = solve_wyon_membrane_surfaces(
            feed_bulk_temperature_c=feed_bulk_temperature_c,
            permeate_bulk_temperature_c=permeate_bulk_temperature_c,
            feed_heat_transfer_coefficient_w_m2_k=(
                feed_channel.heat_transfer_coefficient_w_m2_k
            ),
            permeate_heat_transfer_coefficient_w_m2_k=(
                permeate_channel.heat_transfer_coefficient_w_m2_k
            ),
            membrane_thermal_conductivity_w_m_k=membrane_thermal_conductivity_w_m_k,
            membrane_thickness_m=membrane_thickness_m,
            pore_radius_m=pore_radius_m,
            porosity=porosity,
            total_pore_pressure_pa=total_pore_pressure_pa,
            vapour_pressure_model=vapour_pressure_model,
            feed_salinity_sr_g_kg=(
                feed_salinity_sr_g_kg if vapour_pressure_model == "nayar_2016" else None
            ),
        )

        target_feed_mean_c = 0.5 * (
            feed_bulk_temperature_c + surface.feed_interface_temperature_c
        )
        target_permeate_mean_c = 0.5 * (
            permeate_bulk_temperature_c + surface.permeate_interface_temperature_c
        )
        residual_c = max(
            abs(target_feed_mean_c - feed_mean_c),
            abs(target_permeate_mean_c - permeate_mean_c),
        )
        if residual_c <= temperature_tolerance_c:
            return WyonCoupledChannelSurfaceResult(
                surface=surface,
                feed_channel=feed_channel,
                permeate_channel=permeate_channel,
                feed_mean_fluid_temperature_c=feed_mean_c,
                permeate_mean_fluid_temperature_c=permeate_mean_c,
                fixed_point_residual_c=residual_c,
                iterations=iteration,
            )

        feed_mean_c += relaxation * (target_feed_mean_c - feed_mean_c)
        permeate_mean_c += relaxation * (
            target_permeate_mean_c - permeate_mean_c
        )

    raise RuntimeError(
        "Wyon coupled channel/surface iteration did not converge after "
        f"{max_iterations} iterations (fixed-point residual={residual_c:.3e} C)"
    )
