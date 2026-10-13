# Independent-seed Monte Carlo convergence — phase 2

**Workflow:** [Independent-seed Monte Carlo convergence audit, run #4](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38439319858)  
**Code commit:** `de1b2d6e5292e2a12cc33aa875a5e6d8e600f8c0`  
**Artifact:** `independent-seed-monte-carlo-convergence`, ID `11833574566`, SHA-256 `688df205920a034cfc8cfd0a8d2941a5e2741dd00ae1bfeb5fabf93cb0266bed`; retained until 2027-01-11.  
**Purpose:** Numerical Monte Carlo convergence under the repository's illustrative independent-uniform scenario ranges. This is not empirical uncertainty calibration or model validation.

## Predeclared phase-2 design

Phase 1 used three independent 20,000-draw seeds and one 50,000-draw run. It failed two predeclared tolerances: net-water 5th-percentile spread was 5.26% versus a 5% limit, and freshwater-output 95th-percentile spread was 0.712 L versus a 0.5 L limit. Rather than loosening criteria, phase 2 increased all sample sizes.

| Seed | Draws | Net-water P05 (L) | Median (L) | P95 (L) | Fraction with ΔW below 0 | Freshwater output P95 (L) |
|---:|---:|---:|---:|---:|---:|---:|
| 20261017 | 50,000 | 2.495 | 18.179 | 45.526 | 1.984% | 13.321 |
| 20261018 | 50,000 | 2.423 | 18.079 | 45.541 | 2.058% | 13.658 |
| 20261019 | 50,000 | 2.537 | 18.207 | 45.704 | 1.946% | 13.626 |
| 20261020 | 100,000 | 2.445 | 18.225 | 45.505 | 2.077% | 13.615 |

## Acceptance checks

| Diagnostic | Observed spread | Predeclared limit | Result |
|---|---:|---:|---|
| Net-water P05 relative spread | 4.58% | 5.00% | Pass |
| Fraction with ΔW below zero | 0.131 percentage points | 0.50 percentage points | Pass |
| Net-water P95 relative spread | 0.437% | 2.00% | Pass |
| Freshwater-output P95 absolute spread | 0.337 L | 0.500 L | Pass |

All four numerical convergence checks passed. The Monte Carlo convergence gate can therefore be marked **true for numerical stability under the declared scenario ranges**.

## Interpretation limits

- The parameter ranges remain illustrative independent uniforms, not empirical distributions.
- The modeled median freshwater output is zero, and the sign fraction is conditional on the model, scenario bounds, and water-displacement counterfactual.
- This does not validate the MD model, demonstrate a real-world probability of net water benefit, or support a water-positive claim.
- The Sobol indices for freshwater output remain unstable between the existing 512- and 2,048-point matrices; sensitivity-ranking convergence remains unresolved even though Monte Carlo convergence passed.
- Independent validation, source reconstruction, geography/electricity-water integration, and manuscript/publication gates remain incomplete.
