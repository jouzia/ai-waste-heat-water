# From AI Waste Heat to Water

**Research 2 — AI infrastructure waste-heat recovery for thermal desalination and net freshwater impact**

## Research question

Under what combinations of AI workload intensity, thermal conditions, waste-heat recovery efficiency, membrane-distillation operation, cooling burden, electricity-water intensity, and geographic water stress can waste-heat recovery produce a positive net freshwater benefit?

## Scientific principle

Gross freshwater production is not treated as net water benefit. The system boundary explicitly separates IT heat, recoverable heat, MD thermal duty, cooling duty, pumping, auxiliary electricity, direct cooling water, electricity-related water, withdrawal, consumption, and recovered freshwater.

## Current implementation

- Reproducible Python package skeleton established.
- Transparent baseline energy and water accounting engine implemented.
- MD vapor-pressure transport primitive implemented with NIST SRD 69 water Antoine coefficients.
- Explicit first-order system thermal-balance module added.
- Parameter provenance registry added; unsupported literature numbers remain excluded from empirical claims.
- Reproducible benchmark-suite definitions added.
- Coupled system-model scope documented.
- Automated tests cover baseline limiting cases and MD temperature behavior.

## Evidence-led architecture

AI workload -> IT energy -> heat generation -> cooling architecture -> recoverable heat -> heat exchanger -> MD interface conditions -> vapor-pressure driving force -> freshwater -> cooling/pumping/pretreatment -> electricity-related water -> net consumption change.

## Key evidence anchors

Lei et al. (2025) demonstrate that workload-level data-center water use is highly sensitive to server efficiency, grid water factors, utilization, cooling technology, infrastructure efficiency, climate, and refresh cycle. Malaguti et al. (2026) show that MD cooling demand can approach the heating burden in some configurations and that pumping can be material at low single-pass recovery. NIST SRD 69 provides the water vapor-pressure coefficients used by the current pure-water transport primitive. Herrera et al. (2025) provides a probabilistic framework for AI-infrastructure water-footprint uncertainty.

## Scientific status

**No positive water-benefit conclusion is claimed.** The current baseline is a screening/accounting model, not an industrial digital twin. Before quantitative deployment claims, the study must add saline-feed activity, membrane-interface temperature polarization, latent/conductive heat balance, cooling and heat-sink constraints, hydraulic losses, site-specific electricity-water factors, uncertainty distributions, geographic water-stress data, literature reproduction, and physical validation where feasible.

## Reproducibility policy

Every externally sourced parameter must carry a source identifier, definition, unit, applicability range, transformation, uncertainty treatment, and validation status. Scenario-only values remain visibly labelled. Negative or non-beneficial outcomes are preserved rather than filtered from the results.
