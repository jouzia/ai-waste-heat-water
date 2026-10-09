# Remaining work and effort estimate — 2026-10-09

## Status snapshot

This is a planning estimate, not a completion claim. The publication-critical scientific work is not complete.

From `05_validation/FINAL_GATE_STATUS.yaml`, 4 of 18 gates are marked true and 14 remain false. The true gates cover software correctness (previously recorded), public-source access verification, time-varying workload-coupling infrastructure, and counterfactual net-water accounting. These are not equivalent to a completed empirical study.

## Work packages and active effort

Estimates below are person-hours of focused work, assuming the original experimental files are accessible, parseable, and licensed for the intended use. They are not elapsed calendar hours and do not include waiting for external access, review, or new experiments.

| Work package | Estimated active hours | Dependency / exit criterion |
|---|---:|---|
| Acquire, checksum, inventory and document source workbooks | 2–5 | Original XLS/XLSX files are available |
| Map sheets/columns, create source-linked ledgers, audit units and independently check extraction | 8–18 | Source workbook layouts understood; ambiguities resolved |
| Source-match the model and perform unfitted validation with residuals and diagnostics | 10–18 | Audited observations and boundary conditions exist |
| Diagnose structural error, make justified corrections, freeze model and run held-out evaluation | 12–24 | Development/held-out split frozen; no held-out leakage |
| Cooling-architecture and time-varying workload case studies | 8–16 | Defensible parameter sources and at least one documented workload trace/scenario |
| Monte Carlo, convergence, global sensitivity and failure/break-even envelopes | 12–22 | Model executes reliably and parameter ranges are sourced/frozen |
| Geographic screening and electricity-water integration | 8–16 | Versioned spatial/water-stress and grid-water datasets documented |
| Multi-objective decision analysis, figures and tables | 6–12 | Validated study outputs available |
| Reproducibility archive, manuscript, supplement and claim audit | 16–30 | Main results stable; all claims trace to data/code |
| Final test/CI run, review and repair allowance | 4–8 | Candidate manuscript and artifact package assembled |

**Estimated remaining focused effort: 86–169 hours.** A realistic planning midpoint is about **120 hours**, roughly 3–4 full-time work weeks for one researcher, plus review and any data-access delays. If only the Ali dataset is used and geographic/workload claims are narrowed, a smaller scoped paper may take less time, but it would answer a narrower research question.

## Important uncertainty

The largest risk is not typing or coding time: it is the time needed to obtain and interpret valid experimental data and to resolve model–experiment mismatch without tuning to held-out observations. If source workbooks cannot be retrieved, the study cannot honestly complete empirical validation; replacing them with synthetic data would not solve that gap.

## Definition of complete

The research is complete only when:
1. the raw-data provenance and extraction ledgers are reproducible;
2. unfitted and independent held-out validation have been run and reported;
3. all planned scenario, uncertainty, sensitivity, break-even, geographic and multi-objective analyses have saved outputs;
4. tests and CI pass on the final commit;
5. the manuscript and supplement are fully linked to reproducible artifacts;
6. `scripts/publication_gate.py` and a final manual claim audit pass without weakening criteria to manufacture a pass.

No completion date is guaranteed by the hour estimate. Any estimate must be revised after the source workbooks are extracted and the first unfitted validation results are available.
