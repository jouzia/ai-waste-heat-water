import importlib.util
import sys
from pathlib import Path


def _load_publication_gate():
    path = Path(__file__).resolve().parents[1] / "scripts" / "publication_gate.py"
    spec = importlib.util.spec_from_file_location("publication_gate_module", path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load publication gate from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_gate = _load_publication_gate()


def test_publication_gate_fails_when_project_is_incomplete() -> None:
    status = {
        "status": "INCOMPLETE",
        "gates": {"software_correctness": True, "independent_validation": False},
        "claim_policy": {"publication_ready_claim": False},
    }
    failures = _gate._status_failures(status)
    assert any("expected 'COMPLETE'" in failure for failure in failures)
    assert any("independent_validation" in failure for failure in failures)


def test_publication_gate_fails_if_any_gate_is_false_even_when_status_says_complete() -> None:
    status = {
        "status": "COMPLETE",
        "gates": {"software_correctness": True, "independent_validation": False},
        "claim_policy": {"publication_ready_claim": False},
    }
    failures = _gate._status_failures(status)
    assert len(failures) == 1
    assert "independent_validation" in failures[0]


def test_publication_gate_accepts_only_complete_true_gates() -> None:
    status = {
        "status": "COMPLETE",
        "gates": {"software_correctness": True, "independent_validation": True},
        "claim_policy": {"publication_ready_claim": False},
    }
    assert _gate._status_failures(status) == []
