"""Run a bounded physical-admissibility matrix for Ali et al. (2020).

This is a diagnostic, not a parameter-fitting or validation script. It records
failures rather than silently discarding them and never chooses parameters by
agreement with experimental observations.
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from ai_water.ali_dynamic_model import (
    PUBLISHED_FLOS_LUMPED,
    AliDynamicConfig,
    simulate_lumped_transient,
)


def run_case(
    *,
    case_id: str,
    flow_l_h: float,
    config: AliDynamicConfig,
    heat_loss_correction: float,
) -> dict[str, object]:
    time_min = np.array([0.0, 0.5, 1.0])
    hot_inlet_c = np.full(3, 60.0)
    cold_inlet_c = np.full(3, 25.0)
    row: dict[str, object] = {
        "case_id": case_id,
        "flow_l_h": flow_l_h,
        "area_m2": config.membrane_area_m2,
        "pore_radius_um": config.pore_radius_m * 1e6,
        "heat_loss_correction": heat_loss_correction,
        "status": "not_run",
        "error": "",
        "hot_outlet_min_c": None,
        "hot_outlet_max_c": None,
        "cold_outlet_min_c": None,
        "cold_outlet_max_c": None,
        "final_accumulated_mass_kg": None,
        "final_mass_rate_kg_h": None,
        "mass_rate_nonnegative": False,
    }
    try:
        result = simulate_lumped_transient(
            time_min=time_min,
            hot_inlet_c=hot_inlet_c,
            cold_inlet_c=cold_inlet_c,
            nominal_flow_l_h=flow_l_h,
            heat_loss_correction=heat_loss_correction,
            config=config,
        )
        row.update(
            {
                "status": "admissible",
                "hot_outlet_min_c": float(np.min(result.hot_outlet_c)),
                "hot_outlet_max_c": float(np.max(result.hot_outlet_c)),
                "cold_outlet_min_c": float(np.min(result.cold_outlet_c)),
                "cold_outlet_max_c": float(np.max(result.cold_outlet_c)),
                "final_accumulated_mass_kg": float(result.accumulated_mass_kg[-1]),
                "final_mass_rate_kg_h": float(result.mass_rate_kg_h[-1]),
                "mass_rate_nonnegative": bool(np.all(result.mass_rate_kg_h >= -1e-9)),
            }
        )
    # Record every failed case as diagnostic evidence rather than hiding it.
    except Exception as exc:  # noqa: BLE001
        row["status"] = "rejected"
        row["error"] = f"{type(exc).__name__}: {exc}"
    return row


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="artifacts/ali_dynamic_admissibility")
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    cases: list[dict[str, object]] = []
    for flow in (50.0, 100.0, 200.0, 300.0):
        base = AliDynamicConfig()
        cases.append(
            run_case(
                case_id=f"source_default_{int(flow)}",
                flow_l_h=flow,
                config=base,
                heat_loss_correction=0.0,
            )
        )
        cases.append(
            run_case(
                case_id=f"pore_diameter_interpretation_{int(flow)}",
                flow_l_h=flow,
                config=replace(base, pore_radius_m=0.2e-6),
                heat_loss_correction=0.0,
            )
        )
        cases.append(
            run_case(
                case_id=f"reported_area_9_8_{int(flow)}",
                flow_l_h=flow,
                config=replace(base, membrane_area_m2=9.8),
                heat_loss_correction=0.0,
            )
        )
        cases.append(
            run_case(
                case_id=f"published_lumped_correction_{int(flow)}",
                flow_l_h=flow,
                config=base,
                heat_loss_correction=PUBLISHED_FLOS_LUMPED[int(flow)],
            )
        )

    # A reduced-area case is solely an integrator smoke control, not a source
    # geometry case and not evidence of experimental model performance.
    cases.append(
        run_case(
            case_id="reduced_area_numerical_control",
            flow_l_h=50.0,
            config=replace(AliDynamicConfig(), membrane_area_m2=0.1),
            heat_loss_correction=0.0,
        )
    )

    csv_path = output_dir / "ali_dynamic_admissibility_matrix.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(cases[0]))
        writer.writeheader()
        writer.writerows(cases)

    summary = {
        "scope": "physical-admissibility diagnostic only; not fitted or validated",
        "input_trace": {
            "time_min": [0.0, 0.5, 1.0],
            "hot_inlet_c": 60.0,
            "cold_inlet_c": 25.0,
            "initial_outlets_c": "model default room temperature (25 C)",
        },
        "cases": len(cases),
        "admissible_cases": sum(case["status"] == "admissible" for case in cases),
        "rejected_cases": sum(case["status"] == "rejected" for case in cases),
        "all_mass_rates_nonnegative_when_admissible": all(
            case["mass_rate_nonnegative"]
            for case in cases
            if case["status"] == "admissible"
        ),
        "case_results": cases,
        "interpretation": [
            "The published heat-loss corrections are included as source-reproduction cases, not as independent physical estimates.",
            "The 0.2 micrometre pore-radius case tests the paper's diameter/radius ambiguity and is not selected by fit.",
            "The 9.8 square metre case tests the 14 m by 0.7 m geometric-area product against the reported 10 square metre effective area.",
            "A passing outlet-envelope check is necessary but not sufficient for model validity.",
            "No experimental observations are used to select a parameterization.",
        ],
    }
    (output_dir / "ali_dynamic_admissibility_summary.json").write_text(
        json.dumps(summary, indent=2, allow_nan=False), encoding="utf-8"
    )
    print(
        f"Cases={summary['cases']}; admissible={summary['admissible_cases']}; "
        f"rejected={summary['rejected_cases']}"
    )
    for case in cases:
        print(
            f"{case['case_id']}: {case['status']}; "
            f"hot=[{case['hot_outlet_min_c']}, {case['hot_outlet_max_c']}]; "
            f"cold=[{case['cold_outlet_min_c']}, {case['cold_outlet_max_c']}]; "
            f"error={case['error']}"
        )


if __name__ == "__main__":
    main()
