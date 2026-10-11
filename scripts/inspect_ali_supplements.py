"""Create a provenance manifest for locally downloaded Ali et al. (2020) XLSX supplements.

This utility inspects workbook metadata only. It does not extract observations,
interpret plotted values, or treat source-model predictions as measurements.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile

SOURCE_DOI = "10.1371/journal.pone.0230207"
SOURCE_URL = "https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230207"
MAIN_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL_NS = {"rel": "http://schemas.openxmlformats.org/package/2006/relationships"}
OFFICE_REL_ID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect_xlsx(path: Path) -> dict[str, object]:
    """Return immutable-file metadata and worksheet names from an XLSX archive."""
    with ZipFile(path) as archive:
        workbook_root = ET.fromstring(archive.read("xl/workbook.xml"))
        rels_root = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        relationships = {
            item.attrib["Id"]: item.attrib["Target"]
            for item in rels_root.findall("rel:Relationship", REL_NS)
        }
        worksheets = []
        for sheet in workbook_root.findall("m:sheets/m:sheet", MAIN_NS):
            relationship_id = sheet.attrib.get(OFFICE_REL_ID)
            worksheets.append(
                {
                    "name": sheet.attrib["name"],
                    "target": relationships.get(relationship_id),
                }
            )

    return {
        "filename": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "worksheets": worksheets,
    }


def build_manifest(input_dir: Path) -> dict[str, object]:
    files = sorted(
        path for path in input_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".xlsx", ".xlsm"}
    )
    if not files:
        raise ValueError(f"No XLSX/XLSM files found in {input_dir}")

    inspected = [inspect_xlsx(path) for path in files]
    return {
        "source_doi": SOURCE_DOI,
        "source_url": SOURCE_URL,
        "retrieval_manifest_created_at_utc": datetime.now(UTC).isoformat(),
        "input_directory": str(input_dir),
        "files": inspected,
        "scope_note": (
            "Metadata-only manifest. Worksheet contents have not been extracted, "
            "classified as observations, or validated against the paper."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/raw/ali_2020"),
        help="Directory containing publisher-downloaded XLSX supplements.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/provenance/ali_2020_supplement_manifest.json"),
        help="Path for the generated JSON manifest.",
    )
    args = parser.parse_args()

    try:
        manifest = build_manifest(args.input_dir)
    except (OSError, ValueError, KeyError, ET.ParseError, BadZipFile) as exc:
        parser.error(str(exc))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote metadata manifest for {len(manifest['files'])} workbook(s): {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
