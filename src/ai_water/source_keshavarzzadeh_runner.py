"""Source-compatible axial counter-current DCMD runner.

The runner implements the published Keshavarzzadeh et al. (2020) control-volume
structure (Eqs. 9-18): mass balances, enthalpy balances, membrane conduction,
and source Nusselt correlation. The paper does not publish a complete numerical
property table/enthalpy closure in the displayed equations, so this module
makes the property closure explicit instead of silently inventing one.

It is a source-structure reproduction, not an experimental validation claim.
Primary-source observations must be extracted and compared only after the
operating conditions and property assumptions are frozen.
"""

from dataclasses import dataclass
import math

from .channel_transport import (
    keshavarzzadeh_dimensionless_position,
    keshavarzzadeh_nusselt,
)
from .source_keshavarzzadeh import (
    source_membrane_conductivity_w_m_k,
    source_membrane_flux_coefficient,
    source_water_activity_from_molar_nacl,
    source_saturation_pressure_pa,
)


@dataclass(frozen=True)
class SourceRunnerConfig:
    membrane_thickness_m: float
    pore_radius_m: float
    porosity: float
    tortuosity: float
    channel_area_m2: float
    membrane_area_m2: float
    cells: int
    channel_width_m: float = 0.007
    channel_length_m: float = 0.055
    pressure_pa: float = 101325.0
    source_pd_exponent: float = 2.072
    gamma: float = -0.3
    relaxation: float = 0.35
    interface_iterations: int = 200
    shooting_iterations: int = 80
    shooting_tolerance_k: float = 1e-6


@dataclass(frozen=True)
class SourceCellResult:
    axial_position_m: float
    feed_bulk_temperature_c: float
    permeate_bulk_temperature_c: float
    feed_interface_temperature_c: float
    permeate_interface_temperature_c: float
    feed_mass_flow_kg_s: float
    permeate_mass_flow_kg_s: float
    flux_kg_m2_s: float
    membrane_heat_flux_w_m2: float
    feed_heat_transfer_coefficient_w_m2_k: float
    permeate_heat_transfer_coefficient_w_m2_k: float
    feed_salinity_mol_l: float


@dataclass(frozen=True)
class SourceRunnerResult:
    cells: tuple[SourceCellResult, ...]
    feed_outlet_temperature_c: float
    permeate_outlet_temperature_c: float
    feed_outlet_mass_flow_kg_s: float
    permeate_outlet_mass_flow_kg_s: float
    total_flux_kg_m2_s_m2: float
    total_distillate_kg_s: float
    converged: bool
    permeate_inlet_temperature_c: float
    shooting_residual_k: float = 0.0


def source_vapor_pressure_pa(
    *,
    temperature_c: float,
    nacl_molarity_mol_l: float,
) -> float:
    """Source Eq. 7: activity-adjusted feed vapor pressure."""
    if nacl_molarity_mol_l < 0:
        raise ValueError("NaCl molarity must be non-negative")
    activity = source_water_activity_from_molar_nacl(nacl_molarity_mol_l)
    return activity * source_saturation_pressure_pa(temperature_c)


def source_pure_vapor_pressure_pa(temperature_c: float) -> float:
    """Source Eq. 5: pure-water saturation pressure."""
    return source_saturation_pressure_pa(temperature_c)


def source_membrane_flux_kg_m2_s(
    *,
    feed_interface_temperature_c: float,
    permeate_interface_temperature_c: float,
    feed_nacl_molarity_mol_l: float,
    config: SourceRunnerConfig,
) -> float:
    """Evaluate source Eq. 1 using source Eq. 2 membrane coefficient."""
    tf_k = feed_interface_temperature_c + 273.15
    tp_k = permeate_interface_temperature_c + 273.15
    if tf_k <= 0 or tp_k <= 0:
        raise ValueError("interface temperatures must be above absolute zero")
    membrane_k = 0.5 * (tf_k + tp_k)
    coefficient = source_membrane_flux_coefficient(
        temperature_k=membrane_k,
        pore_radius_m=config.pore_radius_m,
        thickness_m=config.membrane_thickness_m,
        porosity=config.porosity,
        tortuosity=config.tortuosity,
        atmospheric_pressure_pa=config.pressure_pa,
    )
    dp_pa = (
        source_vapor_pressure_pa(
            temperature_c=feed_interface_temperature_c,
            nacl_molarity_mol_l=feed_nacl_molarity_mol_l,
        )
        - source_pure_vapor_pressure_pa(
            temperature_c=permeate_interface_temperature_c
        )
    )
    return max(0.0, coefficient * dp_pa)


