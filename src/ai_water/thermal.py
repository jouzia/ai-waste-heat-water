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
