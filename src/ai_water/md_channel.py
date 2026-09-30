"""Reduced-order one-dimensional DCMD channel model.

This module resolves axial bulk-temperature and salinity changes with
finite-volume control volumes. At each cell it solves the steady interface
energy balance:

    q_feed = q_membrane = q_permeate

with membrane heat transfer represented by conductive plus latent terms.
The model is intentionally reduced-order: heat-transfer coefficients and
membrane transport parameters are explicit inputs, while detailed CFD,
property variation, and concentration-polarization correlations remain
outside this layer.
"""

from dataclasses import dataclass
from typing import Literal

from .channel_transport import concentration_polarization_coefficient, interface_salinity_g_kg
from .md import seawater_water_activity, vapor_pressure_driving_force_bar


@dataclass(frozen=True)
class ChannelConfig:
    membrane_area_m2: float
    membrane_permeance_kg_m2_h_bar: float
    latent_heat_kwh_th_per_kg: float
    membrane_thermal_conductivity_w_m_k: float
    membrane_thickness_m: float
    feed_heat_transfer_coefficient_w_m2_k: float
    permeate_heat_transfer_coefficient_w_m2_k: float
    feed_mass_flow_kg_h: float
    permeate_mass_flow_kg_h: float
    feed_cp_kj_kg_k: float = 4.0
    permeate_cp_kj_kg_k: float = 4.18
    feed_salinity_g_kg: float = 35.0
    duration_h: float = 1.0
    cells: int = 20
    water_activity_override: float | None = None
    salt_mass_transfer_coefficient_m_s: float | None = None
    solvent_density_kg_m3: float | None = None
    flow_arrangement: Literal["co_current", "counter_current"] = "co_current"


@dataclass(frozen=True)
class ChannelCellResult:
    cell: int
    feed_bulk_temperature_c: float
    permeate_bulk_temperature_c: float
    feed_interface_temperature_c: float
    permeate_interface_temperature_c: float
    feed_salinity_g_kg: float
    interface_salinity_g_kg: float
    concentration_polarization_coefficient: float
    flux_kg_m2_h: float
    product_water_kg: float
    feed_heat_kw: float
    membrane_latent_heat_kw: float
    membrane_conductive_heat_kw: float


@dataclass(frozen=True)
class ChannelResult:
    cells: tuple[ChannelCellResult, ...]
    feed_out_temperature_c: float
    permeate_out_temperature_c: float
    feed_out_mass_kg_h: float
    permeate_out_mass_kg_h: float
    concentrate_salinity_g_kg: float
    freshwater_produced_kg: float
    hot_side_thermal_demand_kwh_th: float
    conductive_heat_leak_kwh_th: float
    latent_duty_kwh_th: float


def _cell_interfaces(
    *,
    feed_bulk_c: float,
    permeate_bulk_c: float,
    feed_h: float,
    permeate_h: float,
    membrane_k: float,
    membrane_thickness_m: float,
    latent_heat_kwh_per_kg: float,
    permeance: float,
    water_activity: float,
) -> tuple[float, float, float]:
    """Solve the coupled steady cell interface temperatures by bisection."""
    if feed_bulk_c <= permeate_bulk_c:
        raise ValueError("feed bulk temperature must exceed permeate bulk temperature")
    alpha = membrane_k / membrane_thickness_m

    def residual(feed_interface_c: float) -> tuple[float, float, float]:
        q_feed = feed_h * (feed_bulk_c - feed_interface_c)
        permeate_interface_c = permeate_bulk_c + q_feed / permeate_h
        dp_bar = vapor_pressure_driving_force_bar(
            feed_interface_c, permeate_interface_c, water_activity
        )
        flux = permeance * dp_bar
        q_latent = flux * latent_heat_kwh_per_kg * 1000.0
        q_conductive = alpha * (feed_interface_c - permeate_interface_c)
        q_membrane = q_latent + q_conductive
        return q_feed - q_membrane, permeate_interface_c, flux

    low = permeate_bulk_c
    high = feed_bulk_c
    f_low, _, _ = residual(low)
    f_high, _, _ = residual(high)
    if f_low < 0 or f_high > 0:
        raise ValueError("cell interface energy balance has no physical bisection bracket")

    for _ in range(100):
        mid = 0.5 * (low + high)
        f_mid, _, _ = residual(mid)
        if abs(f_mid) < 1e-8:
            low = high = mid
            break
        if f_mid > 0:
            low = mid
        else:
            high = mid

    feed_interface = 0.5 * (low + high)
    _, permeate_interface, flux = residual(feed_interface)
    return feed_interface, permeate_interface, flux


