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


@dataclass(frozen=True)
class ChannelCellResult:
    cell: int
    feed_bulk_temperature_c: float
    permeate_bulk_temperature_c: float
    feed_interface_temperature_c: float
    permeate_interface_temperature_c: float
    feed_salinity_g_kg: float
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
    """Simulate a co-current DCMD module with explicit axial control volumes."""
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
    if config.feed_cp_kj_kg_k <= 0 or config.permeate_cp_kj_kg_k <= 0:
        raise ValueError("heat capacities must be positive")
    if not 0 <= config.feed_salinity_g_kg <= 120:
        raise ValueError("feed salinity must remain within the IAPWS-08 range")
    if config.water_activity_override is not None and not 0 < config.water_activity_override <= 1:
        raise ValueError("water activity override must be in (0,1]")

    cell_area = config.membrane_area_m2 / config.cells
    feed_temperature = feed_in_temperature_c
    permeate_temperature = permeate_in_temperature_c
    feed_mass_flow = config.feed_mass_flow_kg_h
    permeate_mass_flow = config.permeate_mass_flow_kg_h
    salt_mass_flow = feed_mass_flow * config.feed_salinity_g_kg / 1000.0
    cells: list[ChannelCellResult] = []

    for index in range(config.cells):
        feed_salinity = salt_mass_flow / feed_mass_flow * 1000.0
        if config.water_activity_override is not None:
            activity = config.water_activity_override
        elif feed_salinity > 0:
            activity = seawater_water_activity(feed_temperature, feed_salinity)
        else:
            activity = 1.0

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

        product_rate = flux * cell_area
        product_kg = product_rate * config.duration_h
        q_feed_w = config.feed_heat_transfer_coefficient_w_m2_k * (feed_temperature - tfm) * cell_area
        q_latent_w = product_rate * config.latent_heat_kwh_th_per_kg * 1000.0
        q_conductive_w = (
            config.membrane_thermal_conductivity_w_m_k
            / config.membrane_thickness_m
            * (tfm - tpm)
            * cell_area
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
                flux_kg_m2_h=flux,
                product_water_kg=product_kg,
                feed_heat_kw=q_feed_w / 1000.0,
                membrane_latent_heat_kw=q_latent_w / 1000.0,
                membrane_conductive_heat_kw=q_conductive_w / 1000.0,
            )
        )

    product_total = sum(c.product_water_kg for c in cells)
    latent_total = sum(c.membrane_latent_heat_kw for c in cells) * config.duration_h
    conductive_total = sum(c.membrane_conductive_heat_kw for c in cells) * config.duration_h
    return ChannelResult(
        cells=tuple(cells),
        feed_out_temperature_c=feed_temperature,
        permeate_out_temperature_c=permeate_temperature,
        feed_out_mass_kg_h=feed_mass_flow,
        permeate_out_mass_kg_h=permeate_mass_flow,
        concentrate_salinity_g_kg=salt_mass_flow / feed_mass_flow * 1000.0,
        freshwater_produced_kg=product_total,
        hot_side_thermal_demand_kwh_th=latent_total + conductive_total,
        conductive_heat_leak_kwh_th=conductive_total,
        latent_duty_kwh_th=latent_total,
    )