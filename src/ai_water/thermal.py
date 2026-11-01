"""First-order system thermal balance primitives."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ThermalBalance:
    it_heat_kwh_th: float
    recoverable_source_kwh_th: float
    md_heating_kwh_th: float
    md_cooling_kwh_th: float
    unrecovered_heat_kwh_th: float
    residual_heat_rejection_kwh_th: float

def balance(*, it_energy_kwh: float, recoverable_heat_fraction: float,
            recovery_efficiency: float, heat_exchanger_effectiveness: float,
            usable_heat_fraction: float, md_heating_kwh_th: float,
            cooling_to_heating_ratio: float = 0.0) -> ThermalBalance:
    vals=(it_energy_kwh,recoverable_heat_fraction,recovery_efficiency,
          heat_exchanger_effectiveness,usable_heat_fraction,md_heating_kwh_th,
          cooling_to_heating_ratio)
    if any(x < 0 for x in vals): raise ValueError("thermal inputs cannot be negative")
    if any(x > 1 for x in (recoverable_heat_fraction,recovery_efficiency,
                           heat_exchanger_effectiveness,usable_heat_fraction)):
        raise ValueError("thermal fractions must be <= 1")
    it_heat=it_energy_kwh
    recoverable=(it_heat*recoverable_heat_fraction*recovery_efficiency*
                 heat_exchanger_effectiveness*usable_heat_fraction)
    supplied=min(recoverable,md_heating_kwh_th)
    cooling=supplied*cooling_to_heating_ratio
    return ThermalBalance(it_heat, recoverable, supplied, cooling,
                          max(0.0,it_heat-recoverable), max(0.0,it_heat-supplied))


def heat_exergy_kwh(*, heat_kwh_th: float, source_temperature_c: float, ambient_temperature_c: float) -> float:
    """Return physical exergy of heat relative to an ambient reference.

    For a heat quantity Q supplied reversibly at constant source temperature T,
    the maximum work potential is Q*(1-T0/T). This is a quality metric, not an
    assertion that the MD subsystem can convert the exergy to work.
    """
    if heat_kwh_th < 0:
        raise ValueError("heat cannot be negative")
    if source_temperature_c <= -273.15 or ambient_temperature_c <= -273.15:
        raise ValueError("temperatures must exceed absolute zero")
    source_k = source_temperature_c + 273.15
    ambient_k = ambient_temperature_c + 273.15
    if source_k <= ambient_k:
        return 0.0
    return heat_kwh_th * (1.0 - ambient_k / source_k)


def exergy_efficiency(*, useful_heat_kwh_th: float, source_heat_kwh_th: float,
                      source_temperature_c: float, ambient_temperature_c: float) -> float:
    """Return useful heat exergy divided by available source heat exergy."""
    if useful_heat_kwh_th < 0 or source_heat_kwh_th < 0:
        raise ValueError("heat quantities cannot be negative")
    available = heat_exergy_kwh(
        heat_kwh_th=source_heat_kwh_th,
        source_temperature_c=source_temperature_c,
        ambient_temperature_c=ambient_temperature_c,
    )
    if available == 0:
        return 0.0
    useful = min(useful_heat_kwh_th, source_heat_kwh_th)
    return heat_exergy_kwh(
        heat_kwh_th=useful,
        source_temperature_c=source_temperature_c,
        ambient_temperature_c=ambient_temperature_c,
    ) / available
