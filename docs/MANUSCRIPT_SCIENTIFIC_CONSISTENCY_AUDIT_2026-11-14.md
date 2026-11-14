# Manuscript scientific-consistency audit — 2026-11-14

**Scope:** Internal audit of `10_manuscript/WORKING_MANUSCRIPT_DRAFT_v0.1.md` against the repository's experiment records, source audits, validation-gate declaration, and cited publisher/institutional records.

**Decision:** The draft remains an internal, evidence-bounded working manuscript. This audit does not pass any scientific validation gate, establish novelty, or support a positive net-water-benefit claim.

## Claim-by-claim findings

| Manuscript claim | Evidence checked | Audit finding |
|---|---|---|
| Ali et al. steady-state grouped comparison (Section 4.1) | `docs/ALI_2020_LEAVE_ONE_FLOW_OUT_2026-10-14.md` | Supported as a within-source four-fold comparison over 16 S1 observations. Under the stated 0.5% salinity interpretation, flow-dependent TPC MAE/RMSE are 0.1164/0.1439 kg m⁻² h⁻¹ versus 0.5713/0.6879 for fixed TPC. The source's salinity discrepancy and small sample remain material; this is not independent validation. |
| Sobol convergence (Section 4.2) | `docs/GLOBAL_SENSITIVITY_PROTOCOL.md`; `docs/MONTE_CARLO_CONVERGENCE_RESULTS_2026-10-13.md` | Supported with an important distinction. The nested 4,096/8,192 comparison used the same seed and illustrative independent-uniform bounds; freshwater total-effect maximum index change was 0.02885 with no top-five rank shift, while net-water maximum change was 0.00182. Monte Carlo numerical convergence separately passed its four predeclared checks. Neither result calibrates distributions or validates the physical model. The earlier 512/2,048 freshwater ranking instability should remain documented as superseded by the higher-resolution nested comparison, not erased. |
| Ali transient diagnostics (Section 4.3) | `docs/ALI_DYNAMIC_MODEL_FAILURE_ANALYSIS_2026-10-13.md`; `docs/ALI_2020_HELDOUT_TRACE_RESULTS_2026-10-13.md`; `docs/ALI_MASS_SERIES_QUALITY_AUDIT_2026-10-14.md` | Supported with limits. The 10-cell S2/50 model is physically admissible but cold-outlet RMSE remains 4.980 °C without correction and 2.457 °C with the published correction. The preregistered S3/60 within-source holdout has hot/cold RMSE 2.079/3.323 °C without correction and 2.173/2.643 °C with correction. Raw `mw` is nonmonotonic in 14/19 complete timed traces; cumulative-mass semantics remain unresolved and mass-error metrics are withdrawn. |
| Geographic screening (Section 4.4 and Section 6) | `docs/GEOGRAPHIC_ELECTRICITY_WATER_FACTOR_AUDIT_2026-10-22.md` | Supported. The six locations are approximate city-centre proxies, not facility coordinates. No defensible site-specific electricity-water factor join exists. Aqueduct is contextual basin-risk screening, not a physical water-volume multiplier. |
| HTC stress test (Section 4.5 and Section 5.1) | `docs/HTC_UNCERTAINTY_PROPAGATION_2026-11-07.md` and independently audited 600-row artifact | The 600-scenario design, coverage, successful solver statuses, finite outputs, and artifact checksums are supported. The original manuscript mixed extrema from the two energy modes while describing the ranges as mode-wise. This audit corrects the section to show mode-specific extrema and the combined envelopes explicitly. The factors remain illustrative deterministic stress-test inputs, not empirical distributions; independent feed/permeate perturbations do not model correlation; concentration polarization is disabled; the HTC correlation itself is not validated. |
| System boundary, sign convention, and water accounting (Sections 1–3) | `README.md`, `docs/RESEARCH_GAP_AND_FALSIFIABLE_DESIGN.md`, `docs/GEOGRAPHIC_ELECTRICITY_WATER_FACTOR_AUDIT_2026-10-22.md` | Framing is appropriately conditional. The manuscript states that withdrawal and consumption are distinct, gross distillate is not displaced consumption, and basin risk is not a water-volume multiplier. The sign convention still needs a final executable cross-check and freeze before any net-water results are reported. |
| Novelty and prior art (Section 1) | `docs/PRIOR_ART_GAP_AUDIT_2026-10-14.md`, Chen/Yang/Katakam/Wang/Bindels source audits | The narrowed, provisional contribution language is appropriate. The search is targeted, not systematic; complete search/screening records and full-text comparisons remain incomplete. No “first” or established novelty claim is supported. |
| Publication and validation status (Abstract and Section 7) | `05_validation/FINAL_GATE_STATUS.yaml`; `docs/PRIMARY_SOURCE_VALIDATION_GATE.md`; `docs/RESEARCH2_SCOPE_DECISION_PRIMARY_ACCESS_2026-10-15.md` | The manuscript correctly says it is not submission-ready and makes no validated net-water-benefit claim. The primary 1999 observation ledger remains empty; unfitted/independent validation and geographic integration remain blocked. The gate file remains authoritative and must not be manually advanced based on numerical diagnostics. |

## Corrections made in this audit branch

1. Replaced the mixed-mode HTC extrema sentence with a mode-specific table for freshwater/latent duty, hot-side thermal demand, conductive heat leak, and both outlet temperatures.
2. Added the combined cross-mode envelopes, computed from the full extrema across both modes.
3. Added bibliographic entries for Wyon (2025), Chen et al. (2026), Yang et al. (2026), and Bindels et al. (2026), which were cited in the introduction but absent from the initial reference list.
4. Updated the bibliography warning to distinguish completed metadata insertion from still-incomplete full-text prior-art comparison.

## Residual blockers — unchanged

- Primary Martínez-Díez & Vázquez-González (1999) observations and exact boundary conditions have not been extracted into the primary ledger.
- The Ali transient mass field semantics remain unresolved; no transient mass-validation claim is allowed.
- The Villa 12-condition workbook remains a candidate benchmark under audit, not a passed validation dataset; prior leakage-affected metrics are superseded.
- No site-specific electricity-generation water-consumption factor has been joined to defensible facility/grid/year data.
- HTC perturbation factors and broader scenario distributions remain illustrative and uncalibrated.
- Complete full-text prior-art review, systematic search/screening, supplementary package, and final reproducibility/publication audit remain open.
- No positive net-water-benefit, deployment prediction, independent-validation, or established novelty claim is supported.

## Reproducibility and source records

- Ali grouped flow-level diagnostic: `docs/ALI_2020_LEAVE_ONE_FLOW_OUT_2026-10-14.md`
- Monte Carlo convergence: `docs/MONTE_CARLO_CONVERGENCE_RESULTS_2026-10-13.md`
- Sobol convergence: `docs/GLOBAL_SENSITIVITY_PROTOCOL.md`
- Ali transient and mass-series audits: `docs/ALI_DYNAMIC_MODEL_FAILURE_ANALYSIS_2026-10-13.md`, `docs/ALI_2020_HELDOUT_TRACE_RESULTS_2026-10-13.md`, `docs/ALI_MASS_SERIES_QUALITY_AUDIT_2026-10-14.md`
- Geographic factor audit: `docs/GEOGRAPHIC_ELECTRICITY_WATER_FACTOR_AUDIT_2026-10-22.md`
- HTC artifact and methods: `docs/HTC_UNCERTAINTY_PROPAGATION_2026-11-07.md`
- Hard gate: `05_validation/FINAL_GATE_STATUS.yaml`

This is a claim-consistency audit, not a new simulation, experimental validation, systematic review, or publication-readiness certification.
