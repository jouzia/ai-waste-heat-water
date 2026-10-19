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

Lei et al. (2025) demonstrate that workload-level data-center water use is highly sensitive to server efficiency, grid water factors, utilization, cooling technology, infrastructure efficiency, climate, and refresh cycle. Malaguti et al. (2026) show that MD cooling demand can approach the heating burden in some configurations and that pumping can be material at low single-pass recovery. Katakam et al. (online 2026; DOI 10.1016/j.watres.2026.126748) analyze system-scale desalination options for data-centre water demand and introduce a water-stress-linked metric; Wang et al. (2026; DOI 10.1016/j.ese.2026.100702) analyze global data-centre/WWTP water and heat symbiosis. These studies narrow the novelty claim; see `docs/PRIOR_ART_GAP_AUDIT_2026-10-14.md`. NIST SRD 69 provides the water vapor-pressure coefficients used by the current pure-water transport primitive. Herrera et al. (2025) provides a probabilistic framework for AI-infrastructure water-footprint uncertainty.

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
- **Evidence-gate regression tests:** benchmark entries with empty primary-observation ledgers cannot be labeled development-validated or held-out-validated; software smoke tests remain distinct from empirical validation.
- **Bounded counterfactual displacement:** avoided freshwater consumption is either an explicit, substantiated volume no greater than distillate produced or a declared displacement fraction between 0 and 1; the two inputs cannot be combined.

These additions do not supply unsupported membrane properties, heat-transfer coefficients, grid-water factors, or site-specific cooling assumptions. Membrane-specific transport parameters, channel heat-transfer coefficients, and geographic water factors remain explicit inputs awaiting source extraction.

## Scientific status

**No positive water-benefit conclusion is claimed.** The current baseline is a screening/accounting model, not an industrial digital twin. Before quantitative deployment claims, the study must validate the new channel transport correlations and concentration-polarization layer against source-matched experiments. The first literature case is a flat-sheet counter-current DCMD benchmark, for which the source confirms two recirculation rates and four NaCl concentrations; the benchmark remains unvalidated until the experimental observations and complete boundary conditions are reconstructed.

The next stages are source-matched membrane-property closures and experimental observations, quantitative unfitted validation, realistic cooling-architecture and heat-sink constraints, source-linked uncertainty distributions, Monte Carlo convergence, study-level Sobol/Morris sensitivity, site-specific electricity-water factors, geographic water-stress integration, break-even/failure-envelope analysis, multi-objective results, and the full manuscript. These remain incomplete; software tests do not substitute for physical validation.

## External data and legal reproducibility

The geographic evidence layer uses official scientific and government sources under their applicable reuse terms. WRI Aqueduct 4.0 is used for basin-level water-risk screening; NASA POWER/MERRA-2 is used for climate forcing; India OGD and India-WRIS are reserved for dataset-specific Indian hydrological evidence. Exact source version, retrieval date, license, transformation, and uncertainty are recorded. See `docs/DATA_PROVENANCE.md`, `docs/EXTERNAL_DATA_LEGAL.md`, and `docs/NASA_POWER_PROTOCOL.md`.

## Literature and validation provenance

The source register in `01_literature/literature_matrix.csv` distinguishes primary experiments, secondary reproductions, model studies, and open datasets, and records the specific validation gap for each. The 2026 analysis by Malaguti et al. makes cooling and pumping burdens central constraints; this project therefore does not claim that waste heat alone makes MD viable. The intended contribution is the coupled, site- and workload-aware **net freshwater impact** accounting layer, evaluated only after source-matched membrane validation. See `docs/ALI_2020_TRANSIENT_SOURCE_AUDIT.md` for the transient DCMD benchmark's source-confirmed conditions and extraction rules.
The falsifiable research question, counterfactual definition, hypothesis set, comparison plan, and release gate are specified in `docs/RESEARCH_GAP_AND_FALSIFIABLE_DESIGN.md`.
The uncertainty register distinguishes evidence-based distributions from engineering priors and scenario grids: `docs/UNCERTAINTY_PRIOR_REGISTER.md`.

## Retrieving the open DCMD benchmark

The GDR/NREL Villa et al. (2018) dataset is available under CC BY 4.0. To retrieve one configuration and generate a local SHA-256 manifest:

```bash
python scripts/download_gdr_villa.py --dataset clarcor-countercurrent
```

Use `--dataset all` to download the full seven-workbook collection (about 96 MB). Raw workbooks are written under the git-ignored `data/raw/gdr_villa_2018/` directory. The source page identifies the `Specifications` sheet as experiment inputs, `Data` as the full data, temperature-named sheets as subsets, and `Theoretical` as steady-state experimental values plus calculated values. Do not mix these categories: quantitative extraction and source-condition crosswalk are still pending.

## Local verification

Run the regression suite and lint checks before interpreting any quantitative output:

```bash
python -m pip install -e ".[dev]"
pytest -q
ruff check .
```

Latest recorded software CI evidence is in `docs/CI_STATUS_2026-10-11.md`. Software tests and lint are separate from empirical membrane-model validation.

## Reproducibility policy

Every externally sourced parameter must carry a source identifier, definition, unit, applicability range, transformation, uncertainty treatment, and validation status. Scenario-only values remain visibly labelled. Negative or non-beneficial outcomes are preserved rather than filtered from the results.
