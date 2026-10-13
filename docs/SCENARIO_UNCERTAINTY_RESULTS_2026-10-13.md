# Scenario-only Monte Carlo and global sensitivity execution

**Run:** [GitHub Actions run #8](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38428133917)  
**Commit:** `ec7624afd7cecd34b12802a6e0d779a75ce97ff`  
**Artifact:** `scenario-only-uncertainty-study`, ID `11829716834`, SHA-256 `f8d4380906e0fe45ad5f377c828339b7f0eb06b08b516ebf8be63d114a4e7faf`, expires 2027-01-11.  
**Reproducibility:** seed 20261013; 20,000 Monte Carlo draws, 0 invalid draws; Sobol matrices of 512 and 2,048 points for 15 inputs and two outputs. Artifact manifest contains SHA-256 values for every output file.

## Results under the declared illustrative scenario ranges

- Net operational water-consumption change: median **+18.24 L** per one-hour scenario; 5th–95th percentiles **+2.45 to +45.37 L**.
- Conditional fraction with modeled net consumption change below zero: **1.935%**; above zero: **98.065%**.
- Modeled freshwater output: median **0 L**, 95th percentile **14.02 L**.
- Break-even freshwater-displacement fraction among draws with positive production: median **1.97**, 5th–95th percentiles **0.378 to 15.30**; **76.8%** of those positive-production draws require displacement above 100%, making net-water break-even impossible under the declared accounting for those draws.

These numbers are **not real-world probabilities or physical predictions**. The input ranges are illustrative independent uniform assumptions; the one-hour workload and baseline are not empirically calibrated; water activity is fixed at 0.995; and the MD model has not passed source-matched or held-out validation.

## Convergence and model-form warning

The estimated negative-net-water fraction was 2.08% at 5,000 draws, 1.87% at 10,000, and 1.935% at 20,000. This sign fraction is more stable at the larger prefixes, but the 5th percentile moved from 2.25 L at 5,000 to 2.45 L at 20,000. Do not declare the full Monte Carlo distribution converged yet.

For net-water change, absolute changes in Sobol first-order indices between 512 and 2,048 samples were generally modest (maximum about 0.020). For freshwater production, the index estimates were substantially less stable: total-effect changes reached about **0.099**. Do not report a definitive freshwater parameter ranking from this run.

The zero-production mass in the Monte Carlo output is an important failure-regime signal from the current thermal accounting: with membrane conductivity 0.03 W m⁻¹ K⁻¹, thickness 0.2 mm, 10 m² area, and the chosen interface-temperature model, the conductive term can exceed available recovered heat. This is not proof that the real system produces zero water; it shows that the outcome is sensitive to model structure and assumptions that must be validated.

## Decisions

1. Global sensitivity **execution** is now reproducible; its freshwater-output convergence is not established.
2. Keep the Monte Carlo convergence gate **false** until lower-tail and sign estimates meet a predeclared tolerance across larger independent seeds/sample sizes.
3. Keep unfitted validation, held-out validation, break-even envelope, and publication readiness **false**.
4. Before interpreting these outputs physically, source and justify distributions, validate membrane heat transfer and interface temperatures against experiments, and couple realistic cooling architecture and workload traces.
