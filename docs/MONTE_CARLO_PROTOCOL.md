# Monte Carlo execution protocol

## Implemented capability

src/ai_water/monte_carlo.py implements seeded Monte Carlo execution over a base Scenario. Callers must supply a distribution for every varied parameter. No empirical distribution is built into the package.

The runner records sampled parameter values and key energy/water outputs. It reports requested, successful, and failed sample counts. Invalid draws are rejected by model validation and counted; they are not clipped to bounds. Unknown parameter paths fail before sampling.

## Evidence and provenance requirements

For every varied parameter, preserve a separate registry entry containing:

- parameter path and unit;
- distribution family and parameterization;
- source citation, DOI/URL, table/figure/page, or measurement protocol;
- whether the distribution represents measurement, parameter, scenario, or model-form uncertainty;
- rationale for bounds and any truncation/rejection;
- retrieval date and licence for external data.

If no empirical distribution is defensible, use a clearly labelled scenario range and do not describe it as a probability distribution inferred from evidence.

## Dependence and invalid draws

The current runner samples each declared marginal independently. It does not model parameter dependence or correlated uncertainty. If parameters are physically or statistically dependent, independent sampling is a limitation; do not imply joint uncertainty is represented. A future extension should accept a documented joint sampler or correlation model.

Report the invalid-draw fraction alongside results. If invalid draws are concentrated in particular regions of parameter space, the accepted-sample distribution may be selection-biased. Investigate the failures and do not silently treat successful draws as representative of the entire declared input space.

## Required outputs for a manuscript

At minimum, report:

- random seed, Git commit, config and parameter-registry version;
- requested and successful sample counts and invalid-draw fraction;
- median and 5th/95th percentiles for the primary response;
- estimated fraction of valid simulations with Delta_W_net < 0, clearly described as conditional on the declared model, distributions, and counterfactual;
- Monte Carlo convergence check for key quantiles and sign probability;
- sensitivity analysis and model-form comparison;
- negative outcomes and failure regimes.

A Monte Carlo probability is not a real-world probability unless the model structure, parameter distributions, dependencies, and counterfactual are defensible. The first implementation is a reproducible execution primitive, not evidence that any distribution is empirically calibrated.
