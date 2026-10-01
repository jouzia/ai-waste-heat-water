# Uncertainty and Sensitivity Plan

The primary response is net freshwater consumption change:

Delta_W = W_additional_consumption - W_avoided

Negative values indicate lower modeled consumption than the declared counterfactual; positive values indicate additional consumption. Recovered distillate is not automatically treated as avoided consumption. Unless displacement is demonstrated, W_avoided is zero.

## Analyses

1. Reproducible Monte Carlo propagation. The seeded runner is implemented in
   src/ai_water/monte_carlo.py; see docs/MONTE_CARLO_PROTOCOL.md for the
   distribution provenance, invalid-draw, dependence, and reporting rules.
   This is an execution primitive only; no empirical distributions are currently
   asserted by default.
2. Rank-based sensitivity screening.
3. Morris screening for nonlinear/high-dimensional behavior.
4. Sobol variance decomposition for the final reduced parameter set.
5. Break-even surfaces for heat quality, recovery, cooling burden, electricity
   water intensity and hydraulic burden.
6. Scenario stratification by cooling architecture, climate and water stress.

## Distribution policy

Every distribution must be evidence-linked. If a paper reports uncertainty,
preserve it. If only a range exists, document the distribution choice. An
unsupported scenario range remains a scenario assumption.

## Implementation status

- Distribution sampling primitives: implemented.
- Seeded scenario Monte Carlo runner: implemented and CI-tested.
- Source-linked parameter distributions: not yet populated for the full study.
- Monte Carlo convergence analysis: pending.
- Morris/Sobol global sensitivity: pending.
- Break-even and failure-envelope analysis: pending.

## Required outputs

- median and uncertainty interval;
- probability that Delta_W < 0;
- parameter importance;
- sensitivity of sign as well as magnitude;
- constraint/failure rates;
- negative-result cases.

A probability from the uncertainty model is not a universal technology claim.
