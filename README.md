# From AI Waste Heat to Water

**Research 2 — AI infrastructure waste-heat recovery for thermal desalination and net freshwater impact**

## Research question

Under what combinations of AI workload intensity, thermal conditions, waste-heat recovery efficiency, membrane-distillation operation, cooling burden, electricity-water intensity, and geographic water stress can waste-heat recovery produce a positive net freshwater benefit?

## Scientific principle

Gross freshwater production is not treated as net water benefit. The system boundary explicitly separates IT heat, recoverable heat, MD thermal duty, cooling duty, pumping, auxiliary electricity, direct cooling water, electricity-related water, withdrawal, consumption, and recovered freshwater.

## Reproducible demo

The presentation-safe demo can be run with `python scripts/run_demo.py`. It emits a JSON accounting ledger that keeps gross distillate, additional water consumption, declared avoided consumption, and net consumption change separate. Demo values are illustrative and are not validation results.

## Current implementation

- Reproducible Python package skeleton established.
- Transparent baseline energy and water accounting engine implemented.
- MD vapor-pressure transport primitive implemented with NIST SRD 69 water Antoine coefficients.
- Explicit first-order system thermal-balance module added.
- Parameter provenance registry added; unsupported literature numbers remain excluded from empirical claims.
- Reproducible benchmark-suite definitions added.
- Coupled system-model scope documented.
- Automated tests cover baseline limiting cases, MD temperature behavior, single-pass salinity concentration, and explicit water-accounting sign conventions.

## Evidence-led architecture

AI workload -> IT energy -> heat generation -> cooling architecture -> recoverable heat -> heat exchanger -> MD interface conditions -> vapor-pressure driving force -> freshwater -> cooling/pumping/pretreatment -> electricity-related water -> net consumption change.

## Key evidence anchors

Lei et al. (2025) demonstrate that workload-level data-center water use is highly sensitive to server efficiency, grid water factors, utilization, cooling technology, infrastructure efficiency, climate, and refresh cycle. Malaguti et al. (2026) show that MD cooling demand can approach the heating burden in some configurations and that pumping can be material at low single-pass recovery. NIST SRD 69 provides the water vapor-pressure coefficients used by the current pure-water transport primitive. Herrera et al. (2025) provides a probabilistic framework for AI-infrastructure water-footprint uncertainty.

## Model layers added

- **MD thermal layer:** separates latent vaporization duty from membrane conductive heat leak when membrane properties are supplied.
- **1-D DCMD channel layer:** resolves axial feed/permeate temperature and flow changes for co-current operation and explicitly couples counter-current operation as a two-point boundary-value problem.
- **Concentration polarization:** selectable exponential boundary-layer CPC model now couples feed-side mass transfer to membrane-interface salinity and IAPWS activity.
- **Hydraulic layer:** converts pressure drop, feed recovery, flow, and pump efficiency into electrical pumping demand; direct literature specific-energy inputs remain supported.
- **Cooling burden:** MD cooling duty can now propagate into electrical demand and direct cooling-water consumption instead of remaining a diagnostic-only value. Incremental water accounting excludes baseline facility cooling from the intervention burden.
- **Time-resolved workload profile:** piecewise-constant IT power and source-temperature intervals can be integrated to estimate thermally eligible duration and heat-weighted source temperature. This is a tested primitive, not yet coupled to measured workload traces or the full MD engine.
- **Source-structured DCMD runner:** a dedicated counter-current runner follows the published Keshavarzzadeh balance structure with explicit engineering property closures. Its eight-case smoke matrix checks software behavior only; it is not source-exact reproduction or experimental validation.
- **Uncertainty tools:** a seeded Monte Carlo scenario runner and Sobol first-order/total-effect estimators are implemented and covered by synthetic tests. Source-linked empirical distributions, convergence analysis, and study-level sensitivity results are still pending.
- **Interface temperatures:** measured/interface temperatures can override the reduced-order temperature-polarization estimate.
- **Salinity/thermodynamics:** standard-seawater cases now use IAPWS-08 water activity with an explicit single-pass concentration layer; concentrate salinity is reported.
- **Continuous integration:** GitHub Actions runs the test suite and Ruff on pushes and pull requests.

These additions do not supply unsupported membrane properties, heat-transfer coefficients, grid-water factors, or site-specific cooling assumptions. Membrane-specific transport parameters, channel heat-transfer coefficients, and geographic water factors remain explicit inputs awaiting source extraction.

## Scientific status

**No positive water-benefit conclusion is claimed.** The current baseline is a screening/accounting model, not an industrial digital twin. Before quantitative deployment claims, the study must validate the new channel transport correlations and concentration-polarization layer against source-matched experiments. The first literature case is a flat-sheet counter-current DCMD benchmark, for which the source confirms two recirculation rates and four NaCl concentrations; the benchmark remains unvalidated until the experimental observations and complete boundary conditions are reconstructed.

The next stages are source-matched membrane-property closures and experimental observations, quantitative unfitted validation, realistic cooling-architecture and heat-sink constraints, source-linked uncertainty distributions, Monte Carlo convergence, study-level Sobol/Morris sensitivity, site-specific electricity-water factors, geographic water-stress integration, break-even/failure-envelope analysis, multi-objective results, and the full manuscript. These remain incomplete; software tests do not substitute for physical validation.

## External data and legal reproducibility

The geographic evidence layer uses official scientific and government sources under their applicable reuse terms. WRI Aqueduct 4.0 is used for basin-level water-risk screening; NASA POWER/MERRA-2 is used for climate forcing; India OGD and India-WRIS are reserved for dataset-specific Indian hydrological evidence. Exact source version, retrieval date, license, transformation, and uncertainty are recorded. See `docs/DATA_PROVENANCE.md`, `docs/EXTERNAL_DATA_LEGAL.md`, and `docs/NASA_POWER_PROTOCOL.md`.

## Reproducibility policy

Every externally sourced parameter must carry a source identifier, definition, unit, applicability range, transformation, uncertainty treatment, and validation status. Scenario-only values remain visibly labelled. Negative or non-beneficial outcomes are preserved rather than filtered from the results.
