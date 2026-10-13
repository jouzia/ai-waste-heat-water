"""Inspect WRI Aqueduct 4.0 geodatabase layer metadata through GDAL virtual HTTP ranges.

This step inventories layers and schemas only. It does not download the full
archive, extract the geodatabase, select sites, or claim geographic results.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path

ARCHIVE_URL = "https://files.wri.org/aqueduct/aqueduct-4-0-water-risk-data.zip"
GDB_IN_ARCHIVE = (
    "Aqueduct40_waterrisk_download_Y2023M07D05/GDB/"
    "Aq40_Y2023D07M05.gdb"
)
VSI_GDB_PATH = f"/vsizip//vsicurl/{ARCHIVE_URL}/{GDB_IN_ARCHIVE}"


def inspect_layers() -> dict[str, object]:
    try:
        import pyogrio
    except ImportError as exc:
        raise RuntimeError("Install pyogrio with: python -m pip install pyogrio") from exc

    os.environ.setdefault("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".zip,.gdbtable,.gdbtablx,.gdbindexes,.spx")
    layers_raw = pyogrio.list_layers(VSI_GDB_PATH)
    layers: list[dict[str, object]] = []
    for item in layers_raw:
        name = str(item[0])
        geometry_type = None if item[1] is None else str(item[1])
        try:
            info = pyogrio.read_info(VSI_GDB_PATH, layer=name)
            layers.append(
                {
                    "name": name,
                    "geometry_type_from_list": geometry_type,
                    "feature_count": int(info["features"]),
                    "geometry_type": info["geometry_type"],
                    "crs": info["crs"],
                    "fields": [str(value) for value in info["fields"]],
                    "dtypes": [str(value) for value in info["dtypes"]],
                    "total_bounds": [
                        float(value) for value in info["total_bounds"]
                    ] if info.get("total_bounds") is not None else None,
                    "fid_column": info.get("fid_column"),
                    "geometry_name": info.get("geometry_name"),
                }
            )
        except Exception as exc:  # Preserve per-layer errors as evidence.
            layers.append(
                {
                    "name": name,
                    "geometry_type_from_list": geometry_type,
                    "metadata_error": f"{type(exc).__name__}: {exc}",
                }
            )
    return {
        "dataset": "WRI Aqueduct 4.0 Current and Future Global Maps Data",
        "source_page": "https://www.wri.org/data/aqueduct-global-maps-40-data",
        "archive_url": ARCHIVE_URL,
        "archive_member_geodatabase": GDB_IN_ARCHIVE,
        "vsi_path": VSI_GDB_PATH,
        "inspected_at_utc": datetime.now(UTC).isoformat(),
        "layers": layers,
        "layer_count": len(layers),
        "data_policy": (
            "Metadata inspection only through GDAL virtual filesystem. No complete "
            "archive download or site-level indicator extraction has been performed."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/aqueduct_discovery/aqueduct_geodatabase_layers.json"),
    )
    args = parser.parse_args()
    result = inspect_layers()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({"layer_count": result["layer_count"], "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
