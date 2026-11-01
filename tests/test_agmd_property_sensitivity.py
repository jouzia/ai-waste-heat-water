from __future__ import annotations

from scripts.agmd_property_sensitivity import build_rows


def test_predeclared_agmd_sensitivity_grid_is_complete_and_auditable() -> None:
    rows = build_rows()
    assert len(rows) == 108
    assert {row["salinity_sr_g_kg"] for row in rows} == {30.0, 35.0, 40.0}
    assert {row["cp_distillate_eval_c"] for row in rows} == {35.0, 42.5, 50.0}
    assert {row["latent_heat_eval_c"] for row in rows} == {35.0, 42.5, 50.0}
    assert {row["eta"] for row in rows} == {0.5, 0.7}
    assert {row["delta_t_c"] for row in rows} == {30.0, 50.0}
    assert all(row["cp_hot_eval_c"] == row["hot_inlet_c"] for row in rows)
    assert all(row["cp_cold_eval_c"] == 20.0 for row in rows)

    successful = [row for row in rows if row["status"] == "ok"]
    assert successful
    for row in successful:
        assert 0.0 < float(row["recovery_fraction"]) <= 1.0
        assert float(row["delta_t_h_out_c"]) >= 0.5
        assert abs(float(row["s2_residual"])) < 1e-10
        assert abs(float(row["s8_residual"])) < 1e-7
