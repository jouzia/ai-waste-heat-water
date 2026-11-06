"""Decompose Nayar-vs-Wyon local DCMD vapour-pressure model sensitivity.

The diagnostic Nayar-pure-water run isolates the pure-water correlation
difference; the paired Nayar natural-seawater run then isolates the salinity
correction relative to that same Nayar pure-water reference.
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
MODELS = {
    "wyon": "wyon_2025",
    "nayar_pure_water": "nayar_2016_pure_water",
    "nayar_seawater": "nayar_2016",
}
TEMPERATURE_METRICS = (
    ("feed_interface_temperature_c", "feed_interface_temperature_c"),
    ("permeate_interface_temperature_c", "permeate_interface_temperature_c"),
    ("mean_membrane_temperature_k", "mean_membrane_temperature_k"),
)
PERCENT_METRICS = (
    ("feed_vapour_pressure_pa", "vapour_pressure_feed_pa"),
    ("permeate_vapour_pressure_pa", "vapour_pressure_permeate_pa"),
    ("mass_flux_kg_m2_h", "mass_flux_kg_m2_h"),
    ("heat_flux_w_m2", "heat_flux_w_m2"),
    ("latent_heat_flux_w_m2", "latent_heat_flux_w_m2"),
    ("conductive_heat_flux_w_m2", "conductive_heat_flux_w_m2"),
    ("membrane_mass_transfer_coefficient_kg_m2_s_pa",
     "membrane_mass_transfer_coefficient_kg_m2_s_pa"),
)
RESIDUAL_METRIC = ("energy_balance_residual_w_m2", "energy_balance_residual_w_m2")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _solve(feed_temperature_c: float, salinity: float, model: str):
    return solve_wyon_coupled_channel_surface(
        feed_bulk_temperature_c=feed_temperature_c,
        feed_salinity_sr_g_kg=salinity,
        vapour_pressure_model=model,
        **FIXED_CASE,
    ).surface


def _relative_change_pct(value: float, reference: float) -> float | str:
    if reference == 0:
        return ""
    return (value / reference - 1.0) * 100.0


def run(output_dir: Path) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, object]] = []
    for temperature_c in FEED_TEMPERATURES_C:
        for salinity in FEED_SALINITIES_SR_G_KG:
            results = {
                label: _solve(temperature_c, salinity, model)
                for label, model in MODELS.items()
            }
            row: dict[str, object] = {
                "feed_bulk_temperature_c": temperature_c,
                "permeate_bulk_temperature_c": FIXED_CASE["permeate_bulk_temperature_c"],
                "feed_reference_salinity_g_kg": salinity,
            }
            for label, result in results.items():
                for output_name, attribute in (
                    *TEMPERATURE_METRICS,
                    *PERCENT_METRICS,
                    RESIDUAL_METRIC,
                ):
                    row[f"{label}_{output_name}"] = getattr(result, attribute)

            # Temperature differences are reported in their physical units,
            # never as percentages of Celsius temperatures.
            for output_name, attribute in TEMPERATURE_METRICS:
                wyon_value = getattr(results["wyon"], attribute)
                pure_value = getattr(results["nayar_pure_water"], attribute)
                seawater_value = getattr(results["nayar_seawater"], attribute)
                row[f"nayar_pure_water_vs_wyon_{output_name}_delta"] = (
                    pure_value - wyon_value
                )
                row[f"nayar_seawater_vs_nayar_pure_water_{output_name}_delta"] = (
                    seawater_value - pure_value
                )
                row[f"nayar_seawater_vs_wyon_{output_name}_delta"] = (
                    seawater_value - wyon_value
                )

            # Two-step decomposition:
            # (1) Nayar pure-water equation vs Wyon pure-water equation.
            # (2) Nayar seawater vs Nayar pure-water at identical salinity.
            for output_name, attribute in PERCENT_METRICS:
                wyon_value = getattr(results["wyon"], attribute)
                pure_value = getattr(results["nayar_pure_water"], attribute)
                seawater_value = getattr(results["nayar_seawater"], attribute)
                row[f"nayar_pure_water_vs_wyon_{output_name}_change_pct"] = (
                    _relative_change_pct(pure_value, wyon_value)
                )
                row[f"nayar_seawater_vs_nayar_pure_water_{output_name}_change_pct"] = (
                    _relative_change_pct(seawater_value, pure_value)
                )
                row[f"nayar_seawater_vs_wyon_{output_name}_change_pct"] = (
                    _relative_change_pct(seawater_value, wyon_value)
                )
            rows.append(row)

    csv_path = output_dir / "nayar_wyon_temperature_salinity_sweep.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    manifest: dict[str, object] = {
        "experiment_id": "NAYAR-WYON-TEMP-SALINITY-DECOMPOSITION-2026-11-06",
        "row_count": len(rows),
        "feed_temperatures_c": list(FEED_TEMPERATURES_C),
        "feed_reference_salinity_g_kg": list(FEED_SALINITIES_SR_G_KG),
        "fixed_case": FIXED_CASE,
        "three_model_decomposition": {
            "wyon": "Wyon 2025 pure-water vapour pressure on feed, permeate, and mean-pore terms.",
            "nayar_pure_water": "Nayar 2016 Eq. (6) pure-water vapour pressure on all three terms; diagnostic only.",
            "nayar_seawater": "Nayar 2016 Eq. (6) pure-water permeate and Eq. (5) natural-seawater feed/mean-pore terms.",
            "first_contrast": "Nayar pure-water diagnostic relative to Wyon isolates the pure-water reference-correlation difference.",
            "second_contrast": "Nayar natural seawater relative to Nayar pure-water isolates the salinity correction at the same channel salinity.",
        },
        "assumptions": [
            "Bulk feed Reference Salinity is used as a proxy for feed-interface salinity.",
            "The same bulk Reference Salinity is used for mean-pore vapour pressure in the seawater model.",
            "No concentration-polarization or axial module balance is solved.",
            "The Nayar pure-water-only mode is a diagnostic decomposition, not a seawater model.",
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
