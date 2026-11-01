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


## Higher-resolution convergence audit (2026-10-14)

A follow-up nested Sobol comparison was run at 4,096 and 8,192 samples per matrix with the same seed (20261023), using the same 15 independent-uniform scenario ranges and the two outputs used in the earlier exploratory run. Reproducible outputs are in [workflow run #1](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38595867645), artifact ID `11908833471`, SHA-256 `d2a14213799c49bfbb1d92fa425feb43722b3422d50c0cc8b9340491000003bf`, retained until 2027-01-12.

- **Net-water output:** maximum absolute change in total-effect index was 0.00182; maximum rank shift was 1 position.
- **Freshwater-output:** maximum absolute change in total-effect index was 0.02885; maximum rank shift was 0 positions. The top-five total-effect ranking was identical at 4,096 and 8,192.
- Freshwater production's top five were recoverable-heat fraction, IT power, TPC, recovery efficiency, and heat-exchanger effectiveness. These are conditional rankings under the current model and bounds, not general truths about data centres.
- The 4,096/8,192 comparison improves the numerical stability evidence relative to the earlier 512/2,048 run, but the largest freshwater total-effect index shift is still about 0.029. Treat rank order as stable for this nested sequence while retaining uncertainty about individual index magnitudes and any inference beyond the chosen ranges.

The result is **numerical sensitivity convergence under illustrative assumptions only**. It does not repair the model's lack of empirical validation, calibrate input distributions, justify a real-world probability, or complete the geographic and source-validation gates.
