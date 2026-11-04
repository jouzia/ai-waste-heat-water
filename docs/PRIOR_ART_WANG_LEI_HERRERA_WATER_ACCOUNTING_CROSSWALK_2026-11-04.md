# Wang (2026), Lei (2025), and Herrera (2025): water-accounting prior-art crosswalk — 2026-11-04

This audit compares three accessible full-text or institutional-record sources against the proposed Research 2 contribution. It is not a systematic review and does not establish novelty.

## 1. Wang et al. (2026): global data–water symbiosis

**Citation:** Aijie Wang, Congchao Zhang, Tiefu Xu, Dragan Savic, Jingjing Jiang, Peng Xiao, Chuan He, Yu Tao, Glen Daigger, and Nanqi Ren, “Global data–water symbiosis reduces AI infrastructure's carbon and water footprint,” *Environmental Science & Ecotechnology* 31 (2026), 100702. DOI: [10.1016/j.ese.2026.100702](https://doi.org/10.1016/j.ese.2026.100702). Full text: [PubMed Central PMC13147368](https://pmc.ncbi.nlm.nih.gov/articles/PMC13147368/).

### 1.1 System boundary and method

The study constructs a global geodatabase of more than 4,775 data centres and 57,547 municipal wastewater treatment plants (WWTPs) across 98 countries. It models symbiotic pairings in which treated WWTP effluent replaces freshwater for data-centre cooling and data-centre return heat is recovered to support sludge drying and anaerobic digestion.

It uses a 2023 baseline counterfactual, with data-centre inventory from 2024 and WWTP inventory from 2022. It optimizes candidate pairings within countries under economic feasibility constraints, allowing one-to-many and many-to-one links. A spatial water-stress index is constructed using HydroBASINS level-06 sub-basins, GADM first-level administrative units and Aqueduct 4.0 baseline water stress; WSI >0.4 is treated as a feasibility threshold in the described model.

The article uses an attributional gate-to-gate LCA and life-cycle cost analysis. It also supplies cradle-to-grave results in the SI. The functional unit is 1 kWh of IT load and the assumed infrastructure life is 20 years. The gate-to-gate boundary includes energy recycling, sludge dehydration, anaerobic digestion, treated-water use, displaced freshwater extraction/treatment, advanced wastewater treatment, and manufacture, installation and operation of cooling-water pipelines. Pipeline construction and pumping are included.

The article defines freshwater consumption as the share of freshwater withdrawal not returned to its original natural source (also described as net loss relative to the originating water body). This is a materially relevant accounting convention for Research 2.

### 1.2 Reported results and interpretation

The abstract reports approximately 84 million tonnes CO2-equivalent avoided annually, approximately 1,300 million m3 freshwater conserved and approximately US$95.4 billion annual net cost savings in the modeled global symbiosis. The paper reports that 87.8% of beneficial data–water linkages are within 40 km.

Its table attributes a large freshwater reduction to data-centre cooling energy utilisation and separately accounts for advanced treatment and pipeline construction/operation. The authors explicitly caution that the ecosystem-replenishment implications of the remaining unused effluent depend on local allocation priorities and should not be overstated.

These are global modelled scenario outcomes, not observed universal savings. The global results depend on inventory coverage, pairing feasibility, cooling assumptions, local factors and counterfactual definitions. The article itself notes that a consequential LCA with explicit market modelling would better capture dynamic interactions and long-term systemic effects.

### 1.3 Prior-art overlap with Research 2

Wang et al. establish prior art for:
- counterfactual comparison of data-centre water/energy infrastructure configurations;
- explicit direct freshwater-consumption accounting;
- combining reclaimed-water substitution with data-centre heat recovery;
- inclusion of additional treatment, pipeline, pumping and infrastructure burdens;
- geographic water-stress constraints;
- a common IT-energy functional unit;
- integrated water and energy system assessment at facility and global scales.

This means Research 2 cannot claim that counterfactual net freshwater accounting, geographic water-stress weighting, or the general coupling of data-centre heat recovery with an alternative cooling-water source is novel by itself.

### 1.4 Important difference

Wang et al. study reclaimed wastewater as a cooling-water source and return data-centre heat as a resource for WWTP sludge drying and anaerobic digestion. They do not, in the accessible paper, model membrane distillation desalination driven by data-centre waste heat or a desalination product-water displacement pathway. Their system is a data–water infrastructure symbiosis and gate-to-gate LCA, not the Research 2 MD process model.

