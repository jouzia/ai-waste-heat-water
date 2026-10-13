"""Discover official Aqueduct 4.0 downloadable assets without guessing file URLs.

The script retrieves only the WRI landing page, records its checksum and
candidate linked assets, and does not download large geospatial datasets. It
is a source-discovery step, not a geographic analysis.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

SOURCE_URLS = (
    "https://datasets.wri.org/datasets/aqueduct-global-maps-40-data",
    "https://www.wri.org/data/aqueduct-global-maps-40-data",
)
DATA_EXTENSIONS = (
    ".zip", ".gpkg", ".shp", ".geojson", ".tif", ".tiff", ".csv", ".xlsx", ".geopackage"
)
LINK_KEYWORDS = ("download", "attachment", "asset", "file", "aqueduct", "dataset")


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[dict[str, str]] = []
        self.title_parts: list[str] = []
        self.in_title = False
        self.current_anchor_index: int | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag in {"a", "link"} and attributes.get("href"):
            self.links.append(
                {
                    "tag": tag,
                    "href": str(attributes["href"]),
                    "text": "",
                    "rel": str(attributes.get("rel") or ""),
                }
            )
            if tag == "a":
                self.current_anchor_index = len(self.links) - 1

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data.strip())
        if self.current_anchor_index is not None:
            self.links[self.current_anchor_index]["text"] += data.strip()

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.in_title = False
        if tag == "a":
            self.current_anchor_index = None


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def candidate_links(page_url: str, links: list[dict[str, str]]) -> list[dict[str, str]]:
    candidates: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in links:
        href = urljoin(page_url, item["href"])
        parsed = urlparse(href)
        if parsed.scheme not in {"http", "https"}:
            continue
        lower_path = parsed.path.lower()
        lower_text = f"{item['href']} {item['text']}".lower()
        same_source_family = (
            parsed.netloc.lower() == "wri.org"
            or parsed.netloc.lower().endswith(".wri.org")
        )
        looks_like_data = lower_path.endswith(DATA_EXTENSIONS) or any(
            keyword in lower_text for keyword in LINK_KEYWORDS
        )
        if same_source_family and looks_like_data and href not in seen:
            seen.add(href)
            candidates.append(
                {
                    "url": href,
                    "link_text": item["text"][:240],
                    "tag": item["tag"],
                    "rel": item["rel"],
                    "file_extension": Path(parsed.path).suffix.lower(),
                }
            )
    return candidates


def fetch_page(url: str) -> dict[str, object]:
    request = Request(
        url,
        headers={"User-Agent": "ai-waste-heat-water/1.0 (research source discovery)"},
    )
    with urlopen(request, timeout=60) as response:
        body = response.read()
        final_url = response.geturl()
        content_type = response.headers.get("Content-Type", "")
        status = getattr(response, "status", 200)
    parser = PageParser()
    parser.feed(body.decode("utf-8", errors="replace"))
    assets = candidate_links(final_url, parser.links)
    return {
        "requested_url": url,
        "final_url": final_url,
        "http_status": status,
        "content_type": content_type,
        "page_title": " ".join(part for part in parser.title_parts if part),
        "page_sha256": sha256_bytes(body),
        "page_bytes": len(body),
        "candidate_asset_links": assets,
        "candidate_asset_link_count": len(assets),
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
    }


def discover(output_path: Path) -> dict[str, object]:
    pages: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []
    for url in SOURCE_URLS:
        try:
            pages.append(fetch_page(url))
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            errors.append({"url": url, "error": f"{type(exc).__name__}: {exc}"})
    if not pages:
        raise RuntimeError(f"Could not retrieve either official WRI landing page: {errors}")

    candidate_urls = sorted(
        {
            str(item["url"])
            for page in pages
            for item in page["candidate_asset_links"]
        }
    )
    manifest: dict[str, object] = {
        "dataset": "WRI Aqueduct Global Maps 4.0",
        "license_claim_in_project_docs": "CC BY 4.0; confirm on retrieved source page before redistribution",
        "source_urls": list(SOURCE_URLS),
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        "pages": pages,
        "candidate_asset_url_count": len(candidate_urls),
        "candidate_asset_urls": candidate_urls,
        "errors": errors,
        "status": "landing_page_retrieved_assets_need_manual_verification" if candidate_urls else "landing_page_retrieved_no_candidate_asset_links",
        "next_step": (
            "Verify asset metadata, file size, version, licence and download terms; then acquire only the needed versioned layers."
        ),
        "not_an_analysis": (
            "No raster/vector data were downloaded or interpreted. No site water-stress value has been generated."
        ),
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=Path("artifacts/aqueduct_discovery/aqueduct_asset_discovery.json")
    )
    args = parser.parse_args()
    result = discover(args.output)
    print(json.dumps({
        "status": result["status"],
        "pages_retrieved": len(result["pages"]),
        "candidate_asset_url_count": result["candidate_asset_url_count"],
        "output": str(args.output),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
