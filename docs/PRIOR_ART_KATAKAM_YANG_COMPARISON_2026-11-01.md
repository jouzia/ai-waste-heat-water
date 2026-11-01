# Targeted prior-art comparison: Katakam et al. (2026/2027) and Yang et al. (2026)

**Review date:** 2026-11-01  
**Review status:** targeted source audit; **not** a systematic review, complete full-text extraction, or novelty clearance.

## Purpose

This note records two direct prior-art constraints on the proposed data-centre / desalination / water-impact contribution. It distinguishes what is supported by accessible article text from what remains unverified. The comparison is intended to prevent broad or misleading novelty claims; it does not establish that the present repository's candidate contribution is novel.

## 1. Katakam et al. — system-scale desalination for data-centre water demand

**Citation:** Katakam, V. S. S., Arzumanyan, M., Lin, N., & Bahadur, V. (online 17 August 2026; *Water Research* 308, Part B, article 126748, 2027 issue). “System-scale design and analysis of desalination systems for meeting water needs of data centers.” DOI: https://doi.org/10.1016/j.watres.2026.126748.  
**Publisher record:** https://www.sciencedirect.com/science/article/pii/S0043135426014223  
**Bibliographic record:** https://pubmed.ncbi.nlm.nih.gov/42731480/

### Source-supported scope and methods

The PubMed record reports technical and techno-economic analysis of desalination for data-centre freshwater production (product TDS <500 ppm). It evaluates two-stage reverse osmosis (RO), mechanical vapour compression (MVC), and hybrid configurations for brackish water (5,000 ppm), seawater (35,000 ppm), and produced water at or above 50,000 ppm. Brine-management options include conventional disposal, minimum liquid discharge (MLD), and zero liquid discharge (ZLD). Reported metrics include freshwater recovery, input energy, and water cost. The paper introduces Saline Water Utilization Intensity (SWUI) to quantify desalination-related impact on local water stress.

The accessible publisher-indexed article text states that the paper's system-level integration is the coupling of the desalination treatment train to data-centre freshwater-quality needs and the translation of desalination performance into regional water-stress impact through SWUI. It explicitly says that further thermal or operational integration between the desalination system and the data centre is outside its scope. The indexed text also identifies prior data-centre desalination work, including waste-heat-driven thermally driven processes and thermoelectrically coupled RO.

### Comparison with this repository

| Dimension | Katakam et al. (source-supported) | Current Research 2 status | Implication |
|---|---|---|---|
| Primary desalination technology | Two-stage RO, MVC, RO/MVC hybrids | MD/AGMD/DCMD pathway | Technology-specific distinction exists, but is not sufficient by itself to establish novelty |
| Feedwater | Brackish, seawater, produced water through hypersaline ranges | Current MD source-validation work uses defined saline-feed experimental sources; data-centre scenario feedwater remains separately specified | Compare feed chemistry and concentration range; do not imply common operating domain |
| Brine management | Conventional disposal, MLD, ZLD | Current project does not yet have a comparably validated, integrated brine-treatment train | Do not claim comprehensive brine-management coverage |
| Data-centre coupling | Desalination treatment train designed for data-centre water-quality demand; article says further thermal/operational coupling is outside scope | Candidate framework explicitly couples time-varying waste-heat eligibility to MD and operational water accounting, but several inputs remain illustrative | A possible boundary distinction, not proof of novelty or successful implementation |
| Water-stress metric | SWUI links saline-water utilization / desalination performance to local water-stress implications | Aqueduct basin-risk context and electricity-water join remain incomplete; stress is not a physical water-volume multiplier | Do not claim first data-centre desalination water-stress metric; any different metric must be clearly defined and compared |
| Energy/economic outputs | Freshwater recovery, energy input, water cost, second-law efficiency per article text | Current central claim is conditional net operational blue-water consumption; full system costs are not a validated output | Keep estimands distinct; compare only after boundary normalization |
| Validation and data | Article reports a detailed system-level modeling and techno-economic framework; full validation protocol and accessible datasets not yet extracted here | Independent primary MD validation remains incomplete | Do not imply superiority or stronger validation without extracting both protocols |
| Code/data | Not established in this audit | Research 2 repository is public | Verify source availability/licensing before any reproducibility comparison |

### Limits of this extraction

The PubMed abstract and publisher-indexed article text were accessible. A direct open of the ScienceDirect article returned HTTP 403 in this review session. The indexed page exposed the introduction, broad methods/results/conclusion snippets, but this note does **not** claim a complete line-by-line review of all equations, tables, supplementary information, uncertainty treatment, or validation details. Those remain required before closing the full-text comparison criterion in issue #16.

## 2. Yang, Konstantinou & Hou — thermo-electric data-centre / RO coordination

