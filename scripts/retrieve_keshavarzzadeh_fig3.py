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
    source_copy = target.with_name(target.stem + "_source_payload.bin")
    source_temporary = source_copy.with_suffix(source_copy.suffix + ".part")
    request = Request(
        FIGURE_URL,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; ai-waste-heat-water/1.0)",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        },
    )
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            from PIL import Image, UnidentifiedImageError

            with urlopen(request, timeout=90) as response:
                content_type = response.headers.get("Content-Type", "")
                response_url = response.geturl()
                payload = response.read()
            source_temporary.write_bytes(payload)
            try:
                with Image.open(source_temporary) as source_image:
                    source_format = source_image.format or "unknown"
                    source_image.verify()
                with Image.open(source_temporary) as source_image:
                    width, height = source_image.size
                    mode = source_image.mode
                    normalized_mode = "RGBA" if mode in ("RGBA", "LA") else "RGB"
                    source_image.convert(normalized_mode).save(
                        temporary, format="PNG", optimize=False
                    )
            except (UnidentifiedImageError, OSError) as exc:
                prefix = payload[:100].decode("utf-8", errors="replace")
                raise ValueError(
                    f"Endpoint did not return a recognizable image; "
                    f"content_type={content_type!r}, bytes={len(payload)}, prefix={prefix!r}"
                ) from exc
            temporary.replace(target)
            source_temporary.replace(source_copy)
            return {
                "status": "retrieved_and_image_verified",
                "file_name": target.name,
                "size_bytes": target.stat().st_size,
                "sha256": sha256_file(target),
                "source_payload_file": source_copy.name,
                "source_payload_size_bytes": source_copy.stat().st_size,
                "source_payload_sha256": sha256_file(source_copy),
                "source_payload_content_type": content_type,
                "source_payload_format": source_format,
                "response_url": response_url,
                "width_px": width,
                "height_px": height,
                "mode": mode,
            }
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            last_error = exc
            temporary.unlink(missing_ok=True)
            source_temporary.unlink(missing_ok=True)
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
