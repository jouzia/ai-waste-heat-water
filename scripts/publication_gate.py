"""Publication-readiness gate.

This script intentionally fails while any mandatory scientific gate remains
unmet. It is a claim-control mechanism, not a quality score.
"""


def _root():
    from pathlib import Path

    return Path(__file__).resolve().parents[1]


def _load(path: str):
    import yaml

    root = _root()
    return yaml.safe_load((root / path).read_text(encoding="utf-8"))


REQUIRED_GATE_NAMES = frozenset(
    {
        "software_correctness",
        "open_data_access_verified",
        "source_reconstruction",
        "primary_observation_extraction",
        "unfitted_validation",
        "held_out_validation",
        "model_form_comparison",
        "cooling_architecture_scenarios",
        "time_varying_workload_coupling",
        "monte_carlo_convergence",
        "global_sensitivity_execution",
        "break_even_failure_envelope",
        "geographic_integration",
        "counterfactual_net_water_accounting",
        "multi_objective_analysis",
        "reproducibility_package",
        "manuscript_and_supplement",
        "final_publication_audit",
    }
)


def _status_failures(status: dict) -> list[str]:
    """Return hard-gate failures; protocol presence alone is never readiness."""
    failures: list[str] = []
    if status.get("status") != "COMPLETE":
        failures.append(
            f"final gate status is {status.get('status')!r}, expected 'COMPLETE'"
        )
    gates = status.get("gates")
    if not isinstance(gates, dict) or not gates:
        failures.append("final gate status has no scientific gate mapping")
    else:
        missing = sorted(REQUIRED_GATE_NAMES.difference(gates))
        unexpected = sorted(set(gates).difference(REQUIRED_GATE_NAMES))
        if missing:
            failures.append("missing required scientific gates: " + ", ".join(missing))
        if unexpected:
            failures.append("unexpected scientific gates: " + ", ".join(unexpected))
        incomplete = sorted(
            name for name in REQUIRED_GATE_NAMES.intersection(gates)
            if gates[name] is not True
        )
        if incomplete:
            failures.append("unmet scientific gates: " + ", ".join(incomplete))
    claim_policy = status.get("claim_policy", {})
    if claim_policy.get("publication_ready_claim") is True and (
        status.get("status") != "COMPLETE"
        or not isinstance(gates, dict)
        or any(value is not True for value in gates.values())
    ):
        failures.append(
            "publication_ready_claim cannot be true while any scientific gate is unmet"
        )
    return failures


def main() -> int:
    failures: list[str] = []
    final_status = _load("05_validation/FINAL_GATE_STATUS.yaml")
    failures.extend(_status_failures(final_status))

    registry = _load("04_experiments/BENCHMARK_REGISTRY.yaml")
    matrix = _load("04_experiments/VALIDATION_MATRIX.yaml")
    for case in registry.get("cases", []):
        status = case.get("validation_status")
        if status == "validated_held_out":
            bench = case.get("benchmark_file")
            if not bench:
                failures.append(f"{case['source_id']}: held-out case has no benchmark file")
            else:
                ledger = _root() / bench.replace(".yaml", "_observations.yaml")
                if not ledger.exists():
                    failures.append(f"{case['source_id']}: observation ledger missing")

    for case in matrix.get("cases", []):
        if case.get("quantitative_claim") is True:
            failures.append(
                f"{case['source_id']}: quantitative_claim must remain false until validation gate passes"
            )

    required_docs = [
        "docs/PRIMARY_SOURCE_VALIDATION_GATE.md",
        "docs/UNCERTAINTY_PLAN.md",
        "docs/GLOBAL_SENSITIVITY_PROTOCOL.md",
        "docs/GEOGRAPHIC_LAYER.md",
        "10_manuscript/MANUSCRIPT_PLAN.md",
    ]
    root = _root()
    for path in required_docs:
        if not (root / path).exists():
            failures.append(f"missing required protocol: {path}")

    if failures:
        print("PUBLICATION GATE: NOT READY")
        for item in failures:
            print(f"- {item}")
        return 1

    print("PUBLICATION GATE: READY FOR FINAL AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
