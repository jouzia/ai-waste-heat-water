"""Hydraulic screening primitives for membrane-distillation circulation.

The pressure-drop route follows P_pump = ΔP * Q / η. If a literature- or
manufacturer-derived specific pumping energy is supplied directly, that
value remains available for legacy/reproduction cases.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class PumpingResult:
    feed_flow_m3_h: float
    pressure_drop_pa: float
    hydraulic_power_kw: float
    electrical_power_kw: float
    specific_electricity_kwh_m3: float

def pumping_from_pressure_drop(
    *,
    distillate_l: float,
    duration_h: float,
    recovery_fraction: float,
    pressure_drop_bar: float,
    pump_efficiency: float,
) -> PumpingResult:
    if distillate_l < 0 or duration_h <= 0:
        raise ValueError("distillate_l must be non-negative and duration_h positive")
    if not 0 < recovery_fraction < 1:
        raise ValueError("recovery_fraction must be in (0,1)")
    if pressure_drop_bar < 0:
        raise ValueError("pressure_drop_bar must be non-negative")
    if not 0 < pump_efficiency <= 1:
        raise ValueError("pump_efficiency must be in (0,1]")

    distillate_m3 = distillate_l / 1000.0
    feed_m3 = distillate_m3 / recovery_fraction
    feed_flow_m3_h = feed_m3 / duration_h
    pressure_drop_pa = pressure_drop_bar * 100_000.0
    hydraulic_power_kw = pressure_drop_pa * (feed_flow_m3_h / 3600.0) / 1000.0
    electrical_power_kw = hydraulic_power_kw / pump_efficiency
    specific = electrical_power_kw / feed_flow_m3_h if feed_flow_m3_h > 0 else 0.0

    return PumpingResult(
        feed_flow_m3_h=feed_flow_m3_h,
        pressure_drop_pa=pressure_drop_pa,
        hydraulic_power_kw=hydraulic_power_kw,
        electrical_power_kw=electrical_power_kw,
        specific_electricity_kwh_m3=specific,
    )