This is a process-boundary difference, not automatic novelty. Research 2's remaining potential distinction would need to be demonstrated at the level of MD-specific validated thermodynamics and temperature/time-resolved heat eligibility, not by claiming net water accounting or counterfactuals as new.

## 2. Lei et al. (2025): workload-level water determinants

**Citation:** Nuoa Lei, Jun Lu, Arman Shehabi, and Eric R. Masanet, “The water use of data center workloads: A review and assessment of key determinants,” *Resources, Conservation and Recycling* 219 (2025), 108310. DOI: [10.1016/j.resconrec.2025.108310](https://doi.org/10.1016/j.resconrec.2025.108310). Institutional abstract: [Lawrence Berkeley National Laboratory](https://seta.lbl.gov/publications/water-use-data-center-workloads).

The institutional abstract evaluates water use at workload level in litres consumed per workload. It reports variations exceeding 10,000-fold, driven by more than 1,000-fold differences in water consumption per kWh of server electricity and approximately 10-fold differences in server workload efficiency. It ranks server efficiency, electricity-grid water-consumption factors, server utilization, cooling-system type, infrastructure efficiency, climate zone, inactive-server percentage and server refresh cycle among key determinants.

**Research 2 implication:** workload-level water accounting and the importance of electricity-grid water factors, utilization, cooling technology and climate are prior art. Research 2 should not claim to introduce workload-level water footprinting or to identify grid-water factors as a new determinant. Its implementation should use workload energy as the denominator consistently and document whether factors represent withdrawal or consumption, their geography, year, technology and source.

**Evidence limit:** the institutional record exposes the abstract and bibliographic metadata, not the full equation set, datasets or supplementary methods. No further methodological detail is inferred here.

## 3. Herrera et al. (2025): scenario-based AI infrastructure water footprint

**Citation:** Manuel Herrera, Xiang Xie, Alessandro Menapace, Andrea Zanfei, and Bruno M. Brentan, “Sustainable AI infrastructure: A scenario-based forecast of water footprint under uncertainty,” *Journal of Cleaner Production* 526 (2025), 146528. DOI: [10.1016/j.jclepro.2025.146528](https://doi.org/10.1016/j.jclepro.2025.146528). Institutional record: [Newcastle University ePrints](https://eprints.ncl.ac.uk/307765). Data/code statement: [waterforAI GitHub repository](https://github.com/manuelhf/waterforAI).

The institutional abstract describes a global assessment that separates:
- operational water consumption at the facility;
- off-site water consumption associated with electricity generation;
- embodied water consumption from hardware manufacturing and supply chains.

It uses a scenario-based probabilistic forecasting framework inspired by Bayesian methods, combining sparse empirical data, expert-informed assumptions and policy-relevant growth trajectories for 2030 and 2050. It reports that, without mitigation, global data-centre water consumption could increase more than seven-fold by mid-century, with cooling-related operational consumption accounting for most demand. Sensitivity analysis identifies compute growth and efficiency trends as important drivers.

The institutional record states that the data and code supporting the findings are openly available in the cited repository.

**Research 2 implication:** separating operational, electricity-related and embodied water; scenario-based uncertainty; and mitigation comparisons are established prior art. Research 2 should not claim these broad accounting or uncertainty concepts as new. A narrower MD-specific operational ledger may still be useful, but only if it demonstrates a clearly defined additional question and is independently reproducible.

**Evidence limit:** this audit uses the institutional abstract and metadata, not a complete paper/SI extraction. It does not independently inspect or reproduce the open repository. No exact probabilistic model, prior, likelihood or parameter distribution is inferred.

## 4. Combined comparison against Research 2

| Candidate Research 2 element | Prior-art status after this audit | What remains to be demonstrated |
|---|---|---|
| Data-centre waste-heat recovery | Established by Kanbur, Wyon, Chen, Yang and Wang in different system architectures | A distinct and validated MD-specific use case |
| Data-centre cooling + desalination/freshwater | Established by Kanbur, Wyon, Chen, Yang and Katakam | No broad first-of-kind claim |
| Counterfactual water accounting | Explicit in Wang; workload-level framing in Lei; scenario counterfactuals in Herrera | A precise MD-specific ledger with defensible system boundary |
| Direct and electricity-related water | Explicit in Wang, Lei, Herrera and Katakam | Correctly sourced, geography/time-specific factor metadata and no category double-counting |
| Geographic water stress | Explicit in Wang (WSI), Katakam (SWUI), Herrera's regional availability framing | Validated basin-resolved factor integration, not a new concept claim |
| Workload-level water footprint | Explicit in Lei | A new MD intervention question with workload-linked, time-resolved thermal eligibility |
| Uncertainty/scenario analysis | Explicit in Herrera and other system studies | Reproducible parameter uncertainty and independent validation, not only deterministic sweeps |
| MD physics | Explicit in Kanbur and Wyon; different technology in Chen/Yang/Katakam/Wang | Independent source reconstruction and configuration-specific validation |
| Net operational blue-water effect of waste-heat MD | Not established as equivalent by these three papers alone | Exact prior-art comparison across all direct MD papers; explicit withdrawal/consumption/return/displacement; validation |

## 5. Updated novelty position

The combined literature now rules out the following broad claims:
- first data-centre waste-heat desalination/cooling system;
- first data-centre MD concept;
- first workload-level water-use assessment;
- first counterfactual water-accounting framework for data centres;
- first separation of operational and electricity-related water;
- first geographically weighted data-centre water-stress metric;
- first scenario-based assessment of AI/data-centre water footprints;
- first integrated data-centre/water-infrastructure heat and water symbiosis.

The only remaining candidate contribution should be framed as a **narrow, falsifiable MD-specific assessment question**:

> For a specified MD configuration, under what source-traceable, time-varying data-centre heat conditions does incremental freshwater production yield a net operational blue-water benefit after accounting for cooling-system changes, pumping and auxiliary electricity, electricity-related water, feed/concentrate handling, and demonstrable displacement of a defined freshwater counterfactual?

This is a candidate research question, not a novelty clearance. It must be compared against the full methods and evidence of Kanbur, Wyon, and the relevant MD studies, and against any MD-specific counterfactual water accounting in the wider literature.

## 6. Required Research 2 model changes before making a substantive claim

Do not change physical parameters simply to fit a desired sign. First define the inventory schema and evidence requirements:

1. Water flow type: withdrawal, consumption, returned flow, evaporation, product water, concentrate/brine, and water quality.
2. Source identity: surface water, groundwater, seawater, reclaimed effluent, or other source.
3. Geography: basin or sub-basin and spatial allocation rule.
4. Time: source year, operating interval, season and temporal resolution.
5. Factor metadata: factor value, units, source, technology, geography, year, uncertainty, and withdrawal-versus-consumption definition.
6. Electricity boundary: grid mix, onsite generation, cooling electricity, MD pumping, pretreatment, post-treatment and auxiliary equipment.
7. Counterfactual displacement: end use, product quality, displaced source, fraction/volume, and evidence that product water substitutes for freshwater consumption.
8. Heat eligibility: time-matched workload power, heat-rejection temperature, recoverable heat, exchanger approach temperature, MD operating envelope and downtime.
9. Uncertainty: evidence-based distributions or intervals, separated from scenario sweeps and expert assumptions.
10. Functional unit: preferably 1 kWh IT energy for workload comparisons, with additional per-m³ product-water reporting and explicit conversion.

The code should not use one unlabelled `L/kWh` scalar for factors that represent different water sources or consumption definitions. A typed factor schema is a candidate design requirement, but implement only after an audit of existing interfaces, manifests and backward-compatibility tests.

## 7. Next actions and decision

- [x] Audit Wang et al. full open-access article for system boundary, counterfactual, functional unit, freshwater definition, water-stress treatment and LCA boundary.
- [x] Audit Lei et al. institutional abstract for workload-level determinants and grid-water factors.
- [x] Audit Herrera et al. institutional abstract for operational/off-site/embodied water separation and scenario uncertainty.
- [ ] Retrieve and inspect Herrera full paper/SI and repository data/code before making detailed methodological comparisons.
- [ ] Inspect Wang supplementary notes and data tables before attempting numerical reproduction.
- [ ] Complete source-by-source Kanbur and Wyon equation/validation crosswalk.
- [ ] Compare the exact water-factor semantics and functional units across Wang, Lei, Herrera and Katakam.
- [ ] Only then decide whether to add a typed water-factor schema and revise the engine.
- [ ] Keep Issue #16, source reconstruction, independent validation and novelty gates open.

**Decision:** these sources substantially narrow the candidate contribution. Counterfactual freshwater accounting, direct/indirect water burdens, geographic water-stress weighting, workload-level water determinants, and scenario uncertainty are not novel concepts. Research 2's possible distinction is the combination of independently validated MD process physics with source-traceable, time-varying heat eligibility and an explicitly bounded operational blue-water counterfactual. That combination is not yet established as novel or validated.
