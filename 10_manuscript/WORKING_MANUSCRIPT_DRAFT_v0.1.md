# Working manuscript draft v0.1 — evidence-bounded

**Status:** Internal working draft; not submission-ready. The manuscript-and-supplement gate remains false. This file deliberately distinguishes completed implementation diagnostics from scientific validation and leaves claims unresolved where primary evidence is missing.

## Working title

**From AI Waste Heat to Water: A Counterfactual Net-Operational-Water Framework for Sustainable AI Infrastructure**

## Abstract (provisional; do not submit)

AI infrastructure consumes water directly through some cooling systems and indirectly through electricity generation. Recovering low-grade data-centre heat for membrane distillation (MD) could produce freshwater, but gross distillate production is not equivalent to a net freshwater benefit: heat availability and temperature, cooling-system changes, pumping and auxiliary electricity, electricity-related water consumption, and the displaced water source all affect the result. This study develops a source-traceable accounting and modelling framework to evaluate the conditional net operational blue-water impact of waste-heat-assisted MD against an explicit counterfactual. The framework separates physical water volumes from basin-level water-risk indicators and keeps withdrawals distinct from consumptive use. The repository implements heat/workload, MD transport, cooling and hydraulic burdens, scenario uncertainty, sensitivity analysis, break-even analysis, and a geographic screening interface. Preliminary software and numerical diagnostics are reproducible, including a within-source leave-one-flow-level-out comparison of two temperature-polarization forms and a higher-resolution Sobol convergence audit. However, primary-source reconstruction and independent experimental validation remain incomplete; transient mass-field semantics are unresolved, input ranges remain illustrative, and site-specific electricity-water factors have not been joined. Therefore, no validated deployment prediction or positive net-water-benefit claim is made at this stage. The final abstract, quantitative conclusions, and publication decision must be written only after the primary-source, independent-validation, geographic, and reproducibility gates pass—or the paper's claims are narrowed to the evidence that can be established.

## 1. Introduction

Data-centre water impacts cannot be represented by one universal water-use coefficient. Workload-level analysis by Lei et al. identifies server efficiency, electricity-generation water factors, utilization, cooling technology, infrastructure efficiency, climate, inactive servers, and refresh cycles as important determinants, with large variation across scenarios. This makes the operational context and the accounting boundary central to any claim that an intervention saves water. See Lei et al. (2025), *Resources, Conservation and Recycling*, 219, 108310, DOI: 10.1016/j.resconrec.2025.108310.

Membrane distillation is a thermally driven separation process that may use low-grade heat. Nevertheless, the availability of a heat source does not guarantee useful water production. The thermal driving force depends on membrane-interface temperatures and feed chemistry; temperature and concentration polarization can reduce the effective vapour-pressure difference. Cooling duty, circulation and pumping, pretreatment, post-treatment, and the actual destination of product water can change the system-level result. A model that reports gross distillate alone does not establish water savings.

The data-centre-to-desalination concept is not itself a new contribution. Prior work includes data-centre cooling coupled to DCMD (Kanbur et al., 2020, DOI 10.1002/er.5677), a data-centre waste-heat/DCMD techno-economic case study (Wyon, 2025), CPU-waste-heat MD (Chen et al., 2026), and data-centre waste heat for seawater preheating in reverse osmosis (Yang et al., 2026, DOI 10.1016/j.apenergy.2026.127428). Recent work further narrows the contribution: Katakam et al. (online 2026; DOI 10.1016/j.watres.2026.126748) model system-scale desalination options for data-centre freshwater demand and introduce a water-stress-linked metric; Wang et al. (2026, DOI 10.1016/j.ese.2026.100702) conduct global geospatial and life-cycle analysis of data-centre/wastewater-treatment-plant symbiosis, including treated-effluent cooling and bidirectional heat recovery. These studies use pathways and boundaries that differ from membrane-distillation product-water generation, but they overlap substantially with the broad themes of data-centre water impact, heat recovery, geographic context, and net environmental benefits. The defensible novelty claim must therefore be limited to the specific, reproducible combination actually demonstrated here: counterfactual operational blue-water accounting with separate withdrawal/consumption boundaries, MD heat-quality and cooling/pumping constraints, and source-audited uncertainty/failure envelopes. It must not claim the first data-centre desalination framework, first water-stress metric, first global geospatial water assessment, or first waste-heat/water symbiosis study. The contribution remains provisional until full-text prior-art comparison and independent validation are completed.

