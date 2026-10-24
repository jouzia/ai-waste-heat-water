# Claim-by-claim prior-art comparison protocol — 2026-10-24

**Status:** Protocol and initial evidence-based decisions. This is not a systematic review, novelty clearance, or model validation.

## 1. Purpose and decision rule

This protocol determines whether the present reduced-order counterfactual net-water model needs a model-form extension to support its research claims. Compare published methods against the implementation in this repository, not just the project title or abstract.

**Decision rule:** do not add model complexity merely to resemble another paper. Extend only when (a) a target claim depends on a physical mechanism the current model omits, (b) the required inputs can be sourced with provenance, and (c) the extension can be tested against independent observations or a clearly labelled analytical benchmark. Otherwise narrow the claim and retain the reduced-order model.

## 2. Current project boundary and implementation baseline

The current scenario runner is a reduced-order screening model. The inspected default envelope uses illustrative values including 100 kW IT load for one hour, source/cold-side temperatures of 70/25 °C, heat-recovery fraction 0.5, heat-exchanger effectiveness 0.8, MD cooling-to-heating ratio 0.5, cooling electricity 0.05 kWh per kWh-th of MD cooling, MD cooling-water intensity 0.1 L/kWh-th, facility cooling-water factors swept across 0, 0.2, and 1.0 L/kWh electricity, and a fixed pumping factor of 0.4 kWh/m³ in the scenario runner. The engine has a pressure-drop-based pumping path only when pressure drop and pump efficiency are supplied explicitly.

These are scenario assumptions, not measurements from the Villa workbook. The current default envelope does not resolve Malaguti et al.'s three MD configurations, configuration-specific SCR/STEC, heat-sink availability/temperature, or joint pressure-drop/recovery behaviour. Net-water results also depend on incremental facility electricity, grid-water factor, and the selected freshwater displacement assumption.

## 3. Claim-by-claim evidence matrix

Evidence labels:
- **Established overlap**: directly supported by the cited publication record/article text.
- **Implementation mismatch**: source-code inspection shows the current implementation does not yet represent the published method.
- **Open**: requires full-text/supplement extraction, provenance, or a reproducible calculation before a claim can be made.

| Proposed claim | Malaguti et al. (2026) | Chen et al. (2026) | Current repository status | Decision |
|---|---|---|---|---|
| Waste heat can drive water production | MD is thermally driven and evaluated with waste heat among heating options | Coupled data-centre waste-heat system produces freshwater and cooling | Broad idea already exists in prior art | Do not claim novelty |
| Data-centre cooling and freshwater can be co-produced | Not the main application framing; MD cooling is modelled as a process burden | Directly described as the purpose of the proposed seawater-evaporation system | Broad coupling concept overlaps directly with Chen | Do not claim novelty |
| MD cooling burden matters | Explicitly models specific cooling requirement (SCR) for three configurations | Different technology/system; full methods not extracted | Current envelope uses a fixed cooling/heating ratio and fixed cooling coefficients | Must acknowledge prior art; no claim to have reproduced SCR physics |
| MD pumping burden matters | Explicitly models pressure drop, pump efficiency, and single-pass recovery | Full-text equation-level relevance not yet assessed | Default envelope uses a fixed 0.4 kWh/m³ pumping factor; optional pressure-drop path is not the default sweep | Treat current pumping as simplified |
| Heat-sink availability and temperature constrain feasibility | Explicit concern in Malaguti; cooling technologies and sink conditions affect actual consumption | Full-text detail not yet extracted | No explicit heat-sink availability/temperature feasibility calculation in default envelope | Do not claim this is already resolved; extend only if sourced inputs exist |
| Convert thermal requirements to actual energy burdens | Malaguti maps theoretical requirements to illustrative technology-dependent consumption | Chen reports system-level power/production results; detailed normalization pending | Current model uses fixed illustrative electricity and water coefficients | Compare boundaries carefully; no direct numeric comparison yet |
| Compute counterfactual net operational blue-water impact | Not established from inspected Malaguti article as the same explicit facility-level displacement ledger | Not established from abstract alone; full-text extraction required | Implemented as avoided water minus modeled incremental burdens, conditional on displacement and factors | Candidate distinction, not proven novelty |
| Separate water withdrawal from water consumption | Malaguti article focuses on energy requirements and cooling configurations; water-accounting definitions need targeted extraction | Full text required | Project aims to label consumption/withdrawal boundaries; gate still open | Keep as a required accounting dimension; verify exact definitions and source factors |
| Couple time-varying workload/heat eligibility to net-water impact | Not established by the inspected article description | Full text required | Project has time-varying workload/coupling work, but empirical source reconstruction and validation gates remain incomplete | Possible scope distinction; requires audit and validation |
| Provide evidence-labelled uncertainty and explicit failure envelopes | Malaguti is a thermodynamic screening framework; exact uncertainty treatment should be checked against full text/supplement | Chen uncertainty and validation protocol not yet extracted | Scenario and sensitivity envelopes exist; their proportions are not real-world probabilities | Describe only as conditional scenario analysis until uncertainty sources are calibrated |
| Empirically validate MD predictions | Malaguti builds on prior work but is not a validation substitute for this repository | Chen's validation evidence has not been extracted or reproduced | Villa primary-source reconstruction, unfitted validation, and model-form comparison remain incomplete | No claim of validation |

