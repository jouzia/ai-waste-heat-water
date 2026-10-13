"""Sample WRI Aqueduct baseline/future water-risk polygons at explicit city-centroid proxies.

All coordinates are illustrative city proxies, not real data-centre locations.
Water-stress indicators are reported as context and are never multiplied into
physical water-consumption volumes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ARCHIVE_URL = "https://files.wri.org/aqueduct/aqueduct-4-0-water-risk-data.zip"
GDB_MEMBER = (
    "Aqueduct40_waterrisk_download_Y2023M07D05/GDB/"
    "Aq40_Y2023D07M05.gdb"
)
VSI_GDB_PATH = f"/vsizip//vsicurl/{ARCHIVE_URL}/{GDB_MEMBER}"
BASELINE_FIELDS = [
    "pfaf_id", "gid_0", "name_0", "name_1", "area_km2",
    "bws_score", "bws_cat", "bws_label",
    "bwd_score", "bwd_cat", "bwd_label",
    "iav_score", "iav_cat", "iav_label",
    "sev_score", "sev_cat", "sev_label",
]
FUTURE_FIELDS = ["pfaf_id"]
for scenario in ("bau", "opt", "pes"):
    for year in (30, 50, 80):
        prefix = f"{scenario}{year}_ws_x"
        FUTURE_FIELDS.extend([f"{prefix}_r", f"{prefix}_s", f"{prefix}_c", f"{prefix}_l"])


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_sites(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError(f"No sites found in {path}")
    required = {"site_id", "city_proxy", "country", "latitude", "longitude", "coordinate_provenance"}
    for row in rows:
        missing = required.difference(row)
        if missing:
            raise ValueError(f"Missing site fields {sorted(missing)} in {row}")
    return rows


def _read_candidate_polygons(
    geopandas: Any,
    *,
    layer: str,
    columns: list[str],
    latitude: float,
    longitude: float,
) -> Any:
    last_frame = None
    for radius in (0.1, 0.5, 2.0, 5.0):
        bbox = (
            longitude - radius,
            latitude - radius,
            longitude + radius,
            latitude + radius,
        )
        frame = geopandas.read_file(
            VSI_GDB_PATH,
            layer=layer,
            columns=columns,
            bbox=bbox,
            engine="pyogrio",
        )
        last_frame = frame
        if not frame.empty:
            return frame
    return last_frame


def sample_layer(
    geopandas: Any,
    shapely_point: Any,
    *,
    layer: str,
    columns: list[str],
    latitude: float,
    longitude: float,
) -> tuple[dict[str, object], str]:
    frame = _read_candidate_polygons(
        geopandas,
        layer=layer,
        columns=columns,
        latitude=latitude,
        longitude=longitude,
    )
    if frame is None or frame.empty:
        return {}, "no_candidate_polygon_in_expanding_bbox"
    point = shapely_point(longitude, latitude)
    matched = frame[frame.geometry.covers(point)]
    if matched.empty:
        return {}, "candidate_polygons_found_but_point_not_covered"
    if len(matched) > 1:
        matched = matched.assign(_geometry_area=matched.geometry.area).sort_values(
            "_geometry_area"
        )
    record = matched.iloc[0]
    attributes: dict[str, object] = {}
    for column in columns:
        value = record.get(column)
        if value is None:
            attributes[column] = None
        elif hasattr(value, "item"):
            value = value.item()
            attributes[column] = None if isinstance(value, float) and not math.isfinite(value) else value
        elif isinstance(value, float) and not __import__("math").isfinite(value):
            attributes[column] = None
        else:
            attributes[column] = value
    return attributes, "matched"


def extract(site_path: Path, output_dir: Path) -> dict[str, object]:
    try:
        import geopandas
        from shapely.geometry import Point
    except ImportError as exc:
        raise RuntimeError("Install geographic dependencies with: python -m pip install geopandas pyogrio") from exc

    os.environ.setdefault(
        "CPL_VSIL_CURL_ALLOWED_EXTENSIONS",
        ".zip,.gdbtable,.gdbtablx,.gdbindexes,.spx",
    )
    sites = load_sites(site_path)
    records: list[dict[str, object]] = []
    for site in sites:
        latitude = float(site["latitude"])
        longitude = float(site["longitude"])
        baseline, baseline_status = sample_layer(
            geopandas,
            Point,
            layer="baseline_annual",
            columns=BASELINE_FIELDS,
            latitude=latitude,
            longitude=longitude,
        )
        future, future_status = sample_layer(
            geopandas,
            Point,
            layer="future_annual",
            columns=FUTURE_FIELDS,
            latitude=latitude,
            longitude=longitude,
        )
        record: dict[str, object] = {
            **site,
            "latitude": latitude,
            "longitude": longitude,
            "aqueduct_archive_url": ARCHIVE_URL,
            "baseline_layer": "baseline_annual",
            "baseline_match_status": baseline_status,
            "baseline_pfaf_id": baseline.get("pfaf_id"),
            "baseline_country_code": baseline.get("gid_0"),
            "baseline_country_name": baseline.get("name_0"),
            "baseline_admin1_name": baseline.get("name_1"),
            "baseline_area_km2": baseline.get("area_km2"),
            "future_layer": "future_annual",
            "future_match_status": future_status,
            "future_pfaf_id": future.get("pfaf_id"),
            "water_stress_interpretation": (
                "BWS is a basin-level water-stress indicator, not a water volume. "
                "It is reported as contextual metadata and does not scale net-water accounting."
            ),
        }
        for field in BASELINE_FIELDS:
            if field not in {"pfaf_id", "gid_0", "name_0", "name_1", "area_km2"}:
                record[f"baseline_{field}"] = baseline.get(field)
        for field in FUTURE_FIELDS:
            if field != "pfaf_id":
                record[f"future_{field}"] = future.get(field)
        records.append(record)

    output_dir.mkdir(parents=True, exist_ok=True)
    sites_sha = sha256_file(site_path)
    csv_path = output_dir / "aqueduct_city_proxy_water_stress.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

    manifest = {
        "dataset": "WRI Aqueduct 4.0 Current and Future Global Maps Data",
        "source_page": "https://www.wri.org/data/aqueduct-global-maps-40-data",
        "archive_url": ARCHIVE_URL,
        "archive_member_geodatabase": GDB_MEMBER,
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        "site_input_file": str(site_path),
        "site_input_sha256": sites_sha,
        "site_count": len(sites),
        "baseline_matched_count": sum(row["baseline_match_status"] == "matched" for row in records),
        "future_matched_count": sum(row["future_match_status"] == "matched" for row in records),
        "site_status": {str(row["site_id"]): {
            "baseline": row["baseline_match_status"],
            "future": row["future_match_status"],
            "baseline_pfaf_id": row["baseline_pfaf_id"],
            "future_pfaf_id": row["future_pfaf_id"],
        } for row in records},
        "output_file": csv_path.name,
        "output_sha256": sha256_file(csv_path),
        "limitations": [
            "City-centroid proxies are illustrative and are not actual data-centre site coordinates.",
            "Baseline and future annual layers have different feature counts/resolution; their basin IDs are recorded separately and are not assumed identical.",
            "Future scenario codes are retained exactly as source fields; interpretation must be checked against the dataset README before publication.",
            "Water stress is contextual and is not multiplied into physical consumption volumes.",
            "No electricity-water consumption factor is included in this extraction; geography gate remains incomplete until grid-water and carbon factors are sourced and joined.",
        ],
    }
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sites", type=Path, default=Path("data/geography/site_proxies.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/aqueduct_sites"))
    args = parser.parse_args()
    result = extract(args.sites, args.output_dir)
    print(json.dumps({
        "site_count": result["site_count"],
        "baseline_matched_count": result["baseline_matched_count"],
        "future_matched_count": result["future_matched_count"],
        "output_file": result["output_file"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