The MD validation lineage is itself a critical issue. Martínez-Díez and Vázquez-González (1999), DOI 10.1016/S0376-7388(98)00349-4, is the primary experimental provenance target for flat-sheet DCMD conditions later used by Keshavarzzadeh (2020), DOI 10.1038/s41598-020-73964-7. A published model's reported agreement with experiments is not validation of a new implementation. This repository therefore requires source observations and boundary conditions to be reconstructed and compared against a frozen, unfitted implementation. A recent cross-system comparator reinforces this requirement: Bindels et al. (2026; DOI 10.1016/j.desal.2025.119674) compared and refined four pilot-scale AGMD/V-AGMD models against 2,716 aggregated observations and identified model-structure choices affecting predictions. The authors state that they cannot share the aggregated dataset, so this paper is methodological prior art rather than a directly reproducible benchmark for the present study. Its AGMD/V-AGMD configuration is not interchangeable with the DCMD validation cases considered here. The relevant design implication is to freeze model forms before held-out evaluation, report condition-specific errors and model-form sensitivity, and propagate unresolved prediction differences into the net-water and break-even analyses. See `docs/EXTERNAL_MD_VALIDATION_COMPARATOR_BINDels_2026.md`.

### Research question

Under what combinations of time-varying recoverable heat, MD operating conditions, cooling and pumping burden, electricity-related water intensity, and declared water-displacement counterfactual does waste-heat-assisted MD reduce net operational blue-water consumption relative to a defined baseline?

### Hypotheses and falsification criteria

- **H1 — Conditionality:** MD gross distillate does not by itself determine the sign of net water impact. Falsified if a complete, boundary-consistent accounting shows the sign is invariant across all supported scenarios.
- **H2 — Heat quality and availability:** time-varying source temperature and eligible operating duration materially constrain usable heat and product-water output. Falsified if these variables do not change results over empirically supported ranges.
- **H3 — Cooling and auxiliary burden:** incremental cooling, pumping, and electricity-related water can materially reduce or reverse the apparent water benefit. Falsified if their bounded contributions are negligible in all supported operating regimes.
- **H4 — Geographic context:** local water-risk context changes the interpretation and prioritization of a physical water-volume result but is not itself a physical water-volume multiplier. The analysis must keep these two quantities separate.

## 2. System boundary and estimand

The primary estimand is the change in operational blue-water consumption between an intervention and a specified baseline over the same service and time horizon:

\[
\Delta W_{\mathrm{net}} =
W_{\mathrm{consumed, intervention}} -
W_{\mathrm{consumed, baseline}} -
W_{\mathrm{displaced, substantiated}}.
\]

A negative value indicates lower net consumption under this sign convention; a positive value indicates increased net consumption. The sign convention must be checked against the executable accounting implementation and frozen before final analysis.

The ledger must distinguish at least:

1. direct facility cooling-water withdrawal and consumption;
2. electricity-generation water withdrawal and consumption for IT and intervention auxiliary loads;
3. gross MD distillate and water meeting the intended quality specification;
4. additional cooling, pumping, pretreatment, and post-treatment burdens;
5. the volume of freshwater consumption actually displaced, capped by substantiated product-water use;
6. baseline versus incremental burdens, so existing data-centre cooling is not incorrectly charged entirely to the intervention;
7. physical water volume versus contextual basin-risk indicators.

Withdrawal is not interchangeable with consumption. The water accounting must state whether each factor is consumption- or withdrawal-based and must not combine incompatible factors without explicit conversion or a sensitivity case. Aqueduct risk scores are used for basin-level screening and stratification only, never as multipliers on water volumes.

## 3. Model and data

### 3.1 Evidence hierarchy

Every parameter and observation must be assigned one of these evidence classes: (i) primary measured data, (ii) source-reported derived data, (iii) independently published secondary data, (iv) calibrated parameter, (v) illustrative scenario assumption, or (vi) unknown/unresolved. Only the first categories with a documented provenance chain may support empirical claims. Illustrative ranges can test code and explore conditional scenarios but cannot be described as empirical probability distributions.

### 3.2 MD transport and thermal model

The codebase includes a source-structured one-dimensional DCMD formulation, a counter-current runner, membrane vapor-pressure transport primitives, concentration-polarization options, hydraulic energy accounting, cooling burden propagation, and time-resolved workload primitives. Software correctness is necessary but not sufficient: source-equation reproduction, unit consistency, physical admissibility, and comparison against experimental observations must be independently demonstrated.

