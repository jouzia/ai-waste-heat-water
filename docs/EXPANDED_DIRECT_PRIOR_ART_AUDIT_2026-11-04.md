# Expanded direct-prior-art audit: data-centre waste heat and desalination

**Audit date:** 2026-11-04  
**Purpose:** Screen primary sources named in Katakam et al. (2026) and identify additional direct competitors to the repository's proposed contribution.  
**Evidence boundary:** Bibliographic records, abstracts, and publisher/institutional indexed text were inspected. Evidence levels are stated per paper. Except where explicitly noted, this is not a full-text equation audit or independent reproduction.

## Executive finding

The initial distinction that Katakam et al. excludes physical thermal/operational coupling is correct for that paper's stated scope, but it does **not** establish that this integration is an open research gap generally. Two particularly important direct competitors emerged:

1. **Yang, Konstantinou & Hou (2026), Applied Energy 408, 127428, DOI 10.1016/j.apenergy.2026.127428** explicitly couples data-centre waste heat to temperature-dependent seawater RO through a high-fidelity thermo-electric model and jointly optimizes planning and operation using a two-stage stochastic framework. Publisher text also describes a case study based on co-located facilities in Jubail Industrial City. This is direct prior art for waste-heat-assisted desalination and integrated planning/operation. The abstract reports 86.5% reduction in total annualized cost, with waste-heat synergy contributing 17%; these are authors' case-study model results, not independent validation.
2. **Chen et al. (2026), Applied Thermal Engineering 287, article 129458, DOI 10.1016/j.applthermaleng.2025.129458** proposes a dual-purpose seawater evaporation system for data-centre cooling and freshwater production. The abstract describes low-pressure phase-change absorption of data-centre waste heat, salt-free vapour condensation, and cogeneration of cooling and freshwater. Publisher highlights report power reductions and freshwater production for two system configurations. This is direct prior art for combined cooling and freshwater production from data-centre waste heat, though the detailed model boundary and comparison with membrane distillation remain to be audited.

Consequently, the broad proposition “integrate data-centre waste heat with desalination to produce freshwater” is not a defensible novelty claim. Any remaining contribution must be narrower, explicitly compared with these systems, and supported by full-text methods and results. Issue #16 remains open.

## Primary-source screening

### 1. Kanbur, Wu & Duan (2020) — direct contact membrane distillation

