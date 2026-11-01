# Source acquisition and extraction execution note

## Ali, Orfi & Najib (2020) supplementary data

**Acquisition and source-linked extraction are complete.** The five publisher XLSX files (S1 Data–S5 Data) were downloaded from the PLOS supporting-information endpoints, verified as XLSX/ZIP payloads, hashed, inspected, and processed by the reproducible GitHub Actions workflow.

- Source article: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230207
- License: CC BY 4.0.
- Latest artifact: [Ali 2020 source-data ingestion run #12](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38427509655), artifact ID `11829695926`, SHA-256 `1a12fadca90d89452c11f0f7cc5bcbc6b7804e5c16c78528c5a5f70723e15224`, expiry 2027-01-11.
- File-level hashes and byte sizes are in `01_literature/derived/ali_2020_supplementary_acquisition_ledger.csv`.
- Structured outputs and source row locators are recorded in `04_experiments/literature_benchmarks/MD-DCMD-DYNAMIC-ALI-2020_observations.yaml` and `docs/ALI_2020_SUPPORTING_DATA_AUDIT_2026-10-13.md`.

## Extracted source records

- Raw nonblank worksheet-row ledger: 17,430 rows.
- Structured transient ledger: 17,385 rows; 16,837 rows have both time and cumulative mass; 548 temperature-only rows have no timestamp and are excluded from time-domain fitting but retained in the ledger.
- Steady-state table: 16 valid flow/temperature conditions.
- Two non-condition rows are preserved in a separate exclusion ledger.
- Tail-slope comparison between the transient traces and the S1 steady-state table is available as a within-paper consistency diagnostic only; it is not independent validation.

## Required next steps

1. Audit the exact source model equations, geometry, heat-loss correction, and measured input histories against the full article.
2. Preserve the distinction between time-indexed accumulated mass, measured temperatures, circulation flow, source-derived production rates, and source model predictions.
3. Investigate S2 sheet 55's nonzero initial cumulative mass and unattained target; S5 sheets 50/60/70's temperature-only rows without timestamps; S5 sheet 80's failure to reach 80 °C; and the two excluded S1 rows.
4. Implement a dynamic model with explicit heater lag and measured cold-inlet fluctuations before evaluating the time series.
5. Pre-register development and held-out operating conditions at the condition level; do not randomly split adjacent points from one trace.
6. Report accumulated-mass error, response-lag error, and production-rate error separately. Preserve source uncertainty and repeated-run structure.
7. Only after source-model comparison and boundary reconstruction, use the Ali dataset as an external study-level validation set. Do not tune to these observations and then report the same cases as validation.

Acquisition, checksums, and row extraction are now complete. **Model validation and net-water-benefit evidence remain incomplete.**
