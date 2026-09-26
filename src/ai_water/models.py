"""Core research parameter and result models. SI units unless documented otherwise."""
from pydantic import BaseModel, Field

class Workload(BaseModel):
    it_power_kw: float = Field(gt=0)
    duration_h: float = Field(gt=0)
    recoverable_heat_fraction: float = Field(ge=0, le=1, default=0.8)

class Cooling(BaseModel):
    facility_overhead_fraction: float = Field(ge=0, default=0.0)
    cooling_water_consumption_l_per_kwh_facility: float = Field(ge=0, default=0.0)
    cooling_heat_penalty_fraction: float = Field(ge=0, le=1, default=0.0)
    md_cooling_to_heating_ratio: float = Field(ge=0, default=0.0)

class HeatRecovery(BaseModel):
    recovery_efficiency: float = Field(ge=0, le=1, default=0.5)
    heat_exchanger_effectiveness: float = Field(ge=0, le=1, default=0.8)
    usable_heat_fraction: float = Field(ge=0, le=1, default=1.0)
    source_temperature_c: float
    cold_side_temperature_c: float

class MembraneDistillation(BaseModel):
    membrane_area_m2: float = Field(gt=0)
    membrane_permeance_kg_m2_h_bar: float = Field(gt=0)
    thermal_energy_kwh_th_per_kg: float = Field(gt=0)
    feed_recovery_fraction: float = Field(ge=0, lt=1, default=0.2)
    feed_salinity_g_kg: float = Field(ge=0, default=0.0)
    water_activity: float = Field(gt=0, le=1, default=1.0)
    temperature_polarization_coefficient: float = Field(gt=0, le=1, default=1.0)
    cold_interface_temperature_c: float | None = None
    feed_interface_temperature_c: float | None = None

class AuxiliaryLoads(BaseModel):
    pump_kwh_per_m3: float = Field(ge=0, default=0.0)
    pretreatment_kwh_per_m3: float = Field(ge=0, default=0.0)
    other_kwh_per_m3: float = Field(ge=0, default=0.0)

class WaterFactors(BaseModel):
    grid_water_l_per_kwh: float = Field(ge=0, default=0.0)

class Scenario(BaseModel):
    workload: Workload
    cooling: Cooling
    recovery: HeatRecovery
    md: MembraneDistillation
    auxiliary: AuxiliaryLoads = Field(default_factory=AuxiliaryLoads)
    water: WaterFactors = Field(default_factory=WaterFactors)

class Result(BaseModel):
    it_energy_kwh: float
    facility_energy_kwh: float
    heat_generated_kwh_th: float
    recoverable_heat_kwh_th: float
    md_thermal_demand_kwh_th: float
    md_cooling_demand_kwh_th: float
    freshwater_produced_l: float
    direct_cooling_consumption_l: float
    auxiliary_electricity_kwh: float
    indirect_water_consumption_l: float
    additional_water_consumption_l: float
    net_freshwater_benefit_l: float
    heat_limited: bool
