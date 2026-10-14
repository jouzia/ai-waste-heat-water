# Research 2 completion handoff — 2026-10-14

Project: **From AI Waste Heat to Water: A Net-Water-Impact Framework for Sustainable AI Infrastructure**

Repository: https://github.com/jouzia/ai-waste-heat-water

## Status

**INCOMPLETE — do not release as a validated study or claim net freshwater benefit.**

The authoritative hard gate is `05_validation/FINAL_GATE_STATUS.yaml`. It records 10/18 gates as satisfied. Gate status is evidence-driven; documentation, successful software tests, numerical convergence, or an attractive scenario result cannot substitute for physical validation.

## Newly recorded evidence

### Steady-state within-study model comparison

Four leave-one-flow-level-out folds each favored the flexible three-parameter temperature-polarization model over the fixed-coefficient model. Aggregate out-of-fold MAE was 0.116 versus 0.571 kg m^-2 h^-1. This is a within-source diagnostic on 16 observations and is conditional on the documented salinity interpretation. It is not independent experimental validation and does not, by itself, pass the publication-grade model-form gate.

### Sensitivity numerical convergence

At 4,096 versus 8,192 Sobol samples per matrix, the top-five freshwater-output total-effect ranking was unchanged; maximum total-effect index change was approximately 0.029. This supports numerical stability of the estimator under the current setup. The input ranges/distributions remain illustrative and uncalibrated, and the model remains unvalidated; no real-world probability or calibrated uncertainty claim follows.

### Transient validation warning

The Ali et al. (2020) source audit reports material outlet-temperature errors and unresolved semantics for the raw `mw (kg)` measurement field. The field is nonmonotonic in 14 of 19 complete timed worksheet traces, so prior mass-error metrics and tail-slope flux comparisons remain withdrawn/disabled. Do not reinstate them without resolving the source measurement semantics. Within-source held-out temperature results are diagnostics, not independent validation.

## Additional completion work — 2026-10-14

- Added a targeted prior-art audit at `docs/PRIOR_ART_GAP_AUDIT_2026-10-14.md`.
- Added recent direct-overlap studies to `01_literature/literature_matrix.csv`: Katakam et al. (online 2026; DOI 10.1016/j.watres.2026.126748) and Wang et al. (2026; DOI 10.1016/j.ese.2026.100702). The manuscript and README now reflect that these studies narrow the novelty claim.
- Updated the working manuscript to avoid broad “first” claims and added verified reference metadata for Malaguti et al. (2026), Katakam et al. (online 2026 / issue 2027), and Wang et al. (2026). Wyon (2025), Chen et al. (2026), and Yang et al. (2026) still need full bibliographic verification and a source-by-source comparison.
- Rechecked the primary 1999 source route. A publisher record/abstract is accessible, but a verified legally accessible full text or machine-readable experimental table was not found in this pass. The primary observation ledger remains intentionally empty. `docs/PRIMARY_SOURCE_VALIDATION_GATE.md` now records the blocker and the exact optional user assistance needed.
- Refreshed the hard-gate status date without changing any scientific gate. Status remains **INCOMPLETE**; documentation work does not count as validation.

## Required completion sequence

1. **Resolve source reconstruction and measurement semantics.**
   - Reconcile the 1999 Martínez-Díez & Vázquez-González primary experimental conditions with the 2020 secondary reproduction.
   - Populate `04_experiments/literature_benchmarks/MD-DCMD-MARTINEZ-1999_observations.yaml` only with source-located observations, units, exact boundary conditions, extraction method, and uncertainty.
   - Archive axis calibration and independent repeat digitization for any figure-derived values.
   - Resolve the Ali `mw` measurement/reset/cumulative semantics from source documentation or exclude mass validation explicitly.

2. **Run a frozen, unfitted primary-source comparison.**
   - Freeze model parameters and source-condition mapping before comparing observations.
   - Report MAE, RMSE, bias, and relative error only where mathematically appropriate.
   - Preserve failed cases and physically inadmissible states.
   - If primary data or boundary conditions cannot be recovered, document the limitation and downgrade the validation claim; do not fill gaps with defaults.

3. **Complete the independent/held-out validation and model-form gates.**
   - Keep the four-fold flow-level result labelled as within-study evidence.
   - Use a genuinely independent dataset/configuration or a pre-registered holdout with defensible boundary conditions.
   - Separate calibration cases from evaluation cases. Report the fixed and flexible forms without hiding failures.

4. **Complete the geographic electricity–water join.**
   - Review the existing Aqueduct city-centroid proxy workflow and source-native future-field semantics.
   - Keep city-centroid proxies clearly distinct from actual data-centre sites.
   - Join defensible, traceable electricity-water factors with an explicit withdrawal/consumption and generation-boundary definition.
   - Treat Aqueduct as basin-level contextual risk, not as a multiplier on water volume. Record source version, retrieval date, transformation, and uncertainty.

5. **Freeze the analysis package.**
   - Re-run tests, lint, source extraction, validation, uncertainty, sensitivity, break-even/failure-envelope, and geographic workflows from a clean environment.
   - Record exact commit SHA, commands, environment, workflow links, checksums, and artifact retention/retrieval instructions.
   - Regenerate all manuscript figures and tables from the frozen outputs; exclude superseded or invalid metrics.

6. **Finish manuscript and claim audit.**
   - Write the manuscript from the frozen evidence, including negative/non-beneficial outcomes and model failures.
   - Distinguish observed evidence, within-study cross-validation, illustrative scenario results, and unresolved assumptions.
   - Audit prior art and narrow novelty claims to the coupled, counterfactual net-water accounting contribution supported by evidence.
   - Mark a gate true only when its required artifact and provenance are present. Run `python scripts/publication_gate.py`; it should fail until all mandatory gates genuinely pass.

## Claim language allowed before completion

The repository supports a reproducible accounting/modeling framework and preliminary within-study diagnostics. It does **not** yet support claims that the physical system is independently validated, that its illustrative uncertainty distributions describe real-world uncertainty, or that AI waste-heat recovery produces a positive net freshwater benefit.

## Official geographic source references

- WRI Aqueduct 4.0 dataset: https://datasets.wri.org/datasets/aqueduct-global-maps-40-data
- WRI guidance for water use embedded in purchased electricity: https://www.wri.org/data/dataset-guidance-calculating-water-use-embedded-purchased-electricity

These references do not replace recording the exact downloaded version, source factors, transformations, and analysis artifacts used in the final run.
