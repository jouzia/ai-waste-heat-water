import importlib.util
import sys
from pathlib import Path


def _load_module():
    path = Path(__file__).resolve().parents[1] / "scripts" / "discover_aqueduct_assets.py"
    spec = importlib.util.spec_from_file_location("aqueduct_discovery", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load discovery module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_discovery = _load_module()


def _load_zip_inspector():
    path = Path(__file__).resolve().parents[1] / "scripts" / "inspect_aqueduct_zip_directory.py"
    spec = importlib.util.spec_from_file_location("aqueduct_zip_inspector", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load ZIP inspector from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_zip_inspector = _load_zip_inspector()


def test_parser_records_title_and_anchor_text() -> None:
    parser = _discovery.PageParser()
    parser.feed(
        '<html><head><title>Aqueduct 4.0</title></head>'
        '<body><a href="/download/data.zip">Download archive</a>'
        '<a href="/about">About</a></body></html>'
    )
    assert "Aqueduct 4.0" in " ".join(parser.title_parts)
    assert parser.links[0]["text"] == "Download archive"
    assert parser.links[1]["text"] == "About"


def test_candidate_links_keep_wri_assets_and_skip_external_domains() -> None:
    links = [
        {"tag": "a", "href": "/files/aqueduct.zip", "text": "Download Aqueduct", "rel": ""},
        {"tag": "a", "href": "https://example.com/aqueduct.zip", "text": "external", "rel": ""},
        {"tag": "a", "href": "https://www.wri.org/data/aqueduct", "text": "Dataset page", "rel": ""},
    ]
    candidates = _discovery.candidate_links("https://datasets.wri.org/datasets/aqueduct", links)
    assert len(candidates) == 2
    assert candidates[0]["url"].startswith("https://datasets.wri.org/")
    assert candidates[1]["url"] == "https://www.wri.org/data/aqueduct"


def test_range_reader_can_list_local_zip_without_reading_full_archive() -> None:
    import io
    from zipfile import ZipFile

    payload = io.BytesIO()
    with ZipFile(payload, "w") as archive:
        archive.writestr("baseline/baseline_water_stress.tif", b"raster placeholder")
        archive.writestr("metadata/readme.txt", b"metadata")
    source_bytes = payload.getvalue()
    reader = _zip_inspector.RangeReader(
        "https://example.invalid/aqueduct.zip",
        len(source_bytes),
        fetch_range=lambda start, end: source_bytes[start : end + 1],
        chunk_size=64,
    )
    with ZipFile(reader) as archive:
        assert archive.namelist() == [
            "baseline/baseline_water_stress.tif",
            "metadata/readme.txt",
        ]
    reader.close()
