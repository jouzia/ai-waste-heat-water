"""Deterministic reduced-order coupled system model."""
from .hydraulics import pumping_from_pressure_drop
from .md import flux_kg_m2_h, interface_temperatures
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
        md_flux = flux_kg_m2_h(
            hot_i,
            cold_i,
            s.md.membrane_permeance_kg_m2_h_bar,
            s.md.water_activity,
        )

    potential_water_kg = md_flux * s.md.membrane_area_m2 * s.workload.duration_h

    if s.md.latent_heat_kwh_th_per_kg is None:
        effective_duty_per_kg = s.md.thermal_energy_kwh_th_per_kg
        potential_demand = potential_water_kg * effective_duty_per_kg
        conductive_leak = 0.0
        latent_demand = (
            potential_water_kg * s.md.thermal_energy_kwh_th_per_kg
        )
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
        effective_duty_per_kg = thermal.hot_side_duty_kwh_th / potential_water_kg if potential_water_kg else s.md.latent_heat_kwh_th_per_kg
        potential_demand = thermal.hot_side_duty_kwh_th
        conductive_leak = thermal.conductive_heat_leak_kwh_th
        latent_demand = thermal.latent_duty_kwh_th

    actual_water_kg = potential_water_kg
    heat_limited = False
    if potential_demand > recoverable:
        actual_water_kg = recoverable / effective_duty_per_kg
        heat_limited = True

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
        + freshwater_l / 1000.0
        * (s.auxiliary.pretreatment_kwh_per_m3 + s.auxiliary.other_kwh_per_m3)
        + md_cooling_electricity
    )
    cooling_l = (
        facility_energy * s.cooling.cooling_water_consumption_l_per_kwh_facility
        + md_cooling_water
    )
    indirect_l = (facility_energy + auxiliary_kwh) * s.water.grid_water_l_per_kwh
    additional_l = cooling_l + indirect_l

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
        direct_cooling_consumption_l=cooling_l,
        pumping_electricity_kwh=pumping_electricity,
        auxiliary_electricity_kwh=auxiliary_kwh,
        indirect_water_consumption_l=indirect_l,
        additional_water_consumption_l=additional_l,
        net_freshwater_benefit_l=freshwater_l - additional_l,
        heat_limited=heat_limited,
    )
