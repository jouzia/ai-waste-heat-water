"""Isolated transcription of Wyon (2025) DCMD membrane-surface equations.

This module reproduces the local, steady DCMD interface calculation only.
It is deliberately separate from the production screening engine and does
not claim to reproduce Wyon's full module outlet-state, heat-exchanger,
hydraulic, or 80-module plant calculations.

Source: Annie Wyon (2025), Lund University thesis, Section 3.2.2,
Eqs. (7)-(17), Appendix A Eq. (9)-(10), report
LUTFD2/TFEM--25/5229--SE.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, log, pi, sqrt
from typing import Literal

from .nayar_2016_vapour_pressure import (
    nayar_natural_seawater_vapour_pressure_pa,
    nayar_pure_water_vapour_pressure_pa,
)

VapourPressureModel = Literal["wyon_2025", "nayar_2016"]


def _selected_vapour_pressure_pa(
    temperature_c: float,
    *,
    model: VapourPressureModel,
    feed_salinity_sr_g_kg: float | None,
    seawater: bool,
) -> float:
    if model == "wyon_2025":
        return wyon_pure_water_vapour_pressure_pa(temperature_c)
    if model == "nayar_2016":
        if feed_salinity_sr_g_kg is None:
            raise ValueError(
                "feed_salinity_sr_g_kg is required when vapour_pressure_model='nayar_2016'"
            )
        if seawater:
            return nayar_natural_seawater_vapour_pressure_pa(
                temperature_c, feed_salinity_sr_g_kg
            )
        return nayar_pure_water_vapour_pressure_pa(temperature_c)
    raise ValueError("vapour_pressure_model must be 'wyon_2025' or 'nayar_2016'")

R_UNIVERSAL_J_MOL_K = 8.314462618
M_WATER_KG_MOL = 0.01801528


def _finite_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and > 0")


def wyon_pure_water_vapour_pressure_pa(temperature_c: float) -> float:
    """Wyon Appendix A Eq. (9), returning pure-water vapour pressure in Pa.

    Wyon explicitly uses this pure-water correlation for both the seawater
    feed and pure-water permeate over the modelled 40-100 C range. No seawater
    activity correction is applied in this source-faithful baseline.
    """
    if not isfinite(temperature_c):
        raise ValueError("temperature_c must be finite")
    temperature_k = temperature_c + 273.15
    if not 273.15 <= temperature_k <= 373.15:
        raise ValueError("Wyon Eq. A9 is used here only over 0-100 C")
    value = (
        -5800.0 / temperature_k
        + 1.391
        - 4.846e-2 * temperature_k
        + 4.176e-5 * temperature_k**2
        - 1.445e-8 * temperature_k**3
        + 6.545 * log(temperature_k)
    )
    return __import__("math").exp(value)


def wyon_tortuosity(porosity: float) -> float:
    """Wyon Eq. (16): tau = (2 - epsilon)^2 / epsilon."""
    if not isfinite(porosity) or not 0 < porosity <= 1:
        raise ValueError("porosity must be in (0, 1]")
    return (2.0 - porosity) ** 2 / porosity


def wyon_mass_transfer_coefficient_kg_m2_s_pa(
    *,
    mean_membrane_temperature_k: float,
    pore_radius_m: float,
    membrane_thickness_m: float,
    porosity: float,
    total_pore_pressure_pa: float = 100000.0,
    vapour_pressure_model: VapourPressureModel = "wyon_2025",
    feed_salinity_sr_g_kg: float | None = None,
) -> float:
    """Wyon Eq. (14) combined Knudsen/molecular diffusion coefficient.

    Returns c in kg/(m2 s Pa), where J = c * (p_feed,m - p_permeate,m).
    Wyon assumes transitional diffusion (Knudsen number 0.5), ideal-gas
    behaviour, and total pore pressure of 1 bar. The combined coefficient is
    the reciprocal sum of the Knudsen and molecular transport resistances.
    """
    _finite_positive("mean_membrane_temperature_k", mean_membrane_temperature_k)
    _finite_positive("pore_radius_m", pore_radius_m)
    _finite_positive("membrane_thickness_m", membrane_thickness_m)
    _finite_positive("total_pore_pressure_pa", total_pore_pressure_pa)
    if not 0 < porosity <= 1:
        raise ValueError("porosity must be in (0, 1]")

    temperature_k = mean_membrane_temperature_k
    tau = wyon_tortuosity(porosity)
    vapour_pressure = _selected_vapour_pressure_pa(
        temperature_k - 273.15,
        model=vapour_pressure_model,
        feed_salinity_sr_g_kg=feed_salinity_sr_g_kg,
        seawater=(vapour_pressure_model == "nayar_2016"),
    )
    air_partial_pressure = total_pore_pressure_pa - vapour_pressure
    if air_partial_pressure <= 0:
        raise ValueError("water vapour pressure must remain below total pore pressure")

    # Wyon Appendix A Eq. (10): D * P_m, in Pa m2/s.
    diffusion_pressure_product = 1.895e-5 * temperature_k**2.072

    # Eq. (14), first bracket: Knudsen contribution.
    knudsen = (
        (2.0 * pore_radius_m * porosity)
        / (3.0 * tau * membrane_thickness_m)
        * sqrt(
            8.0 * M_WATER_KG_MOL
            / (pi * R_UNIVERSAL_J_MOL_K * temperature_k)
        )
    )

    # Eq. (14), second bracket: ordinary molecular diffusion contribution.
    molecular = (
        porosity
        * M_WATER_KG_MOL
        * diffusion_pressure_product
        / (
            tau
            * membrane_thickness_m
            * R_UNIVERSAL_J_MOL_K
            * temperature_k
            * air_partial_pressure
        )
    )
    if knudsen <= 0 or molecular <= 0:
        raise ArithmeticError("diffusion coefficients must be positive")
    return 1.0 / (1.0 / knudsen + 1.0 / molecular)


def wyon_nusselt_number(*, reynolds: float, prandtl: float, hydraulic_diameter_m: float, channel_length_m: float) -> float:
    """Wyon Eq. (10), turbulent rectangular-channel correlation."""
    _finite_positive("reynolds", reynolds)
    _finite_positive("prandtl", prandtl)
    _finite_positive("hydraulic_diameter_m", hydraulic_diameter_m)
    _finite_positive("channel_length_m", channel_length_m)
    return 0.023 * (1.0 + 6.0 * hydraulic_diameter_m / channel_length_m) * reynolds**0.8 * prandtl ** (1.0 / 3.0)


def wyon_convective_heat_transfer_coefficient_w_m2_k(
    *, nusselt: float, fluid_thermal_conductivity_w_m_k: float, hydraulic_diameter_m: float
) -> float:
    """Wyon Eq. (9): alpha = Nu * k / d_h."""
    _finite_positive("nusselt", nusselt)
    _finite_positive("fluid_thermal_conductivity_w_m_k", fluid_thermal_conductivity_w_m_k)
    _finite_positive("hydraulic_diameter_m", hydraulic_diameter_m)
    return nusselt * fluid_thermal_conductivity_w_m_k / hydraulic_diameter_m


@dataclass(frozen=True)
class WyonSurfaceResult:
    feed_interface_temperature_c: float
    permeate_interface_temperature_c: float
    mean_membrane_temperature_k: float
    membrane_mass_transfer_coefficient_kg_m2_s_pa: float
    mass_flux_kg_m2_s: float
    mass_flux_kg_m2_h: float
    heat_flux_w_m2: float
    latent_heat_flux_w_m2: float
    conductive_heat_flux_w_m2: float
    feed_convective_heat_flux_w_m2: float
    permeate_convective_heat_flux_w_m2: float
    vapour_pressure_feed_pa: float
    vapour_pressure_permeate_pa: float
    energy_balance_residual_w_m2: float


def solve_wyon_membrane_surfaces(
    *,
    feed_bulk_temperature_c: float,
    permeate_bulk_temperature_c: float,
    feed_heat_transfer_coefficient_w_m2_k: float,
    permeate_heat_transfer_coefficient_w_m2_k: float,
    membrane_thermal_conductivity_w_m_k: float,
    membrane_thickness_m: float,
    pore_radius_m: float,
    porosity: float,
    total_pore_pressure_pa: float = 100000.0,
    tolerance_w_m2: float = 1e-7,
    max_iterations: int = 200,
    vapour_pressure_model: VapourPressureModel = "wyon_2025",
    feed_salinity_sr_g_kg: float | None = None,
) -> WyonSurfaceResult:
    """Solve Wyon Eqs. (7)-(17) for the two membrane-interface temperatures.

    The scalar unknown is the common heat flux q. From q_f=q_p=q, the
    interface temperatures follow directly from the two film resistances.
    Bisection then enforces q = J*Hv + k_m/delta_m*(T_f,m-T_p,m).

    The vapour enthalpy correlation in Eq. (17) is evaluated with absolute
    temperature in kelvin and returns kJ/kg; the latent term is converted to
    W/m2. This function returns a local steady-state solution only.
    """
    for name, value in (
        ("feed_bulk_temperature_c", feed_bulk_temperature_c),
        ("permeate_bulk_temperature_c", permeate_bulk_temperature_c),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
        if not 0.0 <= value <= 100.0:
            raise ValueError(
                f"{name} must be within the implemented Wyon Eq. A9 range of 0-100 C"
            )
    if feed_bulk_temperature_c <= permeate_bulk_temperature_c:
        raise ValueError("feed bulk temperature must exceed permeate bulk temperature")
    _finite_positive("feed_heat_transfer_coefficient_w_m2_k", feed_heat_transfer_coefficient_w_m2_k)
    _finite_positive("permeate_heat_transfer_coefficient_w_m2_k", permeate_heat_transfer_coefficient_w_m2_k)
    if not isfinite(membrane_thermal_conductivity_w_m_k) or membrane_thermal_conductivity_w_m_k < 0:
        raise ValueError("membrane thermal conductivity must be finite and non-negative")
    _finite_positive("membrane_thickness_m", membrane_thickness_m)
    _finite_positive("pore_radius_m", pore_radius_m)
    _finite_positive("total_pore_pressure_pa", total_pore_pressure_pa)
    _finite_positive("tolerance_w_m2", tolerance_w_m2)
    if not 0 < porosity <= 1:
        raise ValueError("porosity must be in (0, 1]")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")
    if vapour_pressure_model not in ("wyon_2025", "nayar_2016"):
        raise ValueError("vapour_pressure_model must be 'wyon_2025' or 'nayar_2016'")
    if vapour_pressure_model == "nayar_2016" and feed_salinity_sr_g_kg is None:
        raise ValueError(
            "feed_salinity_sr_g_kg is required when vapour_pressure_model='nayar_2016'"
        )

    delta_bulk = feed_bulk_temperature_c - permeate_bulk_temperature_c
    q_low = 0.0
    q_high = delta_bulk / (
        1.0 / feed_heat_transfer_coefficient_w_m2_k
        + 1.0 / permeate_heat_transfer_coefficient_w_m2_k
    )
    membrane_conductance = membrane_thermal_conductivity_w_m_k / membrane_thickness_m

    def evaluate(q_w_m2: float):
        tfm = feed_bulk_temperature_c - q_w_m2 / feed_heat_transfer_coefficient_w_m2_k
        tpm = permeate_bulk_temperature_c + q_w_m2 / permeate_heat_transfer_coefficient_w_m2_k
        tm_k = 0.5 * (tfm + tpm) + 273.15
        c = wyon_mass_transfer_coefficient_kg_m2_s_pa(
            mean_membrane_temperature_k=tm_k,
            pore_radius_m=pore_radius_m,
            membrane_thickness_m=membrane_thickness_m,
            porosity=porosity,
            total_pore_pressure_pa=total_pore_pressure_pa,
            vapour_pressure_model=vapour_pressure_model,
            feed_salinity_sr_g_kg=feed_salinity_sr_g_kg,
        )
        pvf = _selected_vapour_pressure_pa(
            tfm,
            model=vapour_pressure_model,
            feed_salinity_sr_g_kg=feed_salinity_sr_g_kg,
            seawater=(vapour_pressure_model == "nayar_2016"),
        )
        pvp = _selected_vapour_pressure_pa(
            tpm,
            model=vapour_pressure_model,
            feed_salinity_sr_g_kg=feed_salinity_sr_g_kg,
            seawater=False,
        )
        flux = c * (pvf - pvp)
        # Wyon Eq. (17): H_v = 1.7535*T + 2024.3 kJ/kg, T in K.
        vapour_enthalpy_kj_kg = 1.7535 * tm_k + 2024.3
        latent = flux * vapour_enthalpy_kj_kg * 1000.0
        conductive = membrane_conductance * (tfm - tpm)
        q_membrane = latent + conductive
        return q_w_m2 - q_membrane, tfm, tpm, tm_k, c, flux, pvf, pvp, latent, conductive

    # The mass-transfer correlation requires the mean-pore water-vapour
    # pressure to remain below total pore pressure. For some unequal film
    # coefficients, q=0 violates this domain even though the physical root
    # lies inside it. Find the first admissible heat flux before evaluating.
    def mean_pore_pressure_is_admissible(q_w_m2: float) -> bool:
        tfm = feed_bulk_temperature_c - q_w_m2 / feed_heat_transfer_coefficient_w_m2_k
        tpm = permeate_bulk_temperature_c + q_w_m2 / permeate_heat_transfer_coefficient_w_m2_k
        mean_c = 0.5 * (tfm + tpm)
        if not 0.0 <= mean_c <= 100.0:
            return False
        mean_pore_vapour_pressure = _selected_vapour_pressure_pa(
            mean_c,
            model=vapour_pressure_model,
            feed_salinity_sr_g_kg=feed_salinity_sr_g_kg,
            seawater=(vapour_pressure_model == "nayar_2016"),
        )
        return mean_pore_vapour_pressure < total_pore_pressure_pa

    if not mean_pore_pressure_is_admissible(q_high):
        raise ValueError(
            "Wyon mean membrane temperature remains outside the vapour-pressure "
            "domain over the physical heat-flux interval"
        )
    if mean_pore_pressure_is_admissible(q_low):
        f_low = evaluate(q_low)[0]
    else:
        inadmissible_q = q_low
        admissible_q = q_high
        for _ in range(80):
            candidate_q = 0.5 * (inadmissible_q + admissible_q)
            if mean_pore_pressure_is_admissible(candidate_q):
                admissible_q = candidate_q
            else:
                inadmissible_q = candidate_q
        q_low = admissible_q + max(1e-10, (q_high - admissible_q) * 1e-10)
        if q_low >= q_high:
            raise ValueError("No interior heat-flux interval remains inside the Wyon vapour-pressure domain")
        f_low = evaluate(q_low)[0]

    f_high = evaluate(q_high)[0]
    if not f_low < 0 < f_high:
        raise ValueError("Wyon interface energy balance is not bracketed by physical heat-flux limits")

    for _ in range(max_iterations):
        q_mid = 0.5 * (q_low + q_high)
        values = evaluate(q_mid)
        residual = values[0]
        if abs(residual) <= tolerance_w_m2:
            break
        if residual < 0:
            q_low = q_mid
        else:
            q_high = q_mid
    else:
        raise RuntimeError("Wyon membrane-surface iteration did not converge")

    _, tfm, tpm, tm_k, c, flux, pvf, pvp, latent, conductive = values
    q_feed = feed_heat_transfer_coefficient_w_m2_k * (feed_bulk_temperature_c - tfm)
    q_permeate = permeate_heat_transfer_coefficient_w_m2_k * (tpm - permeate_bulk_temperature_c)
    return WyonSurfaceResult(
        feed_interface_temperature_c=tfm,
        permeate_interface_temperature_c=tpm,
        mean_membrane_temperature_k=tm_k,
        membrane_mass_transfer_coefficient_kg_m2_s_pa=c,
        mass_flux_kg_m2_s=flux,
        mass_flux_kg_m2_h=flux * 3600.0,
        heat_flux_w_m2=0.5 * (q_feed + q_permeate),
        latent_heat_flux_w_m2=latent,
        conductive_heat_flux_w_m2=conductive,
        feed_convective_heat_flux_w_m2=q_feed,
        permeate_convective_heat_flux_w_m2=q_permeate,
        vapour_pressure_feed_pa=pvf,
        vapour_pressure_permeate_pa=pvp,
        energy_balance_residual_w_m2=values[0],
    )
