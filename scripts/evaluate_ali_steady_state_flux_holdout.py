"""Evaluate the reduced vapor-pressure flux law on Ali et al. (2020) steady-state data.

This is a calibration/held-out-flow diagnostic for the flux submodel only.
It is not independent validation of the complete coupled water/energy model.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

from ai_water.md import (
    interface_temperatures,
    seawater_water_activity,
    vapor_pressure_driving_force_bar,
)

SOURCE_DOI = "10.1371/journal.pone.0230207"
TRAIN_FLOWS_L_H = (50.0, 100.0, 200.0)
HELD_OUT_FLOW_L_H = 300.0
FIXED_TPC = 0.8
SALINITY_CASES = {
    "reported_0p5_percent_feed_salinity": "Use the article's stated 0.5% feed salinity as 5 g/kg.",
    "measured_TDS_E_proxy": "Use the S1 TDS_E column (ppm/1000) as an alternative salinity proxy; source discrepancy remains unresolved.",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_float(row: dict[str, str], key: str) -> float:
    try:
        value = float(row[key])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Missing or nonnumeric source field {key!r}: {row}") from exc
    if not math.isfinite(value):
        raise ValueError(f"Non-finite source field {key!r}: {row}")
    return value


def prepare_observation(row: dict[str, str], salinity_case: str) -> dict[str, object]:
    flow = parse_float(row, "nominal_flow_l_h")
    hot_in = parse_float(row, "hot_inlet_temperature_c")
    hot_out = parse_float(row, "hot_outlet_temperature_c")
    cold_in = parse_float(row, "cold_inlet_temperature_c")
    cold_out = parse_float(row, "cold_outlet_temperature_c")
    measured_flux = parse_float(row, "mass_flux_kg_m2_h")

    hot_bulk = 0.5 * (hot_in + hot_out)
    cold_bulk = 0.5 * (cold_in + cold_out)
    hot_interface, cold_interface = interface_temperatures(
        hot_bulk, cold_bulk, FIXED_TPC
    )
    if salinity_case == "reported_0p5_percent_feed_salinity":
        salinity_g_kg = 5.0
    elif salinity_case == "measured_TDS_E_proxy":
        salinity_g_kg = parse_float(row, "tds_hot_ppm_raw") / 1000.0
    else:
        raise ValueError(f"Unknown salinity case: {salinity_case}")

    activity = seawater_water_activity(hot_interface, salinity_g_kg)
    delta_p_bar = vapor_pressure_driving_force_bar(
        hot_interface, cold_interface, activity
    )
    return {
        "observation_id": row["observation_id"],
        "source_workbook": row["workbook_filename"],
        "source_worksheet": row["worksheet_name"],
        "source_excel_row_1based": int(row["excel_row_1based"]),
        "flow_l_h": flow,
        "hot_inlet_c": hot_in,
        "hot_outlet_c": hot_out,
        "cold_inlet_c": cold_in,
        "cold_outlet_c": cold_out,
        "hot_mean_bulk_c": hot_bulk,
        "cold_mean_bulk_c": cold_bulk,
        "hot_interface_c": hot_interface,
        "cold_interface_c": cold_interface,
        "salinity_case": salinity_case,
        "salinity_g_kg_used": salinity_g_kg,
        "water_activity_used": activity,
        "vapor_pressure_difference_bar": delta_p_bar,
        "measured_flux_kg_m2_h": measured_flux,
        "split": "train" if any(abs(flow - target) < 0.1 for target in TRAIN_FLOWS_L_H) else (
            "held_out_flow_300_l_h" if flow == HELD_OUT_FLOW_L_H else "excluded"
        ),
    }


def fit_flow_dependent_tpc(
    rows: list[dict[str, str]],
    salinity_case: str,
    training_flows_l_h: tuple[float, ...] = TRAIN_FLOWS_L_H,
    held_out_flow_l_h: float = HELD_OUT_FLOW_L_H,
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Fit permeance plus bounded log-flow TPC on specified training flows only."""
    training = [
        row for row in rows
        if any(abs(parse_float(row, "nominal_flow_l_h") - target) < 0.1 for target in training_flows_l_h)
    ]
    held_out = [
        row for row in rows
        if abs(parse_float(row, "nominal_flow_l_h") - held_out_flow_l_h) < 0.1
    ]
    expected_training = 4 * len(training_flows_l_h)
    if len(training) != expected_training or len(held_out) != 4:
        raise ValueError(
            f"Expected {expected_training} training and 4 held-out rows for flow-dependent TPC, "
            f"got {len(training)} and {len(held_out)}"
        )

    def evaluate_one(row: dict[str, str], params: np.ndarray) -> tuple[float, float, float]:
        log_permeance, intercept, slope = (float(value) for value in params)
        flow = parse_float(row, "nominal_flow_l_h")
        logit = intercept + slope * math.log(flow / 100.0)
        logistic = 1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, logit))))
        tpc = 0.5 + 0.5 * logistic
        hot_bulk = 0.5 * (
            parse_float(row, "hot_inlet_temperature_c")
            + parse_float(row, "hot_outlet_temperature_c")
        )
        cold_bulk = 0.5 * (
            parse_float(row, "cold_inlet_temperature_c")
            + parse_float(row, "cold_outlet_temperature_c")
        )
        hot_interface, cold_interface = interface_temperatures(hot_bulk, cold_bulk, tpc)
        if salinity_case == "reported_0p5_percent_feed_salinity":
            salinity = 5.0
        else:
            salinity = parse_float(row, "tds_hot_ppm_raw") / 1000.0
        activity = seawater_water_activity(hot_interface, salinity)
        delta_p = vapor_pressure_driving_force_bar(hot_interface, cold_interface, activity)
        prediction = math.exp(log_permeance) * delta_p
        return prediction, tpc, delta_p

    observed_train = np.asarray(
        [parse_float(row, "mass_flux_kg_m2_h") for row in training], dtype=float
    )

    def residuals(params: np.ndarray) -> np.ndarray:
        return np.asarray(
            [
                evaluate_one(row, params)[0] - observed
                for row, observed in zip(training, observed_train, strict=True)
            ],
            dtype=float,
        )

    fitted = least_squares(
        residuals,
        x0=np.asarray([math.log(30.0), 0.0, 0.0]),
        bounds=(
            np.asarray([math.log(0.1), -8.0, -4.0]),
            np.asarray([math.log(200.0), 8.0, 4.0]),
        ),
        max_nfev=5000,
    )
    if not fitted.success:
        raise RuntimeError(f"Flow-dependent TPC fit did not converge: {fitted.message}")

    prediction_rows: list[dict[str, object]] = []
    for row in rows:
        prediction, tpc, delta_p = evaluate_one(row, fitted.x)
        observed = parse_float(row, "mass_flux_kg_m2_h")
        flow = parse_float(row, "nominal_flow_l_h")
        prediction_rows.append(
            {
                "observation_id": row["observation_id"],
                "source_workbook": row["workbook_filename"],
                "source_worksheet": row["worksheet_name"],
                "source_excel_row_1based": int(row["excel_row_1based"]),
                "flow_l_h": flow,
                "salinity_case": salinity_case,
                "model_form": "flow_dependent_logistic_tpc",
                "split": "train" if any(abs(flow - target) < 0.1 for target in training_flows_l_h) else f"held_out_flow_{held_out_flow_l_h:g}_l_h",
                "fitted_permeance_kg_m2_h_bar": math.exp(float(fitted.x[0])),
                "fitted_tpc": tpc,
                "vapor_pressure_difference_bar": delta_p,
                "measured_flux_kg_m2_h": observed,
                "predicted_flux_kg_m2_h": prediction,
                "residual_predicted_minus_measured": prediction - observed,
                "absolute_error_kg_m2_h": abs(prediction - observed),
                "absolute_relative_error_percent": abs(prediction - observed) / observed * 100.0 if observed > 0 else "",
            }
        )

    def metrics(subset: list[dict[str, object]]) -> dict[str, float | int]:
        observed = np.asarray([float(row["measured_flux_kg_m2_h"]) for row in subset])
        predicted = np.asarray([float(row["predicted_flux_kg_m2_h"]) for row in subset])
        residual = predicted - observed
        return {
            "n": len(subset),
            "mae_kg_m2_h": float(np.mean(np.abs(residual))),
            "rmse_kg_m2_h": float(np.sqrt(np.mean(residual**2))),
            "bias_predicted_minus_measured_kg_m2_h": float(np.mean(residual)),
            "mean_absolute_relative_error_percent": float(np.mean(np.abs(residual) / observed) * 100.0),
        }

    train_predictions = [row for row in prediction_rows if row["split"] == "train"]
    holdout_predictions = [
        row for row in prediction_rows
        if row["split"] == f"held_out_flow_{held_out_flow_l_h:g}_l_h"
    ]
    summary = {
        "model_form": "flow_dependent_logistic_tpc",
        "tpc_function": "0.5 + 0.5 * logistic(intercept + slope * ln(flow_l_h / 100))",
        "fitted_log_permeance": float(fitted.x[0]),
        "fitted_permeance_kg_m2_h_bar": math.exp(float(fitted.x[0])),
        "fitted_tpc_logistic_intercept": float(fitted.x[1]),
        "fitted_tpc_log_flow_slope": float(fitted.x[2]),
        "training_flows_l_h": list(training_flows_l_h),
        "held_out_flow_l_h": held_out_flow_l_h,
        "training_metrics": metrics(train_predictions),
        "held_out_metrics": metrics(holdout_predictions),
        "interpretation": (
            "Exploratory three-parameter flow-dependent TPC alternative fitted only on the declared training flows; "
            "the declared held-out flow is not used for fitting. This is model-form exploration within one source study, "
            "not independent validation."
        ),
    }
    return prediction_rows, summary


