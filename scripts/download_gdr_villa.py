"""Download licensed GDR membrane-distillation benchmark files with checksums.

The files remain local and are not committed to the repository. The source page
identifies the collection as CC BY 4.0; cite the dataset and record modifications.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SOURCE_DOI = "10.15121/1452747"
SOURCE_PAGE = "https://gdr.openei.org/submissions/1016"
LICENSE_URL = "https://creativecommons.org/licenses/by/4.0/"

DATASETS = {
    "3m-countercurrent": {
        "filename": "3M 0.2 Micron Plate and Frame Countercurrent DCMD.xls",
        "url": "https://gdr.openei.org/files/1016/Countercurrent%20DCMD%203M%200.231m%5E2%201%20LPM%204g%20NaCl_08.11.2017.xls",
        "configuration": "plate-and-frame counter-current DCMD",
        "membrane_area_m2": 0.231,
        "flow_lpm": 1.0,
    },
    "aquastill-plate-countercurrent": {
        "filename": "Aquastill 0.3 Micron Plate and Frame Counter-Current DCMD.xls",
        "url": "https://gdr.openei.org/files/1016/Countercurrent%20DCMD%20Aquastill%200.231m%5E2%201%20LPM%204g%20NaCl_8.10.17.xls",
        "configuration": "plate-and-frame counter-current DCMD",
        "membrane_area_m2": 0.231,
        "flow_lpm": 1.0,
    },
    "aquastill-spiral-countercurrent": {
        "filename": "Aquastill 0.3 Micron Spiral Wound Countercurrent DCMD.xls",
        "url": "https://gdr.openei.org/files/1016/Countercurrent%20Spiral%20DCMD%20Aquastill%203.6m%5E2%2013.5LPM_4g%20NaCl%2007.27.2017.xls",
        "configuration": "spiral-wound counter-current DCMD",
        "membrane_area_m2": 3.6,
        "flow_lpm": 13.5,
    },
    "aquastill-polyethylene-spiral": {
        "filename": "Aquastill Polyethylene Spiral Wound Countercurrent DCMD.xls",
        "url": "https://gdr.openei.org/files/1016/Countercurrent%20DCMD%20Aquastill%200.692%20m%5E2%201%20LPM%204g%20NaCl_low.xls",
        "configuration": "polyethylene spiral-wound counter-current DCMD",
        "membrane_area_m2": 0.692,
        "flow_lpm": 1.0,
    },
    "clarcor-air-gap": {
        "filename": "CLARCOR QL822 Flat Sheet Air-Gap MD.xls",
        "url": "https://gdr.openei.org/files/1016/Airgap%20CLARCOR%20QL822%200.14m%5E2%201.5LPM_4g%20NaCl%2005.15.2017.xls",
        "configuration": "flat-sheet air-gap MD",
        "membrane_area_m2": 0.14,
        "flow_lpm": 1.5,
    },
    "clarcor-cocurrent": {
        "filename": "CLARCOR QL822 Flat Sheet Cocurrent DCMD.xls",
        "url": "https://gdr.openei.org/files/1016/Cocurrent%20DCMD%20CLARCOR%20QL822%200.231m%5E2%201.5LPM_4g%20NaCl%2005.15.2017.xls",
        "configuration": "flat-sheet co-current DCMD",
        "membrane_area_m2": 0.231,
        "flow_lpm": 1.5,
    },
    "clarcor-countercurrent": {
        "filename": "CLARCOR QL822 Flat Sheet Counter-Current DCMD.xls",
        "url": "https://gdr.openei.org/files/1016/Countercurrent%20DCMD%20CLARCOR%20QL822%200.231m%5E2%201.5LPM_4g%20NaCl%2005.15.2017.xls",
        "configuration": "flat-sheet counter-current DCMD",
        "membrane_area_m2": 0.231,
        "flow_lpm": 1.5,
    },
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_file(url: str, target: Path, *, force: bool = False) -> dict[str, object]:
    if target.exists() and not force:
        return {
            "status": "already_present",
            "size_bytes": target.stat().st_size,
            "sha256": sha256_file(target),
        }

    partial = target.with_suffix(target.suffix + ".part")
    request = Request(
        url,
        headers={"User-Agent": "ai-waste-heat-water/1.0 (research data provenance)"},
    )
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            with urlopen(request, timeout=90) as response, partial.open("wb") as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
            partial.replace(target)
            return {
                "status": "downloaded",
                "size_bytes": target.stat().st_size,
                "sha256": sha256_file(target),
            }
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            last_error = exc
            partial.unlink(missing_ok=True)
            if attempt < 3:
                time.sleep(min(2**attempt, 20))
    raise RuntimeError(f"Could not download {url}: {last_error}") from last_error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset",
        choices=["all", *DATASETS],
        default="clarcor-countercurrent",
        help="Dataset to retrieve; use 'all' to download the full ~96 MB collection.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/raw/gdr_villa_2018"),
        help="Local directory for source workbooks (ignored by git).",
    )
    parser.add_argument("--force", action="store_true", help="Redownload existing files.")
    args = parser.parse_args()

    keys = list(DATASETS) if args.dataset == "all" else [args.dataset]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for key in keys:
        item = DATASETS[key]
        target = args.output_dir / item["filename"]
        result = download_file(item["url"], target, force=args.force)
        records.append(
            {
                "dataset_key": key,
                **item,
                "local_path": str(target),
                **result,
            }
        )
        print(f"{key}: {result['status']} ({result['size_bytes']} bytes)")

    manifest = {
        "source_doi": SOURCE_DOI,
        "source_page": SOURCE_PAGE,
        "license": "CC BY 4.0",
        "license_url": LICENSE_URL,
        "retrieval_manifest_created_at_utc": datetime.now(UTC).isoformat(),
        "files": records,
        "scope_note": (
            "Downloaded workbook bytes are not yet observations. Inspect worksheet "
            "names and separate Data-sheet measurements from Theoretical calculations "
            "before quantitative use."
        ),
    }
    manifest_path = args.output_dir / "download_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