**Citation:** Yang, R., Konstantinou, C., & Hou, Y. (2026). “Enabling grid-interactive data center-desalination coordination through thermo-electric coupling-based waste heat utilization.” *Applied Energy* 408, article 127428. DOI: https://doi.org/10.1016/j.apenergy.2026.127428.  
**Publisher record:** https://www.sciencedirect.com/science/article/pii/S0306261926000802  
**Institutional record:** https://hub.hku.hk/handle/10722/379334

### Source-supported scope and methods

The publisher and institutional records describe a flexible data-centre / seawater-desalination system using data-centre waste heat for seawater preheating in temperature- and salinity-dependent reverse osmosis. The study presents a thermo-electric model and a two-stage stochastic planning/operation optimization, solved using Benders decomposition and McCormick-envelope linearization. The publisher highlights report a case-study reduction in total annualized cost of 86.5%, with waste-heat synergy contributing 17% savings. Those are publisher-reported case-study results, not values reproduced by this repository.

### Comparison with this repository

| Dimension | Yang et al. (source-supported) | Current Research 2 status | Implication |
|---|---|---|---|
| Heat source/use | Data-centre waste heat used to preheat seawater | Waste heat is proposed as the MD thermal source | Waste-heat/desalination integration is established prior art |
| Desalination | Temperature-/salinity-dependent RO | MD/AGMD/DCMD | Different process physics; compare heat integration and water boundary rather than claiming integration novelty |
| Optimization | Two-stage stochastic joint planning and operation | Scenario and uncertainty analysis exist, but evidence-calibrated operational distributions and geography remain incomplete | Do not claim first thermo-electric co-optimization or stochastic planning |
| Grid interaction | Explicitly grid-interactive framing | Current framework includes electricity-related water burden but not an equivalent grid-dispatch model | Scope distinction must be explicit |
| Water impact | Publisher records emphasize energy-water coordination and desalination | Candidate net operational blue-water estimand includes withdrawal/consumption and displacement counterfactual | Need normalize boundaries and compare whether either study counts physical water consumption, withdrawal, and avoided water |
| Validation/data | Full methods, case-study inputs, and validation details not extracted in this note | Independent MD validation incomplete | Full-text extraction remains necessary before detailed comparison |

The publisher record's abstract/highlights do not provide enough detail to establish the exact RO membrane equations, heat-exchanger effectiveness, thermal losses, water withdrawal/consumption definitions, or independent validation design. Do not infer those details.

## 3. Claim-level implications

The two studies establish that the following are **not** defensible standalone novelty claims:

- connecting data-centre waste heat to desalination;
- using waste heat to improve RO performance or coordinate data-centre and desalination operation;
- evaluating desalination trains for data-centre freshwater demand;
- linking data-centre desalination to regional water-stress indicators;
- performing thermo-electric or techno-economic optimization of data-centre/desalination systems.

A narrower candidate question remains: whether an evidence-traceable, time-resolved MD model, after source-matched validation, can be integrated with a counterfactual physical operational blue-water ledger that separates direct withdrawal from consumption, incremental cooling and pumping, electricity-generation water, and substantiated freshwater displacement, while reporting failure regimes and uncertainty. This is a candidate distinction only. It is not a cleared novelty claim, and the present model has not passed its independent validation and geographic-data gates.

## 4. Search and access record

- Date: 2026-11-01.
- Sources: PubMed bibliographic/abstract record; ScienceDirect indexed article record and accessible text snippets; HKU Scholars Hub institutional record; ScienceDirect publisher record for Yang et al.
- Search targets: exact article titles and DOIs; publisher and institutional full-text records.
- Direct publisher page for Katakam et al. returned HTTP 403 on open; indexed publisher text was available through search results.
- Full supplements, detailed equations, complete uncertainty/validation sections, and reproducibility assets were not verified for either study in this pass.
- No PRISMA screening or comprehensive citation-chain search has been performed.

## 5. Required follow-up before issue #16 can close

1. Obtain lawful full text and supplements for both papers, or document author/institutional access attempts and the resulting limitation.
2. Extract equations, system-boundary figures, tables, validation protocols, uncertainty treatment, and all water definitions with page/section locators.
3. Compare each item against the exact current implementation and experiment manifests, not the intended future architecture.
4. Complete the same extraction for Kanbur et al. (2020), Wyon (2025), Chen et al. (2026), and the other direct threats listed in `docs/PRIOR_ART_GAP_AUDIT_2026-10-14.md`.
5. Archive reproducible database queries, date ranges, inclusion/exclusion rules, citation chasing, and a claim-to-evidence matrix.
6. Keep the novelty and publication gates false until the comparison and empirical validation acceptance criteria are met.

**Decision:** this update strengthens the prior-art boundary but does not close issue #16. Publication/reproduction status is unchanged.
