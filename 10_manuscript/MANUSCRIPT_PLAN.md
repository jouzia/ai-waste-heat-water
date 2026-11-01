# Manuscript development plan

Working title: **From AI Waste Heat to Water: A Net-Water-Impact Framework for Sustainable AI Infrastructure**

## Current evidence status — 2026-10-14

This plan remains intentionally provisional. Current executable evidence is:
- Source-linked primary observation ledgers exist for the 12-condition GDR/NREL 3M workbook and the five Ali et al. (2020) supporting workbooks.
- The Ali S1 flux-law split holds out 300 L/h. Fixed TPC underpredicts the held-out flow; a fitted flow-dependent TPC improves error but is an internal same-paper diagnostic only.
- The Ali lumped reconstruction fails the S2/50 trace physically; the 3-cell spatial model also falls below the outlet envelope. The 10-cell spatial model is physically admissible on the full 1,662-row trace, with hot/cold outlet RMSE 0.324/4.980 °C without correction and 0.363/2.457 °C with the published correction. **Do not use the previously reported transient mass-error metrics:** raw `mw (kg)` is nonmonotonic in 14 of 19 complete timed worksheet traces and its cumulative/reset semantics are unverified. The extractor now preserves raw `mw`, leaves cumulative mass unset, and disables tail-slope flux comparisons. The time-indexed temperature residuals are archived; source measurement semantics and the pre-registered S3/60 holdout has now been evaluated, but its hot/cold RMSE (2.079/3.323 °C without correction) remains material and is within-source, not independent, validation; numerical grid/tolerance behavior is partially characterized but not a validation pass.
- Scenario-only uncertainty: 20,000 Monte Carlo draws and Sobol matrices of 512/2,048 points execute reproducibly. Monte Carlo numerical convergence passes under the declared illustrative scenario ranges after independent-seed 50k/100k runs; freshwater-output Sobol ranking and empirical uncertainty calibration remain unresolved. No real-world probability claim is allowed.
- Cooling architecture Pareto sweep and break-even/failure envelope execute reproducibly, but their architecture/grid/model ranges are illustrative, not source-backed empirical priors.
- Geographic Aqueduct/electricity-water integration, primary Martínez-Díez figure extraction, unfitted source-matched validation, independent external validation, final manuscript, and publication audit remain incomplete.

Do not transfer any scenario-only number into the manuscript's principal results as if it were an empirical finding. The authoritative hard gate remains INCOMPLETE (10/18 gates true; see `05_validation/FINAL_GATE_STATUS.yaml`).

## Publication status

This is a manuscript plan, not a completed paper. Quantitative results, validated claims, and conclusions must remain unwritten until the source-matched experiments, uncertainty analysis, and geographic scenarios are complete. Do not fill the placeholders with illustrative demo outputs.

## Research question

Under what combinations of AI workload intensity, recoverable heat quantity and temperature, MD operating conditions, cooling burden, auxiliary electricity, electricity-water intensity, and local water stress does waste-heat-driven membrane distillation reduce operational freshwater consumption relative to a declared counterfactual?

## Proposed contribution

A coupled, uncertainty-aware thermo-hydraulic-water accounting framework that identifies conditional feasibility and failure regimes for data-center waste-heat-assisted MD. The contribution is the integrated boundary, explicit counterfactual, source-traceable model comparison, and quantified feasibility envelope—not the broad idea of coupling waste heat to desalination by itself.

The novelty boundary, recent adjacent studies, falsifiable hypotheses, primary estimand, and release gate are maintained in `docs/RESEARCH_GAP_AND_FALSIFIABLE_DESIGN.md`. A targeted 2026-10-14 audit has now added Katakam et al. (online 2026; DOI 10.1016/j.watres.2026.126748) and Wang et al. (2026; DOI 10.1016/j.ese.2026.100702) as direct prior art; see `docs/PRIOR_ART_GAP_AUDIT_2026-10-14.md`. This is not yet a systematic literature review: full-text comparison, reproducible search/screening records, and complete bibliography verification remain required before submission. Do not claim global novelty from the current shortlist.

## Planned structure

1. **Abstract** — complete only after results are frozen; include research question, model boundary, validation evidence, principal quantitative findings, uncertainty, and limits.
2. **Introduction** — AI infrastructure water footprint; operational versus electricity-related water; waste-heat recovery opportunities and constraints; specific gap; research questions and contributions.
3. **Related work** — data-center heat recovery; MD thermodynamics and polarization; MD cooling/pumping burdens; data-center water-footprint accounting; integrated heat-water systems.
4. **System boundary and counterfactuals** — baseline data center, recovery intervention, incremental cooling, product-water displacement, withdrawal/consumption distinction, operational boundary exclusions.
5. **Mathematical framework** — workload/heat, exergy and recoverability, heat exchanger, MD mass/energy balances, cooling and hydraulics, water accounting, geography.
6. **Data and provenance** — parameter registry, source hierarchy, open datasets, licences, unit transformations, missingness and exclusion rules.
7. **Verification and validation** — software invariants, source-equation reproduction, unfitted source-matched comparison, independent/held-out validation, model-form comparison.
8. **Scenario design** — baseline and intervention scenarios, cooling architectures, workload/time availability, climate and water-stress strata.
9. **Uncertainty and sensitivity** — source-linked distributions, Monte Carlo convergence, Sobol/Morris analysis, uncertainty classes, failure rates.
10. **Results** — only measured/model outputs from frozen experiment manifests; include negative and non-beneficial cases.
11. **Failure envelope and trade-offs** — break-even surfaces and Pareto fronts for water, energy, carbon, and cost where data support them.
12. **Discussion** — interpretation, comparison with prior studies, implications, transferability limits.
13. **Limitations** — property closures, missing observations, reduced-order transport, geographic resolution, system boundary, parameter dependence.
14. **Conclusion** — answer the RQs only to the extent supported by validation and uncertainty.