def source_membrane_conductivity(
    *,
    membrane_temperature_c: float,
    porosity: float,
) -> float:
    """Source Eqs. 19-21; conductivity in W m-1 K-1."""
    return source_membrane_conductivity_w_m_k(
        temperature_k=membrane_temperature_c + 273.15,
        porosity=porosity,
    )


def validate_source_config(config: SourceRunnerConfig) -> None:
    """Validate geometry and numerical controls."""
    if config.membrane_thickness_m <= 0:
        raise ValueError("membrane thickness must be positive")
    if config.pore_radius_m <= 0:
        raise ValueError("pore radius must be positive")
    if not 0 < config.porosity <= 1:
        raise ValueError("porosity must be in (0,1]")
    if config.tortuosity <= 0:
        raise ValueError("tortuosity must be positive")
    if config.channel_area_m2 <= 0 or config.membrane_area_m2 <= 0:
        raise ValueError("areas must be positive")
    if config.channel_width_m <= 0 or config.channel_length_m <= 0:
        raise ValueError("channel dimensions must be positive")
    if config.cells <= 0:
        raise ValueError("cells must be positive")
    if config.pressure_pa <= 0:
        raise ValueError("pressure must be positive")
    if not 0 < config.relaxation <= 1:
        raise ValueError("relaxation must be in (0,1]")
    if config.interface_iterations <= 0 or config.shooting_iterations <= 0:
        raise ValueError("iteration counts must be positive")


def source_cell_area(config: SourceRunnerConfig) -> float:
    validate_source_config(config)
    return config.membrane_area_m2 / config.cells


def _water_cp_j_kg_k(temperature_c: float) -> float:
    """Explicit liquid-water cp closure used when source tables are absent.

    This is a numerical property closure, not a published Keshavarzzadeh
    correlation. The closure is intentionally isolated so it can be replaced
    by a source-matched property package when primary supporting data are found.
    """
    if not -20 <= temperature_c <= 150:
        raise ValueError("temperature outside supported water cp closure")
    return 4180.0 + 0.3 * (temperature_c - 20.0)


def _water_density_kg_m3(temperature_c: float) -> float:
    """Approximate liquid-water density for hydraulic Reynolds calculations."""
    if not 0 <= temperature_c <= 100:
        raise ValueError("temperature outside supported density closure")
    t = temperature_c
    return 1000.0 * (
        1.0
        - ((t + 288.9414) / (508929.2 * (t + 68.12963))) * (t - 3.9863) ** 2
    )


def _water_viscosity_pa_s(temperature_c: float) -> float:
    """Vogel-type dynamic-viscosity closure, isolated from source equations."""
    t = temperature_c + 273.15
    return 2.414e-5 * 10.0 ** (247.8 / (t - 140.0))


def _water_conductivity_w_m_k(temperature_c: float) -> float:
    """Smooth engineering closure for liquid-water conductivity."""
    return 0.561 + 0.0019 * (temperature_c - 20.0) - 3.5e-6 * (
        temperature_c - 20.0
    ) ** 2


def _liquid_enthalpy_j_kg(temperature_c: float) -> float:
    """Reference-independent liquid enthalpy from the explicit cp closure."""
    return _water_cp_j_kg_k(temperature_c) * temperature_c


def _latent_heat_j_kg(temperature_c: float) -> float:
    """Engineering latent-heat closure over the DCMD temperature range."""
    if not 0 <= temperature_c <= 100:
        raise ValueError("latent-heat closure requires 0-100 C")
    return 2_500_900.0 - 2365.0 * temperature_c


