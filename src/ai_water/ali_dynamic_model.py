"""Lumped dynamic DCMD model reconstructed from Ali et al. (2020).

This is an equation-level reconstruction, not an assertion of exact source-code
reproduction. It uses the published dynamic outlet-temperature and mass-rate
equations, IAPWS95 pure-water properties, and a dimensionally consistent
series-resistance form for the transition-regime membrane coefficient. The
paper's printed transition expression and incomplete property provenance are
documented in docs/ALI_2020_MODEL_RECONSTRUCTION.md.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from iapws import IAPWS95
from scipy.integrate import solve_ivp

R_UNIVERSAL_J_MOL_K = 8.314462618
M_WATER_KG_MOL = 0.01801528
K_BOLTZMANN_J_K = 1.380649e-23
WATER_MOLECULE_DIAMETER_M = 2.641e-10
ATMOSPHERIC_PRESSURE_PA = 101_325.0

PUBLISHED_FLOS_LUMPED = {
    50: 0.077,
    100: 0.11,
    200: 0.10,
    300: 0.17,
}


@dataclass(frozen=True)
class AliDynamicConfig:
    membrane_area_m2: float = 10.0
    membrane_thickness_m: float = 230e-6
    membrane_porosity: float = 0.8
    membrane_tortuosity: float = 2.0
    pore_radius_m: float = 0.1e-6
    membrane_solid_conductivity_w_m_k: float = 0.2
    pore_gas_conductivity_w_m_k: float = 0.026
    channel_length_m: float = 14.0
    channel_width_m: float = 0.7
    channel_gap_m: float = 0.002
    salinity_mass_fraction: float = 0.005
    room_temperature_c: float = 25.0
    reference_temperature_c: float = 25.0
    interface_tolerance_k: float = 1e-7
    max_interface_iterations: int = 100
    max_step_s: float = 10.0
    relative_tolerance: float = 1e-6
    absolute_tolerance_temperature_k: float = 1e-5
    absolute_tolerance_mass_rate_kg_s: float = 1e-10
    absolute_tolerance_mass_kg: float = 1e-7

    @property
    def channel_volume_m3(self) -> float:
        return self.channel_length_m * self.channel_width_m * self.channel_gap_m

    @property
    def membrane_conduction_w_m2_k(self) -> float:
        eps = self.membrane_porosity
        return (
            (1.0 - eps) * self.membrane_solid_conductivity_w_m_k
            + eps * self.pore_gas_conductivity_w_m_k
        ) / self.membrane_thickness_m


@dataclass(frozen=True)
class WaterProperties:
    density_kg_m3: float
    heat_capacity_j_kg_k: float
    viscosity_pa_s: float
    conductivity_w_m_k: float


@dataclass(frozen=True)
class InterfaceState:
    hot_membrane_k: float
    cold_membrane_k: float
    bulk_hot_k: float
    bulk_cold_k: float
    mass_flux_kg_m2_s: float
    membrane_coefficient_s_m: float
    vapor_enthalpy_j_kg: float
    hot_heat_transfer_w_m2_k: float
    cold_heat_transfer_w_m2_k: float
    membrane_heat_transfer_w_m2_k: float
    beta_hot_pa_k: float
    beta_cold_pa_k: float
    a_hot: float
    a_cold: float
    b_hot: float
    b_cold: float
    c_hot_m2_k_w: float
    c_cold_m2_k_w: float
    iterations: int


@dataclass(frozen=True)
class AliDynamicResult:
    time_min: np.ndarray
    hot_inlet_c: np.ndarray
    cold_inlet_c: np.ndarray
    hot_outlet_c: np.ndarray
    cold_outlet_c: np.ndarray
    mass_rate_kg_h: np.ndarray
    accumulated_mass_kg: np.ndarray
    membrane_flux_kg_m2_h: np.ndarray
    hot_membrane_c: np.ndarray
    cold_membrane_c: np.ndarray
    solver_success: bool
    solver_message: str


def water_properties(temperature_k: float) -> WaterProperties:
    """Return IAPWS95 pure-water properties at 0.101325 MPa.

    IAPWS95 reports cp in kJ/(kg K); convert it to J/(kg K). This is a
    documented reconstruction closure, not a claim that the original paper
    used exactly the same property implementation.
    """
    if not math.isfinite(temperature_k) or not 273.15 <= temperature_k <= 373.15:
        raise ValueError("water-property temperature must be in 273.15–373.15 K")
    state = IAPWS95(T=temperature_k, P=0.101325)
    return WaterProperties(
        density_kg_m3=float(state.rho),
        heat_capacity_j_kg_k=float(state.cp) * 1000.0,
        viscosity_pa_s=float(state.mu),
        conductivity_w_m_k=float(state.k),
    )


def vapor_enthalpy_j_kg(temperature_k: float) -> float:
    """Ali Appendix B correlation, interpreted as kJ/kg and converted to J/kg."""
    value_kj_kg = (
        1850.7 + 2.8273 * temperature_k - 1.6e-3 * temperature_k**2
    )
    return value_kj_kg * 1000.0


def vapor_pressures_pa(
    hot_membrane_k: float,
    cold_membrane_k: float,
    salinity_mass_fraction: float,
) -> tuple[float, float]:
    """Ali Appendix B Antoine/activity expression; temperatures are absolute K."""
    if not 0 <= salinity_mass_fraction < 1:
        raise ValueError("salinity mass fraction must be in [0,1)")
    for temperature in (hot_membrane_k, cold_membrane_k):
        if temperature <= 45.0:
            raise ValueError("Ali Antoine correlation requires T_K > 45")
    hot_pure = math.exp(23.238 - 3841.0 / (hot_membrane_k - 45.0))
    cold_pure = math.exp(23.238 - 3841.0 / (cold_membrane_k - 45.0))
    activity = (1.0 - salinity_mass_fraction) * (
        1.0 - 0.5 * salinity_mass_fraction
        - 10.0 * salinity_mass_fraction**2
    )
    return hot_pure * activity, cold_pure


def pressure_diffusivity_pa_m2_s(temperature_k: float) -> float:
    """Engineering closure for P*D; source provenance must remain explicit.

    This power-law is used in MD literature but is not fully specified in the
    Ali article's main text. It is therefore a reconstruction assumption.
    """
    return 1.895e-5 * temperature_k**2.072


def membrane_mass_transfer_coefficient_s_m(
    temperature_k: float, config: AliDynamicConfig
) -> tuple[float, float, str]:
    """Return membrane coefficient, Knudsen number, and selected regime.

    The transition regime uses the dimensionally consistent series-resistance
    form 1/Cm = 1/Cm_K + 1/Cm_MD. This avoids blindly evaluating the printed
    Appendix B expression whose terms appear dimensionally incompatible under
    the paper's stated P_D nomenclature.
    """
    eps = config.membrane_porosity
    tau = config.membrane_tortuosity
    delta = config.membrane_thickness_m
    radius = config.pore_radius_m
    if min(eps, tau, delta, radius, temperature_k) <= 0:
        raise ValueError("membrane transport parameters must be positive")

    mean_free_path = (
        K_BOLTZMANN_J_K * temperature_k
        / (
            math.sqrt(2.0)
            * math.pi
            * ATMOSPHERIC_PRESSURE_PA
            * WATER_MOLECULE_DIAMETER_M**2
        )
    )
    knudsen_number = (4.0 / 3.0) * mean_free_path / radius
    cm_knudsen = (
        2.0 * eps * radius / (3.0 * tau * delta)
        * math.sqrt(
            8.0 * M_WATER_KG_MOL
            / (math.pi * R_UNIVERSAL_J_MOL_K * temperature_k)
        )
    )
    pd = pressure_diffusivity_pa_m2_s(temperature_k)
    cm_molecular = (
        eps * pd * M_WATER_KG_MOL
        / (
            tau * delta * ATMOSPHERIC_PRESSURE_PA
            * R_UNIVERSAL_J_MOL_K * temperature_k
        )
    )
    if knudsen_number > 1.0:
        return cm_knudsen, knudsen_number, "knudsen"
    if knudsen_number < 0.01:
        return cm_molecular, knudsen_number, "molecular"
    coefficient = 1.0 / (1.0 / cm_knudsen + 1.0 / cm_molecular)
    return coefficient, knudsen_number, "transition_series_resistance"


def _convective_coefficient_w_m2_k(
    mass_flow_kg_s: float,
    temperature_k: float,
    config: AliDynamicConfig,
) -> float:
    props = water_properties(temperature_k)
    cross_section_m2 = config.channel_width_m * config.channel_gap_m
    hydraulic_diameter_m = (
        2.0 * config.channel_width_m * config.channel_gap_m
        / (config.channel_width_m + config.channel_gap_m)
    )
    volumetric_flow_m3_s = mass_flow_kg_s / props.density_kg_m3
    velocity_m_s = volumetric_flow_m3_s / cross_section_m2
    reynolds = (
        props.density_kg_m3 * velocity_m_s * hydraulic_diameter_m
        / props.viscosity_pa_s
    )
    prandtl = (
        props.heat_capacity_j_kg_k * props.viscosity_pa_s
        / props.conductivity_w_m_k
    )
    if reynolds <= 0 or prandtl <= 0:
        raise ValueError("Reynolds and Prandtl numbers must be positive")
    nusselt = 0.298 * reynolds**0.646 * prandtl**0.316
    return nusselt * props.conductivity_w_m_k / hydraulic_diameter_m


def interface_state(
    hot_inlet_k: float,
    hot_outlet_k: float,
    cold_inlet_k: float,
    cold_outlet_k: float,
    mass_flow_kg_s: float,
    config: AliDynamicConfig,
) -> InterfaceState:
    """Solve the source's iterative pseudo-steady membrane-interface equations."""
    if min(hot_inlet_k, hot_outlet_k, cold_inlet_k, cold_outlet_k) <= 0:
        raise ValueError("absolute temperatures must be positive")
    bulk_hot_k = math.sqrt(hot_inlet_k * hot_outlet_k)
    bulk_cold_k = math.sqrt(cold_inlet_k * cold_outlet_k)
    hf = _convective_coefficient_w_m2_k(mass_flow_kg_s, bulk_hot_k, config)
    hp = _convective_coefficient_w_m2_k(mass_flow_kg_s, bulk_cold_k, config)
    hm = config.membrane_conduction_w_m2_k
    denominator = hp * hf + hm * (hp + hf)
    a_hot = hf * (hm + hp) / denominator
    a_cold = hp * hm / denominator
    b_hot = hf * hm / denominator
    b_cold = hp * (hm + hf) / denominator
    c_hot = hp / denominator
    c_cold = hf / denominator

    hot_membrane_k = bulk_hot_k
    cold_membrane_k = bulk_cold_k
    hv = vapor_enthalpy_j_kg((hot_membrane_k + cold_membrane_k) / 2.0)
    cm = 0.0
    jw = 0.0
    iterations = 0
    for iterations in range(1, config.max_interface_iterations + 1):
        mean_membrane_k = (hot_membrane_k + cold_membrane_k) / 2.0
        cm, _, _ = membrane_mass_transfer_coefficient_s_m(mean_membrane_k, config)
        p_hot, p_cold = vapor_pressures_pa(
            hot_membrane_k, cold_membrane_k, config.salinity_mass_fraction
        )
        jw = cm * (p_hot - p_cold)
        hv = vapor_enthalpy_j_kg(mean_membrane_k)
        new_hot = (
            a_hot * bulk_hot_k + a_cold * bulk_cold_k
            - c_hot * jw * hv
        )
        new_cold = (
            b_hot * bulk_hot_k + b_cold * bulk_cold_k
            + c_cold * jw * hv
        )
        error = max(abs(new_hot - hot_membrane_k), abs(new_cold - cold_membrane_k))
        if error <= config.interface_tolerance_k:
            hot_membrane_k, cold_membrane_k = new_hot, new_cold
            break
        # Under-relaxation makes the source fixed-point iteration robust near
        # low driving force without changing the converged equations.
        hot_membrane_k = 0.5 * hot_membrane_k + 0.5 * new_hot
        cold_membrane_k = 0.5 * cold_membrane_k + 0.5 * new_cold
    else:
        raise RuntimeError("Ali membrane-interface iteration did not converge")

    mean_membrane_k = (hot_membrane_k + cold_membrane_k) / 2.0
    cm, _, _ = membrane_mass_transfer_coefficient_s_m(mean_membrane_k, config)
    p_hot, p_cold = vapor_pressures_pa(
        hot_membrane_k, cold_membrane_k, config.salinity_mass_fraction
    )
    jw = cm * (p_hot - p_cold)
    hv = vapor_enthalpy_j_kg(mean_membrane_k)
    beta_hot = p_hot * 3841.0 / (hot_membrane_k - 45.0) ** 2
    beta_cold = p_cold * 3841.0 / (cold_membrane_k - 45.0) ** 2
    return InterfaceState(
        hot_membrane_k=hot_membrane_k,
        cold_membrane_k=cold_membrane_k,
        bulk_hot_k=bulk_hot_k,
        bulk_cold_k=bulk_cold_k,
        mass_flux_kg_m2_s=jw,
        membrane_coefficient_s_m=cm,
        vapor_enthalpy_j_kg=hv,
        hot_heat_transfer_w_m2_k=hf,
        cold_heat_transfer_w_m2_k=hp,
        membrane_heat_transfer_w_m2_k=hm,
        beta_hot_pa_k=beta_hot,
        beta_cold_pa_k=beta_cold,
        a_hot=a_hot,
        a_cold=a_cold,
        b_hot=b_hot,
        b_cold=b_cold,
        c_hot_m2_k_w=c_hot,
        c_cold_m2_k_w=c_cold,
        iterations=iterations,
    )


