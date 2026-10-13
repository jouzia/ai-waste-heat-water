import importlib.util
import sys
from pathlib import Path


def _load_evaluator():
    path = Path(__file__).resolve().parents[1] / "scripts" / "evaluate_ali_steady_state_flux_holdout.py"
    spec = importlib.util.spec_from_file_location("ali_flux_holdout_evaluator", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load evaluator from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_evaluator = _load_evaluator()


def _synthetic_rows():
    rows = []
    for flow in (50.0, 100.0, 200.0, 300.0):
        for temp in (50.0, 60.0, 70.0, 80.0):
            rows.append({
                "observation_id": f"synthetic-{flow}-{temp}",
                "workbook_filename": "S1_Data.xlsx",
                "worksheet_name": f"Q={flow:g}",
                "excel_row_1based": "5",
                "nominal_flow_l_h": str(flow),
                "hot_inlet_temperature_c": str(temp),
                "hot_outlet_temperature_c": str(temp - 10.0),
                "cold_inlet_temperature_c": "25.0",
                "cold_outlet_temperature_c": str(temp - 20.0),
                "mass_flux_kg_m2_h": str(0.05 + flow / 1000.0 + temp / 1000.0),
                "tds_hot_ppm_raw": "650.0",
            })
    return rows


def test_flux_law_diagnostic_holds_out_entire_300_l_h_flow() -> None:
    _, predictions, summary = _evaluator.fit_and_score(
        _synthetic_rows(), "reported_0p5_percent_feed_salinity"
    )
    assert len(predictions) == 16
    assert summary["training_metrics"]["n"] == 12
    assert summary["held_out_metrics"]["n"] == 4
    assert summary["held_out_flow_l_h"] == 300.0
    assert summary["fitted_permeance_kg_m2_h_bar"] > 0