**Citation:** B. B. Kanbur, C. Wu, F. Duan, “Multi-criteria thermoeconomic and thermodynamic assessments of the desalination-integrated two-phase liquid-immersion data center cooling system,” *International Journal of Energy Research* 44 (2020), 10453–10470. DOI: [10.1002/er.5677](https://doi.org/10.1002/er.5677).

**Evidence inspected:** Wiley full-text landing page and abstract/summary. The study proposes a two-phase immersion-cooled data centre whose waste heat heats the feed side of a direct-contact membrane distillation (DCMD) module. Reported cooling load is 0.7–1.5 kW; membrane area 5–75 cm²; maximum thermal and exergy efficiencies 64.5% and 53.7%; maximum daily distilled water 6.13 kg. The hybrid system is reported to have higher capital and operating costs than standalone data-centre cooling, with a 3.72-year payback and a reported levelized product cost in SGD/h.

**Threat:** Direct prior art for data-centre waste heat driving DCMD and thermoeconomic optimization. The repository must not claim this integration concept, DCMD coupling, or thermoeconomic evaluation as new.

**Still unknown:** Full model equations, exact water accounting boundary, source-water withdrawal/consumption, brine treatment/disposal, counterfactual freshwater displacement, time resolution, and source-matched validation were not established in this screen.

### 2. Sondur, Gross & Li (2018) — low-temperature desalination and energy-aware control

**Citation:** S. Sondur, K. C. Gross, M. Li, “Data Center Cooling System Integrated with Low-Temperature Desalination and Intelligent Energy-Aware Control,” *Proceedings of the International Green and Sustainable Computing Conference* (IGSC 2018).

**Evidence inspected:** Author/lab publication page and public PDF landing; abstract text. The paper describes a work-in-progress experimental setup using heat removed by fluid-cooled rack heat exchangers in data centres and a controlled low-pressure desalination technique to produce drinking/irrigation water while improving PUE. The abstract states the purpose is to demonstrate heat reuse, not that a fully validated commercial system was achieved.

**Threat:** Earlier conceptual/experimental work on data-centre heat reuse for low-temperature desalination and energy-aware control.

**Still unknown:** Experimental results, achieved water quality/rate, exact process architecture, energy and water boundary, and whether the proposed setup was completed. Do not describe the abstract's intended demonstration as validated performance.

### 3. Wyon (2025) — direct-to-chip data centre and DCMD case study

**Citation:** A. Wyon, “Desalination utilizing data centre waste heat,” Lund University, Master's thesis, 2025, record 9198095.

**Evidence inspected:** Official Lund University student-paper record and abstract; earlier repository audit documents the detailed thesis content reviewed from an accessible copy, with the caveat that the previously inspected copy was not authenticated as the official institutional PDF. The thesis models a hypothetical 1.5 MW Barcelona direct-to-chip data centre, DCMD, a commercial heat exchanger and two pumps, with three product-water use cases (data-centre cooling, electrolyser, or sale to local grid). It reports technical feasibility but economic challenges driven by pump capital and operating costs and low production at low waste-heat temperatures.

**Threat:** Direct prior art for DC waste-heat-driven DCMD, a concrete facility-scale case study, and alternative freshwater use cases.

**Still unknown:** Official full-text source reconciliation, exact model reproduction, and whether a net withdrawal/consumption counterfactual or stress-weighted water ledger was performed.

### 4. Yang, Konstantinou & Hou (2026) — thermo-electric RO and joint planning/operation

**Citation:** R. Yang, C. Konstantinou, Y. Hou, “Enabling grid-interactive data center-desalination coordination through thermo-electric coupling-based waste heat utilization,” *Applied Energy* 408 (2026), article 127428. DOI: [10.1016/j.apenergy.2026.127428](https://doi.org/10.1016/j.apenergy.2026.127428).

**Evidence inspected:** HKU Scholars Hub record, ScienceDirect publisher abstract/highlights, and indexed publisher text including case-study and conclusion snippets. The article presents a thermo-electric model linking data-centre waste heat and seawater preheating to temperature- and salinity-dependent RO specific energy consumption. It embeds this physics in a two-stage stochastic planning/operation model using Benders decomposition and McCormick linearization. Publisher text describes a Jubail Industrial City case study with a data centre and desalination plant less than 1 km apart. The abstract reports an 86.5% reduction in total annualized cost, with waste-heat synergy contributing 17%.

**Threat:** This is direct prior art for physical thermal coupling, temperature-dependent RO performance, and joint planning/operational optimization. It is a particularly strong competitor to any proposed Research 2 contribution framed as co-optimizing data-centre waste heat and desalination operation.

**Potential distinction to investigate, not claim:** The visible source concerns seawater preheating and RO, whereas this repository includes membrane distillation and an explicit net-water accounting motivation. Whether Yang includes comprehensive withdrawal-versus-consumption accounting, stress-weighted impacts, brine impacts, and counterfactual freshwater displacement is not established by the abstract/indexed text. Those must be checked in full text.

### 5. Chen et al. (2026) — dual-purpose seawater evaporation, cooling and freshwater

**Citation:** L. Chen, H. Xie, M. Xie, L. Zhang, K. Ye, S. Li, “A dual-purpose seawater evaporation system for data center cooling and freshwater production: design and performance analysis,” *Applied Thermal Engineering* 287 (2026), article 129458. DOI: [10.1016/j.applthermaleng.2025.129458](https://doi.org/10.1016/j.applthermaleng.2025.129458).

**Evidence inspected:** ScienceDirect abstract and highlights. The abstract proposes seawater evaporation-based technology that simultaneously provides data-centre cooling and cogenerates freshwater. It uses low-pressure phase change driven by data-centre waste heat and condenses salt-free vapour. Publisher highlights report power decreases of 41.5% and 40.0% for two systems and freshwater production of 10,004 t/day and 10,744 t/day, respectively. These are reported system-model outputs, not independently verified measurements.

**Threat:** Direct prior art for combined cooling and freshwater production using data-centre waste heat and seawater phase change. It may be closer to a dual-purpose cooling/desalination architecture than to conventional standalone desalination.

**Still unknown:** Detailed process flow, whether evaporation is membrane-separated or open-surface/other architecture, mass/energy balance, source-water withdrawal and consumption, salt/brine fate, auxiliary electricity, and validation. These details are required before a fair technical comparison.

### 6. Katakam et al. (2026 online / 2027 issue) — system-scale RO/MVC desalination and SWUI

**Citation:** V. S. S. Katakam, M. Arzumanyan, N. Lin, V. Bahadur, “System-scale design and analysis of desalination systems for meeting water needs of data centers,” *Water Research* 308 (2027), article 126748. DOI: [10.1016/j.watres.2026.126748](https://doi.org/10.1016/j.watres.2026.126748).

**Evidence inspected:** PubMed abstract and ScienceDirect extended indexed text, including introduction, scope statement and visible section snippets. It evaluates two-stage RO, MVC and hybrids for brackish, seawater and produced-water feeds, with conventional/MLD/ZLD concentrate management, data-centre freshwater quality target <500 ppm TDS, techno-economic optimization, and the SWUI water-stress metric. The article explicitly says physical thermal or operational integration between desalination and the data centre is outside its scope.

**Threat:** Direct prior art for data-centre desalination system design, broad salinity/concentrate pathway comparison, and a desalination-to-regional-water-stress metric.

**Still unknown:** Exact SWUI equation, stress factors, withdrawal/consumption definitions, time horizon, allocation and counterfactual displacement. The complete PDF and SI remain unaudited.

## Cross-paper comparison: what is and is not established

| Paper | Waste-heat coupling | Desalination/process | Operational optimization | Data-centre cooling co-production | Water-stress / net-water accounting |
|---|---|---|---|---|---|
| Sondur 2018 | Yes, low-temperature waste heat | Low-pressure desalination; exact process details need full paper | Energy-aware control discussed | Cooling system + water production concept | Not established from abstract |
| Kanbur 2020 | Yes, immersion heat | DCMD | Multiobjective thermoeconomic optimization | DC cooling + DCMD | Not established from abstract |
| Wyon 2025 | Yes, direct-to-chip heat | DCMD | Scenario/model analysis | Water use cases include cooling | Not established as a complete net ledger |
| Yang 2026 | Yes, heat to seawater preheat | Temperature-dependent RO | Two-stage stochastic planning/operation | Data-centre and desalination coordination | Full boundary not yet checked |
| Chen 2026 | Yes, low-pressure phase change | Seawater evaporation | Design/performance analysis | Explicit dual-purpose cooling + freshwater | Full boundary not yet checked |
| Katakam 2026/27 | Physical coupling explicitly out of scope | RO/MVC/hybrids; MLD/ZLD | System-scale techno-economic optimization | Data-centre freshwater supply, not thermal co-production | SWUI introduced; exact equation/boundary still to audit |

## Consequences for Research 2 positioning

The following broad claims are ruled out or unsafe:
- “First use of data-centre waste heat for desalination.”
- “First coupling of data-centre cooling and freshwater production.”
- “First waste-heat-driven DCMD for data centres.”
- “First thermo-economic or operational optimization of data-centre desalination.”
- “First desalination/water-stress metric for data-centre water supply.”

A potentially defensible contribution, subject to full-text confirmation, may involve a **source-resolved net-water ledger** that distinguishes withdrawals from consumption and evaluates whether additional saline-water extraction, concentrate handling, process electricity, cooling water, and marginal freshwater displacement yield a positive net freshwater outcome. However, it must be checked against Yang, Chen, Katakam, and the remaining prior art. A new accounting label alone is not sufficient; the ledger must be operationally defined, avoid double counting, and use traceable region- and technology-specific factors.

The existing repository already has preliminary net-water accounting components and AGMD model work. The next engineering step should be a formal crosswalk from each competitor's equations/system boundary to implemented code, with every term tagged as implemented, caller-supplied, omitted, or not source-verifiable. Do not represent the present code as validated against any of these systems.

## Required next steps

1. Obtain and read the full Yang (2026) paper and SI. Extract heat source/sink temperatures, heat exchanger/thermal coupling, RO temperature/salinity functions, stochastic variables, time resolution, objective terms, and all water accounting.
2. Obtain and read the full Chen (2026) paper and SI. Identify the evaporation architecture, cooling duty, freshwater quality/recovery, energy boundary, brine fate, and experimental versus modeled validation.
3. Obtain Kanbur (2020) full article and SI through institutional access/interlibrary loan or user-provided copy. No paid purchase or author contact has been made.
4. Obtain official Wyon thesis PDF and reconcile it against the previously inspected copy.
5. Retrieve Sondur (2018) PDF and determine whether it reports experimental results or only a proposed setup.
6. Obtain Katakam full text/SI and extract exact SWUI formula and water-stress boundary.
7. Update the implementation crosswalk and revise the research question if these comparisons show that the proposed distinction is already addressed.
8. Keep Issue #16 open until these tasks and database-specific search/screening are complete.

## Source links and access log

- Kanbur et al. 2020, Wiley full text: https://onlinelibrary.wiley.com/doi/full/10.1002/er.5677 — abstract/summary inspected; complete paper/SI not fully audited.
- Sondur et al. 2018, author/lab record: https://www.li-realab.info/publication/oracle/li2018desal/ — abstract and PDF landing inspected; full results not audited.
- Wyon 2025, official Lund record: https://lup.lub.lu.se/student-papers/record/9198095 — official abstract/metadata inspected; official PDF reconciliation pending.
- Yang et al. 2026, HKU record: https://hub.hku.hk/handle/10722/379334 — abstract/metadata inspected.
- Yang et al. 2026, ScienceDirect: https://www.sciencedirect.com/science/article/pii/S0306261926000802 — abstract, highlights and indexed case-study/conclusion text inspected; full methods/SI audit pending.
- Chen et al. 2026, ScienceDirect: https://www.sciencedirect.com/science/article/abs/pii/S1359431125040505 — abstract/highlights inspected; full methods/SI audit pending.
- Katakam et al. 2026/27, ScienceDirect: https://www.sciencedirect.com/science/article/abs/pii/S0043135426014223 — abstract, highlights, extended introduction and scope statement inspected; full methods/SI audit pending.

No numerical reproduction or independent validation of any competitor model was performed in this audit.
