"""Membrane-distillation transport primitives.

The model separates bulk temperatures from membrane-interface temperatures
and applies a water-activity correction to the ideal vapor-pressure driving
force. It remains a reduced-order transport model, not CFD.
"""
_ANTOINE = (
    (304.0, 333.0, 5.20389, 1733.926, -39.485),
    (334.0, 363.0, 5.0768, 1659.793, -45.854),
)

def saturation_pressure_bar(temperature_c: float) -> float:
    temperature_k = temperature_c + 273.15
    for lower, upper, a, b, c in _ANTOINE:
        if lower <= temperature_k <= upper:
            return 10.0 ** (a - b / (temperature_k + c))
    raise ValueError("temperature outside implemented NIST Antoine ranges: 304-363 K")

def interface_temperatures(
    hot_bulk_c: float,
    cold_bulk_c: float,
    temperature_polarization_coefficient: float,
) -> tuple[float, float]:
    """Reduced-order interface temperatures using a TPC.

    T_fi = T_cold + TPC*(T_hot-T_cold)
    T_pi = T_hot - TPC*(T_hot-T_cold)

    This symmetric representation is a screening approximation. A later
    module should replace it with channel-specific heat-transfer balances.
    """
    if not 0 < temperature_polarization_coefficient <= 1:
        raise ValueError("temperature polarization coefficient must be in (0,1]")
    if hot_bulk_c <= cold_bulk_c:
        raise ValueError("hot bulk temperature must exceed cold bulk temperature")
    delta = hot_bulk_c - cold_bulk_c
    return (
        cold_bulk_c + temperature_polarization_coefficient * delta,
        hot_bulk_c - temperature_polarization_coefficient * delta,
    )

def water_vapor_pressure_bar(temperature_c: float, water_activity: float = 1.0) -> float:
    if not 0 < water_activity <= 1:
        raise ValueError("water activity must be in (0,1]")
    return water_activity * saturation_pressure_bar(temperature_c)

def vapor_pressure_driving_force_bar(
    hot_c: float,
    cold_c: float,
    water_activity: float = 1.0,
) -> float:
    return max(0.0, water_vapor_pressure_bar(hot_c, water_activity)
               - water_vapor_pressure_bar(cold_c, 1.0))

def flux_kg_m2_h(
    hot_c: float,
    cold_c: float,
    membrane_permeance_kg_m2_h_bar: float,
    water_activity: float = 1.0,
) -> float:
    if membrane_permeance_kg_m2_h_bar < 0:
        raise ValueError("membrane permeance must be non-negative")
    return membrane_permeance_kg_m2_h_bar * vapor_pressure_driving_force_bar(
        hot_c, cold_c, water_activity
    )
