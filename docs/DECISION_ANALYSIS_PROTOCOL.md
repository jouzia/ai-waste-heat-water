# Decision-analysis protocol

## Break-even analysis

Break-even analysis is performed on a declared scalar response, normally:

net_consumption_change_l = additional_water_consumption_l - avoided_freshwater_consumption_l

A break-even point is reported only when a sampled parameter interval contains a sign change or an exact zero. The repository utility uses bisection only inside a supplied bracket and therefore does not claim a global optimum or a universal threshold.

The study must report:
- varied parameter;
- fixed parameters;
- counterfactual;
- search interval;
- sampled grid;
- sign-changing brackets;
- root tolerance;
- whether monotonicity was independently established;
- failure/no-crossing cases.

## Pareto analysis

The Pareto utility supports caller-declared objective directions. Candidate study objectives may include:
- net blue-water consumption;
- electricity use;
- operational carbon;
- cost.

No objective weighting is imposed by the framework. Weighted utility scores, if used, must be a separate declared decision analysis.

## Failure envelope

The final study should classify parameter combinations into:
- water-beneficial;
- approximately neutral;
- water-burden-increasing;
- infeasible due to heat availability;
- infeasible due to thermal/operating constraints.

These classes should be reported with uncertainty rather than as a single deterministic boundary.
