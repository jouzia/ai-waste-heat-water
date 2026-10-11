"""Fit a membrane permeance on 20 C cold-side cases and test 30 C cases.

This is a within-workbook held-out-condition experiment, not external validation.
All geometry/correlation/property assumptions are exported alongside predictions.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from scipy.optimize import minimize_scalar

from ai_water.channel_transport import (
    graetz_leveque_nusselt,
    heat_transfer_coefficient,
    watertap_nusselt,
)
from ai_water.md_channel import ChannelConfig, simulate_dcmd_channel

SOURCE_AREA_M2 = 0.23088
SOURCE_LENGTH_M = 1.04
SOURCE_WIDTH_M = 0.222
SOURCE_HEIGHT_M = 0.0018
SOURCE_FLOW_AREA_M2 = SOURCE_WIDTH_M * SOURCE_HEIGHT_M
SOURCE_SPACER_POROSITY = 0.921035
SOURCE_DH_SMOOTH_M = 2.0 * SOURCE_WIDTH_M * SOURCE_HEIGHT_M / (SOURCE_WIDTH_M + SOURCE_HEIGHT_M)
SOURCE_DH_POROSITY_M = 0.002519819
MEMBRANE_THICKNESS_M = 110e-6
MEMBRANE_POROSITY = 0.85
NOMINAL_FLOW_LPM = 1.0
FEED_SALINITY_G_L = 4.0
POLYPROPYLENE_K_W_M_K = 0.22
VAPOR_K_W_M_K = 0.026


def _number(value: object) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"Expected finite numeric value, got {value!r}")
    return number


def _water_properties(temp_c: float) -> dict[str, float]:
    from iapws import IAPWS97

    state = IAPWS97(T=temp_c + 273.15, P=0.101325)
    return {
        "rho": float(state.rho),
        "mu": float(state.mu),
        "k": float(state.k),
        "cp": float(state.cp) * 1000.0,
    }


def _latent_heat_kwh_kg(temp_c: float) -> float:
    from iapws import IAPWS97

    temp_k = temp_c + 273.15
    liquid = IAPWS97(T=temp_k, x=0)
    vapor = IAPWS97(T=temp_k, x=1)
    return (float(vapor.h) - float(liquid.h)) / 3600.0


def _nacl_water_activity() -> float:
    # Keshavarzzadeh-style low-salinity NaCl activity closure; solution density
    # is approximated as 1 kg/L for converting the source's 4 g/L setting.
    salt_mol = FEED_SALINITY_G_L / 58.44277
    water_mol = (1000.0 - FEED_SALINITY_G_L) / 18.01528
    mole_fraction = salt_mol / (salt_mol + water_mol)
    gamma_w = 1.0 - 0.5 * mole_fraction - 10.0 * mole_fraction**2
    return gamma_w * (1.0 - mole_fraction)


def _htc(
    temp_c: float,
    *,
    correlation: str,
    hydraulic_diameter_m: float,
    flow_area_m2: float,
    channel_length_m: float,
) -> tuple[float, float, float]:
    props = _water_properties(temp_c)
    flow_m3_s = NOMINAL_FLOW_LPM / 1000.0 / 60.0
    velocity = flow_m3_s / flow_area_m2
    reynolds = props["rho"] * velocity * hydraulic_diameter_m / props["mu"]
    prandtl = props["cp"] * props["mu"] / props["k"]
    if correlation == "graetz_leveque":
        nusselt = graetz_leveque_nusselt(
            reynolds, prandtl, hydraulic_diameter_m, channel_length_m
        )
    elif correlation == "watertap":
        nusselt = watertap_nusselt(reynolds, prandtl)
    else:
        raise ValueError(f"Unknown heat-transfer correlation: {correlation}")
    htc = heat_transfer_coefficient(
        nusselt=nusselt,
        thermal_conductivity_w_m_k=props["k"],
        hydraulic_diameter_m=hydraulic_diameter_m,
    )
    return htc, reynolds, prandtl


def _read_summary(path: Path) -> list[dict[str, float | str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        rows = list(csv.DictReader(stream))
    expected = {f"{cold}-{hot}" for cold in (20, 30) for hot in (40, 45, 50, 55, 60, 65)}
    if {row["condition_id"] for row in rows} != expected:
        raise ValueError("Summary must contain exactly the 12 audited temperature conditions.")
    return rows


def _make_config(
    row: dict[str, float | str],
    permeance: float,
    *,
    correlation: str,
    geometry: str,
    cells: int,
) -> tuple[ChannelConfig, dict[str, float]]:
    feed_in = _number(row["feed_inlet_mean_c"])
    perm_in = _number(row["distillate_inlet_mean_c"])
    feed_out_measured = _number(row["feed_outlet_mean_c"])
    perm_out_measured = _number(row["distillate_outlet_mean_c"])
    feed_mean = (feed_in + feed_out_measured) / 2.0
    perm_mean = (perm_in + perm_out_measured) / 2.0

    if geometry == "smooth_channel":
        hydraulic_diameter = SOURCE_DH_SMOOTH_M
        flow_area = SOURCE_FLOW_AREA_M2
    elif geometry == "spacer_porosity":
        hydraulic_diameter = SOURCE_DH_POROSITY_M
        flow_area = SOURCE_FLOW_AREA_M2 * SOURCE_SPACER_POROSITY
    else:
        raise ValueError(f"Unknown geometry: {geometry}")

    feed_props = _water_properties(feed_mean)
    perm_props = _water_properties(perm_mean)
    feed_htc, feed_re, feed_pr = _htc(
        feed_mean,
        correlation=correlation,
        hydraulic_diameter_m=hydraulic_diameter,
        flow_area_m2=flow_area,
        channel_length_m=SOURCE_LENGTH_M,
    )
    perm_htc, perm_re, perm_pr = _htc(
        perm_mean,
        correlation=correlation,
        hydraulic_diameter_m=hydraulic_diameter,
        flow_area_m2=flow_area,
        channel_length_m=SOURCE_LENGTH_M,
    )

    # Effective porous-polymer conductivity bounds from series/parallel mixing.
    k_series = 1.0 / (
        MEMBRANE_POROSITY / VAPOR_K_W_M_K
        + (1.0 - MEMBRANE_POROSITY) / POLYPROPYLENE_K_W_M_K
    )
    k_parallel = (
        MEMBRANE_POROSITY * VAPOR_K_W_M_K
        + (1.0 - MEMBRANE_POROSITY) * POLYPROPYLENE_K_W_M_K
    )
    membrane_k = k_parallel  # named scenario; series value is reported as a bound

    feed_mass_flow = 0.06 * feed_props["rho"]  # 1 L/min = 0.06 m3/h
    perm_mass_flow = 0.06 * perm_props["rho"]
    latent_temp = (feed_mean + perm_mean) / 2.0
    config = ChannelConfig(
        membrane_area_m2=SOURCE_AREA_M2,
        membrane_permeance_kg_m2_h_bar=permeance,
        membrane_thermal_conductivity_w_m_k=membrane_k,
        membrane_thickness_m=MEMBRANE_THICKNESS_M,
        feed_mass_flow_kg_h=feed_mass_flow,
        permeate_mass_flow_kg_h=perm_mass_flow,
        feed_cp_kj_kg_k=feed_props["cp"] / 1000.0,
        permeate_cp_kj_kg_k=perm_props["cp"] / 1000.0,
        latent_heat_kwh_th_per_kg=_latent_heat_kwh_kg(latent_temp),
        feed_heat_transfer_coefficient_w_m2_k=feed_htc,
        permeate_heat_transfer_coefficient_w_m2_k=perm_htc,
        feed_salinity_g_kg=FEED_SALINITY_G_L,
        water_activity_override=_nacl_water_activity(),
        cells=cells,
        duration_h=1.0,
        flow_arrangement="counter_current",
    )
    meta = {
        "feed_reynolds": feed_re,
        "feed_prandtl": feed_pr,
        "permeate_reynolds": perm_re,
        "permeate_prandtl": perm_pr,
        "feed_htc_w_m2_k": feed_htc,
        "permeate_htc_w_m2_k": perm_htc,
        "membrane_k_parallel_w_m_k": k_parallel,
        "membrane_k_series_w_m_k": k_series,
        "membrane_k_used_w_m_k": membrane_k,
        "hydraulic_diameter_m": hydraulic_diameter,
        "flow_area_m2": flow_area,
        "water_activity": _nacl_water_activity(),
        "nominal_flow_lpm_each_side": NOMINAL_FLOW_LPM,
    }
    return config, meta


def _predict(
    row: dict[str, float | str],
    permeance: float,
    *,
    correlation: str,
    geometry: str,
    cells: int,
) -> tuple[float, float, float, dict[str, float]]:
    config, meta = _make_config(
        row, permeance, correlation=correlation, geometry=geometry, cells=cells
    )
    result = simulate_dcmd_channel(
        config=config,
        feed_in_temperature_c=_number(row["feed_inlet_mean_c"]),
        permeate_in_temperature_c=_number(row["distillate_inlet_mean_c"]),
    )
    # Convert model mass flux to volumetric flux using pure-water density at
    # the mean permeate bulk temperature. The source observation is L/m2/h.
    perm_mean = (
        _number(row["distillate_inlet_mean_c"])
        + _number(row["distillate_outlet_mean_c"])
    ) / 2.0
    rho_distillate = _water_properties(perm_mean)["rho"]
    mass_flux_kg_m2_h = result.freshwater_produced_kg / (config.membrane_area_m2 * config.duration_h)
    predicted_l_m2_h = mass_flux_kg_m2_h / (rho_distillate / 1000.0)
    return (
        predicted_l_m2_h,
        result.feed_out_temperature_c,
        result.permeate_out_temperature_c,
        meta,
    )


def _metrics(observed: list[float], predicted: list[float]) -> dict[str, float]:
    errors = [p - o for o, p in zip(observed, predicted, strict=True)]
    n = len(errors)
    return {
        "n": n,
        "mae_l_m2_h": sum(abs(e) for e in errors) / n,
        "rmse_l_m2_h": math.sqrt(sum(e * e for e in errors) / n),
        "bias_l_m2_h": sum(errors) / n,
        "mape_percent": 100.0 * sum(abs(e / o) for e, o in zip(errors, observed, strict=True)) / n,
    }


def run_comparison(
    summary_path: Path,
    output_dir: Path,
    *,
    cells: int = 20,
) -> dict[str, object]:
    rows = _read_summary(summary_path)
    variants = [
        (correlation, geometry)
        for correlation in ("graetz_leveque", "watertap")
        for geometry in ("smooth_channel", "spacer_porosity")
    ]
    detail_rows: list[dict[str, object]] = []
    model_summaries: list[dict[str, object]] = []

    for correlation, geometry in variants:
        train = [row for row in rows if str(row["condition_id"]).startswith("20-")]
        held_out = [row for row in rows if str(row["condition_id"]).startswith("30-")]
        observed_train = [_number(row["derived_flux_l_m2_h"]) for row in train]

        def objective(log10_permeance: float) -> float:
            permeance = 10.0**log10_permeance
            try:
                predicted = [
                    _predict(
                        row,
                        permeance,
                        correlation=correlation,
                        geometry=geometry,
                        cells=cells,
                    )[0]
                    for row in train
                ]
            except (ValueError, RuntimeError, ArithmeticError):
                return 1e12
            return sum(
                math.log(max(p, 1e-12) / o) ** 2
                for o, p in zip(observed_train, predicted, strict=True)
            )

        optimum = minimize_scalar(
            objective, bounds=(-3.0, 3.0), method="bounded", options={"xatol": 0.03}
        )
        fitted_permeance = 10.0**float(optimum.x)
        all_predictions = []
        metadata_for_variant = None
        for row in rows:
            observed = _number(row["derived_flux_l_m2_h"])
            try:
                predicted, feed_out_pred, perm_out_pred, meta = _predict(
                    row,
                    fitted_permeance,
                    correlation=correlation,
                    geometry=geometry,
                    cells=cells,
                )
                metadata_for_variant = meta
                status = "ok"
                error = predicted - observed
                rel_error = error / observed
            except (ValueError, RuntimeError, ArithmeticError) as exc:
                predicted = feed_out_pred = perm_out_pred = math.nan
                status = f"solver_error:{type(exc).__name__}:{exc}"
                error = rel_error = math.nan
                meta = {}
            split = "development_fit" if str(row["condition_id"]).startswith("20-") else "held_out_condition"
            record = {
                "model_form": f"{correlation}__{geometry}",
                "heat_transfer_correlation": correlation,
                "channel_geometry_assumption": geometry,
                "membrane_permeance_fitted_kg_m2_h_bar": fitted_permeance,
                "condition_id": row["condition_id"],
                "split": split,
                "observed_flux_l_m2_h": observed,
                "predicted_flux_l_m2_h": predicted,
                "error_l_m2_h": error,
                "relative_error": rel_error,
                "predicted_feed_outlet_c": feed_out_pred,
                "observed_feed_outlet_mean_c": row["feed_outlet_mean_c"],
                "predicted_permeate_outlet_c": perm_out_pred,
                "observed_permeate_outlet_mean_c": row["distillate_outlet_mean_c"],
                "solver_status": status,
                **meta,
            }
            detail_rows.append(record)
            if status == "ok":
                all_predictions.append((split, observed, predicted))

        summary_record: dict[str, object] = {
            "model_form": f"{correlation}__{geometry}",
            "heat_transfer_correlation": correlation,
            "channel_geometry_assumption": geometry,
            "fitted_membrane_permeance_kg_m2_h_bar": fitted_permeance,
            "training_objective_log_relative_sse": float(optimum.fun),
            "optimization_success": bool(optimum.success),
            "cells": cells,
            "water_activity_model": "Keshavarzzadeh-style NaCl activity at 4 g/L, approximate density conversion",
            "latent_heat_model": "IAPWS97 saturated liquid-vapor enthalpy difference at mean bulk temperature",
            "membrane_k_model": "parallel mixing rule; series mixing bound exported per condition",
            "flow_model": "nominal 1 L/min each side; suspect signed/Inf workbook flow channels excluded",
            "split": "20 C cold-side sheets fit; 30 C cold-side sheets held out within same workbook",
        }
        for split_name, split_rows in (
            ("development", [r for r in all_predictions if r[0] == "development_fit"]),
            ("held_out", [r for r in all_predictions if r[0] == "held_out_condition"]),
        ):
            if split_rows:
                metrics = _metrics(
                    [item[1] for item in split_rows],
                    [item[2] for item in split_rows],
                )
                summary_record.update({f"{split_name}_{key}": value for key, value in metrics.items()})
        if metadata_for_variant:
            summary_record.update(metadata_for_variant)
        model_summaries.append(summary_record)

    output_dir.mkdir(parents=True, exist_ok=True)
    detail_fields = list(dict.fromkeys(key for row in detail_rows for key in row))
    with (output_dir / "model_form_comparison.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=detail_fields)
        writer.writeheader()
        writer.writerows(detail_rows)
    summary_fields = list(dict.fromkeys(key for row in model_summaries for key in row))
    with (output_dir / "model_form_metrics.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(stream, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(model_summaries)
    return {
        "n_conditions": len(rows),
        "n_model_forms": len(variants),
        "development_split": "20 C cold-side nominal setpoint (six conditions)",
        "held_out_split": "30 C cold-side nominal setpoint (six conditions)",
        "status": "within-workbook held-out-condition evaluation; not external validation",
        "model_forms": model_summaries,
        "critical_caveat": (
            "Membrane permeance is fitted only to the 20 C group. The held-out 30 C "
            "group is not an independent study. Flow rate is nominal because sensor "
            "channels are inconsistent; effective membrane conductivity and heat-transfer "
            "correlations are engineering assumptions. Interpret results as a diagnostic "
            "model-form comparison, not a validated predictive claim."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--summary",
        type=Path,
        default=Path("04_experiments/literature_benchmarks/MD-OEDI-VILLA-2018_3M_flux_summary.csv"),
    )
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/gdr_villa_exports"))
    parser.add_argument("--cells", type=int, default=20)
    args = parser.parse_args()
    try:
        report = run_comparison(args.summary, args.output_dir, cells=args.cells)
    except (OSError, ValueError, RuntimeError, ArithmeticError) as exc:
        parser.error(str(exc))
    (args.output_dir / "model_form_metrics.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Compared {report['n_model_forms']} model forms on {report['n_conditions']} conditions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