## 4. Source-level extraction required before a final novelty statement

### Malaguti et al. (2026)

**Source:** Marco Malaguti et al., “Waste heat won't make membrane distillation cool: Thermodynamic analysis of cooling and pumping burdens,” *Desalination* 628, article 120039 (15 June 2026), DOI [10.1016/j.desal.2026.120039](https://doi.org/10.1016/j.desal.2026.120039). Publisher article: https://www.sciencedirect.com/science/article/pii/S0011916426001955

The publisher article text supports the following:
- Three representative configurations: open-feed/closed-distillate DCMD; DCMD with external heat recovery; AGMD with internal heat recovery.
- Derives STEC, SCR, single-pass recovery, and pumping-energy estimates.
- SCR is cooling duty per unit distillate; pumping depends on pressure drop, pump efficiency, and single-pass recovery.
- Reports cooling loads of 80–100% of heating in some open-loop cases and illustrative pumping penalties of about 0.2–0.5 kWh/m³ for stated hydraulic conditions.
- Explicitly distinguishes theoretical energy requirements from actual consumption after accounting for heating/cooling technology and resource availability.
- Describes its framework as rapid screening/conceptual design; selected technology factors are illustrative rather than prescriptive.

**Comparison to run:** extract equations and boundary conditions from the supplementary information; map each term to this repository's variables; document where the current model uses a coefficient instead of a resolved equation. Do not use the 80–100% range or 0.2–0.5 kWh/m³ as universal constants.

### Chen et al. (2026)

