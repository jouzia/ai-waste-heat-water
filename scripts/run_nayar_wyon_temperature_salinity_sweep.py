"""Compare Wyon and Nayar vapour-pressure modes across feed temperature/salinity.

This is a deterministic local membrane-surface sensitivity sweep, not
experimental validation or a full axial DCMD module simulation.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from ai_water.wyon_2025_coupled_channel_surface import (
    solve_wyon_coupled_channel_surface,
)

FEED_TEMPERATURES_C = (40.0, 50.0, 60.0, 70.0)
FEED_SALINITIES_SR_G_KG = (15.0, 35.0, 38.0)
FIXED_CASE = {
    "permeate_bulk_temperature_c": 20.0,
    "feed_velocity_m_s": 1.85,
    "permeate_velocity_m_s": 2.92,
    "hydraulic_diameter_m": 0.003,
    "channel_length_m": 0.1,
    "membrane_thermal_conductivity_w_m_k": 0.041,
    "membrane_thickness_m": 126e-6,
    "pore_radius_m": 0.11e-6,
    "porosity": 0.75,
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _solve(feed_temperature_c: float, salinity: float, model: str):
    return solve_wyon_coupled_channel_surface(
        feed_bulk_temperature_c=feed_temperature_c,
        feed_salinity_sr_g_kg=salinity,
        vapour_pressure_model=model,
        **FIXED_CASE,
    ).surface


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for temperature_c in FEED_TEMPERATURES_C:
        for salinity in FEED_SALINITIES_SR_G_KG:
            wyon = _solve(temperature_c, salinity, "wyon_2025")
            nayar = _solve(temperature_c, salinity, "nayar_2016")
            row: dict[str, object] = {
                "feed_bulk_temperature_c": temperature_c,
                "permeate_bulk_temperature_c": FIXED_CASE["permeate_bulk_temperature_c"],
                "feed_reference_salinity_g_kg": salinity,
                "vapour_pressure_mode_comparison": "Nayar 2016 relative to Wyon 2025",
            }
            metrics = (
                ("feed_interface_temperature_c", "feed_interface_temperature_c"),
                ("permeate_interface_temperature_c", "permeate_interface_temperature_c"),
                ("mean_membrane_temperature_k", "mean_membrane_temperature_k"),
                ("feed_vapour_pressure_pa", "vapour_pressure_feed_pa"),
                ("permeate_vapour_pressure_pa", "vapour_pressure_permeate_pa"),
                ("mass_flux_kg_m2_h", "mass_flux_kg_m2_h"),
                ("heat_flux_w_m2", "heat_flux_w_m2"),
                ("latent_heat_flux_w_m2", "latent_heat_flux_w_m2"),
                ("conductive_heat_flux_w_m2", "conductive_heat_flux_w_m2"),
                ("membrane_mass_transfer_coefficient_kg_m2_s_pa",
                 "membrane_mass_transfer_coefficient_kg_m2_s_pa"),
                ("energy_balance_residual_w_m2", "energy_balance_residual_w_m2"),
            )
            for output_name, attribute in metrics:
                wyon_value = getattr(wyon, attribute)
                nayar_value = getattr(nayar, attribute)
                row[f"wyon_{output_name}"] = wyon_value
                row[f"nayar_{output_name}"] = nayar_value
                if wyon_value != 0:
                    row[f"nayar_vs_wyon_{output_name}_change_pct"] = (
                        (nayar_value / wyon_value) - 1.0
                    ) * 100.0
                else:
                    row[f"nayar_vs_wyon_{output_name}_change_pct"] = ""
            rows.append(row)

    csv_path = output_dir / "nayar_wyon_temperature_salinity_sweep.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    manifest: dict[str, object] = {
        "experiment_id": "NAYAR-WYON-TEMP-SALINITY-SWEEP-2026-11-06",
        "row_count": len(rows),
        "feed_temperatures_c": list(FEED_TEMPERATURES_C),
        "feed_reference_salinity_g_kg": list(FEED_SALINITIES_SR_G_KG),
        "fixed_case": FIXED_CASE,
        "comparison": (
            "Nayar paired pure-water/natural-seawater vapour pressure relative "
            "to Wyon pure-water vapour pressure; both runs use identical "
            "channel salinity and all other local solver inputs."
        ),
        "assumptions": [
            "Bulk feed Reference Salinity is used as a proxy for feed-interface salinity.",
            "The same bulk Reference Salinity is used for mean-pore vapour pressure.",
            "No concentration-polarization or axial module balance is solved.",
        ],
        "interpretation": (
            "Deterministic local surface-model sensitivity; not experimental "
            "validation and not a reproduction of Wyon Figure 9."
        ),
        "files": {csv_path.name: _sha256(csv_path)},
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/nayar_wyon_temperature_salinity_sweep"),
    )
    args = parser.parse_args()
    print(json.dumps(run(args.output_dir), indent=2))


if __name__ == "__main__":
    main()
