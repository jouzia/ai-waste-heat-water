# Research status audit — 2026-10-14

**Project:** From AI Waste Heat to Water: A Net-Water-Impact Framework for Sustainable AI Infrastructure  
**Status:** INCOMPLETE. Software and accounting infrastructure are substantial, and one open experimental workbook has now been extracted and used for a diagnostic model-form comparison. The core empirical study, independent validation, and publication package are not finished.

## Verified progress

- CI passed on commit `9201d1e8308c629a78e2c2489b9e42a5b7c7e0f6`: 142 tests passed, 1 skipped; Ruff passed. The subsequent audit-doc updates are documentation-only; the next CI run is pending. Independent-seed Monte Carlo convergence passes under illustrative scenario ranges; the overall publication gate remains INCOMPLETE (10/18). Independent-seed Monte Carlo convergence now passes under illustrative scenario ranges; the overall publication gate remains INCOMPLETE (10/18). The fixed publication gate now requires all 18 named scientific gates to be true and currently fails by design because the status is INCOMPLETE.
- GDR/NREL open-data source: Villa et al. (2018), DOI 10.15121/1452747. The original 3M counter-current DCMD workbook was downloaded in a workflow artifact, SHA-256 recorded, and 12 condition-level cumulative-volume traces were extracted into `04_experiments/literature_benchmarks/MD-OEDI-VILLA-2018_3M_flux_summary.csv`. See `docs/GDR_3M_WORKBOOK_AUDIT_2026-10-11.md`.
- A reproducible four-way comparison of Graetz–Lévêque/WaterTAP transfer correlations and smooth-channel/spacer-porosity assumptions was run with a 20 °C development group and a 30 °C within-workbook held-out group. Results are recorded in `docs/GDR_3M_MODEL_FORM_COMPARISON_2026-10-11.md` and the GitHub Actions artifact. This is diagnostic evidence, not independent validation.
- A counter-current permeate outlet-state bug was corrected; a regression test checks the correct outlet temperature/mass state. A separate duration-invariance defect in steady-state channel temperatures was corrected and tested.
- Ali et al. (2020) source ingestion now produces a lossless 17,430-row workbook ledger, 17,385 transient records, 16 steady-state observations, and a reproducible raw `mw` quality audit. The audit confirms 14/19 timed traces are nonmonotonic and deliberately does not repair or reinterpret them; see `docs/ALI_MASS_SERIES_QUALITY_AUDIT_2026-10-14.md`.
- A grouped four-fold leave-one-flow-level-out flux-law diagnostic holds out 50, 100, 200, and 300 L/h in turn. The fixed-TPC/single-permeance form has out-of-fold MAE 0.571 kg m⁻² h⁻¹; a flexible three-parameter flow-dependent TPC form has MAE 0.116 under the stated salinity interpretation. This is within-source model-form evidence only, not independent validation; see `docs/ALI_2020_LEAVE_ONE_FLOW_OUT_2026-10-14.md`.
- The primary source-structured Keshavarzzadeh (2020) runner remains separate from the modern model. Its eight source cases are still blocked by missing exact primary boundary conditions and the Figure 3 citation mismatch.
- The model has explicit baseline/counterfactual water accounting, cooling burden, workload coupling, uncertainty utilities, sensitivity utilities, break-even/Pareto primitives, geographic schemas, and manuscript plans. These are not equivalent to executed scientific analyses.

## Validation interpretation

The GDR model-form comparison shows substantial sensitivity to transfer correlation and geometry. The Graetz–Lévêque fits reach the upper membrane-permeance search bound; the WaterTAP variants have lower flux errors in this small split but do not achieve uniformly best held-out metrics. Outlet-temperature residuals remain non-negligible. Because the held-out cases come from the same workbook, flow channels are inconsistent, and geometry/transport properties remain engineering assumptions, the run cannot support a claim of experimentally validated predictive accuracy.

The source model has not yet been validated against the primary 1999 Martínez-Díez and Vázquez-González observations. The 2020 Keshavarzzadeh Figure 3 markers remain secondary reproduced data because its caption cites an unrelated ground-source heat-exchanger paper.

## Updated prior-art risk

The literature review now records direct overlap from:
- Kanbur, Wu, and Duan (2020): data-center immersion-cooling waste heat coupled to DCMD with thermoeconomic optimization.
- Wyon (2025): open-access thesis modeling a 1.5 MW direct-to-chip data center coupled to DCMD, heat exchanger, and pumps, with several distillate-use cases.
- Chen et al. (2026): CPU-waste-heat-driven MD experimental system (official journal abstract and metadata verified).
- Yang et al. (2026): data-center waste heat coupled to RO feedwater preheating with planning/operation co-optimization.
- Katakam et al. (2026, online ahead of print): system-scale data-center desalination and the SWUI water-stress metric.

The project must not claim that data-center-to-MD integration, waste-heat-driven MD, thermoeconomic optimization, or water-stress assessment is novel by itself. The potential contribution must be narrower and proven: independently validated transport plus boundary-consistent, counterfactual net operational blue-water accounting and uncertainty. A full-text comparison with Kanbur (2020) and Wyon (2025) remains necessary before claiming that gap.

## Remaining publication-critical work

1. Ali, Orfi & Najib (2020) source acquisition and row-level extraction are complete (five XLSX files, 17,385 transient records, 16 steady-state observations). A grouped within-source steady-state flux-law cross-validation is now available, but the dynamic MD model is still not validated against these data. The raw `mw` measurement semantics remain unresolved, so mass/flux errors against that field remain disabled. Source-matched dynamic reconstruction and external validation are still required.
2. Obtain or lawfully reconstruct primary 1999 MD observations and exact operating boundary conditions; digitization must include pixel coordinates, axis calibration, uncertainty, and repeat extraction.
3. Resolve GDR flow-sensor/sign issues and source-match the 3M channel geometry before treating the GDR run as a physical validation case.
4. Complete unfitted validation and independent study-level held-out validation.
5. Finish source-model comparison, cooling-architecture scenarios, measured workload/time coupling, Monte Carlo convergence, global sensitivity, break-even/failure envelope, geography/electricity-water integration, and multi-objective analysis.
6. Generate manuscript figures and tables only from frozen, reproducible outputs; complete manuscript, supplement, artifact archive, and final claim audit.

## Current hard gate

`05_validation/FINAL_GATE_STATUS.yaml` is the authoritative release gate. It currently records 10 of 18 gates as true: software correctness, open-data access, primary-observation extraction, cooling-architecture scenario execution, time-varying workload coupling, Monte Carlo convergence under illustrative ranges, global-sensitivity execution, break-even/failure-envelope execution, counterfactual net-water accounting, and exploratory multi-objective analysis. Eight gates remain false, including source reconstruction, unfitted validation, held-out validation, model-form comparison at publication standard, geographic integration, the reproducibility package, manuscript/supplement, and final publication audit. It intentionally leaves independent validation, uncertainty/sensitivity execution, geographic analysis, manuscript, and publication audit incomplete.

## Completion rule

Do not claim publication readiness or a positive net-water benefit until all relevant data, assumptions, code revisions, validation outputs, uncertainty results, and figures are traceable. Green software CI is not experimental validation.
