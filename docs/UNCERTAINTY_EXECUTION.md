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