The first primary benchmark is the flat-sheet PTFE DCMD experiment of Martínez-Díez and Vázquez-González (1999). Its observation ledger must include a source locator, axis calibration and pixel coordinates for digitized points, units, salinity, inlet temperatures, flow rates, membrane properties and geometry, area, transformation code, extraction uncertainty, and a repeat extraction for a subset of figure-derived observations. Missing conditions must remain missing; they cannot be filled with convenient defaults.

The Ali, Orfi and Najib (2020) transient study provides source-linked supporting workbooks and valuable dynamic diagnostics. However, the raw `mw (kg)` field is nonmonotonic in 14 of 19 complete timed worksheet traces. Its cumulative/reset semantics remain unresolved, so previously reported mass-error metrics are withdrawn and mass-flux comparisons based on that field are disabled. Temperature residuals can be reported as diagnostics with explicit limitations, but they do not resolve the mass-measurement issue.

### 3.3 Validation design

The validation sequence is frozen as: source recovery → observation extraction → provenance/unit audit → independent extraction check → frozen unfitted comparison → development/holdout split → calibration on development cases only if justified → final held-out evaluation. A within-source cross-validation split is not independent validation. The final report must disclose all failed cases, inadmissible states, exclusions, and source mismatches.

## 4. Preliminary results that are currently supportable

### 4.1 Within-source steady-state comparison

The 14 October 2026 repository record reports four leave-one-flow-level-out folds over 16 observations from the Ali et al. (2020) source. Each fold favored the flexible three-parameter flow-dependent temperature-polarization form over the fixed-coefficient form. Aggregate out-of-fold MAE was 0.116 versus 0.571 kg m⁻² h⁻¹; RMSE was 0.144 versus 0.688 kg m⁻² h⁻¹, conditional on the documented 0.5% salinity interpretation. This is a within-source model-form diagnostic, not independent validation. The comparison remains sensitive to source interpretation and cannot be promoted to a general predictive-accuracy claim.

### 4.2 Numerical sensitivity convergence

The higher-resolution Sobol audit at 4,096 and 8,192 samples per matrix preserved the top-five freshwater-output total-effect ranking, with a maximum total-effect index change of approximately 0.029. This supports numerical stability of the estimator under the declared setup. The ranges remain illustrative independent-uniform inputs; convergence does not establish that those ranges describe real-world uncertainty or that the underlying physical model is valid.

### 4.3 Dynamic model limitations

The repository records that a lumped transient reconstruction and a coarse three-cell spatial model produced inadmissible outlet states for source-scale cases. A ten-cell spatial model was physically admissible for the audited S2/50 trace, but cold-side outlet-temperature errors remain material. The pre-registered S3/60 trace was evaluated without refitting; it is within-source holdout evidence rather than independent validation. Because the raw mass-field semantics remain unresolved, no mass-prediction error should be reported against that field.

### 4.4 Geographic screening status

A reproducible Aqueduct 4.0 sampling workflow has been exercised on six approximate city-centre proxies. These are not actual facility coordinates. Aqueduct's indicators provide basin-level context and prioritization, not direct local measurements. The electricity-water factor join and defensible facility-site data remain incomplete; consequently, no site-specific geographic net-water result is available.

## 5. Uncertainty and sensitivity

The study separates numerical uncertainty, measurement/digitization uncertainty, parameter uncertainty, model-form uncertainty, scenario uncertainty, and system-boundary/counterfactual uncertainty. These classes must not be collapsed into a single interval without justification. Monte Carlo convergence and Sobol convergence are computational diagnostics, not empirical calibration. Final reporting must include the distributions and provenance of every input, seeds, sample sizes, invalid-draw rates, sign convention, counterfactual displacement, code revision, and output checksums. Invalid draws must be investigated rather than silently dropped if their failure is concentrated in meaningful regions of the parameter space.

## 6. Geographic analysis

WRI Aqueduct 4.0 supplies basin-level baseline indicators and future projections under CMIP6-based scenarios. WRI explicitly cautions that composite risk indicators are not directly measurable and should be used as prioritization tools supplemented by local analysis. The final geographic layer must preserve dataset version and retrieval date, spatial mapping method, basin identifier, scenario/year, electricity-water factor source and boundary, and uncertainty. A city-centre proxy must never be described as an actual data-centre site. A country-average electricity-water factor must not be described as facility-specific.

## 7. Current limitations and decision