def _vapor_enthalpy_j_kg(temperature_c: float) -> float:
    """Source Eq. 13/14 structure: h_v = h_f - h_fg."""
    return _liquid_enthalpy_j_kg(temperature_c) - _latent_heat_j_kg(
        temperature_c
    )


def _source_hydraulic_properties(temperature_c: float) -> tuple[float, float, float]:
    return (
        _water_density_kg_m3(temperature_c),
        _water_viscosity_pa_s(temperature_c),
        _water_conductivity_w_m_k(temperature_c),
    )


def _source_htc(
    *,
    temperature_c: float,
    mass_flow_kg_s: float,
    config: SourceRunnerConfig,
    axial_position_m: float,
) -> float:
    rho, mu, k = _source_hydraulic_properties(temperature_c)
    velocity = mass_flow_kg_s / (rho * config.channel_area_m2)
    re_sqrt_a = rho * velocity * math.sqrt(config.channel_area_m2) / mu
    pr = _water_cp_j_kg_k(temperature_c) * mu / k
    z_star = keshavarzzadeh_dimensionless_position(
        axial_position_m=max(axial_position_m, config.channel_length_m / config.cells / 2.0),
        cross_section_area_m2=config.channel_area_m2,
        reynolds_sqrt_area=re_sqrt_a,
        prandtl=pr,
    )
    aspect_ratio = min(
        config.channel_width_m,
        config.channel_area_m2 / config.channel_width_m,
    ) / max(
        config.channel_width_m,
        config.channel_area_m2 / config.channel_width_m,
    )
    nu = keshavarzzadeh_nusselt(
        reynolds_sqrt_area=re_sqrt_a,
        prandtl=pr,
        z_star=z_star,
        aspect_ratio=aspect_ratio,
        gamma=config.gamma,
    )
    hydraulic_diameter = 4.0 * config.channel_area_m2 / (
        2.0 * (config.channel_width_m + config.channel_area_m2 / config.channel_width_m)
    )
    return nu * k / hydraulic_diameter


def _solve_interfaces(
    *,
    feed_bulk_c: float,
    permeate_bulk_c: float,
    feed_mass_flow_kg_s: float,
    permeate_mass_flow_kg_s: float,
    feed_salinity_mol_l: float,
    config: SourceRunnerConfig,
    axial_position_m: float,
) -> tuple[float, float, float, float, float, float]:
    """Solve Eqs. 17-18 and membrane conduction by damped fixed point."""
    if feed_bulk_c <= permeate_bulk_c:
        raise ValueError("feed bulk temperature must exceed permeate bulk temperature")

    ht_f = _source_htc(
        temperature_c=feed_bulk_c,
        mass_flow_kg_s=feed_mass_flow_kg_s,
        config=config,
        axial_position_m=axial_position_m,
    )
    ht_p = _source_htc(
        temperature_c=permeate_bulk_c,
        mass_flow_kg_s=permeate_mass_flow_kg_s,
        config=config,
        axial_position_m=axial_position_m,
    )

    tfm = feed_bulk_c - 1.0
    tpm = permeate_bulk_c + 1.0
    for _ in range(config.interface_iterations):
        tm = 0.5 * (tfm + tpm)
        km = source_membrane_conductivity(
            membrane_temperature_c=tm,
            porosity=config.porosity,
        )
        qm = km * (tfm - tpm) / config.membrane_thickness_m
        j = source_membrane_flux_kg_m2_s(
            feed_interface_temperature_c=tfm,
            permeate_interface_temperature_c=tpm,
            feed_nacl_molarity_mol_l=feed_salinity_mol_l,
            config=config,
        )
        hfg_f = _latent_heat_j_kg(tfm)
        hfg_p = _latent_heat_j_kg(tpm)
        hf_m = _liquid_enthalpy_j_kg(tfm)
        hp_m = _liquid_enthalpy_j_kg(tpm)
        hf_b = _liquid_enthalpy_j_kg(feed_bulk_c)
        hp_b = _liquid_enthalpy_j_kg(permeate_bulk_c)
        qf = j * (hfg_f + hf_m - hf_b) + qm
        qp = j * (hfg_p + hp_m - hp_b) + qm
        target_f = feed_bulk_c - qf / ht_f
        target_p = permeate_bulk_c + qp / ht_p
        new_f = (1.0 - config.relaxation) * tfm + config.relaxation * target_f
        new_p = (1.0 - config.relaxation) * tpm + config.relaxation * target_p
        if abs(new_f - tfm) < 1e-8 and abs(new_p - tpm) < 1e-8:
            tfm, tpm = new_f, new_p
            break
        tfm, tpm = new_f, new_p

    km = source_membrane_conductivity(
        membrane_temperature_c=0.5 * (tfm + tpm),
        porosity=config.porosity,
    )
    qm = km * (tfm - tpm) / config.membrane_thickness_m
    j = source_membrane_flux_kg_m2_s(
        feed_interface_temperature_c=tfm,
        permeate_interface_temperature_c=tpm,
        feed_nacl_molarity_mol_l=feed_salinity_mol_l,
        config=config,
    )
    return tfm, tpm, j, qm, ht_f, ht_p


