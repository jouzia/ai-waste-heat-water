# Conditional break-even and failure-envelope execution

**Workflow:** [Break-even and failure envelope run #1](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38429966351)  
**Commit:** `3ec6ef1693986199b7b0743fce25f795dc6ebbdf`  
**Artifact:** `break-even-failure-envelope`, ID `11830905144`, SHA-256 `1090890a7e0fd88a52d7dbd15d9deb6dc8f274790c40e724a036e7f45a947eb7`, expires 2027-01-11.  
**Coverage:** 5,184 unique combinations for the threshold envelope and 25,920 rows across five freshwater-displacement fractions per combination. Artifact manifest includes checksums for both CSV outputs.

## Conditional scenario-grid results

| Classification | Combinations | Share of scenario grid |
|---|---:|---:|
| No freshwater production | 2,808 | 54.17% |
| Break-even impossible even at 100% freshwater displacement | 1,730 | 33.37% |
| Break-even possible at some displacement fraction | 646 | 12.46% |
| **Total** | **5,184** | **100%** |

Among the 2,376 grid combinations that produced nonzero water, the median break-even displacement fraction was **2.47** and the 95th percentile was **27.85**. A threshold above 1 means that even complete freshwater displacement cannot offset modeled additional water consumption under the declared boundary.

These are **fractions of an illustrative parameter grid**, not probabilities that a real facility will fail. Grid points are not random draws from empirical distributions, and the MD model has not passed source-matched or independent validation.

## Input envelope

- Recoverable heat fraction: 0.2, 0.5, 0.8, 1.0
- Temperature-polarization coefficient: 0.6, 0.8, 1.0
- Membrane permeance: 5, 15, 25 kg m⁻² h⁻¹ bar⁻¹
- Membrane area: 2, 5, 10, 20 m²
- Grid electricity-water factor: 0.1, 0.5, 1, 2 L/kWh
- Cooling-water intensity: 0, 0.2, 1 L/kWh facility electricity
- Incremental facility electricity: 2, 10, 20 kWh per one-hour scenario
- Freshwater displacement fraction: 0, 0.25, 0.5, 0.75, 1

Other model values are fixed screening assumptions, including water activity 0.995, 70 °C source heat, 25 °C cold side, membrane conductivity 0.03 W m⁻¹ K⁻¹, and membrane thickness 0.2 mm.

## Interpretation

This envelope demonstrates that the result is highly conditional on production being thermally feasible and on actual freshwater displacement. It does not establish a site-specific failure rate, a universal break-even threshold, or a recommendation for cooling architecture. The break-even/failure **execution** gate is complete; physical validity of the envelope remains blocked by source-matched MD validation, sourced parameter ranges, and geographic electricity-water factors.