def simulate_lumped_transient(
    *,
    time_min: list[float] | np.ndarray,
    hot_inlet_c: list[float] | np.ndarray,
    cold_inlet_c: list[float] | np.ndarray,
    nominal_flow_l_h: float,
    heat_loss_correction: float = 0.0,
    initial_hot_outlet_c: float | None = None,
    initial_cold_outlet_c: float | None = None,
    initial_accumulated_mass_kg: float = 0.0,
    config: AliDynamicConfig | None = None,
) -> AliDynamicResult:
    """Integrate the lumped source ODEs against measured inlet-temperature traces.

    The nominal flow uses the source paper's numeric kg/h convention (1 L/h
    treated as 1 kg/h). The optional initial outlet temperatures allow a
    measured-initial-state run; leaving them unset uses the paper's room-
    temperature initialization. The cumulative mass offset is explicit.
    """
    cfg = config or AliDynamicConfig()
    time_values = np.asarray(time_min, dtype=float)
    hot_values_c = np.asarray(hot_inlet_c, dtype=float)
    cold_values_c = np.asarray(cold_inlet_c, dtype=float)
    if time_values.ndim != 1 or len(time_values) < 3:
        raise ValueError("time_min must be a one-dimensional series with at least 3 points")
    if len(hot_values_c) != len(time_values) or len(cold_values_c) != len(time_values):
        raise ValueError("time and inlet-temperature arrays must have equal length")
    if (
        not np.all(np.isfinite(time_values))
        or not np.all(np.isfinite(hot_values_c))
        or not np.all(np.isfinite(cold_values_c))
    ):
        raise ValueError("time and inlet-temperature arrays must be finite")
    if np.any(np.diff(time_values) <= 0):
        raise ValueError("time_min must be strictly increasing")
    if nominal_flow_l_h <= 0:
        raise ValueError("nominal_flow_l_h must be positive")
    if not math.isfinite(heat_loss_correction) or heat_loss_correction < 0:
        raise ValueError("heat_loss_correction must be finite and non-negative")

    time_seconds = time_values * 60.0
    hot_values_k = hot_values_c + 273.15
    cold_values_k = cold_values_c + 273.15
    mass_flow_kg_s = nominal_flow_l_h / 3600.0
    reference_k = cfg.reference_temperature_c + 273.15
    room_k = cfg.room_temperature_c + 273.15
    initial_hot_k = (
        room_k if initial_hot_outlet_c is None else initial_hot_outlet_c + 273.15
    )
    initial_cold_k = (
        room_k if initial_cold_outlet_c is None else initial_cold_outlet_c + 273.15
    )
    initial_interface = interface_state(
        hot_values_k[0], initial_hot_k, cold_values_k[0], initial_cold_k,
        mass_flow_kg_s, cfg,
    )
    initial_mass_rate = initial_interface.mass_flux_kg_m2_s * cfg.membrane_area_m2
    initial_state = [
        initial_hot_k,
        initial_cold_k,
        initial_mass_rate,
        float(initial_accumulated_mass_kg),
    ]

    def input_at(t_s: float) -> tuple[float, float]:
        return (
            float(np.interp(t_s, time_seconds, hot_values_k)),
            float(np.interp(t_s, time_seconds, cold_values_k)),
        )

    def rhs(t_s: float, state: np.ndarray) -> list[float]:
        hot_out_k, cold_out_k, mass_rate_kg_s, _ = state
        hot_in_k, cold_in_k = input_at(t_s)
        interface = interface_state(
            hot_in_k, hot_out_k, cold_in_k, cold_out_k, mass_flow_kg_s, cfg
        )
        hot_props = water_properties(interface.bulk_hot_k)
        cold_props = water_properties(interface.bulk_cold_k)
        area = cfg.membrane_area_m2
        cp_hot = hot_props.heat_capacity_j_kg_k
        cp_cold = cold_props.heat_capacity_j_kg_k
        mdot = mass_flow_kg_s
        hot_heat_rate = (
            mdot * cp_hot * (hot_in_k - reference_k)
            - mdot * cp_hot * (hot_out_k - reference_k)
            - interface.membrane_heat_transfer_w_m2_k
            * area
            * (interface.hot_membrane_k - interface.cold_membrane_k)
            - interface.mass_flux_kg_m2_s * area * interface.vapor_enthalpy_j_kg
            - heat_loss_correction
            * mdot
            * cp_hot
            * (hot_in_k - hot_out_k)
        )
        cold_heat_rate = (
            mdot * cp_cold * (cold_in_k - reference_k)
            - mdot * cp_cold * (cold_out_k - reference_k)
            + interface.membrane_heat_transfer_w_m2_k
            * area
            * (interface.hot_membrane_k - interface.cold_membrane_k)
            + interface.mass_flux_kg_m2_s * area * interface.vapor_enthalpy_j_kg
        )
        d_hot_out_dt = hot_heat_rate / (
            cfg.channel_volume_m3 * hot_props.density_kg_m3 * cp_hot
        )
        d_cold_out_dt = cold_heat_rate / (
            cfg.channel_volume_m3 * cold_props.density_kg_m3 * cp_cold
        )
        denominator = (
            1.0
            + interface.membrane_coefficient_s_m
            * interface.beta_hot_pa_k
            * interface.c_hot_m2_k_w
            * interface.vapor_enthalpy_j_kg
            + interface.membrane_coefficient_s_m
            * interface.beta_cold_pa_k
            * interface.c_cold_m2_k_w
            * interface.vapor_enthalpy_j_kg
        )
        if abs(denominator) < 1e-12:
            raise RuntimeError("Ali mass-rate derivative denominator approached zero")
        d_mass_rate_dt = (
            interface.membrane_coefficient_s_m
            * area
            / denominator
            * (
                (
                    interface.beta_hot_pa_k * interface.a_hot
                    - interface.beta_cold_pa_k * interface.b_hot
                )
                * 0.5
                * math.sqrt(hot_in_k / hot_out_k)
                * d_hot_out_dt
                + (
                    interface.beta_hot_pa_k * interface.a_cold
                    - interface.beta_cold_pa_k * interface.b_cold
                )
                * 0.5
                * math.sqrt(cold_in_k / cold_out_k)
                * d_cold_out_dt
            )
        )
        return [d_hot_out_dt, d_cold_out_dt, d_mass_rate_dt, mass_rate_kg_s]

    solution = solve_ivp(
        rhs,
        (float(time_seconds[0]), float(time_seconds[-1])),
        np.asarray(initial_state, dtype=float),
        method="RK45",
        t_eval=time_seconds,
        max_step=cfg.max_step_s,
        rtol=cfg.relative_tolerance,
        atol=[
            cfg.absolute_tolerance_temperature_k,
            cfg.absolute_tolerance_temperature_k,
            cfg.absolute_tolerance_mass_rate_kg_s,
            cfg.absolute_tolerance_mass_kg,
        ],
    )
    if not solution.success:
        raise RuntimeError(f"Ali transient ODE failed: {solution.message}")

    predicted_states = solution.y.T
    fluxes: list[float] = []
    hot_membrane_c: list[float] = []
    cold_membrane_c: list[float] = []
    for index, state in enumerate(predicted_states):
        hot_in_k = hot_values_k[index]
        cold_in_k = cold_values_k[index]
        interface = interface_state(
            hot_in_k,
            float(state[0]),
            cold_in_k,
            float(state[1]),
            mass_flow_kg_s,
            cfg,
        )
        fluxes.append(interface.mass_flux_kg_m2_s * 3600.0)
        hot_membrane_c.append(interface.hot_membrane_k - 273.15)
        cold_membrane_c.append(interface.cold_membrane_k - 273.15)

    return AliDynamicResult(
        time_min=time_values.copy(),
        hot_inlet_c=hot_values_c.copy(),
        cold_inlet_c=cold_values_c.copy(),
        hot_outlet_c=predicted_states[:, 0] - 273.15,
        cold_outlet_c=predicted_states[:, 1] - 273.15,
        mass_rate_kg_h=predicted_states[:, 2] * 3600.0,
        accumulated_mass_kg=predicted_states[:, 3],
        membrane_flux_kg_m2_h=np.asarray(fluxes),
        hot_membrane_c=np.asarray(hot_membrane_c),
        cold_membrane_c=np.asarray(cold_membrane_c),
        solver_success=bool(solution.success),
        solver_message=str(solution.message),
    )
