"""Deterministic baseline system model.

This is a transparent accounting model, not a validated digital twin.
"""
from .models import Result, Scenario

def simulate(s: Scenario) -> Result:
    it_energy = s.workload.it_power_kw * s.workload.duration_h
    heat_generated = it_energy
    recoverable = (
        heat_generated
        * s.workload.recoverable_heat_fraction
        * s.recovery.recovery_efficiency
        * s.recovery.heat_exchanger_effectiveness
        * s.recovery.usable_heat_fraction
    )
    facility_energy = it_energy * (1.0 + s.cooling.facility_overhead_fraction)

    md_water_kg = s.md.flux_kg_m2_h * s.md.membrane_area_m2 * s.workload.duration_h
    md_demand = md_water_kg * s.md.thermal_energy_kwh_th_per_kg

    actual_md_water_kg = md_water_kg
    heat_limited = False
    if md_demand > recoverable:
        actual_md_water_kg = recoverable / s.md.thermal_energy_kwh_th_per_kg
        heat_limited = True

    freshwater_l = max(0.0, actual_md_water_kg)
    auxiliary_kwh = freshwater_l / 1000.0 * (
        s.auxiliary.pump_kwh_per_m3
        + s.auxiliary.pretreatment_kwh_per_m3
        + s.auxiliary.other_kwh_per_m3
    )
    cooling_l = facility_energy * s.cooling.cooling_water_consumption_l_per_kwh_facility
    indirect_l = (facility_energy + auxiliary_kwh) * s.water.grid_water_l_per_kwh
    additional_l = cooling_l + auxiliary_kwh * s.water.grid_water_l_per_kwh + indirect_l
    net = freshwater_l - additional_l

    return Result(
        it_energy_kwh=it_energy,
        facility_energy_kwh=facility_energy,
        heat_generated_kwh_th=heat_generated,
        recoverable_heat_kwh_th=recoverable,
        md_thermal_demand_kwh_th=min(md_demand, recoverable),
        freshwater_produced_l=freshwater_l,
        direct_cooling_consumption_l=cooling_l,
        auxiliary_electricity_kwh=auxiliary_kwh,
        indirect_water_consumption_l=indirect_l,
        additional_water_consumption_l=additional_l,
        net_freshwater_benefit_l=net,
        heat_limited=heat_limited,
    )