**Source:** Longxiang Chen et al., “A dual-purpose seawater evaporation system for data center cooling and freshwater production: design and performance analysis,” *Applied Thermal Engineering* 287, article 129458 (February 2026), DOI [10.1016/j.applthermaleng.2025.129458](https://doi.org/10.1016/j.applthermaleng.2025.129458). Publisher record: https://www.sciencedirect.com/science/article/abs/pii/S1359431125040505

The publisher abstract reports a seawater-evaporation system that absorbs data-centre waste heat through low-pressure phase change, provides cooling, and condenses salt-free vapour into freshwater. Publisher highlights report two configurations with 41.5% and 40.0% power reductions and freshwater production of 10,004 and 10,744 t/day. These are **paper-reported system results**, not independently reproduced results.

**Open extraction tasks:** inspect full methods and supplement; record system scale, component boundaries, energy inputs, freshwater product definition, parasitic loads, seawater/brine handling, baseline comparison, sensitivity assumptions, and validation evidence. Do not compare its plant-scale outputs directly with this repository's one-hour illustrative outputs; normalize boundaries and scale first.

## 5. Required apples-to-apples comparison ledger

For each paper and the present model, record:

1. Functional unit and time horizon.
2. System boundary, including IT load, facility cooling, MD/evaporation, pumps, heat exchangers, pretreatment, post-treatment, and brine handling.
3. Counterfactual: what system operates without the proposed water-recovery pathway?
4. Heat source temperature, temporal availability, and eligible/recoverable fraction.
5. Cooling configuration, sink temperature/availability, and cooling technology.
6. Freshwater output definition, quality, and whether product is actually substitutable for the displaced supply.
7. Thermal energy requirement versus actual energy consumption; electricity versus heat must remain separately identified.
8. Pumping equation, pressure drop, pump efficiency, recovery ratio, and whether auxiliary circulation is included.
9. Direct water withdrawal and consumptive loss; distinguish returned water from consumed water.
10. Electricity-related water factor, geographic/temporal scope, and consumption-versus-withdrawal definition.
11. Displacement fraction, substitution cap, and source-water type displaced.
12. Measured inputs versus literature values, assumptions, fitted parameters, and simulated outputs.
13. Calibration data, held-out data, leakage controls, uncertainty intervals, and model-form comparison.
14. Geographic data and whether locations are actual facilities or proxies.
15. Open code/data, licenses, and reproducibility artifacts.
16. Residual gap that remains after the comparison, with page/section/equation references.

## 6. Minimum model-extension decision

### Do now (no new physical parameters required)
- Keep the existing engine as a clearly labelled reduced-order counterfactual screening model.
- Add this matrix to the evidence ledger and use the claim wording below.
- Make scenario assumptions, source-backed values, and empirical observations visually and programmatically distinguishable.
- Do not infer empirical validation from passing software tests or sensitivity-run completion.

### Extend only if the claim requires it and inputs can be sourced
1. **Configuration-resolved MD thermal model:** implement one explicitly selected configuration with documented STEC/SCR equations, boundary conditions, and tests against published benchmark values. Do not implement all configurations by default.
2. **Cooling-sink feasibility:** add sink temperature/availability and cooling-technology mapping only with traceable source data and a defined operating constraint.
3. **Hydraulic pumping model:** expose pressure drop, pump efficiency, and recovery as sourced or uncertainty-labelled inputs; compare against the existing fixed pumping coefficient rather than silently replacing it.
4. **Water-accounting boundary:** separately report direct withdrawal, consumptive water, electricity-related water, and displaced supply where evidence permits. Avoid double counting between facility cooling and process cooling.
5. **Validation gate:** require an unfitted comparison and independent source reconstruction before any physical-performance claim is promoted.

**Do not add all five at once.** First finish source extraction and the claim/boundary ledger. Implement only the smallest model-form change that resolves a demonstrated limitation and can be tested.

## 7. Proposed manuscript wording while evidence gates remain open

> We evaluate a source-traceable, counterfactual operational water-accounting approach for waste-heat-assisted water production. The analysis treats cooling, pumping, electricity-related water, and freshwater displacement as explicit burdens or assumptions rather than presuming that recovered heat guarantees a net water benefit. The approach is a reduced-order screening model; its distinctiveness and predictive validity remain subject to full-text prior-art comparison, source reconstruction, and independent validation.

Do not use “first”, “novel global framework”, “validated”, “net-water-positive”, or “water saving” as established findings at this stage.

## 8. Gate status and next actions

This protocol does **not** change any scientific gate. In particular, source reconstruction, unfitted validation, held-out validation, model-form comparison, geographic integration, reproducibility package, manuscript/supplement, and final publication audit remain open until the required artifacts exist and are reviewed.

Next actions, in order:
- [ ] Extract Chen et al.'s methods and supplement into the comparison ledger.
- [ ] Build a term-by-term mapping from Malaguti's equations to current engine variables.
- [ ] Normalize the system boundaries before making numerical comparisons.
- [ ] Decide whether a single configuration-resolved MD extension is justified by the target claim and available inputs.
- [ ] Update the novelty statement only after the comparisons and validation gates are complete.

## References consulted (retrieved 2026-10-24)

- Malaguti et al. (2026), *Desalination* 628, 120039. https://doi.org/10.1016/j.desal.2026.120039
- Chen et al. (2026), *Applied Thermal Engineering* 287, 129458. https://doi.org/10.1016/j.applthermaleng.2025.129458
- Existing project audit: [PRIOR_ART_GAP_AUDIT_2026-10-14.md](PRIOR_ART_GAP_AUDIT_2026-10-14.md)


## 9. Publisher-page methods extraction — Chen et al. (retrieved 2026-10-24)

**Evidence boundary:** the publisher's HTML page exposes the abstract, introduction, system description/methodology headings, assumptions, results overview, conclusion, and bibliographic information. This is a meaningful extension beyond abstract-only review, but it is **not** a complete supplementary-material audit or independent reproduction. The paper's full equations, detailed tables, and supplement still need extraction.

### System and comparison design reported by the publisher

- Proposed configurations: seawater evaporation-driven system for data-centre cooling and freshwater production (SEFDS), and a water-injection heat-exchange variant (SEFDS-WI).
- Core mechanism: low-pressure seawater phase change absorbs data-centre waste heat; the generated salt-free vapour is compressed and then integrated with multi-effect distillation (MED) to recover condensation heat and increase freshwater output.
- Comparison systems named in the publisher page: an indirect evaporative cooling system for data centres (IECS) and a mechanical-vapour-compression / multi-effect-distillation system (MVC-MED).
- Method stated: thermodynamic and thermoeconomic analysis of the two proposed systems and the comparison systems.
- Simplifying assumptions visible on the publisher page: each component is modelled at steady state; components are treated as adiabatic; throttling is isenthalpic. The page begins a statement about pump/compressor operation but the complete assumption list was not available in the extracted passage, so no further assumptions are inferred here.
- Software/property calculation stated: MATLAB for the system model and REFPROP 9.1 for working-fluid thermodynamic properties. The publisher says these are used for validation of the MVC-MED, IECS, SEFDS, and SEFDS-WI systems; the exact validation datasets and error statistics must be extracted from the full paper before assessing validation strength.
- Reported headline results: SEFDS, 10,004.20 t/day freshwater at 6,095.49 kW and 41.5% lower power than its stated standalone comparison; SEFDS-WI, 10,744.12 t/day at 6,349.08 kW and 40.0% lower power. The abstract also reports economic and CO2 outcomes. These remain author-reported simulated/system-analysis results, not independently reproduced estimates and not directly comparable to this repository's illustrative 100 kW, one-hour screening case.

### What this establishes—and what it does not

**Established from the publisher page:** the study is a coupled cooling/freshwater system analysis with thermodynamic and thermoeconomic comparisons; it includes both seawater evaporation and MED heat recovery, compares against named standalone system baselines, and reports large plant-scale simulated production/power outcomes. Thus the broad proposition that data-centre waste heat can be integrated with a cooling/freshwater production system is already prior art.

**Not established from this extraction:** whether its accounting uses the same operational blue-water consumption boundary as this repository; whether it separates withdrawal from consumption; how it treats seawater intake, cooling-water losses, brine handling, grid-water factors, source-water displacement, uncertainty intervals, time-varying workload, or geographic water stress; whether its validation is independent; and whether the full equations can be mapped to the current MD engine. Those questions require full-text tables/equations and any supplementary material. The absence of those details from this extraction must not be interpreted as evidence that the paper omits them.

### Updated comparison decision

Chen's paper uses a materially different named process architecture from the repository's membrane-distillation screening path. This is a **technology distinction**, not proof of a novel research contribution. Do not add Chen's system equations to the present engine unless the research question is deliberately broadened to compare desalination technologies and the inputs/boundaries can be normalized. For the current project, finish the MD-specific equation mapping against Malaguti first, then decide whether a single MD configuration extension is both necessary and testable.

### Source

Chen et al. (2026), “A dual-purpose seawater evaporation system for data center cooling and freshwater production: design and performance analysis,” *Applied Thermal Engineering* 287, article 129458. Publisher HTML: https://www.sciencedirect.com/science/article/pii/S1359431125040505. Retrieved 2026-10-24.
