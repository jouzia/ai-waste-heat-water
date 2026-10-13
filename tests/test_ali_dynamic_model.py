import numpy as np
import pytest

from ai_water.ali_dynamic_model import (
    AliDynamicConfig,
    interface_state,
    membrane_mass_transfer_coefficient_s_m,
    simulate_lumped_transient,
    simulate_spatial_transient,
    vapor_pressures_pa,
    water_properties,
)


def test_iapws_water_properties_are_physical_in_model_range() -> None:
    props = water_properties(323.15)
    assert 970 < props.density_kg_m3 < 1000
    assert 4000 < props.heat_capacity_j_kg_k < 4500
    assert 1e-4 < props.viscosity_pa_s < 2e-3
    assert 0.4 < props.conductivity_w_m_k < 0.8


def test_ali_vapor_pressure_is_higher_on_hot_side() -> None:
    hot, cold = vapor_pressures_pa(333.15, 298.15, 0.005)
    assert hot > cold > 0


def test_membrane_coefficient_uses_positive_series_resistance() -> None:
    coefficient, knudsen, regime = membrane_mass_transfer_coefficient_s_m(
        323.15, AliDynamicConfig()
    )
    assert coefficient > 0
    assert knudsen > 0
    assert regime in {"knudsen", "molecular", "transition_series_resistance"}


def test_interface_solver_returns_positive_flux_for_hot_feed() -> None:
    state = interface_state(
        333.15, 303.15, 298.15, 298.15, 50.0 / 3600.0, AliDynamicConfig()
    )
    assert state.mass_flux_kg_m2_s > 0
    assert state.hot_membrane_k > state.cold_membrane_k
    assert state.iterations <= 100
    assert state.membrane_coefficient_s_m > 0


def test_lumped_transient_integrates_measured_input_trace() -> None:
    times = np.linspace(0.0, 1.0, 7)
    result = simulate_lumped_transient(
        time_min=times,
        hot_inlet_c=np.full(7, 60.0),
        cold_inlet_c=np.full(7, 25.0),
        nominal_flow_l_h=50.0,
        initial_hot_outlet_c=25.0,
        initial_cold_outlet_c=25.0,
        config=AliDynamicConfig(membrane_area_m2=0.1),
    )
    assert result.solver_success
    assert np.all(np.isfinite(result.accumulated_mass_kg))
    assert result.hot_outlet_c[-1] > result.hot_outlet_c[0]
    assert result.accumulated_mass_kg[-1] > result.accumulated_mass_kg[0]
    assert result.mass_rate_kg_h.shape == times.shape


def test_lumped_transient_rejects_thermodynamically_inadmissible_outlet() -> None:
    times = np.linspace(0.0, 1.0, 7)
    with pytest.raises(RuntimeError, match="outside the inlet-temperature envelope"):
        simulate_lumped_transient(
            time_min=times,
            hot_inlet_c=np.full(7, 60.0),
            cold_inlet_c=np.full(7, 25.0),
            nominal_flow_l_h=50.0,
            initial_hot_outlet_c=25.0,
            initial_cold_outlet_c=25.0,
        )


def test_lumped_transient_rejects_nonmonotonic_time() -> None:
    with pytest.raises(ValueError, match="strictly increasing"):
        simulate_lumped_transient(
            time_min=[0.0, 1.0, 0.5],
            hot_inlet_c=[60.0, 60.0, 60.0],
            cold_inlet_c=[25.0, 25.0, 25.0],
            nominal_flow_l_h=50.0,
        )



def test_spatial_transient_rejects_source_scale_low_flow_envelope_violation() -> None:
    times = np.linspace(0.0, 1.0, 7)
    with pytest.raises(RuntimeError, match="outside the inlet-temperature envelope"):
        simulate_spatial_transient(
            time_min=times,
            hot_inlet_c=np.full(7, 60.0),
            cold_inlet_c=np.full(7, 25.0),
            nominal_flow_l_h=50.0,
            n_cells=10,
            initial_hot_outlet_c=25.0,
            initial_cold_outlet_c=25.0,
        )


def test_spatial_transient_stays_physical_for_reduced_area() -> None:
    times = np.linspace(0.0, 1.0, 7)
    result = simulate_spatial_transient(
        time_min=times,
        hot_inlet_c=np.full(7, 60.0),
        cold_inlet_c=np.full(7, 25.0),
        nominal_flow_l_h=50.0,
        n_cells=10,
        initial_hot_outlet_c=25.0,
        initial_cold_outlet_c=25.0,
        config=AliDynamicConfig(membrane_area_m2=0.1),
    )
    assert result.solver_success
    assert np.all(np.isfinite(result.accumulated_mass_kg))
    assert result.accumulated_mass_kg[-1] > result.accumulated_mass_kg[0]
    assert np.all(result.hot_outlet_c >= 24.0)
    assert np.all(result.cold_outlet_c <= 61.0)
