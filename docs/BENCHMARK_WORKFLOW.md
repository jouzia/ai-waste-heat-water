# Literature Benchmark Workflow

## Objective

Convert published membrane-distillation experiments into auditable, reproducible model-validation cases without treating headline performance numbers as sufficient evidence.

## Evidence chain

1. Identify the original publication and stable identifier.
2. Confirm configuration: DCMD, AGMD, V-AGMD, SGMD, or other.
3. Extract membrane geometry, operating temperatures, flow conditions, feed composition, pressure, recovery, duration, outputs, and uncertainty where available.
4. Record the exact table, figure, equation, supplementary item, or page supporting every parameter.
5. Freeze the extracted case as a YAML benchmark.
6. Run the model without changing source conditions to improve agreement.
7. Record observed and predicted outputs in a result file.
8. Calculate MAE, RMSE, relative error and bias; use MAPE only where observed values are safely non-zero.
9. If a parameter was fitted, label the case as development data.
10. Reserve independent cases for held-out validation.
11. Preserve systematic failures instead of deleting difficult cases.

## Eligibility gate

A paper is quantitatively eligible only when the required variables for the selected model formulation can be reconstructed. A reported flux value by itself is not enough.

## Model-form discipline

If multiple credible transport correlations are applicable, evaluate them rather than selecting one because it gives the smallest error. The spread between defensible formulations is retained as model-form uncertainty when evidence cannot distinguish them.

## Current high-value sources

The 2026 pilot-scale AGMD validation study by Bindels et al. reports validation across 2,716 datapoints and multiple pilot configurations, but its data-availability statement says the authors do not have permission to share the aggregated dataset. It is therefore methodological evidence rather than an automatic machine-readable benchmark. See MD-PILOT-VALIDATION-2026 in SOURCES.yaml.

The 2026 open-access DCMD study by Sulaiman et al. reports experimental fluxes and validation against 14 independent literature datasets. It is a candidate for independent case extraction, but this repository must extract the actual operating conditions before treating it as validation evidence.

## Reproducibility rule

Every quantitative validation result must be traceable to:

source_id -> benchmark YAML -> model version/commit -> config hash -> output record -> error metrics

A result without that chain is not a publication-grade validation result.
