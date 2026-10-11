# GDR 3M DCMD model-form comparison — 2026-10-11

## Scope

This report records an exploratory test of the reduced-order channel model against the 12 condition-level fluxes extracted from the GDR 3M workbook. The development set is the six nominal 20 °C cold-side conditions; the held-out set is the six nominal 30 °C conditions. The split is by operating condition, but both sets come from one workbook and experimental campaign. This is **within-workbook held-out evaluation**, not independent external validation.

Observed flux is the OLS slope of the raw cumulative distillate-volume trace versus runtime divided by the workbook's 0.23088 m² membrane area. The `Theoretical` worksheet is not an independent target because its summary flux exactly reproduces that same slope.

## Model forms tested

- Heat-transfer correlation: Graetz–Leveque or WaterTAP.
- Channel geometry: smooth-channel hydraulic diameter/flow area or the workbook's spacer-porosity hydraulic diameter with flow area multiplied by spacer porosity.
- Membrane: 110 μm thickness; polypropylene polymer conductivity 0.22 W m⁻¹ K⁻¹ and vapor conductivity 0.026 W m⁻¹ K⁻¹ are engineering assumptions. The parallel mixing rule (effective (k_m approx 0.0551) W m⁻¹ K⁻¹) was used; the series mixing value is recorded as a bound but not independently fitted.
- Flow: nominal 1 L min⁻¹ on each side. Workbook sensor channels with negative values or `Inf` were excluded because their provenance/sign convention is unresolved.
- Feed salinity: 4 g L⁻¹ NaCl, with a low-salinity activity closure; liquid and latent-heat properties use IAPWS-IF97.
- Only membrane permeance was fitted, using a coarse log grid from 0.01 to 1000 kg m⁻² h⁻¹ bar⁻¹ in 0.25-decade steps. The fitting objective is squared log-relative flux error on the development set.

## Results at 16 cells

| Model form | Fitted permeance (kg m⁻² h⁻¹ bar⁻¹) | Fit at search boundary? | Development MAPE | Held-out MAPE | Held-out MAE (L m⁻² h⁻¹) | Held-out bias (L m⁻² h⁻¹) |
|---|---:|---|---:|---:|---:|---:|
| Graetz–Leveque, smooth channel | 1000.0 | Yes | 27.23% | 21.35% | 1.126 | −1.066 |
| Graetz–Leveque, spacer-porosity geometry | 1000.0 | Yes | 21.61% | 17.81% | 0.883 | −0.763 |
| WaterTAP, smooth channel | 177.83 | No | 47.38% | 35.75% | 1.776 | −1.776 |
| WaterTAP, spacer-porosity geometry | 100.0 | No | 62.94% | 53.79% | 2.638 | −2.638 |

## Grid-sensitivity finding

Predictions were compared at 4, 8, and 16 axial cells. Mean relative changes in predicted flux were:

| Model form | 4 → 8 cells | 8 → 16 cells |
|---|---:|---:|
| Graetz–Leveque, smooth channel | −5.71% | −2.77% |
| Graetz–Leveque, spacer-porosity geometry | −6.16% | −2.99% |
| WaterTAP, smooth channel | −8.49% | −44.29% |
| WaterTAP, spacer-porosity geometry | −8.94% | −62.38% |

The WaterTAP variants change markedly between 8 and 16 cells and are not numerically converged. Their fitted permeance also shifts with grid resolution because the counter-current solver's feasible parameter range changes. Do not select a “best” correlation based on the 4- or 8-cell results.

The Graetz–Leveque variants are more stable between 8 and 16 cells, but the fitted permeance sits at the upper search boundary (1000) and the model still underpredicts held-out flux. This is evidence that permeance is not identified under these assumptions and/or that the model's heat-transfer, membrane-conduction, or flow boundary conditions are inadequate. It is not evidence that the membrane physically has a permeance of 1000.

## Interpretation

**No tested model form currently passes predictive validation.** The current model is sensitive to axial discretization and heat-transfer correlation; the WaterTAP variants are especially unstable. The best 16-cell held-out MAPE in this exploratory run is 17.81%, but it is based on only six held-out conditions from the same campaign and a permeance fit that is boundary-limited. This number must not be presented as external validation or as a publication-ready performance claim.

The `30-45` condition is a particularly difficult held-out point: observed flux is about 2.14 L m⁻² h⁻¹ while several variants overpredict it substantially. This needs a source-data review and a residual investigation, not post-hoc deletion.

## Required next steps

1. Add and test explicit grid-convergence diagnostics for flux, outlet temperatures, and water/energy balances at 8, 16, and 32 cells.
2. Investigate the counter-current solver's convergence and feasible-permeance region under the WaterTAP correlation; do not silently accept nonconverged solutions.
3. Obtain a defensible membrane permeance or calibrate only after the heat-transfer and effective-conductivity assumptions are constrained by independent data.
4. Resolve the source workbook's conflicting membrane label and questionable flow channels; use the nominal 1 L min⁻¹ only as a documented provisional boundary condition.
5. Repeat the evaluation on an independent, source-matched DCMD dataset before calling the model validated.

Machine-readable outputs are generated by `scripts/validate_gdr_3m.py` and archived with the source-data workflow as `model_form_comparison.csv`, `model_form_metrics.csv`, and `model_form_metrics.json`. The workflow run and source workbook checksum are recorded in the GDR workbook audit.
