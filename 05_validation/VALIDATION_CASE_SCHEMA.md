# Validation case schema

This schema defines the minimum evidence required before a membrane-distillation case can be reported as numerical validation.

| Field | Required | Meaning |
|---|---|---|
| source_id | yes | Immutable literature/data source identifier |
| case_id | yes | Unique operating-condition identifier |
| configuration | yes | DCMD/AGMD/VMD/etc. and module geometry |
| source_location | yes | Table, figure, equation, supplement, or dataset location |
| observed_flux_kg_m2_h | yes for quantitative validation | Experimentally reported or lawfully digitized flux |
| predicted_flux_kg_m2_h | yes | Output from the frozen model/configuration |
| observed_outlet_feed_temperature_c | preferred | Source observation when available |
| predicted_outlet_feed_temperature_c | preferred | Model output |
| observed_outlet_permeate_temperature_c | preferred | Source observation when available |
| predicted_outlet_permeate_temperature_c | preferred | Model output |
| absolute_error | derived | Absolute observed-predicted difference |
| relative_error_percent | derived | Error normalized by observed value |
| fitted_parameters | yes | Explicit list; empty for unfitted validation |
| model_commit | yes | Git commit used for the prediction |
| config_hash | yes | Hash of the exact model/config inputs |
| source_license | yes | Reuse terms governing the evidence |
| status | yes | candidate / development / held_out / excluded / qualitative_only |

## Acceptance rules

1. A numerical validation result requires a traceable observed value.
2. The source operating conditions must be frozen before the prediction is generated.
3. Missing critical boundary conditions are not filled with undocumented defaults.
4. A parameter fitted to the same case disqualifies that case from being labelled held-out validation.
5. Relative error is undefined when the observed value is zero; do not report MAPE in that regime.
6. A source author's own statement that a model agrees with experiment is literature evidence, not an independent validation result for this repository.
7. Every reported failure is retained in the validation ledger.

## Current status

The Keshavarzzadeh 2020 benchmark is not yet numerically validated. The repository currently has the source conditions needed to identify the configuration, but the complete source-condition reconstruction and observed flux extraction remain pending.