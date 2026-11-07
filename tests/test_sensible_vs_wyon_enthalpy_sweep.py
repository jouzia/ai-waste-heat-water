import csv
import json

from scripts.run_sensible_vs_wyon_enthalpy_sweep import run

from ai_water.md_channel import ChannelConfig
from ai_water.md_channel_countercurrent import simulate_countercurrent_dcmd_channel


def test_sensible_vs_wyon_sweep_has_complete_matrix_and_auditable_manifest(tmp_path):
    manifest = run(tmp_path)

    assert manifest["row_count"] == 12
    assert manifest["experiment_id"] == (
        "SENSIBLE-VS-WYON-ENTHALPY-COUNTERCURRENT-2026-11-07"
    )
    assert (tmp_path / "manifest.json").exists()
    assert (tmp_path / "sensible_vs_wyon_enthalpy_sweep.csv").exists()

    with (tmp_path / "sensible_vs_wyon_enthalpy_sweep.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))

    assert len(rows) == 12
    assert len({row["case_id"] for row in rows}) == 12
    for row in rows:
        assert float(row["sensible_cp_freshwater_produced_kg"]) > 0
        assert float(row["wyon_enthalpy_freshwater_produced_kg"]) > 0
        assert float(row["sensible_cp_hot_side_thermal_demand_kwh_th"]) > 0
        assert float(row["wyon_enthalpy_hot_side_thermal_demand_kwh_th"]) > 0
        assert abs(float(row["wyon_enthalpy_global_wyon_enthalpy_residual_w"])) < 1e-5
        assert float(row["wyon_enthalpy_max_abs_combined_cell_residual_w"]) < 1e-8
        assert row["sensible_cp_max_abs_combined_cell_residual_w"] == ""
        assert row["sensible_cp_max_abs_feed_cell_residual_w"] == ""
        assert row["sensible_cp_max_abs_permeate_cell_residual_w"] == ""

    saved_manifest = json.loads((tmp_path / "manifest.json").read_text())
    assert saved_manifest["files"]["sensible_vs_wyon_enthalpy_sweep.csv"]


def test_sweep_changes_only_energy_balance_mode():
    base = {
        "membrane_area_m2": 0.23088,
        "membrane_permeance_kg_m2_h_bar": 100.0,
        "latent_heat_kwh_th_per_kg": 0.67,
        "membrane_thermal_conductivity_w_m_k": 0.0551,
        "membrane_thickness_m": 110e-6,
        "feed_heat_transfer_coefficient_w_m2_k": 500.0,
        "permeate_heat_transfer_coefficient_w_m2_k": 500.0,
        "feed_mass_flow_kg_h": 600.0,
        "permeate_mass_flow_kg_h": 600.0,
        "feed_cp_kj_kg_k": 4.18,
        "permeate_cp_kj_kg_k": 4.18,
        "feed_salinity_g_kg": 35.0,
        "duration_h": 1.0,
        "cells": 20,
        "flow_arrangement": "counter_current",
    }
    sensible = simulate_countercurrent_dcmd_channel(
        config=ChannelConfig(**base, energy_balance_mode="sensible_cp"),
        feed_in_temperature_c=60.0,
        permeate_in_temperature_c=20.0,
    )
    enthalpy = simulate_countercurrent_dcmd_channel(
        config=ChannelConfig(**base, energy_balance_mode="wyon_enthalpy"),
        feed_in_temperature_c=60.0,
        permeate_in_temperature_c=20.0,
    )

    assert sensible.freshwater_produced_kg > 0
    assert enthalpy.freshwater_produced_kg > 0
    assert sensible.feed_out_mass_kg_h < 600.0
    assert enthalpy.feed_out_mass_kg_h < 600.0
    assert sensible.permeate_out_mass_kg_h > 600.0
    assert enthalpy.permeate_out_mass_kg_h > 600.0
