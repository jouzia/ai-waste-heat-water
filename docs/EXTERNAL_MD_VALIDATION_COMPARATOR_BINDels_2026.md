# External validation-practice update: Bindels et al. (2026)

## Bibliographic record

Bindels, M., Andrés-Mañas, J. A., Ding, W., Hitsov, I., Mutlu-Salmanli, O., Hardikar, M., Cath, T. Y., Vanneste, J., Vidic, R. D., Achilli, A., Pawar, R., Koyuncu, I., Hickenbottom, K. L., Nelemans, B., Zaragoza, G., & Childress, A. E. (2026). “Pilot-scale membrane distillation modeling: Validation, comparison, and consensus.” *Desalination*, 620, 119674. https://doi.org/10.1016/j.desal.2025.119674

Accessible records:
- Publisher article: https://www.sciencedirect.com/science/article/pii/S0011916425011518
- Open institutional full-text record: https://biblio.ugent.be/publication/01KAX50FYWCX4MPAGFQ9E5AKZR
- Published PDF landing/download record: https://backoffice.biblio.ugent.be/download/01KAX50FYWCX4MPAGFQ9E5AKZR/01KB2ZKP3MJ3J1R7HTCZWTF3V8

## What the source reports

The paper compares and refines four pilot-scale air-gap membrane distillation (AGMD) and vacuum-assisted AGMD (V-AGMD) model formulations using an aggregated 2,716-point experimental dataset spanning feed salinity, module size, membrane and spacer configuration, and both AGMD and V-AGMD systems. It reports using root-mean-square error and mean error and describes changes involving Nusselt-number correlations, membrane thermal-conductivity resistance in series, the ePTFE support layer in the air gap, and entrapped distillate in the air gap.

The publisher's data-availability statement says the authors do not have permission to share the aggregated dataset. The study is therefore accessible as a methodological and literature comparator, but not a reproducible external data benchmark for this repository.

## Consequences for Research 2

1. **Do not claim first model validation/comparison in MD.** Cross-model, multi-configuration validation is established prior art.
2. **Keep configuration boundaries explicit.** The comparator studies pilot-scale AGMD/V-AGMD; Research 2's present primary validation cases include DCMD and cannot be treated as the same configuration without a justified transport/boundary mapping.
3. **Make model-form uncertainty visible.** Freeze model variants before comparing held-out conditions; report errors by condition/configuration, not only pooled aggregate metrics. Do not tune a model against the same held-out observations later reported as validation.
4. **Do not imply replication of the 2,716-point result.** The aggregated data are not shared. No values from that study are entered into this project's experimental observation ledger.
5. **Keep the accessible Villa et al. 12-condition benchmark as a distinct validation workstream.** Audit measured channels, area/time/unit conversions, and the train/holdout split before interpreting performance. Workbook-derived/theoretical columns are not independent observations.
6. **Link validation quality to downstream conclusions.** If model rankings or flux predictions change materially under defensible model forms, propagate that variation through freshwater output and break-even analysis; if no defensible validation domain is established, report the system-level analysis as exploratory screening only.

## Limitations and source discipline

This note is based on the published abstract/metadata, institutional repository record, and accessible article PDF. It does not assert that every equation or table in the paper has been independently reimplemented. The source does not provide permission to reuse its aggregated dataset; no dataset reconstruction or numeric transfer was attempted.

## Status

Literature-matrix entry added. This is a prior-art and validation-design update, **not** completion of the project's unfitted or independent validation gates.