def fit_and_score(rows: list[dict[str, str]], salinity_case: str) -> tuple[float, list[dict[str, object]], dict[str, object], list[dict[str, object]]]:
    prepared = [prepare_observation(row, salinity_case) for row in rows]
    training = [r for r in prepared if r["split"] == "train"]
    held_out = [r for r in prepared if r["split"] == "held_out_flow_300_l_h"]
    if len(training) != 12 or len(held_out) != 4:
        raise ValueError(
            f"Expected 12 training and 4 held-out observations, got {len(training)} and {len(held_out)}"
        )

    dp_train = np.asarray(
        [float(r["vapor_pressure_difference_bar"]) for r in training], dtype=float
    )
    flux_train = np.asarray(
        [float(r["measured_flux_kg_m2_h"]) for r in training], dtype=float
    )
    denominator = float(np.dot(dp_train, dp_train))
    if denominator <= 0:
        raise ValueError("training vapor-pressure differences have zero squared norm")
    fitted_permeance = float(np.dot(dp_train, flux_train) / denominator)

    for row in prepared:
        prediction = fitted_permeance * float(row["vapor_pressure_difference_bar"])
        observed = float(row["measured_flux_kg_m2_h"])
        row["fitted_permeance_kg_m2_h_bar"] = fitted_permeance
        row["predicted_flux_kg_m2_h"] = prediction
        row["residual_predicted_minus_measured"] = prediction - observed
        row["absolute_error_kg_m2_h"] = abs(prediction - observed)
        row["absolute_relative_error_percent"] = (
            abs(prediction - observed) / observed * 100.0 if observed > 0 else ""
        )

    def metrics(subset: list[dict[str, object]]) -> dict[str, float | int]:
        observed = np.asarray([float(r["measured_flux_kg_m2_h"]) for r in subset])
        predicted = np.asarray([float(r["predicted_flux_kg_m2_h"]) for r in subset])
        residual = predicted - observed
        return {
            "n": len(subset),
            "mae_kg_m2_h": float(np.mean(np.abs(residual))),
            "rmse_kg_m2_h": float(np.sqrt(np.mean(residual**2))),
            "bias_predicted_minus_measured_kg_m2_h": float(np.mean(residual)),
            "mean_absolute_relative_error_percent": float(
                np.mean(np.abs(residual) / observed) * 100.0
            ),
        }

    summary = {
        "salinity_case": salinity_case,
        "salinity_case_definition": SALINITY_CASES[salinity_case],
        "fixed_temperature_polarization_coefficient": FIXED_TPC,
        "fitted_permeance_kg_m2_h_bar": fitted_permeance,
        "training_flows_l_h": list(TRAIN_FLOWS_L_H),
        "held_out_flow_l_h": HELD_OUT_FLOW_L_H,
        "training_metrics": metrics(training),
        "held_out_metrics": metrics(held_out),
        "interpretation": (
            "Single permeance calibrated only on 50/100/200 L/h rows; 300 L/h rows "
            "were held out by operating flow. This is an internal held-out diagnostic "
            "of the reduced vapor-pressure flux law, not independent validation of "
            "the complete MD or data-centre water model."
        ),
    }
    flow_predictions, flow_summary = fit_flow_dependent_tpc(rows, salinity_case)
    summary["flow_dependent_tpc_model"] = flow_summary
    return fitted_permeance, prepared, summary, flow_predictions