def _integrate(
    *,
    feed_inlet_temperature_c: float,
    permeate_outlet_guess_c: float,
    feed_mass_flow_kg_s: float,
    permeate_mass_flow_kg_s: float,
    feed_salinity_mol_l: float,
    config: SourceRunnerConfig,
) -> tuple[SourceRunnerResult, float]:
    """Integrate from feed inlet toward feed outlet.

    The permeate stream is counter-current, so its mass-flow magnitude decreases
    with increasing feed-flow coordinate. The shooting variable is the unknown
    permeate temperature at the feed inlet end.
    """
    dx = config.channel_length_m / config.cells
    area = source_cell_area(config)
    mf = feed_mass_flow_kg_s
    mp = permeate_mass_flow_kg_s
    tfb = feed_inlet_temperature_c
    tpb = permeate_outlet_guess_c
    cells: list[SourceCellResult] = []

    for i in range(config.cells):
        z = (i + 0.5) * dx
        tfm, tpm, j, qm, ht_f, ht_p = _solve_interfaces(
            feed_bulk_c=tfb,
            permeate_bulk_c=tpb,
            feed_mass_flow_kg_s=max(mf, 1e-12),
            permeate_mass_flow_kg_s=max(mp, 1e-12),
            feed_salinity_mol_l=feed_salinity_mol_l,
            config=config,
            axial_position_m=z,
        )
        hfg_f = _latent_heat_j_kg(tfm)
        hfg_p = _latent_heat_j_kg(tpm)
        hf_m = _liquid_enthalpy_j_kg(tfm)
        hp_m = _liquid_enthalpy_j_kg(tpm)
        hf_b = _liquid_enthalpy_j_kg(tfb)
        hp_b = _liquid_enthalpy_j_kg(tpb)
        qf = j * (hfg_f + hf_m - hf_b) + qm
        qp = j * (hfg_p + hp_m - hp_b) + qm

        dm = max(0.0, j * area)
        mf_new = max(mf - dm, 1e-12)
        mp_new = max(mp - dm, 1e-12)
        hf_new = hf_b - qf * area / max(mf, 1e-12)
        hp_new = hp_b - qp * area / max(mp, 1e-12)

        # Invert the monotone liquid enthalpy closure.
        tf_new = hf_new / 4180.0
        tp_new = hp_new / 4180.0
        tfb = tf_new
        tpb = tp_new
        mf, mp = mf_new, mp_new
        cells.append(
            SourceCellResult(
                axial_position_m=z,
                feed_bulk_temperature_c=tf_new,
                permeate_bulk_temperature_c=tp_new,
                feed_interface_temperature_c=tfm,
                permeate_interface_temperature_c=tpm,
                feed_mass_flow_kg_s=mf_new,
                permeate_mass_flow_kg_s=mp_new,
                flux_kg_m2_s=j,
                membrane_heat_flux_w_m2=qm,
                feed_heat_transfer_coefficient_w_m2_k=ht_f,
                permeate_heat_transfer_coefficient_w_m2_k=ht_p,
                feed_salinity_mol_l=feed_salinity_mol_l,
            )
        )

    result = SourceRunnerResult(
        cells=tuple(cells),
        feed_outlet_temperature_c=tfb,
        # tpb is the temperature at the feed-inlet end; this is the physical
        # permeate outlet for the counter-current arrangement.
        permeate_outlet_temperature_c=permeate_outlet_guess_c,
        feed_outlet_mass_flow_kg_s=mf,
        permeate_outlet_mass_flow_kg_s=mp,
        total_flux_kg_m2_s_m2=sum(c.flux_kg_m2_s * area for c in cells),
        total_distillate_kg_s=sum(c.flux_kg_m2_s * area for c in cells),
        converged=True,
        permeate_inlet_temperature_c=permeate_outlet_guess_c,
        shooting_residual_k=tpb - permeate_inlet_temperature_c,
    )
    return result, tpb


