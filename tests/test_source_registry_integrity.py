"""Guard the scientific source registry against metadata regressions."""

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "SOURCES.yaml"


def load_sources() -> dict[str, dict[str, object]]:
    """Load the source registry and reject duplicate or incomplete critical IDs."""
    registry = yaml.safe_load(SOURCE_PATH.read_text(encoding="utf-8"))
    records = registry["sources"]
    ids = [record["id"] for record in records]
    assert len(ids) == len(set(ids)), "SOURCES.yaml contains duplicate source IDs"
    return {record["id"]: record for record in records}


def test_critical_source_records_retain_provenance_metadata() -> None:
    sources = load_sources()
    required_ids = {
        "MD-DCMD-PRIMARY-1999",
        "MD-DCMD-CHANNEL-2020",
        "CEEW-INDIA-THERMAL-WATER-FACTORS-2017",
        "CEA-ANNUAL-REPORT-2024-25",
        "CSE-WATER-INEFFICIENT-POWER-2021",
        "NREL-OPENEI-OPERATIONAL-WATER-FACTORS",
        "CEA-CLEAN-ENERGY-DIVISION-PAGE",
        "CEA-PUBLIC-REPORT-ARCHIVE",
        "CAG-NLC-OPERATIONAL-PERFORMANCE-2025",
        "MD-DCMD-POLARIZATION-2000",
        "MD-DCMD-POLARIZATION-1998",
        "NNTPS-ENVIRONMENTAL-STATEMENT-FY2021-22",
        "RS-AU480-ANNEXURE-II-2024",
    }

    assert required_ids.issubset(sources)
    for source_id in required_ids:
        record = sources[source_id]
        assert record.get("role") in {"A", "B", "C", "D"}, source_id
        assert record.get("url"), source_id
        assert record.get("status"), source_id
        assert record.get("used_for"), source_id


def test_primary_1999_source_is_not_misrepresented_as_extracted_validation_data() -> None:
    record = load_sources()["MD-DCMD-PRIMARY-1999"]
    status = str(record["status"]).lower()

    assert "raw observations not retrieved" in status
    assert "validation remain blocked" in status
    assert "primary-validation-source" not in status


def test_cea_and_ceew_source_urls_match_their_registry_identity() -> None:
    sources = load_sources()

    assert "cea.nic.in" in str(sources["CEA-ANNUAL-REPORT-2024-25"]["url"])
    assert "ceew.in" in str(sources["CEEW-INDIA-THERMAL-WATER-FACTORS-2017"]["url"])
