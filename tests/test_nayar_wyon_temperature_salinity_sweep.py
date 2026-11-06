import csv

from scripts.run_nayar_wyon_temperature_salinity_sweep import run


def test_nayar_wyon_sweep_writes_complete_12_case_decomposition(tmp_path):
    manifest = run(tmp_path)

    assert manifest["row_count"] == 12
    with (tmp_path / "nayar_wyon_temperature_salinity_sweep.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))

    assert len(rows) == 12
    assert {float(row["feed_bulk_temperature_c"]) for row in rows} == {
        40.0, 50.0, 60.0, 70.0
    }
    assert {float(row["feed_reference_salinity_g_kg"]) for row in rows} == {
        15.0, 35.0, 38.0
    }
    for row in rows:
        # The seawater correction must lower the flux relative to Nayar's
        # paired pure-water reference at identical channel salinity.
        assert float(row["nayar_seawater_mass_flux_kg_m2_h"]) < float(
            row["nayar_pure_water_mass_flux_kg_m2_h"]
        )
        assert float(row["nayar_seawater_heat_flux_w_m2"]) < float(
            row["nayar_pure_water_heat_flux_w_m2"]
        )
        # The complete Nayar formulation remains below the Wyon baseline
        # for this parameter grid, as established by the initial sweep.
        assert float(row["nayar_seawater_mass_flux_kg_m2_h"]) < float(
            row["wyon_mass_flux_kg_m2_h"]
        )
        assert float(row["nayar_seawater_heat_flux_w_m2"]) < float(
            row["wyon_heat_flux_w_m2"]
        )
        for model in ("wyon", "nayar_pure_water", "nayar_seawater"):
            assert abs(float(row[f"{model}_energy_balance_residual_w_m2"])) <= 1e-7
        assert float(
            row["nayar_seawater_vs_nayar_pure_water_mass_flux_kg_m2_h_change_pct"]
        ) < 0.0
        assert "nayar_pure_water_vs_wyon_feed_interface_temperature_c_delta" in row