def run_source_countercurrent(
    *,
    feed_inlet_temperature_c: float,
    permeate_inlet_temperature_c: float,
    feed_flow_m3_s: float,
    permeate_flow_m3_s: float,
    feed_salinity_mol_l: float,
    config: SourceRunnerConfig,
) -> SourceRunnerResult:
    """Run the source-form counter-current model with a temperature shooting solve.

    The specified permeate inlet is at the feed outlet side. The unknown
    permeate outlet temperature at the feed inlet side is solved by bisection.
    """
    validate_source_config(config)
    if feed_inlet_temperature_c <= permeate_inlet_temperature_c:
        raise ValueError("feed inlet temperature must exceed permeate inlet temperature")
    if feed_flow_m3_s <= 0 or permeate_flow_m3_s <= 0:
        raise ValueError("flow rates must be positive")
    if feed_salinity_mol_l < 0:
        raise ValueError("salinity cannot be negative")

    rho_f = _water_density_kg_m3(feed_inlet_temperature_c)
    rho_p = _water_density_kg_m3(permeate_inlet_temperature_c)
    mf0 = rho_f * feed_flow_m3_s
    mp0 = rho_p * permeate_flow_m3_s

    low = permeate_inlet_temperature_c
    high = feed_inlet_temperature_c - 1e-6
    best: SourceRunnerResult | None = None

    for _ in range(config.shooting_iterations):
        guess = 0.5 * (low + high)
        result, _permeate_feed_end = _integrate(
            feed_inlet_temperature_c=feed_inlet_temperature_c,
            permeate_outlet_guess_c=guess,
            feed_mass_flow_kg_s=mf0,
            permeate_mass_flow_kg_s=mp0,
            feed_salinity_mol_l=feed_salinity_mol_l,
            config=config,
        )
        residual = result.permeate_outlet_temperature_c - permeate_inlet_temperature_c
        best = result
        if abs(residual) <= config.shooting_tolerance_k:
            return result
        if residual > 0:
            high = guess
        else:
            low = guess

    if best is None:
        raise RuntimeError("source counter-current shooting produced no solution")
    return SourceRunnerResult(
        cells=best.cells,
        feed_outlet_temperature_c=best.feed_outlet_temperature_c,
        permeate_outlet_temperature_c=best.permeate_outlet_temperature_c,
        feed_outlet_mass_flow_kg_s=best.feed_outlet_mass_flow_kg_s,
        permeate_outlet_mass_flow_kg_s=best.permeate_outlet_mass_flow_kg_s,
        total_flux_kg_m2_s_m2=best.total_flux_kg_m2_s_m2,
        total_distillate_kg_s=best.total_distillate_kg_s,
        converged=False,
        permeate_inlet_temperature_c=best.permeate_inlet_temperature_c,
        shooting_residual_k=best.shooting_residual_k,
    )
