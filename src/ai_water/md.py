"""Membrane-distillation transport primitives.

The model separates bulk temperatures from membrane-interface temperatures.
For the primary seawater pathway, IAPWS-08 provides thermodynamic seawater
properties; the pure-water Antoine path remains available as a documented
screening/legacy path.

Salinity handling distinguishes inlet feed salinity from the salinity of a
single-pass feed that becomes progressively concentrated as water is removed.
The latter is a lumped approximation; it is not a substitute for a
channel-resolved concentration-polarization model.
"""
try:
    from iapws import IAPWS95
    from iapws.iapws08 import SeaWater
except ImportError:  # pragma: no cover - dependency is declared in pyproject
    IAPWS95 = None
    SeaWater = None

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
    """Reduced-order interface temperatures using a symmetric TPC approximation."""
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


def concentrate_salinity_g_kg(
    feed_salinity_g_kg: float,
    recovery_fraction: float,
) -> float:
    """Return ideal single-pass concentrate salinity with complete salt retention.

    This is a mass-balance result for a nonvolatile solute:
        S_out = S_in / (1 - R)

    It intentionally does not model precipitation, density changes, leakage,
    multistage recycle, or concentration polarization.
    """
    if feed_salinity_g_kg < 0:
        raise ValueError("feed salinity cannot be negative")
    if not 0 <= recovery_fraction < 1:
        raise ValueError("recovery fraction must be in [0,1)")
    return feed_salinity_g_kg / (1.0 - recovery_fraction)


def mean_single_pass_salinity_g_kg(
    feed_salinity_g_kg: float,
    recovery_fraction: float,
) -> float:
    """Return water-removal-weighted bulk salinity for a lumped single-pass model.

    With ideal salt retention, instantaneous bulk salinity follows
    S(x)=S0/x as the remaining water fraction x falls from 1 to 1-R.
    Averaging over the withdrawn water gives:
        S_mean = S0 * [-ln(1-R)] / R.

    For R -> 0 the limiting value is S0. This is a bulk-feed approximation,
    not a concentration-polarization correction.
    """
    if feed_salinity_g_kg < 0:
        raise ValueError("feed salinity cannot be negative")
    if not 0 <= recovery_fraction < 1:
        raise ValueError("recovery fraction must be in [0,1)")
    if recovery_fraction == 0:
        return feed_salinity_g_kg
    import math
    return feed_salinity_g_kg * (-math.log1p(-recovery_fraction)) / recovery_fraction


def seawater_water_activity(
    temperature_c: float,
    salinity_g_kg: float,
    pressure_mpa: float = 0.101325,
) -> float:
    """Return H2O activity from the IAPWS-08 seawater chemical potential.

    The activity is defined relative to pure-water chemical potential:
    a_w = exp((mu_w,seawater - mu_w,pure) / (R*T)).
    IAPWS-08 uses absolute salinity on the 2008 reference-composition scale.
    """
    if SeaWater is None or IAPWS95 is None:
        raise ImportError("iapws is required for the IAPWS-08 seawater pathway")
    if not 0 <= salinity_g_kg <= 120:
        raise ValueError("IAPWS-08 salinity range is 0-120 g/kg")
    if not 261 <= temperature_c + 273.15 <= 353:
        raise ValueError("IAPWS-08 temperature range is 261-353 K")
    if pressure_mpa <= 0 or pressure_mpa > 100:
        raise ValueError("IAPWS-08 pressure must be in (0,100] MPa")

    temperature_k = temperature_c + 273.15
    sw = SeaWater(T=temperature_k, P=pressure_mpa, S=salinity_g_kg / 1000.0)
    pure = IAPWS95(T=temperature_k, P=pressure_mpa)
    # IAPWS returns chemical potentials on a mass-specific kJ/kg basis.
    # Therefore use the specific gas constant of water, not the molar value.
    import math
    r_kj = 0.46151805
    return math.exp((sw.muw - pure.g) / (r_kj * temperature_k))


def vapor_pressure_driving_force_bar(
    hot_c: float,
    cold_c: float,
    water_activity: float = 1.0,
) -> float:
    return max(
        0.0,
        water_vapor_pressure_bar(hot_c, water_activity)
        - water_vapor_pressure_bar(cold_c, 1.0),
    )


def seawater_vapor_pressure_driving_force_bar(
    hot_c: float,
    cold_c: float,
    salinity_g_kg: float,
    pressure_mpa: float = 0.101325,
) -> float:
    activity = seawater_water_activity(hot_c, salinity_g_kg, pressure_mpa)
    return vapor_pressure_driving_force_bar(hot_c, cold_c, activity)


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
