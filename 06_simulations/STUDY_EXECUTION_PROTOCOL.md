# Study execution protocol

This protocol defines the order in which quantitative study results may be generated.

## Phase 1 — evidence

Do not execute final validation or publication figures until each benchmark has:
- source DOI/landing page;
- license;
- raw-file checksum;
- extraction record;
- observation ledger;
- unit audit.

## Phase 2 — unfitted validation

For each benchmark:
1. freeze the parameter set;
2. run the model without calibration against the target observations;
3. report MAE, RMSE, MAPE where mathematically appropriate;
4. preserve residuals and prediction intervals;
5. record convergence/failure cases.

No parameter optimization may use the held-out cases.

## Phase 3 — independent validation

Partition by experimental configuration or source where possible rather than randomly splitting correlated observations. The held-out set must remain untouched until the model form and development parameters are frozen.

## Phase 4 — uncertainty

Run seeded Monte Carlo using only source-linked or explicitly scenario-labelled distributions. Report:
- requested and successful samples;
- failed draws and reasons;
- convergence of quantiles and sign probability;
- seed;
- distribution provenance.

## Phase 5 — sensitivity

Run Sobol or Morris analysis after the uncertainty ranges are frozen. Report first-order and total-effect indices with the design size, seed, bounds, and model-output definition.

## Phase 6 — decision envelope

Evaluate:
- net blue-water consumption;
- break-even brackets;
- heat-availability failures;
- thermal/operating infeasibility;
- Pareto non-dominated solutions.

Do not collapse these into one threshold.

## Phase 7 — geographic screening

Only after the physical model is validated, combine it with versioned climate, water-stress, and electricity-water datasets. Preserve each site's boundary and data version.

## Publication rule

A result enters the manuscript only if its generating data, assumptions, code revision, and analysis artifact are all traceable.
