# Validation Protocol

## Purpose

The publication analysis must distinguish implementation tests from scientific validation. Passing unit tests demonstrates software consistency; it does not demonstrate physical predictive accuracy.

## Validation hierarchy

### V0 — software invariants
Verify units, conservation relationships, monotonicity, limiting cases, and explicit failure conditions.

### V1 — thermodynamic reproduction
Reproduce source-backed water and seawater thermodynamic quantities within the documented numerical tolerance.

### V2 — literature-source reproduction
Reconstruct independently selected membrane-distillation experiments from the original source conditions. Preserve feed composition, membrane configuration, temperatures, flow rates, recovery, pressure, and duration. Do not copy only headline flux values.

### V3 — cross-source validation
Use experiments not used to tune model parameters. Report performance separately for development and held-out validation datasets.

### V4 — coupled-system validation
Compare the integrated thermal, hydraulic, MD, and water-accounting model against a source-matched experiment or controlled laboratory system where the required measurements are available.

## Required reported metrics

For each validation dataset report:

- observed value;
- model prediction;
- absolute error;
- relative error;
- MAE;
- RMSE;
- MAPE where division by the observed value is meaningful;
- bias;
- uncertainty interval when source uncertainty is available.

For paired experimental/model observations:

$$
RMSE = \sqrt{\frac{1}{n}\sum_i(y_i-\hat y_i)^2}
$$

$$
MAE = \frac{1}{n}\sum_i|y_i-\hat y_i|
$$

$$
MAPE = \frac{100}{n}\sum_i\left|\frac{y_i-\hat y_i}{y_i}\right|
$$

MAPE must not be used when observations are zero or near zero.

## Parameter-fitting rule

Parameters that are fitted to validation data must be explicitly labelled. A parameter fitted on a dataset cannot be described as independently validated on that same dataset.

Preferred sequence:

1. source selection;
2. parameter extraction;
3. immutable benchmark record;
4. model run;
5. error calculation;
6. model-form comparison;
7. held-out validation;
8. uncertainty analysis.

## Model-form comparison

Where multiple published correlations are plausible, compare them rather than silently selecting the one that gives the lowest error. Candidate formulations may include alternative heat-transfer, mass-transfer, temperature-polarization, and concentration-polarization models.

The spread between credible formulations is treated as model-form uncertainty when the available evidence does not identify a single superior formulation.

## Benchmark selection criteria

A benchmark is eligible when the source provides enough information to reconstruct the relevant operating condition, including as applicable:

- membrane material and configuration;
- membrane area;
- membrane thickness and thermal conductivity where required;
- feed and permeate temperatures;
- flow rates or velocities;
- feed composition/salinity;
- pressure;
- flux or permeate production;
- recovery;
- duration;
- relevant uncertainty or measurement information.

## Exclusion rule

A paper is not used as quantitative validation merely because it reports a flux value. If critical boundary conditions are missing, the source may be retained as qualitative evidence but must not be represented as a reproducible quantitative benchmark.

## Publication reporting

The final manuscript must state:

- how validation papers were selected;
- which datasets were used for development versus validation;
- all fitted parameters;
- all excluded datasets and reasons for exclusion;
- model version and commit SHA;
- benchmark configuration hashes;
- software environment;
- random seeds for stochastic analyses.

A successful validation result is not required for publication. Systematic model failure is itself a result and must be reported with diagnosis and limitations.
