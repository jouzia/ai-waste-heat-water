"""Mass-weighted stream enthalpy updates for the opt-in Wyon channel mode."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from .wyon_2025_enthalpy import (
    wyon_specific_enthalpy_j_kg,
    wyon_temperature_from_specific_enthalpy_c,
)


@dataclass(frozen=True)
class StreamEnthalpyStep:
    """One stream's inlet/outlet state and enthalpy-balance residual."""

    outlet_temperature_c: float
    inlet_specific_enthalpy_j_kg: float
    outlet_specific_enthalpy_j_kg: float
    residual_w: float


def advance_wyon_stream_enthalpy(
    *,
    inlet_temperature_c: float,
    inlet_mass_flow_kg_h: float,
    outlet_mass_flow_kg_h: float,
    heat_transfer_w: float,
    salinity_in_g_kg: float,
    salinity_out_g_kg: float,
    direction: str,
) -> StreamEnthalpyStep:
    """Advance a stream using Wyon Eq. (18) and mass-weighted enthalpy rates.

    direction='feed' removes heat from the feed stream; direction='permeate'
    adds the same total heat rate to the permeate stream. Mass flow rates are
    kg/h, specific enthalpies J/kg, and heat transfer W. The Wyon convention
    is Q = H_f,in - H_f,out = H_p,out - H_p,in. Do not add a separate
    transferred-vapour enthalpy term to this same convention.
    """
    values = (
        inlet_temperature_c,
        inlet_mass_flow_kg_h,
        outlet_mass_flow_kg_h,
        heat_transfer_w,
        salinity_in_g_kg,
        salinity_out_g_kg,
    )
    if not all(isfinite(value) for value in values):
        raise ValueError("stream enthalpy inputs must be finite")
    if inlet_mass_flow_kg_h <= 0 or outlet_mass_flow_kg_h <= 0:
        raise ValueError("stream inlet and outlet mass flow rates must be positive")
    if heat_transfer_w < 0:
        raise ValueError("heat_transfer_w must be non-negative")
    if direction not in {"feed", "permeate"}:
        raise ValueError("direction must be 'feed' or 'permeate'")

    h_in = wyon_specific_enthalpy_j_kg(
        inlet_temperature_c, salinity_in_g_kg
    )
    q_j_h = heat_transfer_w * 3600.0
    signed_q_j_h = -q_j_h if direction == "feed" else q_j_h
    h_out = (
        inlet_mass_flow_kg_h * h_in + signed_q_j_h
    ) / outlet_mass_flow_kg_h
    temperature_out = wyon_temperature_from_specific_enthalpy_c(
        h_out, salinity_out_g_kg
    )
    residual_j_h = (
        outlet_mass_flow_kg_h * h_out
        - inlet_mass_flow_kg_h * h_in
        - signed_q_j_h
    )
    return StreamEnthalpyStep(
        outlet_temperature_c=temperature_out,
        inlet_specific_enthalpy_j_kg=h_in,
        outlet_specific_enthalpy_j_kg=h_out,
        residual_w=residual_j_h / 3600.0,
    )
