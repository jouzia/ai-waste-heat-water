"""Presentation-safe end-to-end demo runner.

This module deliberately reports gross water production separately from
incremental/avoided/net freshwater consumption. It is not a validation layer.
"""
from pathlib import Path
from typing import Any

import yaml

from .engine import simulate
from .models import Scenario
from .thermal import heat_exergy_kwh


def load_demo_config(path: str | Path = "configs/demo.yaml") -> tuple[Scenario, float]:
    """Load the illustrative demo scenario and its ambient reference."""
    raw: dict[str, Any] = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if raw.get("mode") != "demo":
        raise ValueError("demo configuration must declare mode: demo")
    analysis = raw.pop("analysis", {})
    raw.pop("mode", None)
    raw.pop("purpose", None)
    ambient_temperature_c = float(analysis.get("ambient_temperature_c", 25.0))
    return Scenario.model_validate(raw), ambient_temperature_c


def run_demo(path: str | Path = "configs/demo.yaml") -> dict[str, Any]:
    """Run the illustrative scenario and return a presentation-ready ledger."""
    scenario, ambient_c = load_demo_config(path)
    result = simulate(scenario)

    source_exergy = heat_exergy_kwh(
        heat_kwh_th=result.heat_generated_kwh_th,
        source_temperature_c=scenario.recovery.source_temperature_c,
        ambient_temperature_c=ambient_c,
    )
    recoverable_exergy = heat_exergy_kwh(
        heat_kwh_th=result.recoverable_heat_kwh_th,
        source_temperature_c=scenario.recovery.source_temperature_c,
        ambient_temperature_c=ambient_c,
    )

    net = result.net_consumption_change_l
    if net < 0:
        interpretation = "reduced_consumption_vs_counterfactual"
    elif net > 0:
        interpretation = "additional_consumption_vs_counterfactual"
    else:
        interpretation = "neutral_vs_counterfactual"

    return {
        "status": "illustrative_demo_only",
        "scientific_claim": False,
        "assumptions": {
            "ambient_temperature_c": ambient_c,
            "source_temperature_c": scenario.recovery.source_temperature_c,
            "cold_side_temperature_c": scenario.recovery.cold_side_temperature_c,
        },
        "energy_and_heat": {
            "it_energy_kwh": result.it_energy_kwh,
            "heat_generated_kwh_th": result.heat_generated_kwh_th,
            "recoverable_heat_kwh_th": result.recoverable_heat_kwh_th,
            "source_heat_exergy_kwh": source_exergy,
            "recoverable_heat_exergy_kwh": recoverable_exergy,
        },
        "md": {
            "thermal_demand_kwh_th": result.md_thermal_demand_kwh_th,
            "latent_demand_kwh_th": result.md_latent_demand_kwh_th,
            "conductive_heat_leak_kwh_th": result.md_conductive_heat_leak_kwh_th,
            "cooling_demand_kwh_th": result.md_cooling_demand_kwh_th,
            "cooling_electricity_kwh": result.md_cooling_electricity_kwh,
            "pumping_electricity_kwh": result.pumping_electricity_kwh,
            "auxiliary_electricity_kwh": result.auxiliary_electricity_kwh,
            "heat_limited": result.heat_limited,
        },
        "water": {
            "gross_distillate_l": result.freshwater_produced_l,
            "feed_withdrawal_l": result.feed_water_withdrawal_l,
            "concentrate_discharge_l": result.concentrate_discharge_l,
            "direct_cooling_consumption_l": result.direct_cooling_consumption_l,
            "indirect_water_consumption_l": result.indirect_water_consumption_l,
            "additional_water_consumption_l": result.additional_water_consumption_l,
            "declared_avoided_freshwater_consumption_l": (
                result.avoided_freshwater_consumption_l
            ),
            "net_consumption_change_l": net,
            "interpretation": interpretation,
        },
        "accounting_note": (
            "Gross distillate is not counted as avoided freshwater consumption "
            "unless a counterfactual displacement is explicitly declared."
        ),
    }
