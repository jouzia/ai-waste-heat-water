import json
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
INSPECTOR = ROOT / "scripts" / "inspect_ali_supplements.py"


def _make_minimal_xlsx(path: Path) -> None:
    workbook = """<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
        xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
        <sheets><sheet name="Measured mass" sheetId="1" r:id="rId1"/></sheets>
    </workbook>"""
    relationships = """<Relationships
        xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
        <Relationship Id="rId1"
        Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"
        Target="worksheets/sheet1.xml"/>
    </Relationships>"""
    with ZipFile(path, "w") as archive:
        archive.writestr("xl/workbook.xml", workbook)
        archive.writestr("xl/_rels/workbook.xml.rels", relationships)
        archive.writestr("xl/worksheets/sheet1.xml", "<worksheet/>")


def test_supplement_inspector_records_hash_and_sheet_names(tmp_path: Path) -> None:
    input_dir = tmp_path / "supplements"
    input_dir.mkdir()
    workbook = input_dir / "S1_Data.xlsx"
    _make_minimal_xlsx(workbook)
    output = tmp_path / "manifest.json"

    subprocess.run(
        [
            sys.executable,
            str(INSPECTOR),
            "--input-dir",
            str(input_dir),
            "--output",
            str(output),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    manifest = json.loads(output.read_text(encoding="utf-8"))
    assert manifest["source_doi"] == "10.1371/journal.pone.0230207"
    assert len(manifest["files"]) == 1
    assert manifest["files"][0]["filename"] == "S1_Data.xlsx"
    assert len(manifest["files"][0]["sha256"]) == 64
    assert manifest["files"][0]["worksheets"][0]["name"] == "Measured mass"
    assert "Metadata-only" in manifest["scope_note"]


def test_supplement_inspector_rejects_empty_directory(tmp_path: Path) -> None:
    input_dir = tmp_path / "empty"
    input_dir.mkdir()
    output = tmp_path / "manifest.json"

    result = subprocess.run(
        [
            sys.executable,
            str(INSPECTOR),
            "--input-dir",
            str(input_dir),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "No XLSX/XLSM files found" in result.stderr
    assert not output.exists()



def test_supplement_inspector_reports_invalid_workbook(tmp_path: Path) -> None:
    input_dir = tmp_path / "invalid"
    input_dir.mkdir()
    (input_dir / "broken.xlsx").write_bytes(b"not a zip archive")
    output = tmp_path / "manifest.json"

    result = subprocess.run(
        [
            sys.executable,
            str(INSPECTOR),
            "--input-dir",
            str(input_dir),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "File is not a zip file" in result.stderr
    assert not output.exists()
