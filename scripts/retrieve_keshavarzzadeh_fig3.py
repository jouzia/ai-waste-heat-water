"""Retrieve and checksum the open-access Keshavarzzadeh et al. (2020) Figure 3 image.

Figure 3 is a secondary reproduction of experimental markers whose primary-source
crosswalk is unresolved. This script retrieves the figure only; it does not
digitize markers or turn the secondary image into primary observations.
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

SOURCE_DOI = "10.1038/s41598-020-73964-7"
FIGURE_URL = (
    "https://media.springernature.com/lw685/springer-static/image/"
    "art%3A10.1038%2Fs41598-020-73964-7/MediaObjects/"
    "41598_2020_73964_Fig3_HTML.png"
)
ARTICLE_URL = "https://www.nature.com/articles/s41598-020-73964-7"
LICENSE = "CC BY 4.0"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def retrieve_image(target: Path) -> dict[str, object]:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_suffix(target.suffix + ".part")
    request = Request(
        FIGURE_URL,
        headers={"User-Agent": "ai-waste-heat-water/1.0 (reproducible figure audit)"},
    )
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            with urlopen(request, timeout=90) as response, temporary.open("wb") as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
            with temporary.open("rb") as stream:
                signature = stream.read(8)
            if signature != b"\x89PNG\r\n\x1a\n":
                raise ValueError("Springer endpoint did not return a PNG image")
            from PIL import Image

            with Image.open(temporary) as image:
                image.verify()
            temporary.replace(target)
            with Image.open(target) as image:
                width, height = image.size
                mode = image.mode
            return {
                "status": "retrieved_and_image_verified",
                "file_name": target.name,
                "size_bytes": target.stat().st_size,
                "sha256": sha256_file(target),
                "width_px": width,
                "height_px": height,
                "mode": mode,
            }
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            last_error = exc
            temporary.unlink(missing_ok=True)
            if attempt < 3:
                time.sleep(min(2**attempt, 20))
    raise RuntimeError(f"Figure retrieval failed: {last_error}") from last_error


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/figure_digitization/keshavarzzadeh_2020_fig3.png"),
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("artifacts/figure_digitization/keshavarzzadeh_2020_fig3_manifest.json"),
    )
    args = parser.parse_args()
    result = retrieve_image(args.output)
    manifest = {
        "source_doi": SOURCE_DOI,
        "article_url": ARTICLE_URL,
        "figure": "Figure 3",
        "figure_url": FIGURE_URL,
        "license": LICENSE,
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        **result,
        "scientific_scope": (
            "Secondary-reproduced experimental markers. The figure caption's cited "
            "reference does not cleanly crosswalk to the 1999 primary source in the "
            "article bibliography. Do not label digitized points as independently "
            "verified primary observations or use them to claim independent validation."
        ),
    }
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
