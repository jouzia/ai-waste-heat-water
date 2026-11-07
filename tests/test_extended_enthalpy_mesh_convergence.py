import csv
import json

from scripts.run_extended_enthalpy_mesh_convergence import run


def test_extended_enthalpy_mesh_grid_is_complete_and_auditable(tmp_path):
    manifest = run(tmp_path)

    assert manifest["experiment_id"] == "DCMD-ENTHALPY-EXTENDED-MESH-GRID-2026-11-07"
    assert manifest["row_count"] == 96
    assert manifest["case_count"] == 12
    assert manifest["cell_counts"] == [10, 20, 40, 80]
    assert manifest["reference_mesh_cells"] == 80
    assert manifest["case_temperatures_c"] == [40.0, 50.0, 60.0, 70.0]
    assert manifest["reference_salinity_g_kg"] == [15.0, 35.0, 38.0]
    assert set(manifest["modes"]) == {"sensible_cp", "wyon_enthalpy"}

    csv_path = tmp_path / "extended_enthalpy_mesh_convergence.csv"
    summary_path = tmp_path / "extended_mesh_convergence_summary.json"
    with csv_path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 96
    keys = {
        (row["case_id"], row["energy_balance_mode"], int(row["cells"]))
        for row in rows
    }
    assert len(keys) == 96

    for row in rows:
        assert float(row["freshwater_produced_kg"]) > 0
        assert float(row["hot_side_thermal_demand_kwh_th"]) > 0
        assert float(row["feed_out_mass_kg_h"]) < 600.0
        assert float(row["permeate_out_mass_kg_h"]) > 600.0
        assert row["feed_out_temperature_c_relative_delta_vs_80_pct"] == ""
        assert row["permeate_out_temperature_c_relative_delta_vs_80_pct"] == ""
        if int(row["cells"]) == 80:
            assert abs(float(row["feed_out_temperature_c_delta_vs_80"])) < 1e-12
            assert abs(float(row["freshwater_produced_kg_delta_vs_80"])) < 1e-12
        if row["energy_balance_mode"] == "wyon_enthalpy":
            assert abs(float(row["global_wyon_enthalpy_residual_w"])) < 1e-5
            assert float(row["max_abs_combined_cell_residual_w"]) < 1e-7
        else:
            assert row["max_abs_combined_cell_residual_w"] == ""

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert len(summary) == 72
    assert all(item["reference_cells"] == 80 for item in summary)
    saved_manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert saved_manifest["files"]["extended_enthalpy_mesh_convergence.csv"]
    assert saved_manifest["files"]["extended_mesh_convergence_summary.json"]
