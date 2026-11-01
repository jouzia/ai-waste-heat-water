# Reproducibility protocol

A result is publication-grade only when a second researcher can identify the exact source data, assumptions, code revision, and transformations used to produce it.

## Required provenance record

For every external data object:
- citation and DOI/landing page;
- access date;
- license;
- original filename;
- byte size;
- SHA-256;
- parser/library version;
- worksheet/table/figure identifier;
- selected rows/columns or pixel calibration;
- unit conversions;
- exclusions and missing-value rules;
- transformation code revision.

## Execution layers

### Layer A — software
- clean install;
- tests;
- Ruff;
- deterministic unit tests.

### Layer B — source reconstruction
- reproduce published equations;
- reproduce published parameterization;
- no fitting during first reproduction run.

### Layer C — observations
- extract raw measurements;
- preserve original values;
- independently re-extract a sample;
- quantify extraction uncertainty.

### Layer D — validation
- development cases;
- held-out cases;
- unfitted metrics;
- model-form comparison.

### Layer E — study
- Monte Carlo;
- convergence;
- global sensitivity;
- break-even/failure envelope;
- geographic analysis;
- multi-objective analysis.

### Layer F — publication
- manuscript tables/figures generated from versioned analysis outputs;
- final claim audit;
- final license audit;
- reproducibility audit.

## Prohibited shortcuts

Do not:
- invent missing observations;
- transcribe values without provenance;
- tune against the same observations used for validation;
- treat a literature figure as raw data without documenting digitization;
- call a scenario result validation;
- call a reduced-order model industrially validated;
- report recovered distillate as avoided freshwater without a declared displacement counterfactual.
