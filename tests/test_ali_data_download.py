import importlib.util
import sys
from pathlib import Path

import pytest


def _load_script():
    path = Path(__file__).resolve().parents[1] / "scripts" / "download_ali_2020_data.py"
    spec = importlib.util.spec_from_file_location("ali_2020_data_downloader", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load downloader from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_downloader = _load_script()


def test_ali_supporting_data_registry_has_five_distinct_cc_by_objects() -> None:
    assert len(_downloader.DATA_OBJECTS) == 5
    assert len({item["doi"] for item in _downloader.DATA_OBJECTS}) == 5
    assert [item["supporting_data_id"] for item in _downloader.DATA_OBJECTS] == [
        "S1", "S2", "S3", "S4", "S5"
    ]
    assert all(item["url"].startswith("https://journals.plos.org/plosone/article/file?") for item in _downloader.DATA_OBJECTS)


def test_existing_non_xlsx_payload_is_rejected(tmp_path: Path) -> None:
    target = tmp_path / "bad.xlsx"
    target.write_text("<html>not an XLSX</html>", encoding="utf-8")
    with pytest.raises(ValueError, match="not an XLSX"):
        _downloader.download_xlsx("https://example.invalid/file", target)
