# Uncertainty Execution Protocol

The primary response variable is:

`Delta_W_net = W_additional_consumption - W_recovered`

For every Monte Carlo run record:

- experiment_id
- git commit SHA
- configuration hash
- parameter-registry version
- source dataset versions
- random seed
- sample size
- distribution name and parameters for every sampled input
- model version
- failure/constraint counts
- output summary

## Required outputs

At minimum report:

- median
- 5th and 95th percentiles
- probability that `Delta_W_net < 0`
- probability that `Delta_W_net > 0`
- fraction of runs violating a model constraint
- parameter-importance results
- cases where the sign changes under plausible uncertainty

The probability of a negative `Delta_W_net` is conditional on the declared uncertainty model. It must not be reported as a universal probability that waste-heat MD is water-positive.

## Distribution provenance

No empirical distribution is embedded in the Python package. A distribution may be used only when its parameters and interpretation are traceable to a source, measurement dataset, or explicitly declared scenario assumption.

Scenario assumptions must be reported separately from empirical uncertainty.

## Study-level execution utility

`src/ai_water/study_analysis.py` now provides:

- median, 5th/95th percentile and conditional sign-probability summaries;
- deterministic prefix convergence curves for fixed Monte Carlo records;
- sign-change bracketing for one-dimensional break-even sweeps.

These are analysis utilities, not empirical calibration. The manuscript must report the declared distributions, counterfactual, valid/invalid sample counts, seed, Git SHA, and parameter provenance alongside every result.


## Execution record — scenario-only study

- Commit: `ec7624afd7cecd34b12802a6e0d779a75ce97ff`
- Seed: `20261013`
- Monte Carlo: 20,000 requested, 20,000 successful, 0 invalid draws.
- Sobol: 512 and 2,048 samples per matrix, 15 independent uniform scenario ranges, two outputs.
- Artifact: [run #8](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38428133917), artifact ID `11829716834`, SHA-256 `f8d4380906e0fe45ad5f377c828339b7f0eb06b08b516ebf8be63d114a4e7faf`.
- Interpretation: conditional on the one-hour illustrative scenario, the model and the selected ranges only. The run is not a physical forecast, empirical uncertainty study, or validation result. Monte Carlo lower-tail and freshwater Sobol convergence remain open.


## Conditional break-even envelope execution

- Workflow: [break-even envelope run #1](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38429966351)
- Artifact ID: `11830905144`; SHA-256 `1090890a7e0fd88a52d7dbd15d9deb6dc8f274790c40e724a036e7f45a947eb7`; expires 2027-01-11.
- 5,184 base combinations and 25,920 displacement-sweep rows. The scenario grid contains 2,808 no-production cases, 1,730 cases where full displacement still cannot break even, and 646 cases where break-even is possible.
- These are grid shares under illustrative assumptions, not real-world probabilities. The break-even execution gate is complete, but the physical envelope is not publication-grade until MD validation and source-backed parameter ranges are complete.
