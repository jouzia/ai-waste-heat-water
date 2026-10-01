"""Deterministic reduced-order coupled system model."""
from .hydraulics import pumping_from_pressure_drop
from .md import (
    flux_kg_m2_h,
    interface_temperatures,
    mean_single_pass_salinity_g_kg,
    seawater_water_activity,
)
from .md_thermal import account_for_membrane_heat
from .models import Result, Scenario


def simulate(s: Scenario) -> Result:
    it_energy = s.workload.it_power_kw * s.workload.duration_h
    heat_generated = it_energy
    raw_recoverable = (
        heat_generated
        * s.workload.recoverable_heat_fraction
        * s.recovery.recovery_efficiency
        * s.recovery.heat_exchanger_effectiveness
        * s.recovery.usable_heat_fraction
    )
    recoverable = raw_recoverable * (1.0 - s.cooling.cooling_heat_penalty_fraction)
    facility_energy = it_energy * (1.0 + s.cooling.facility_overhead_fraction)

    if s.md.flux_kg_m2_h is not None:
        md_flux = s.md.flux_kg_m2_h
        hot_i = s.recovery.source_temperature_c
        cold_i = s.recovery.cold_side_temperature_c
    else:
        if s.md.feed_interface_temperature_c is not None:
            hot_i = s.md.feed_interface_temperature_c
        if s.md.cold_interface_temperature_c is not None:
            cold_i = s.md.cold_interface_temperature_c
        if s.md.feed_interface_temperature_c is None or s.md.cold_interface_temperature_c is None:
            derived_hot, derived_cold = interface_temperatures(
                s.recovery.source_temperature_c,
                s.recovery.cold_side_temperature_c,
                s.md.temperature_polarization_coefficient,
            )
            hot_i = s.md.feed_interface_temperature_c or derived_hot
            cold_i = s.md.cold_interface_temperature_c or derived_cold

        # For a single-pass feed, salt is retained while water is removed.
        # Use a water-removal-weighted bulk salinity for the lumped flux model.
        # This captures recovery-driven concentration without pretending to
        # resolve the separate concentration-polarization boundary layer.
        effective_salinity = mean_single_pass_salinity_g_kg(
            s.md.feed_salinity_g_kg,
            s.md.feed_recovery_fraction,
        )
        if s.md.water_activity is not None:
            activity = s.md.water_activity
        elif s.md.use_iapws_seawater and effective_salinity > 0:
            activity = seawater_water_activity(
                hot_i,
                effective_salinity,
            )
        else:
            activity = 1.0
        md_flux = flux_kg_m2_h(
            hot_i,
            cold_i,
            s.md.membrane_permeance_kg_m2_h_bar,
            activity,
        )

    potential_water_kg = md_flux * s.md.membrane_area_m2 * s.workload.duration_h

    if s.md.latent_heat_kwh_th_per_kg is None:
        effective_duty_per_kg = s.md.thermal_energy_kwh_th_per_kg
        potential_demand = potential_water_kg * effective_duty_per_kg
        conductive_leak = 0.0
    else:
        thermal = account_for_membrane_heat(
            water_kg=potential_water_kg,
            latent_heat_kwh_th_per_kg=s.md.latent_heat_kwh_th_per_kg,
            membrane_area_m2=s.md.membrane_area_m2,
            interface_delta_t_k=max(0.0, hot_i - cold_i),
            membrane_thermal_conductivity_w_m_k=s.md.membrane_thermal_conductivity_w_m_k,
            membrane_thickness_m=s.md.membrane_thickness_m,
            duration_h=s.workload.duration_h,
        )
        effective_duty_per_kg = (
            thermal.latent_duty_kwh_th / potential_water_kg
            if potential_water_kg
            else s.md.latent_heat_kwh_th_per_kg
        )
        potential_demand = thermal.hot_side_duty_kwh_th
        conductive_leak = thermal.conductive_heat_leak_kwh_th

    actual_water_kg = potential_water_kg
    heat_limited = False
    if potential_demand > recoverable:
        heat_limited = True
        if s.md.latent_heat_kwh_th_per_kg is None:
            actual_water_kg = recoverable / effective_duty_per_kg
        else:
            available_for_vaporization = max(0.0, recoverable - conductive_leak)
            actual_water_kg = (
                available_for_vaporization / effective_duty_per_kg
                if effective_duty_per_kg > 0
                else 0.0
            )

    freshwater_l = max(0.0, actual_water_kg)

    if s.md.latent_heat_kwh_th_per_kg is None:
        md_demand = freshwater_l * s.md.thermal_energy_kwh_th_per_kg
        md_latent = md_demand
        md_conductive = 0.0
    else:
        thermal_actual = account_for_membrane_heat(
            water_kg=freshwater_l,
            latent_heat_kwh_th_per_kg=s.md.latent_heat_kwh_th_per_kg,
            membrane_area_m2=s.md.membrane_area_m2,
            interface_delta_t_k=max(0.0, hot_i - cold_i),
            membrane_thermal_conductivity_w_m_k=s.md.membrane_thermal_conductivity_w_m_k,
            membrane_thickness_m=s.md.membrane_thickness_m,
            duration_h=s.workload.duration_h,
        )
        md_demand = thermal_actual.hot_side_duty_kwh_th
        md_latent = thermal_actual.latent_duty_kwh_th
        md_conductive = thermal_actual.conductive_heat_leak_kwh_th

    md_cooling = md_demand * s.cooling.md_cooling_to_heating_ratio
    md_cooling_electricity = (
        md_cooling * s.cooling.md_cooling_electricity_kwh_per_kwh_th
    )
    md_cooling_water = md_cooling * s.cooling.md_cooling_water_l_per_kwh_th

    if s.md.pressure_drop_bar is not None:
        if s.md.pump_efficiency is None:
            raise ValueError("pump_efficiency is required when pressure_drop_bar is supplied")
        pumping = pumping_from_pressure_drop(
            distillate_l=freshwater_l,
            duration_h=s.workload.duration_h,
            recovery_fraction=s.md.feed_recovery_fraction,
            pressure_drop_bar=s.md.pressure_drop_bar,
            pump_efficiency=s.md.pump_efficiency,
        )
        pumping_electricity = pumping.electrical_power_kw * s.workload.duration_h
    else:
        pumping_electricity = freshwater_l / 1000.0 * s.auxiliary.pump_kwh_per_m3

    feed_water_l = freshwater_l / s.md.feed_recovery_fraction
    concentrate_l = max(0.0, feed_water_l - freshwater_l)

    auxiliary_kwh = (
        pumping_electricity
        + freshwater_l
        / 1000.0
        * (s.auxiliary.pretreatment_kwh_per_m3 + s.auxiliary.other_kwh_per_m3)
        + md_cooling_electricity
    )
    # The baseline data-center cooling burden belongs to the counterfactual.
    # Count only incremental facility electricity attributable to the
    # intervention here; MD-specific cooling water is always incremental.
    cooling_l = (
        s.cooling.incremental_facility_electricity_kwh
        * s.cooling.cooling_water_consumption_l_per_kwh_facility
        + md_cooling_water
    )
    indirect_l = (s.cooling.incremental_facility_electricity_kwh + auxiliary_kwh) * s.water.grid_water_l_per_kwh
    additional_l = cooling_l + indirect_l
    avoided_l = s.water.avoided_freshwater_consumption_l

    concentrate_salinity = (
        s.md.feed_salinity_g_kg
        / (1.0 - s.md.feed_recovery_fraction)
        if s.md.feed_salinity_g_kg > 0
        else 0.0
    )
    return Result(
        it_energy_kwh=it_energy,
        facility_energy_kwh=facility_energy,
        heat_generated_kwh_th=heat_generated,
        recoverable_heat_kwh_th=recoverable,
        md_thermal_demand_kwh_th=md_demand,
        md_latent_demand_kwh_th=md_latent,
        md_conductive_heat_leak_kwh_th=md_conductive,
        md_cooling_demand_kwh_th=md_cooling,
        md_cooling_electricity_kwh=md_cooling_electricity,
        md_cooling_water_l=md_cooling_water,
        freshwater_produced_l=freshwater_l,
        feed_water_withdrawal_l=feed_water_l,
        concentrate_discharge_l=concentrate_l,
        concentrate_salinity_g_kg=concentrate_salinity,
        direct_cooling_consumption_l=cooling_l,
        pumping_electricity_kwh=pumping_electricity,
        auxiliary_electricity_kwh=auxiliary_kwh,
        indirect_water_consumption_l=indirect_l,
        additional_water_consumption_l=additional_l,
        avoided_freshwater_consumption_l=avoided_l,
        net_consumption_change_l=additional_l - avoided_l,
        net_freshwater_benefit_l=-(additional_l - avoided_l),
        heat_limited=heat_limited,
    )
