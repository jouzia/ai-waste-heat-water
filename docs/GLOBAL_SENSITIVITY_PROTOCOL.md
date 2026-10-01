# Global sensitivity protocol

## Implemented estimator

The module src/ai_water/global_sensitivity.py implements Saltelli covariance first-order and Jansen total-effect Sobol indices for independently sampled uniform parameter ranges. The caller supplies parameter names, finite lower/upper bounds, a deterministic evaluation function, a power-of-two sample size, and a random seed. Synthetic tests check recovery of variance shares for a known additive function and reject invalid sample sizes/non-finite outputs.

## Interpretation limits

- Uniform ranges are scenario assumptions unless evidence justifies a probabilistic interpretation.
- The current implementation assumes independent inputs. Correlated parameter dependence is not represented.
- First-order indices describe individual effects under the declared input distribution; total-effect indices include interactions involving a parameter.
- Small negative first-order estimates or estimates slightly above one can arise from finite-sample estimator error and must be investigated rather than silently clipped.
- Sobol indices depend on the chosen bounds and model structure; they are not universal parameter rankings.
- Model failures/non-finite outputs stop the run. Do not silently drop failed evaluations.

## Required study procedure

1. Freeze a source-linked parameter registry and scenario bounds.
2. Run at least two increasing powers of two to assess index stability.
3. Preserve the seed, Git SHA, parameter order, bounds, sample size, output variance, and all index estimates.
4. Compare first-order and total-effect indices to identify interactions.
5. Repeat for key outputs, including net water-consumption change and freshwater production.
6. Analyze sign changes and failure constraints in addition to variance shares.
7. Do not report these synthetic estimator tests as sensitivity results for the physical research question.

Application to the full coupled model remains pending until evidence-linked parameter ranges and validated model configurations are available.
