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

\n\ndef test_ali_observation_ledger_export_preserves_sheet_and_row_locator(tmp_path: Path) -> None:
    openpyxl = pytest.importorskip("openpyxl")
    source_dir = tmp_path / "source"
    source_dir.mkdir()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "50"
    sheet.append(["time", "Thin", "mw"])
    sheet.append([0, 21.0, 0])
    sheet.append([0.1666667, 21.1, 0.2])
    second = workbook.create_sheet("80R")
    second.append(["time", "Thin"])
    second.append([0, 20.0])
    workbook.save(source_dir / "S1_Data.xlsx")
    for filename in _downloader.WORKBOOKS[1:]:
        wb = openpyxl.Workbook()
        wb.active.title = "test"
        wb.active.append(["value"])
        wb.active.append([1])
        wb.save(source_dir / filename)

    module_path = Path(__file__).resolve().parents[1] / "scripts" / "extract_ali_2020_observation_ledger.py"
    spec = importlib.util.spec_from_file_location("ali_ledger_exporter", module_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    manifest = module.export_workbooks(source_dir, tmp_path / "out")
    assert manifest["total_nonempty_rows_exported"] == 7
    import csv
    with (tmp_path / "out" / "ali_2020_raw_observation_ledger.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert rows[0]["worksheet"] == "50"
    assert rows[0]["excel_row_1based"] == "2"
    assert rows[0]["source_sha256"]