def _metrics_for_rows(rows: list[dict[str, object]]) -> dict[str, float | int]:
    if not rows:
        raise ValueError("Cannot calculate metrics for an empty prediction set")
    observed = np.asarray([float(row["measured_flux_kg_m2_h"]) for row in rows])
    predicted = np.asarray([float(row["predicted_flux_kg_m2_h"]) for row in rows])
    residual = predicted - observed
    return {
        "n": len(rows),
        "mae_kg_m2_h": float(np.mean(np.abs(residual))),
        "rmse_kg_m2_h": float(np.sqrt(np.mean(residual**2))),
        "bias_predicted_minus_measured_kg_m2_h": float(np.mean(residual)),
        "mean_absolute_relative_error_percent": float(np.mean(np.abs(residual) / observed) * 100.0),
    }


def leave_one_flow_out(
    source_rows: list[dict[str, str]], salinity_case: str
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Group-wise CV: hold out each complete flow level, never individual rows."""
    flows = tuple(sorted({parse_float(row, "nominal_flow_l_h") for row in source_rows}))
    if len(flows) != 4:
        raise ValueError(f"Expected exactly four distinct source flow levels, got {flows}")
    all_predictions: list[dict[str, object]] = []
    fold_summaries: list[dict[str, object]] = []

    for held_out_flow in flows:
        training_flows = tuple(flow for flow in flows if flow != held_out_flow)
        prepared = [prepare_observation(row, salinity_case) for row in source_rows]
        training_prepared = [
            row for row in prepared
            if any(abs(float(row["flow_l_h"]) - flow) < 0.1 for flow in training_flows)
        ]
        held_prepared = [
            row for row in prepared if abs(float(row["flow_l_h"]) - held_out_flow) < 0.1
        ]
        if len(training_prepared) != 12 or len(held_prepared) != 4:
            raise ValueError(
                f"Fold {held_out_flow:g} L/h expected 12 train/4 held-out observations; "
                f"got {len(training_prepared)}/{len(held_prepared)}"
            )

        dp_train = np.asarray(
            [float(row["vapor_pressure_difference_bar"]) for row in training_prepared]
        )
        flux_train = np.asarray(
            [float(row["measured_flux_kg_m2_h"]) for row in training_prepared]
        )
        denominator = float(np.dot(dp_train, dp_train))
        if denominator <= 0:
            raise ValueError(f"Fold {held_out_flow:g} L/h has zero training driving-force norm")
        fixed_permeance = float(np.dot(dp_train, flux_train) / denominator)

        fixed_rows: list[dict[str, object]] = []
        for row in held_prepared:
            predicted = fixed_permeance * float(row["vapor_pressure_difference_bar"])
            fixed_rows.append({
                **row,
                "model_form": "fixed_tpc_single_permeance",
                "split": f"held_out_flow_{held_out_flow:g}_l_h",
                "fold_held_out_flow_l_h": held_out_flow,
                "fold_training_flows_l_h": ";".join(f"{flow:g}" for flow in training_flows),
                "fitted_permeance_kg_m2_h_bar": fixed_permeance,
                "predicted_flux_kg_m2_h": predicted,
                "residual_predicted_minus_measured": predicted - float(row["measured_flux_kg_m2_h"]),
                "absolute_error_kg_m2_h": abs(predicted - float(row["measured_flux_kg_m2_h"])),
            })
        flow_rows, flow_summary = fit_flow_dependent_tpc(
            source_rows,
            salinity_case,
            training_flows_l_h=training_flows,
            held_out_flow_l_h=held_out_flow,
        )
        flow_holdout_rows = [
            {
                **row,
                "fold_held_out_flow_l_h": held_out_flow,
                "fold_training_flows_l_h": ";".join(f"{flow:g}" for flow in training_flows),
            }
            for row in flow_rows
            if row["split"] == f"held_out_flow_{held_out_flow:g}_l_h"
        ]
        for row in fixed_rows:
            row["salinity_case"] = salinity_case
        all_predictions.extend(fixed_rows)
        all_predictions.extend(flow_holdout_rows)
        fold_summaries.append({
            "held_out_flow_l_h": held_out_flow,
            "training_flows_l_h": list(training_flows),
            "fixed_tpc_single_permeance": _metrics_for_rows(fixed_rows),
            "flow_dependent_tpc": _metrics_for_rows(flow_holdout_rows),
            "flow_dependent_tpc_fit": {
                "fitted_permeance_kg_m2_h_bar": flow_summary["fitted_permeance_kg_m2_h_bar"],
                "fitted_tpc_logistic_intercept": flow_summary["fitted_tpc_logistic_intercept"],
                "fitted_tpc_log_flow_slope": flow_summary["fitted_tpc_log_flow_slope"],
                "training_metrics": flow_summary["training_metrics"],
            },
        })

    model_summaries: dict[str, object] = {}
    for model_form in ("fixed_tpc_single_permeance", "flow_dependent_logistic_tpc"):
        model_rows = [row for row in all_predictions if row["model_form"] == model_form]
        model_summaries[model_form] = _metrics_for_rows(model_rows)
    return all_predictions, {
        "design": "four-fold leave-one-flow-level-out; all four observations at each flow held out together",
        "salinity_case": salinity_case,
        "folds": fold_summaries,
        "out_of_fold_metrics": model_summaries,
        "interpretation": (
            "Internal grouped cross-validation over four flow levels in one source study. "
            "It tests flow-level generalization more broadly than a single 300 L/h holdout, "
            "but is not independent external validation and does not validate the coupled dynamic model."
        ),
    }


def run(input_path: Path, output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    with input_path.open(encoding="utf-8", newline="") as stream:
        source_rows = list(csv.DictReader(stream))
    if len(source_rows) != 16:
        raise ValueError(f"Expected 16 S1 steady-state observations, found {len(source_rows)}")

    predictions: list[dict[str, object]] = []
    flow_dependent_predictions: list[dict[str, object]] = []
    cases: dict[str, object] = {}
    for salinity_case in SALINITY_CASES:
        _permeance, rows, summary, flow_rows = fit_and_score(source_rows, salinity_case)
        predictions.extend(rows)
        flow_dependent_predictions.extend(flow_rows)
        cases[salinity_case] = summary

    predictions_path = output_dir / "ali_2020_flux_law_holdout_predictions.csv"
    with predictions_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(predictions[0]))
        writer.writeheader()
        writer.writerows(predictions)

    flow_predictions_path = output_dir / "ali_2020_flow_dependent_tpc_predictions.csv"
    with flow_predictions_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(flow_dependent_predictions[0]))
        writer.writeheader()
        writer.writerows(flow_dependent_predictions)

    summary: dict[str, object] = {
        "experiment_id": "ALI-2020-FLUX-LAW-HELD-OUT-FLOW-2026-10-13",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "source_doi": SOURCE_DOI,
        "input_ledger": str(input_path),
        "input_ledger_sha256": sha256_file(input_path),
        "prediction_rows": len(predictions),
        "flow_dependent_tpc_prediction_rows": len(flow_dependent_predictions),
        "cases": cases,
        "source_discrepancy": (
            "The article reports 0.5% feed salinity, while the S1 TDS_E column contains "
            "values around hundreds of ppm. Both interpretations are evaluated separately; "
            "neither is silently preferred."
        ),
        "claim_limits": [
            "Only the flux law is tested; no channel energy balance, pumping, cooling, or net-water outcome is validated.",
            "The temperature polarization coefficient is fixed at 0.8 as an explicit screening assumption.",
            "Permeance is fitted on 50, 100, and 200 L/h observations; the 300 L/h flow is held out.",
            "This is held-out operating-condition evaluation within one source study, not an independent external validation dataset.",
            "A poor held-out result indicates the single-permeance/fixed-TPC flux form does not generalize under this boundary-temperature reconstruction; it does not invalidate the source measurements.",
        ],
    }
    cv_predictions: list[dict[str, object]] = []
    cv_cases: dict[str, object] = {}
    for salinity_case in SALINITY_CASES:
        fold_rows, fold_summary = leave_one_flow_out(source_rows, salinity_case)
        cv_predictions.extend(fold_rows)
        cv_cases[salinity_case] = fold_summary

    cv_predictions_path = output_dir / "ali_2020_flux_law_leave_one_flow_out_predictions.csv"
    with cv_predictions_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(cv_predictions[0]))
        writer.writeheader()
        writer.writerows(cv_predictions)
    cv_summary = {
        "experiment_id": "ALI-2020-FLUX-LAW-LEAVE-ONE-FLOW-OUT-2026-10-14",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "source_doi": SOURCE_DOI,
        "input_ledger": str(input_path),
        "input_ledger_sha256": sha256_file(input_path),
        "prediction_rows": len(cv_predictions),
        "cases": cv_cases,
        "claim_limits": [
            "Each fold holds out a complete nominal flow level, not random serial rows.",
            "This is within-source model-form diagnostics only; all folds share the same experiment and source assumptions.",
            "The three-parameter flow-dependent TPC alternative is more flexible and may overfit; compare its out-of-fold error and parameter stability rather than selecting by training fit.",
            "The flux-law comparison does not validate transient mass accumulation, energy balances, cooling, electricity-water factors, or net freshwater benefit.",
            "Salinity interpretations are kept separate because the paper's stated 0.5% feed salinity and S1 TDS_E values are inconsistent.",
        ],
    }
    cv_summary_path = output_dir / "ali_2020_flux_law_leave_one_flow_out_summary.json"
    cv_summary_path.write_text(
        json.dumps(cv_summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )

    summary_path = output_dir / "ali_2020_flux_law_holdout_summary.json"
    summary_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    manifest = {
        "summary_file": summary_path.name,
        "predictions_file": predictions_path.name,
        "flow_dependent_tpc_predictions_file": flow_predictions_path.name,
        "leave_one_flow_out_summary_file": cv_summary_path.name,
        "leave_one_flow_out_predictions_file": cv_predictions_path.name,
        "leave_one_flow_out_summary_sha256": sha256_file(cv_summary_path),
        "leave_one_flow_out_predictions_sha256": sha256_file(cv_predictions_path),
        "summary_sha256": sha256_file(summary_path),
        "predictions_sha256": sha256_file(predictions_path),
        "flow_dependent_tpc_predictions_sha256": sha256_file(flow_predictions_path),
        "status": "internal_held_out_flux_law_diagnostic_not_independent_validation",
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("artifacts/ali_2020_exports/ali_2020_steady_state_observation_ledger.csv"),
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("artifacts/ali_2020_flux_holdout")
    )
    args = parser.parse_args()
    summary = run(args.input, args.output_dir)
    print(json.dumps(summary["cases"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