The current evidence does not establish that waste-heat-assisted MD reduces net freshwater consumption in a real deployment. The primary 1999 observations and exact conditions remain unextracted; independent validation has not passed; transient mass semantics remain unresolved; input uncertainty ranges are illustrative; and geographic electricity-water integration is incomplete. Prior art also substantially narrows the novelty claim.

The paper should proceed to submission only if the source-matched and independent validation, geographic factor join, reproducibility package, and final audit pass. If a source or measurement cannot be recovered, the paper must be narrowed accordingly—potentially to a transparent accounting/methods framework with clearly bounded preliminary model diagnostics. No claim of validated net water benefit is permissible without a substantiated counterfactual, source-backed incremental burdens, validated physical behavior in the operating regime, and uncertainty analysis that supports the sign and magnitude of the net response.

## References (initial; expand after systematic search)

1. Lei, N., Lu, J., Shehabi, A., & Masanet, E. (2025). The water use of data center workloads: A review and assessment of key determinants. *Resources, Conservation and Recycling*, 219, 108310. https://doi.org/10.1016/j.resconrec.2025.108310
2. Martínez-Díez, L., & Vázquez-González, M. I. (1999). Temperature and concentration polarization in membrane distillation of aqueous salt solutions. *Journal of Membrane Science*, 156(2), 265–273. https://doi.org/10.1016/S0376-7388(98)00349-4
3. Keshavarzzadeh, A. H. (2020). Design and bio-inspired optimization of direct contact membrane distillation for desalination based on constructal law. *Scientific Reports*, 10, 16790. https://doi.org/10.1038/s41598-020-73964-7
4. Ali, E., Orfi, J., & Najib, A. (2020). PLOS ONE, 15(3), e0230207. https://doi.org/10.1371/journal.pone.0230207
5. Kanbur, B. B., Wu, C., & Duan, F. (2020). Data-centre cooling coupled with direct contact membrane distillation. *International Journal of Energy Research*. https://doi.org/10.1002/er.5677
6. World Resources Institute. (2023; dataset record updated 2026). Aqueduct 4.0 Current and Future Global Maps Data. https://datasets.wri.org/datasets/aqueduct-global-maps-40-data
7. Malaguti, M., Morciano, M., Viano, G., Achilli, A., Ali, A., Quist-Jensen, C. A., & Tiraferri, A. (2026). Waste heat won't make membrane distillation cool: Thermodynamic analysis of cooling and pumping burdens. *Desalination*, 628, 120039. https://doi.org/10.1016/j.desal.2026.120039
8. Katakam, V. S. S., Arzumanyan, M., Lin, N., & Bahadur, V. (online 2026; issue 2027). System-scale design and analysis of desalination systems for meeting water needs of data centers. *Water Research*, 308, 126748. https://doi.org/10.1016/j.watres.2026.126748
9. Wang, A., Zhang, C., Xu, T., Savic, D., Jiang, J., Xiao, P., He, C., Tao, Y., Daigger, G., & Ren, N. (2026). Global data–water symbiosis reduces AI infrastructure's carbon and water footprint. *Environmental Science and Ecotechnology*, 31, 100702. https://doi.org/10.1016/j.ese.2026.100702

**Citation and completeness warning:** The references above are an initial, not systematic, bibliography. Verify full metadata, access/licence terms, exact methods, and direct prior-art overlap before submission. In particular, complete and verify the bibliographic entries and full-text comparisons for Wyon (2025), Chen et al. (2026), and Yang et al. (2026), which are discussed in the introduction but are not yet fully represented in this reference list. This draft is an internal research artifact, not a claim that the manuscript gate has passed.


### Villa et al. 12-condition benchmark: eligibility and freeze status

The public Villa et al. (2018) dataset is a candidate source-matched benchmark, not a completed validation result. The selected workbook contains raw data and a “Theoretical” worksheet with calculated values; the repository audit has identified an inconsistent CLARCOR label in the 3M workbook, a constant 42.0 Flux (LMH) column, near-zero signed MD Water Flux values, and invalid flow-channel entries. The derived flux summary is a processing cross-check because it is computed from cumulative volume/time, not an independent measurement. Source channels, active area, units, and timing must be reconciled before scoring. A pre-fit holdout and condition-level residual report are required. See `docs/VILLA_12_CONDITION_VALIDATION_FREEZE_PROTOCOL.md`. This within-workbook benchmark cannot replace independent external validation or the unresolved 1999 primary-source reconstruction.
