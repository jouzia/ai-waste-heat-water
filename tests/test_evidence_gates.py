"""Evidence-gate regression tests for benchmark registry claims."""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "04_experiments" / "BENCHMARK_REGISTRY.yaml"
VALIDATED_STATES = {"validated_development", "validated_held_out"}


def test_empty_observation_ledger_cannot_be_marked_validated() -> None:
    """Keep software/model readiness separate from empirical validation readiness."""
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    cases = registry.get("cases", [])

    for case in cases:
        ledger_relative = case.get("observation_ledger")
        if not ledger_relative:
            continue

        ledger_path = ROOT / ledger_relative
        assert ledger_path.is_file(), (
            f"{case.get('source_id')} references missing observation ledger: "
            f"{ledger_relative}"
        )
        ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8")) or {}
        observations = ledger.get("observations") or []

        if not observations:
            assert case.get("validation_status") not in VALIDATED_STATES, (
                f"{case.get('source_id')} is marked validated but its observation "
                "ledger is empty."
            )


def test_registry_validation_states_are_declared() -> None:
    """Catch typos that could bypass the documented evidence-state vocabulary."""
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    declared = set((registry.get("status_definitions") or {}).keys())

    for case in registry.get("cases", []):
        status = case.get("validation_status")
        assert status in declared, (
            f"{case.get('source_id')} uses undeclared validation_status: {status!r}"
        )
