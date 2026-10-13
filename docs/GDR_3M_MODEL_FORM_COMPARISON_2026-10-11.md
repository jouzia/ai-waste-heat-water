# GDR Villa 3M DCMD model-form comparison

Date: 2026-10-11  
Workflow commit: `a227769a17fd6c647ba0f78cb5b2e65c5875ba99`  
Workflow run: [GDR DCMD model validation #1](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38150806555)  
Input summary: `04_experiments/literature_benchmarks/MD-OEDI-VILLA-2018_3M_flux_summary.csv`

## Question and split

This is a diagnostic comparison of two heat-transfer correlations and two channel-geometry assumptions on 12 condition-level observations from one GDR/NREL Villa et al. workbook. The six 20 °C cold-side nominal-setpoint conditions were used to fit a single effective membrane permeance; six 30 °C cold-side conditions were held out by condition. The split is not independent external validation and must not be presented as such.

## Results

Metrics below are for volumetric flux in L m⁻² h⁻¹. Bias is predicted minus observed.

| Model form | Fitted permeance (kg m⁻² h⁻¹ bar⁻¹) | Fit at search boundary? | Development MAE | Development RMSE | Development bias | Development MAPE | Held-out MAE | Held-out RMSE | Held-out bias | Held-out MAPE |
|---|---:|:---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Graetz–Lévêque + smooth channel | 1000.0 | Yes | 1.9920 | 2.0986 | −1.9920 | 27.23% | 1.1257 | 1.3202 | −1.0660 | 21.35% |
| Graetz–Lévêque + spacer-porosity geometry | 1000.0 | Yes | 1.5843 | 1.6747 | −1.5843 | 21.61% | 0.8828 | 1.0114 | −0.7625 | 17.81% |
| WaterTAP correlation + smooth channel | 562.34 | No | 0.4671 | 0.4933 | −0.4671 | 6.96% | 0.3161 | 0.4157 | +0.2445 | 10.94% |
| WaterTAP correlation + spacer-porosity geometry | 562.34 | No | 0.1326 | 0.2154 | −0.1170 | 2.41% | 0.5461 | 0.6186 | +0.5165 | 14.91% |

The two Graetz–Lévêque fits reach the upper permeance search bound of 1000. This is a parameter-identifiability/model-form warning, not a successful unconstrained estimate. The WaterTAP variants fit the development conditions more closely, but the best development MAPE does not give the best held-out MAPE. This is evidence that the result depends on heat-transfer and geometry assumptions.

## Interpretation

1. The present reduced-order channel model does not yet provide sufficiently stable cross-condition predictions for use as an empirically validated MD transport engine.
2. A within-workbook held-out split is useful for exposing overfitting and model-form sensitivity, but it cannot replace validation against a separately sourced experimental study.
3. The workbook summary flux agrees with the OLS-derived cumulative-volume slope because it is a processing cross-check, not an independent observation source.
4. Flow rate is treated as nominal because the workbook's flow channels contain inconsistent signed/non-finite values. The assumed membrane conductivity uses a parallel mixing rule, with the series value exported only as a bound. These are engineering assumptions.
5. Predicted outlet temperatures also require explicit residual analysis against the measured outlet temperatures; flux-only ranking is insufficient.

## Required next steps

- Resolve source-level geometry and flow provenance before treating any model variant as physically preferred.
- Add parameter-boundary status to the machine-readable summary and preserve boundary-hit fits as diagnostics rather than unqualified optimization successes.
- Compare predicted and measured outlet temperatures as well as flux.
- Perform spatial-grid convergence and parameter-identifiability analysis.
- Use source-matched observations and an independent study for final validation; do not tune on held-out observations.
- Keep the results and caveats in the final manuscript even if later model variants improve the metrics.

## Reproducibility

The workflow uploads `model_form_comparison.csv`, `model_form_metrics.csv`, and `model_form_metrics.json` as the artifact `gdr-model-validation`. The artifact SHA-256 reported by GitHub Actions is `8af512b47b077e27af349da2cf181796d352c9b0f031b5e6e35d96ebca3d0deb`.

This note records the actual diagnostic output; it does not claim source-exact reconstruction, independent validation, or net-water-benefit evidence.
