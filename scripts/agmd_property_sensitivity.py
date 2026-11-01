"""Predeclared AGMD property-state sensitivity grid.

Run from repository root:
    python scripts/agmd_property_sensitivity.py --output 06_results/agmd_property_sensitivity.csv

The grid is a scenario envelope, not a probabilistic confidence interval and not
an attempt to recover undisclosed article inputs.
"""
from __future__ import annotations

import argparse
import csv
from itertools import product
from pathlib import Path

from ai_water.malaguti_agmd_reference import solve_agmd_reference
from ai_water.sharqawy_2010 import (
    jamieson_seawater_cp_j_kg_k,
    pure_water_cp_j_kg_k,
    pure_water_latent_heat_j_kg,
)

COLD_INLET_C = 20.0
DELTA_T_H_IN_C = 5.0
SALINITIES_G_KG = (30.0, 35.0, 40.0)
DISTILLATE_CP_TEMPERATURES_C = (35.0, 42.5, 50.0)
VAPOR_LATENT_HEAT_TEMPERATURES_C = (35.0, 42.5, 50.0)
BENCHMARKS = ((0.5, 30.0), (0.5, 50.0), (0.7, 30.0), (0.7, 50.0))


def build_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for salinity, cp_d_temp, hfg_temp, (eta, delta_t) in product(
        SALINITIES_G_KG,
        DISTILLATE_CP_TEMPERATURES_C,
        VAPOR_LATENT_HEAT_TEMPERATURES_C,
        BENCHMARKS,
    ):
        hot_inlet_c = COLD_INLET_C + delta_t
        cp_hot = jamieson_seawater_cp_j_kg_k(hot_inlet_c, salinity)
        cp_cold = jamieson_seawater_cp_j_kg_k(COLD_INLET_C, salinity)
        cp_distillate = pure_water_cp_j_kg_k(cp_d_temp)
        latent_heat = pure_water_latent_heat_j_kg(hfg_temp)
        row: dict[str, object] = {
            "salinity_sr_g_kg": salinity,
            "eta": eta,
            "delta_t_c": delta_t,
            "cold_inlet_c": COLD_INLET_C,
            "hot_inlet_c": hot_inlet_c,
            "delta_t_h_in_c": DELTA_T_H_IN_C,
            "cp_hot_eval_c": hot_inlet_c,
            "cp_cold_eval_c": COLD_INLET_C,
            "cp_distillate_eval_c": cp_d_temp,
            "latent_heat_eval_c": hfg_temp,
            "cp_hot_j_kg_k": cp_hot,
            "cp_cold_j_kg_k": cp_cold,
            "cp_distillate_j_kg_k": cp_distillate,
            "latent_heat_j_kg": latent_heat,
            "status": "ok",
            "recovery_fraction": "",
            "delta_t_h_out_c": "",
            "distillate_outlet_c": "",
            "s2_residual": "",
            "s8_residual": "",
            "error": "",
        }
        try:
            result = solve_agmd_reference(
                vaporization_efficiency=eta,
                delta_t_c=delta_t,
                delta_t_h_in_c=DELTA_T_H_IN_C,
                cold_inlet_c=COLD_INLET_C,
                cp_hot_j_kg_k=cp_hot,
                cp_cold_j_kg_k=cp_cold,
                cp_distillate_j_kg_k=cp_distillate,
                latent_heat_j_kg=latent_heat,
            )
            row.update(
                recovery_fraction=result.recovery_fraction,
                delta_t_h_out_c=result.delta_t_h_out_c,
                distillate_outlet_c=result.distillate_outlet_c,
                s2_residual=result.equation_s2_residual,
                s8_residual=result.equation_s8_residual_w_per_kg_k,
            )
        except ValueError as exc:
            row.update(status="no_admissible_root", error=str(exc))
        rows.append(row)
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = build_rows()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    successful = [row for row in rows if row["status"] == "ok"]
    print(f"scenarios={len(rows)} successful={len(successful)} failed={len(rows)-len(successful)}")
    if successful:
        recoveries = [float(row["recovery_fraction"]) for row in successful]
        print(f"recovery_envelope_pct={100*min(recoveries):.6f}..{100*max(recoveries):.6f}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()