## Planned figures

1. Coupled system boundary and counterfactual diagram.
2. Source-model and modern-model validation against observations, with digitization uncertainty.
3. Axial temperature and flux behavior for source-matched cases.
4. Recoverable heat quality/availability versus workload profile.
5. Cooling and pumping burdens by architecture and operating regime.
6. Net water-consumption change with uncertainty intervals.
7. Break-even/feasibility envelope.
8. Sobol first-order and total-effect indices.
9. Geographic screening map with data-resolution caveats.
10. Water-energy-carbon Pareto frontier, if carbon and cost inputs are adequately sourced.

## Planned tables

- Research questions, hypotheses, metrics, and falsification criteria.
- Parameter/source/uncertainty registry summary.
- Validation dataset eligibility and provenance table.
- Unfitted and held-out model performance metrics.
- Scenario definitions and counterfactuals.
- Monte Carlo convergence and invalid-draw summary.
- Sensitivity results and failure-regime summary.

## Claim gate

No statement that the intervention “saves water,” is “net positive,” or is deployable may be made from gross distillate or demo values. Such claims require: (i) a declared counterfactual, (ii) source-backed incremental burdens, (iii) validated model behavior in the applicable operating range, and (iv) uncertainty showing the sign and magnitude of the net response. If those conditions are not met, report the result as exploratory or unresolved.

## Completion checklist

- [ ] Primary observation ledger populated with source locators and units.
- [ ] Digitization uncertainty and independent repeat extraction archived where needed.
- [ ] Source property closures source-matched or explicitly treated as model-form uncertainty.
- [ ] Unfitted source comparison completed.
- [ ] Independent/held-out validation completed or the claim downgraded.
- [ ] Cooling and heat-sink scenarios implemented and checked.
- [ ] Evidence-linked workload and geographic inputs collected.
- [ ] Monte Carlo convergence and global sensitivity completed.
- [ ] Break-even and failure envelope reported.
- [ ] Net water accounting audited against counterfactual.
- [ ] Manuscript figures/tables generated from frozen, reproducible outputs.
- [ ] Final limitations and publication-readiness audit completed.


## Evidence update — 2026-10-14

The latest repository audit records the following additional evidence and limits:

- **Steady-state flow-level comparison:** four leave-one-flow-level-out folds all favor a three-parameter flow-dependent temperature-polarization model over the fixed-coefficient form. Aggregate out-of-fold MAE is 0.116 versus 0.571 kg m^-2 h^-1 (RMSE 0.144 versus 0.688), conditional on the documented 0.5% salinity interpretation and 16 observations from one source. This is within-source cross-validation only; it does not establish independent validation or satisfy the final model-form gate. See `docs/ALI_2020_LEAVE_ONE_FLOW_OUT_2026-10-14.md`.
- **Sobol numerical convergence:** increasing samples per matrix from 4,096 to 8,192 leaves the top-five freshwater-output total-effect ranking unchanged, with maximum total-effect index change about 0.029. This establishes numerical stability only under the current illustrative independent-uniform ranges. It does not calibrate the input distributions or validate the physical model.
- **Transient mass series:** the raw `mw (kg)` field is nonmonotonic in 14 of 19 complete timed worksheet traces. Cumulative-mass interpretation remains unresolved; prior mass-error results remain withdrawn, and predicted cumulative mass must not be compared with the ambiguous raw field.
- **Transient temperature performance:** the 10-cell spatial model is numerically admissible for the audited S2/50 trace, but cold-side outlet RMSE remains material. The pre-registered S3/60 trace is within-source holdout evidence, not independent validation. Do not describe either as a validation pass.
- **Geography:** the existing Aqueduct sample uses approximate city-centre proxies, not facility coordinates. No site-specific electricity-water factor has yet been joined. Aqueduct is a basin-level screening context and must not be converted into a water-volume multiplier.

These results should be included in a manuscript only as scoped diagnostics with source links, code revision, experiment manifest, and archived outputs. The primary 1999 Martínez-Díez experimental flux observations and exact boundary conditions remain unextracted; unfitted source-matched validation, independent validation, geographic integration, the complete reproducibility package, manuscript/supplement, and final publication audit remain open.

## Publication decision rule

The manuscript is not submission-ready while any mandatory gate is false. If a source cannot be recovered or a measurement cannot be interpreted, report the resulting limitation and narrow the paper's claims; do not replace missing evidence with illustrative defaults. A defensible final paper may ultimately be a validated methods-and-accounting framework with explicitly bounded evidence, but it cannot claim physical validation or net freshwater benefit without the corresponding data.
