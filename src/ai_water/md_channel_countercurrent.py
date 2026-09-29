"""Counter-current extension for the reduced-order DCMD channel model.

This solver keeps the same cell physics as md_channel but resolves the
counter-current boundary-value problem by alternating feed-forward and
permeate-backward energy sweeps. It is intentionally separate so the
existing co-current implementation remains backward compatible.
"""

from .md_channel import ChannelCellResult, ChannelConfig, ChannelResult, _cell_interfaces
from .channel_transport import concentration_polarization_coefficient, interface_salinity_g_kg
from .md import seawater_water_activity


def simulate_countercurrent_dcmd_channel(*, config: ChannelConfig, feed_in_temperature_c: float, permeate_in_temperature_c: float, max_iterations: int = 500, tolerance_c: float = 1e-7) -> ChannelResult:
    """Solve a counter-current DCMD module with fixed inlet temperatures.

    feed_in_temperature_c is the feed inlet at x=0. permeate_in_temperature_c
    is the permeate inlet at x=L. The coupled bulk-temperature boundary
    condition is solved iteratively; no parameter fitting is performed.
    """
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

    n = config.cells
    area = config.membrane_area_m2 / n
    # Initial profile: weakly perturbed interpolation between the known inlet
    # and an estimated outlet. The subsequent sweeps determine the outlet.
    permeate_profile = [permeate_in_temperature_c] * (n + 1)
    feed_profile = [feed_in_temperature_c] * (n + 1)
    previous_product = None

    for _ in range(max_iterations):
        # Feed sweep: known feed inlet at x=0.
        feed_profile[0] = feed_in_temperature_c
        feed_mass = config.feed_mass_flow_kg_h
        salt_mass = feed_mass * config.feed_salinity_g_kg / 1000.0
        feed_results = []
        for i in range(n):
            tf = feed_profile[i]
            tp = permeate_profile[i]
            salinity = salt_mass / feed_mass * 1000.0
            activity = (
                config.water_activity_override
                if config.water_activity_override is not None
                else seawater_water_activity(tf, salinity) if salinity > 0 else 1.0
            )
            tfm, tpm, flux = _cell_interfaces(
                feed_bulk_c=tf, permeate_bulk_c=tp,
                feed_h=config.feed_heat_transfer_coefficient_w_m2_k,
                permeate_h=config.permeate_heat_transfer_coefficient_w_m2_k,
                membrane_k=config.membrane_thermal_conductivity_w_m_k,
                membrane_thickness_m=config.membrane_thickness_m,
                latent_heat_kwh_per_kg=config.latent_heat_kwh_th_per_kg,
                permeance=config.membrane_permeance_kg_m2_h_bar,
                water_activity=activity,
            )
            if config.salt_mass_transfer_coefficient_m_s is not None and salinity > 0:
                cpc = concentration_polarization_coefficient(
                    flux_kg_m2_s=flux / 3600.0,
                    mass_transfer_coefficient_m_s=config.salt_mass_transfer_coefficient_m_s,
                    solvent_density_kg_m3=config.solvent_density_kg_m3,
                )
                interface_salinity = interface_salinity_g_kg(salinity, cpc)
                activity = (
                    config.water_activity_override
                    if config.water_activity_override is not None
                    else seawater_water_activity(tfm, interface_salinity)
                )
                tfm, tpm, flux = _cell_interfaces(
                    feed_bulk_c=tf, permeate_bulk_c=tp,
                    feed_h=config.feed_heat_transfer_coefficient_w_m2_k,
                    permeate_h=config.permeate_heat_transfer_coefficient_w_m2_k,
                    membrane_k=config.membrane_thermal_conductivity_w_m_k,
                    membrane_thickness_m=config.membrane_thickness_m,
                    latent_heat_kwh_per_kg=config.latent_heat_kwh_th_per_kg,
                    permeance=config.membrane_permeance_kg_m2_h_bar,
                    water_activity=activity,
                )
            else:
                cpc = 1.0
                interface_salinity = salinity
            product_rate = flux * area
            q_w = config.feed_heat_transfer_coefficient_w_m2_k * (tf - tfm) * area
            product_kg = product_rate * config.duration_h
            feed_cp = config.feed_cp_kj_kg_k * 1000.0
            feed_profile[i + 1] = tf - (q_w / 1000.0 * config.duration_h) * 1000.0 / (feed_mass * feed_cp) * 3600.0
            # Equivalent direct energy form above; retain an explicit mass balance.
            feed_mass -= product_rate
            if feed_mass <= 0:
                raise ValueError("feed flow was exhausted inside the module")
            feed_results.append((tfm, tpm, flux, product_kg, q_w, salinity, interface_salinity, cpc, feed_mass))

        # Permeate sweep: known permeate inlet at x=L, travelling backward.
        permeate_profile[n] = permeate_in_temperature_c
        permeate_mass = config.permeate_mass_flow_kg_h
        for i in range(n - 1, -1, -1):
            tf = feed_profile[i]
            tp = permeate_profile[i + 1]
            tfm, tpm, flux, product_kg, q_w, salinity, interface_salinity, cpc, _ = feed_results[i]
            q_permeate_kwh = q_w / 1000.0 * config.duration_h
            permeate_profile[i] = tp + q_permeate_kwh * 1000.0 / (permeate_mass * config.permeate_cp_kj_kg_k) * 3600.0
            permeate_mass += flux * area

        product = sum(x[3] for x in feed_results)
        change = abs(product - previous_product) if previous_product is not None else float('inf')
        previous_product = product
        if change < tolerance_c * max(1.0, product):
            break
    else:
        raise RuntimeError("counter-current DCMD boundary iteration did not converge")

    cells = []
    latent_total = 0.0
    conductive_total = 0.0
    for i, (tfm, tpm, flux, product_kg, q_w, salinity, interface_salinity, cpc, _) in enumerate(feed_results):
        q_latent_w = flux * area * config.latent_heat_kwh_th_per_kg * 1000.0
        q_cond_w = config.membrane_thermal_conductivity_w_m_k / config.membrane_thickness_m * (tfm - tpm) * area
        latent_total += q_latent_w / 1000.0 * config.duration_h
        conductive_total += q_cond_w / 1000.0 * config.duration_h
        cells.append(ChannelCellResult(
            cell=i + 1,
            feed_bulk_temperature_c=feed_profile[i],
            permeate_bulk_temperature_c=permeate_profile[i],
            feed_interface_temperature_c=tfm,
            permeate_interface_temperature_c=tpm,
            feed_salinity_g_kg=salinity,
            interface_salinity_g_kg=interface_salinity,
            concentration_polarization_coefficient=cpc,
            flux_kg_m2_h=flux,
            product_water_kg=product_kg,
            feed_heat_kw=q_w / 1000.0,
            membrane_latent_heat_kw=q_latent_w / 1000.0,
            membrane_conductive_heat_kw=q_cond_w / 1000.0,
        ))

    feed_out_mass = feed_results[-1][-1]
    permeate_out_mass = config.permeate_mass_flow_kg_h + previous_product / config.duration_h
    salt_mass_flow = config.feed_mass_flow_kg_h * config.feed_salinity_g_kg / 1000.0
    return ChannelResult(
        cells=tuple(cells),
        feed_out_temperature_c=feed_profile[-1],
        permeate_out_temperature_c=permeate_profile[0],
        feed_out_mass_kg_h=feed_out_mass,
        permeate_out_mass_kg_h=permeate_out_mass,
        concentrate_salinity_g_kg=salt_mass_flow / feed_out_mass * 1000.0,
        freshwater_produced_kg=previous_product,
        hot_side_thermal_demand_kwh_th=latent_total + conductive_total,
        conductive_heat_leak_kwh_th=conductive_total,
        latent_duty_kwh_th=latent_total,
    )