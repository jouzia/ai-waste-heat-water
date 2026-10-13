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

An exploratory execution was completed on 2026-10-13 with 512 and 2,048 samples per Sobol matrix for net water-consumption change and freshwater production. The run is archived in [GitHub Actions run #8](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38428133917). Net-water index differences between sample sizes were generally smaller than those for freshwater production; freshwater-output index differences reached about 0.10 in total-effect estimates. This is not adequate to declare the freshwater sensitivity ranking converged. All bounds are illustrative scenario assumptions and water activity is fixed at 0.995, so the results are execution diagnostics, not evidence-calibrated physical sensitivities.
