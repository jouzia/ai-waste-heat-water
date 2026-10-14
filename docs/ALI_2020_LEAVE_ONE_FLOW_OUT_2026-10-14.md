# Ali et al. (2020) grouped leave-one-flow-out flux-law diagnostic

**Workflow:** [Ali source-data ingestion run #33](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38595300266)  
**Code commit:** `9201d1e8308c629a78e2c2489b9e42a5b7c7e0f6`  
**Artifact:** `ali-2020-dynamic-dcmd-source-data`, ID `11910080230`, SHA-256 `36c21f6458922ddc2c999443b135ac6ee45dd9a9395c141809162eede55a3e0d`, retained until 2027-01-12.  
**Source:** Ali, Orfi & Najib (2020), PLOS ONE, DOI [10.1371/journal.pone.0230207](https://doi.org/10.1371/journal.pone.0230207), CC BY 4.0.

## Design

The S1 steady-state ledger contains 16 observations across nominal flow groups 50, 100, 200, and 300 L/h, with four observations per group. The source reports one observation at 200.01 L/h; it is grouped with the nominal 200 L/h condition using a predeclared 0.1 L/h matching tolerance, while the raw value remains preserved in predictions.

Four folds hold out one entire nominal flow group at a time. No individual rows from the held-out flow enter that fold's fit. Two reduced flux-law forms are compared:

1. **Fixed TPC / single permeance:** TPC = 0.8; one permeance coefficient is fitted on the other three flow groups.
2. **Flow-dependent TPC:** a bounded three-parameter logistic TPC-versus-log-flow form plus permeance is fitted on the other three groups.

Two source interpretations are kept separate: the article's stated 0.5% feed salinity (represented as 5 g/kg) and the S1 measured TDS_E field used as a salinity proxy. The source discrepancy is not silently resolved.

## Out-of-fold results

| Salinity interpretation | Model form | Out-of-fold MAE (kg m⁻² h⁻¹) | Out-of-fold RMSE (kg m⁻² h⁻¹) | Mean bias (kg m⁻² h⁻¹) |
|---|---|---:|---:|---:|
| Reported 0.5% salinity | Fixed TPC / single permeance | 0.5713 | 0.6879 | −0.0703 |
| Reported 0.5% salinity | Flow-dependent TPC | 0.1164 | 0.1439 | −0.0392 |
| S1 TDS_E proxy | Fixed TPC / single permeance | 0.5698 | 0.6847 | −0.0684 |
| S1 TDS_E proxy | Flow-dependent TPC | 0.1226 | 0.1716 | −0.0161 |

Each aggregate contains 16 out-of-fold predictions: four observations from each of the four held-out flow levels. The flow-dependent model lowers out-of-fold MAE by about 79.6% under the stated salinity interpretation and 78.5% under the TDS_E proxy interpretation. This is an exploratory within-source comparison, not proof that the more flexible model is physically correct.

## Fold-level stability

| Held-out flow (L/h) | Fixed TPC MAE | Flow-dependent TPC MAE | Fitted log-flow slope, stated salinity |
|---:|---:|---:|---:|
| 50 | 0.7705 | 0.1000 | 2.353 |
| 100 | 0.2314 | 0.0661 | 1.845 |
| 200 | 0.4550 | 0.1188 | 1.631 |
| 300 | 0.8282 | 0.1806 | 1.714 |

All four folds favor the flow-dependent form on MAE, and the fitted slope remains positive in every fold. However, the flow-dependent alternative has three fitted parameters on only 12 training observations per fold; the small four-group dataset is not sufficient to establish universal correlation validity or extrapolation behavior. The relative-error metric is also large because several observed fluxes are small, so absolute-error metrics are emphasized.

## Interpretation and limits

- The fixed-TPC/single-permeance model has systematic out-of-fold error under this temperature-polarization reconstruction; the result is evidence against treating that simple flux law as adequate across all tested flows without further source-backed modeling.
- The flow-dependent TPC form is a candidate model form, not a validated correction. Its better grouped cross-validation score does not establish that TPC is truly a function of flow alone; temperature, geometry, salinity, and measurement uncertainty may be confounded.
- All folds derive from the same paper, membrane/module, and experimental campaign. This is **within-source grouped cross-validation**, not independent external validation.
- This diagnostic tests the reduced steady-state flux law only. It does not validate transient outlet-temperature dynamics, accumulated-mass semantics, channel energy balances, cooling architecture, electricity-water factors, or net freshwater benefit.
- The source's 0.5% salinity statement remains inconsistent with the S1 TDS_E values. Both interpretations are reported.
- Do not select the flow-dependent form for the main claim solely because its MAE is lower. Compare physical plausibility, parameter identifiability, residual structure, and a genuinely independent dataset before model-form selection.

**Decision:** this improves the within-source model-form diagnostic. The independent/held-out validation and final validation-grade model-form gates remain false.