def simulate_dcmd_channel(
    *,
    config: ChannelConfig,
    feed_in_temperature_c: float,
    permeate_in_temperature_c: float,
) -> ChannelResult:
    """Simulate co-current or counter-current DCMD with explicit axial control volumes."""
    if config.membrane_area_m2 <= 0 or config.cells <= 0:
        raise ValueError("membrane area and cells must be positive")
    if config.duration_h <= 0:
        raise ValueError("duration_h must be positive")
    if config.membrane_permeance_kg_m2_h_bar <= 0:
        raise ValueError("membrane permeance must be positive")
    if config.membrane_thermal_conductivity_w_m_k < 0 or config.membrane_thickness_m <= 0:
        raise ValueError("membrane conductivity must be non-negative and thickness positive")
    if config.feed_heat_transfer_coefficient_w_m2_k <= 0 or config.permeate_heat_transfer_coefficient_w_m2_k <= 0:
        raise ValueError("heat-transfer coefficients must be positive")
    if config.feed_mass_flow_kg_h <= 0 or config.permeate_mass_flow_kg_h <= 0:
        raise ValueError("channel mass-flow rates must be positive")
    if config.salt_mass_transfer_coefficient_m_s is not None:
        if config.salt_mass_transfer_coefficient_m_s <= 0:
            raise ValueError("salt mass-transfer coefficient must be positive")
        if config.solvent_density_kg_m3 is None or config.solvent_density_kg_m3 <= 0:
            raise ValueError("solvent density is required when CP is enabled")
    if config.feed_cp_kj_kg_k <= 0 or config.permeate_cp_kj_kg_k <= 0:
        raise ValueError("heat capacities must be positive")
    if not 0 <= config.feed_salinity_g_kg <= 120:
        raise ValueError("feed salinity must remain within the IAPWS-08 range")
    if config.water_activity_override is not None and not 0 < config.water_activity_override <= 1:
        raise ValueError("water activity override must be in (0,1]")

    cell_area = config.membrane_area_m2 / config.cells

    def march(permeate_temperatures: list[float] | None = None, permeate_mass_flows: list[float] | None = None):
        feed_temperature = feed_in_temperature_c
        permeate_temperature = (
            permeate_in_temperature_c if permeate_temperatures is None else permeate_temperatures[0]
        )
        feed_mass_flow = config.feed_mass_flow_kg_h
        permeate_mass_flow = config.permeate_mass_flow_kg_h
        salt_mass_flow = feed_mass_flow * config.feed_salinity_g_kg / 1000.0
        cells: list[ChannelCellResult] = []

        for index in range(config.cells):
            if permeate_temperatures is not None:
                permeate_temperature = permeate_temperatures[index]
            if permeate_mass_flows is not None:
                permeate_mass_flow = permeate_mass_flows[index]
            feed_salinity = salt_mass_flow / feed_mass_flow * 1000.0
            activity = (
                config.water_activity_override
                if config.water_activity_override is not None
                else (seawater_water_activity(feed_temperature, feed_salinity) if feed_salinity > 0 else 1.0)
            )
            tfm, tpm, flux = _cell_interfaces(
                feed_bulk_c=feed_temperature,
                permeate_bulk_c=permeate_temperature,
                feed_h=config.feed_heat_transfer_coefficient_w_m2_k,
                permeate_h=config.permeate_heat_transfer_coefficient_w_m2_k,
                membrane_k=config.membrane_thermal_conductivity_w_m_k,
                membrane_thickness_m=config.membrane_thickness_m,
                latent_heat_kwh_per_kg=config.latent_heat_kwh_th_per_kg,
                permeance=config.membrane_permeance_kg_m2_h_bar,
                water_activity=activity,
            )
            if config.salt_mass_transfer_coefficient_m_s is not None and feed_salinity > 0:
                previous_flux = flux
                for _ in range(30):
                    cpc = concentration_polarization_coefficient(
                        flux_kg_m2_s=flux / 3600.0,
                        mass_transfer_coefficient_m_s=config.salt_mass_transfer_coefficient_m_s,
                        solvent_density_kg_m3=config.solvent_density_kg_m3,
                    )
                    interface_salinity = interface_salinity_g_kg(feed_salinity, cpc)
                    activity = (
                        seawater_water_activity(tfm, interface_salinity)
                        if config.water_activity_override is None
                        else config.water_activity_override
                    )
                    tfm, tpm, flux = _cell_interfaces(
                        feed_bulk_c=feed_temperature,
                        permeate_bulk_c=permeate_temperature,
                        feed_h=config.feed_heat_transfer_coefficient_w_m2_k,
                        permeate_h=config.permeate_heat_transfer_coefficient_w_m2_k,
                        membrane_k=config.membrane_thermal_conductivity_w_m_k,
                        membrane_thickness_m=config.membrane_thickness_m,
                        latent_heat_kwh_per_kg=config.latent_heat_kwh_th_per_kg,
                        permeance=config.membrane_permeance_kg_m2_h_bar,
                        water_activity=activity,
                    )
                    if abs(flux - previous_flux) < 1e-8:
                        break
                    previous_flux = flux
                cpc = concentration_polarization_coefficient(
                    flux_kg_m2_s=flux / 3600.0,
                    mass_transfer_coefficient_m_s=config.salt_mass_transfer_coefficient_m_s,
                    solvent_density_kg_m3=config.solvent_density_kg_m3,
                )
                interface_salinity = interface_salinity_g_kg(feed_salinity, cpc)
            else:
                cpc = 1.0
                interface_salinity = feed_salinity

            product_rate = flux * cell_area
            product_kg = product_rate * config.duration_h
            q_feed_w = config.feed_heat_transfer_coefficient_w_m2_k * (feed_temperature - tfm) * cell_area
            q_latent_w = product_rate * config.latent_heat_kwh_th_per_kg * 1000.0
            q_conductive_w = (
                config.membrane_thermal_conductivity_w_m_k / config.membrane_thickness_m
                * (tfm - tpm) * cell_area
            )
            feed_heat_kwh = q_feed_w / 1000.0 * config.duration_h
            feed_temperature -= feed_heat_kwh * 3600.0 / (feed_mass_flow * config.feed_cp_kj_kg_k)
            permeate_temperature += feed_heat_kwh * 3600.0 / (permeate_mass_flow * config.permeate_cp_kj_kg_k)
            feed_mass_flow -= product_rate
            permeate_mass_flow += product_rate
            if feed_mass_flow <= 0:
                raise ValueError("feed flow was exhausted inside the module")

            cells.append(
                ChannelCellResult(
                    cell=index + 1,
                    feed_bulk_temperature_c=feed_temperature,
                    permeate_bulk_temperature_c=permeate_temperature,
                    feed_interface_temperature_c=tfm,
                    permeate_interface_temperature_c=tpm,
                    feed_salinity_g_kg=feed_salinity,
                    interface_salinity_g_kg=interface_salinity,
                    concentration_polarization_coefficient=cpc,
                    flux_kg_m2_h=flux,
                    product_water_kg=product_kg,
                    feed_heat_kw=q_feed_w / 1000.0,
                    membrane_latent_heat_kw=q_latent_w / 1000.0,
                    membrane_conductive_heat_kw=q_conductive_w / 1000.0,
                )
            )
        return feed_temperature, permeate_temperature, feed_mass_flow, permeate_mass_flow, cells, salt_mass_flow

    if config.flow_arrangement == "co_current":
        feed_out, permeate_out, feed_mass, permeate_mass, cells, salt_mass_flow = march()
    else:
        # Counter-current operation is a two-point boundary-value problem.
        # Solve it by fixed-point iteration on the permeate bulk-temperature profile.
        profile = [permeate_in_temperature_c] * config.cells
        mass_profile = [config.permeate_mass_flow_kg_h] * config.cells
        for _ in range(200):
            feed_out, _, feed_mass, permeate_mass, cells, salt_mass_flow = march(profile, mass_profile)
            candidate_t = [permeate_in_temperature_c] * config.cells
            candidate_m = [config.permeate_mass_flow_kg_h] * config.cells
            for i in range(config.cells - 1, -1, -1):
                if i == config.cells - 1:
                    candidate_t[i] = permeate_in_temperature_c
                    candidate_m[i] = config.permeate_mass_flow_kg_h
                else:
                    downstream = cells[i + 1]
                    candidate_t[i] = downstream.permeate_bulk_temperature_c
                    candidate_m[i] = mass_profile[i + 1] + downstream.product_water_kg / config.duration_h
            error_t = max(abs(a - b) for a, b in zip(profile, candidate_t))
            error_m = max(abs(a - b) for a, b in zip(mass_profile, candidate_m))
            profile = [0.5 * a + 0.5 * b for a, b in zip(profile, candidate_t)]
            mass_profile = [0.5 * a + 0.5 * b for a, b in zip(mass_profile, candidate_m)]
            if error_t < 1e-7 and error_m < 1e-8:
                break
        else:
            raise RuntimeError("counter-current temperature coupling did not converge")
        feed_out, permeate_out, feed_mass, permeate_mass, cells, salt_mass_flow = march(profile, mass_profile)

    product_total = sum(c.product_water_kg for c in cells)
    latent_total = sum(c.membrane_latent_heat_kw for c in cells) * config.duration_h
    conductive_total = sum(c.membrane_conductive_heat_kw for c in cells) * config.duration_h
