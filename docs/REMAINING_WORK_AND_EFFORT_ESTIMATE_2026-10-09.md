# Remaining work and effort estimate — 2026-10-13

## Status snapshot

This remains a planning estimate, not a completion claim. The hard publication gate has **10 of 18 gates true and 8 false**. Software correctness, open-source data access, primary-observation extraction, cooling-architecture scenario execution, time-varying workload coupling, global-sensitivity execution, counterfactual water accounting, and exploratory multi-objective execution have reproducible artifacts. The publication gate still correctly returns incomplete.

The Ali et al. (2020) source data have now been acquired, checksummed, and extracted into source-linked raw, transient, and steady-state ledgers. A 20,000-draw scenario-only Monte Carlo and a 512/2,048-point Sobol study run reproducibly, but the lower-tail estimate and freshwater-production sensitivity indices need more convergence work. A 1,440-row cooling/water/energy/carbon scenario sweep now emits a Pareto set, and a 5,184-combination break-even envelope plus 25,920-row displacement sweep execute reproducibly. Their architecture, grid, and model ranges are illustrative rather than measured, so neither result is publication-grade.

The Ali S1 steady-state data also expose an important flux-model mismatch. With TPC fixed at 0.8, the fitted-permeance model has held-out 300 L/h MAE 0.828 kg m⁻² h⁻¹. A fitted flow-dependent TPC alternative improves this to 0.181 under the article's stated 0.5% salinity interpretation, but this is only an internal held-out-flow diagnostic. The alternative TDS interpretation drives fitted permeance to the optimizer's upper bound. Separately, the default 10 m² / 50 L/h dynamic reconstruction returned an outlet below the inlet-temperature envelope; the code now rejects that trajectory. Dynamic source reconstruction is therefore not validated.

Prior art now includes Kanbur et al. (2020), Wyon (2025), Chen (2026), Yang (2026), Katakam et al. (2026 online-ahead-of-print), and a newly surfaced system-scale data-centre desalination study. The manuscript must not claim novelty from waste-heat-to-MD integration, technoeconomic optimization, or a water-stress metric alone.

## Remaining work packages

Estimates are person-hours of focused research work, not elapsed calendar time. They assume the current public source data remain accessible and no new experiments are needed.

| Work package | Estimated active hours | Exit criterion |
|---|---:|---|
| Recover and digitize the primary Martínez-Díez & Vázquez-González (1999) observations; independently check a subset | 6–12 | Source-located observation ledger with units, conditions, calibration and uncertainty |
| Correct and source-match MD heat/mass-transfer structure; run unfitted comparisons | 10–20 | Physically admissible predictions and source-matched residual report |
| Complete held-out and model-form evaluation using transfer-correlation alternatives | 12–24 | Frozen development split, no holdout fitting, independent/held-out results |
| Source-backed cooling architectures and realistic time-varying workload/temperature traces | 6–12 | Versioned parameter sources and at least one defensible workload profile |
| Monte Carlo convergence, sensitivity convergence, and break-even/failure envelope | 8–16 | Predeclared tolerances, independent-seed checks, stable quantiles/indices |
| Geographic water stress and electricity-water integration | 8–16 | Versioned location/grid/water datasets, licensing and spatial alignment |
| Replace illustrative multi-objective inputs with evidence-linked cases; regenerate figures/tables | 4–8 | Pareto outputs supported by validated cases and sourced factors |
| Reproducibility package, manuscript, supplementary methods/data and claim audit | 16–30 | Every main-text number linked to code/data, artifact package and methods |
| Final review, test/CI, and repair allowance | 4–8 | Final commit CI green, publication gate and manual audit pass |

**Estimated remaining focused effort: 74–146 hours; midpoint approximately 110 hours.** That is roughly 3–4 full-time work weeks for one researcher, excluding peer review and external data-access delays. This is lower than the previous estimate because source data ingestion and initial scenario-analysis execution are now reproducible; it is not a promise of a completion date.

## Largest remaining risks

1. **Model-form validity:** the current dynamic reconstruction can produce inadmissible outlet states under the source-scale low-flow case, and the simpler flux law underpredicts held-out high-flow observations.
2. **Novelty:** direct prior art makes a broad system-concept contribution untenable; the contribution must be narrower and supported by stronger validation/accounting.
3. **Probabilistic claims:** current Monte Carlo/Sobol ranges are illustrative, not empirical priors. No real-world benefit probability can be reported.
4. **Net-water causality:** recovered distillate counts as avoided freshwater only when actual freshwater consumption is displaced. Gross production alone is insufficient.

## Definition of complete

Research is complete only when all 18 hard gates in `05_validation/FINAL_GATE_STATUS.yaml` are true with reproducible evidence, the final source-matched and independent/held-out validation has been reported, geographic and time-varying cases use documented inputs, the manuscript and supplement are assembled, CI passes on the final commit, and the hard publication gate passes without weakening criteria.
