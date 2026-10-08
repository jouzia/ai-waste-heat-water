# Research status audit — 2026-10-08

**Project:** From AI Waste Heat to Water: A Net-Water-Impact Framework for Sustainable AI Infrastructure  
**Status:** INCOMPLETE. The research infrastructure is substantial, but the core empirical study and publication package are not finished.

## What is implemented

- Baseline energy/water accounting with explicit counterfactual avoided-water term.
- Reduced-order membrane-distillation thermal, mass-transfer and hydraulic components, plus a source-structured counter-current runner.
- Cooling-burden fields and cooling-architecture taxonomy/interface.
- Piecewise-constant workload-profile integration and a workload-to-scenario coupling layer.
- Monte Carlo sampling utilities, Sobol estimator utilities, study-summary/convergence helpers, break-even and Pareto primitives.
- Benchmark registry, validation matrix, data-acquisition manifest, extraction inventory utility, protocols, manuscript outline and reproducibility plan.
- A provenance-labelled transcription of the source-reported model–plant error summary in Ali, Orfi & Najib (2020), Table 1, saved as `01_literature/derived/ali_2020_table1_model_errors.csv` with its limits documented in `docs/ALI_2020_TABLE1_EXTRACTION.md`. This is summary evidence only—not raw observations or validation of this repository's model.
- Automated software tests and CI configuration.

These are code capabilities or protocols; they do not themselves demonstrate physical accuracy or complete the corresponding study analyses.

## Still unfinished — publication-critical

1. Download and preserve original experimental files; record source, retrieval time, filenames, sizes and SHA-256.
2. Extract measurements into source-linked observation ledgers with sheet/range, units, missingness and transformation records. The available PDF supports transcription of Table 1 summary errors only; it does not replace the five supporting XLSX files.
3. Independently check extraction and freeze development/held-out partitions by experimental configuration/source.
4. Run unfitted source-matched validation and publish residuals and appropriate error metrics.
5. Complete genuinely held-out validation and model-form comparison.
6. Execute comparative cooling-architecture scenarios with sourced parameter values.
7. Run an end-to-end measured-workload case through heat availability, recovery, MD and cooling.
8. Execute source-linked Monte Carlo uncertainty with convergence diagnostics.
9. Execute global sensitivity analysis using frozen, justified parameter ranges.
10. Generate break-even/failure-envelope results and Pareto analyses.
11. Integrate versioned geographic water-stress and electricity-water data.
12. Produce study-derived figures/tables, complete manuscript and supplement, reproducibility archive, and final claim audit.

## Immediate blocker and lawful path

The official public sources are identified:
- Villa et al. 2018, DOE/NREL GDR: https://gdr.openei.org/submissions/1016 (seven XLS workbooks, about 95.97 MB).
- Ali, Orfi & Najib 2020, PLOS ONE: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230207 (five linked supporting XLSX files).

The execution environment has not successfully retrieved the binary workbooks. No experimental observations have therefore been fabricated or promoted to validation. The highest-value next step is to obtain the original Ali XLSX files first, then Villa XLS files, and feed them through the repository's inventory/extraction pipeline. If a user can upload the original files, that directly unblocks this step; payment is not required.

## Recommended order

A. Acquire and hash source files.  
B. Inventory workbooks and build audited observation ledgers.  
C. Run unfitted validation before any tuning.  
D. Diagnose errors, revise only with documented rationale, and evaluate held-out cases.  
E. Run cooling/workload, uncertainty, sensitivity, break-even, geographic and multi-objective studies.  
F. Generate the manuscript and supplement from reproducible outputs, rerun checks, and audit every claim.

## Completion rule

Do not claim publication readiness or a positive net-water benefit until all relevant data, assumptions, code revisions, validation outputs, uncertainty results and figures are traceable. A green software CI result is not experimental validation.
