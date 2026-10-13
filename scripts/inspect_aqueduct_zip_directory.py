"""Inspect the central directory of the official Aqueduct ZIP via HTTP range requests.

Only archive metadata and small byte ranges are fetched. The full 261 MB dataset
is not downloaded by this script. The URL was discovered on the official WRI
dataset landing page and is pinned here with source provenance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from zipfile import ZipFile

SOURCE_PAGE = "https://www.wri.org/data/aqueduct-global-maps-40-data"
SOURCE_URL = "https://files.wri.org/aqueduct/aqueduct-4-0-water-risk-data.zip"
CHUNK_SIZE = 4 * 1024 * 1024


def remote_size(url: str) -> dict[str, object]:
    request = Request(
        url,
        method="HEAD",
        headers={"User-Agent": "ai-waste-heat-water/1.0 (research archive inventory)"},
    )
    with urlopen(request, timeout=60) as response:
        length = response.headers.get("Content-Length")
        if not length or not length.isdigit():
            raise RuntimeError("Source archive did not provide a numeric Content-Length")
        if response.headers.get("Accept-Ranges", "").lower() != "bytes":
            raise RuntimeError("Source archive does not advertise HTTP byte ranges")
        return {
            "size_bytes": int(length),
            "content_type": response.headers.get("Content-Type", ""),
            "last_modified": response.headers.get("Last-Modified"),
            "etag": response.headers.get("ETag"),
            "accept_ranges": response.headers.get("Accept-Ranges"),
            "final_url": response.geturl(),
        }


class RangeReader:
    """Minimal seekable read-only file object backed by HTTP byte-range requests."""

    def __init__(
        self,
        url: str,
        size: int,
        *,
        fetch_range: Callable[[int, int], bytes] | None = None,
        chunk_size: int = CHUNK_SIZE,
    ) -> None:
        self.url = url
        self.size = size
        self.position = 0
        self.fetch_range = fetch_range or self._fetch_range
        self.chunk_size = chunk_size
        self.cache_start = -1
        self.cache = b""

    def _fetch_range(self, start: int, end: int) -> bytes:
        request = Request(
            self.url,
            headers={
                "User-Agent": "ai-waste-heat-water/1.0 (research archive inventory)",
                "Range": f"bytes={start}-{end}",
            },
        )
        with urlopen(request, timeout=60) as response:
            if getattr(response, "status", 200) != 206:
                raise RuntimeError(
                    f"Expected HTTP 206 for range {start}-{end}, got {getattr(response, 'status', 200)}"
                )
            content_range = response.headers.get("Content-Range", "")
            if not content_range.startswith(f"bytes {start}-"):
                raise RuntimeError(f"Unexpected Content-Range header: {content_range!r}")
            return response.read()

    def seek(self, offset: int, whence: int = 0) -> int:
        if whence == 0:
            target = offset
        elif whence == 1:
            target = self.position + offset
        elif whence == 2:
            target = self.size + offset
        else:
            raise ValueError(f"Invalid whence: {whence}")
        if target < 0:
            raise ValueError("negative seek position")
        self.position = target
        return self.position

    def tell(self) -> int:
        return self.position

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def read(self, size: int = -1) -> bytes:
        if size == 0 or self.position >= self.size:
            return b""
        if size < 0:
            size = self.size - self.position
        remaining = min(size, self.size - self.position)
        pieces: list[bytes] = []
        while remaining > 0:
            cache_end = self.cache_start + len(self.cache)
            if not (self.cache_start <= self.position < cache_end):
                self.cache_start = self.position
                fetch_end = min(self.size - 1, self.cache_start + self.chunk_size - 1)
                self.cache = self.fetch_range(self.cache_start, fetch_end)
                if not self.cache:
                    break
                cache_end = self.cache_start + len(self.cache)
            available = min(remaining, cache_end - self.position)
            offset = self.position - self.cache_start
            pieces.append(self.cache[offset : offset + available])
            self.position += available
            remaining -= available
        return b"".join(pieces)

    def close(self) -> None:
        self.cache = b""


def inspect_zip(url: str = SOURCE_URL) -> dict[str, object]:
    metadata = remote_size(url)
    reader = RangeReader(url, int(metadata["size_bytes"]))
    try:
        with ZipFile(reader) as archive:
            entries = [
                {
                    "path": info.filename,
                    "uncompressed_size_bytes": info.file_size,
                    "compressed_size_bytes": info.compress_size,
                    "compression": info.compress_type,
                    "is_directory": info.is_dir(),
                    "suffix": Path(info.filename).suffix.lower(),
                }
                for info in archive.infolist()
            ]
    finally:
        reader.close()

    return {
        "dataset": "WRI Aqueduct 4.0 Current and Future Global Maps Data",
        "source_page": SOURCE_PAGE,
        "source_archive_url": url,
        "retrieved_at_utc": datetime.now(UTC).isoformat(),
        "archive_metadata": metadata,
        "archive_sha256": None,
        "archive_sha256_note": (
            "The full archive was not downloaded; the archive hash is intentionally null. "
            "The ETag is recorded as an HTTP validator, not misrepresented as a SHA-256."
        ),
        "directory_entry_count": len(entries),
        "entries": entries,
        "source_policy": [
            "Only HTTP byte ranges needed to inspect the ZIP central directory were requested.",
            "No data layer was extracted or interpreted.",
            "The archive URL is linked from the official WRI landing page; verify version and license before using the data.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("artifacts/aqueduct_discovery/aqueduct_zip_directory.json"),
    )
    args = parser.parse_args()
    result = inspect_zip()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "archive_size_bytes": result["archive_metadata"]["size_bytes"],
        "directory_entry_count": result["directory_entry_count"],
        "output": str(args.output),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
