# Katakam et al. (2026) system-scale data-center desalination: extended publisher-text audit

**Audit date:** 2026-11-04  
**Paper:** Vishnu Sree Shanthanu Katakam, Mariam Arzumanyan, Ning Lin, Vaibhav Bahadur, “System-scale design and analysis of desalination systems for meeting water needs of data centers,” *Water Research* 308 Pt B (2027 issue), 126748. Online ahead of print 17 August 2026. DOI: [10.1016/j.watres.2026.126748](https://doi.org/10.1016/j.watres.2026.126748). PMID: 42731480.  
**Primary records checked:** [PubMed record](https://pubmed.ncbi.nlm.nih.gov/42731480/) and [Elsevier ScienceDirect article record](https://www.sciencedirect.com/science/article/abs/pii/S0043135426014223).

## Access and evidence grade

This is an **extended publisher-indexed-text audit, not a full-text or supplementary-information audit**. The ScienceDirect page was accessible through indexed text, including the abstract, substantial portions of the introduction, selected section snippets and conclusions. A direct page retrieval returned HTTP 403. PubMed supplies the bibliographic record and abstract only. The full methods, complete equations, all tables/figures, references, and supplementary information were not obtained in this audit. No equations or model outputs have been independently reproduced.

The source must therefore remain marked **partial-text / model-study evidence**. Do not describe it as fully read, fully reproduced, or experimentally validated.

## What the accessible source establishes

### System and technology scope

- The study evaluates two-stage reverse osmosis (RO), mechanical vapour compression (MVC), and hybrid RO/MVC configurations.
- Feed cases include brackish water at 5,000 ppm TDS, seawater at 35,000 ppm TDS, and produced water at 50,000 ppm and 90,000 ppm TDS in the accessible conclusions; the abstract describes produced water as at least 50,000 ppm.
- Concentrate-management cases include conventional disposal, minimum liquid discharge (MLD), and zero liquid discharge (ZLD). The accessible text gives representative concentrate ranges of about 70,000 ppm for conventional disposal, 130,000–200,000 ppm for MLD, and about 260,000 ppm NaCl near ZLD.
- The stated product-water target is below 500 ppm TDS.
- The article describes a system-scale desalination treatment train and evaluates its consequences for data-center water-stress context. It explicitly states that further system-level thermal or operational integration between the desalination system and data center is outside the study's scope.

### Reported results (publisher abstract)

- Moving from conventional disposal to MLD/ZLD increases freshwater recovery by 4–220% across feed salinities, while reported input energy and water cost rise by more than 12% and 15%, respectively.
- Seawater hybrid RO–MVC with MLD: freshwater recovery 736 L per 1,000 kg feed, input energy 9.4 kWh/m³ permeate, and water cost US$3.2/m³ permeate.
- MVC with MLD for 50,000 ppm produced water: recovery 753 L per 1,000 kg feed, input energy 36 kWh/m³ permeate, and water cost US$10.4/m³ permeate.
- The abstract reports that MLD reduces SWUI by 40% in water-stressed settings. These are modeled results, not field measurements.

### SWUI and data-center water context

The article introduces Saline Water Utilization Intensity (SWUI), reported in L/kWh, to connect desalination recovery and data-center water demand with regional water-stress implications. The accessible introduction discusses PUE and WUE, the direct/indirect water consequences of cooling and electricity generation, saline feedwater sources, and the role of concentrate management.

The exact SWUI equation, normalization choices, spatial datasets, temporal aggregation, and treatment of source-water withdrawal versus consumption have **not** been verified from the full methods or SI. Do not infer those details from the metric name or abstract.

The publisher highlights state that evaporative cooling can produce SWUI above 7 and that a Longview, Texas scenario using brackish groundwater and two-stage RO had the lowest reported local stress. These are scenario-specific model outputs, not general performance guarantees.

## Prior-art comparison against Research 2

| Dimension | Katakam et al. (2026/2027) | Research 2 implication |
|---|---|---|
| Main question | Which mature desalination trains and brine strategies can supply data-center-quality freshwater across saline feed classes, and what are their technical/economic and regional water-stress consequences? | Strong prior art for data-center desalination system design, treatment-train comparison, brine management and water-stress framing. |
| Desalination technology | Two-stage RO, MVC and hybrids | Not an MD/DCMD/AGMD transport study. |
| Heat integration | The article explicitly places further system-level thermal or operational integration between the desalination plant and data center outside its scope. | It does not displace the narrower heat-source/MD coupling question, but it prevents claiming novelty for system-scale desalination or water-stress assessment for data centers. |
| Feed and brine envelope | Brackish, seawater and produced water; conventional disposal, MLD and ZLD | Broader salinity and concentrate-management envelope than the present reduced-order MD screening model. |
| Water metric | SWUI, a regional water-stress-oriented metric | A water-stress metric is established prior art. Any Research 2 metric must be demonstrably different and must not be marketed as the first data-center water-stress metric. |
| Physical validation | The accessible abstract/introduction/conclusion do not establish experimental validation of the complete desalination systems. Full methods and validation details remain unverified. | Do not assert equivalence or superiority on validation until full methods/SI are obtained. |
| Net operational blue-water ledger | Exact withdrawal/consumption and electricity-water accounting equations are not verified from accessible text. | A potential distinction must be demonstrated from full-text comparison, not presumed from absence in the abstract. |
| Time-varying data-center heat eligibility | Explicitly outside the stated scope of further thermal/operational DC–desalination integration. | The time-resolved recoverable-heat-to-MD coupling remains a distinct question, but Kanbur, Wyon and Yang remain direct adjacent prior art. |
| Reproducibility | Complete model equations, parameter tables, source files and SI not obtained in this audit. | Obtain the SI and assess code/data availability before judging reproducibility. |

## Novelty constraints

The paper is a direct prior-art threat to all broad claims that Research 2 is the first to:
- conduct system-scale desalination analysis for data-center freshwater needs;
- compare desalination technologies and brine-management strategies for data centers;
- evaluate data-center desalination in a regional water-stress context; or
- introduce a data-center-specific water-stress performance metric.

The paper does **not**, on the evidence currently accessible, establish:
- an MD/DCMD/AGMD transport model driven by time-resolved data-center heat;
- a coupled data-center thermal-operation and MD dispatch model;
- an experimentally validated MD model for that coupling; or
- a fully audited, counterfactual net operational blue-water ledger for an MD intervention.

These are statements about the evidence inspected, not proof that no other study has addressed them. The candidate Research 2 contribution remains conditional and unproven.

## Required follow-up before closing this prior-art item

1. Obtain the complete accepted manuscript or version of record and all supplementary files from a lawful accessible source.
2. Extract the exact SWUI equation, units, numerator/denominator, geographic water-stress data, temporal resolution and baseline.
3. Reconstruct the desalination system boundaries, process equations, property models, design constraints and cost basis from the methods and SI.
4. Identify all data-center scenarios, cooling technologies, WUE/PUE assumptions, feedwater sources and brine-management assumptions.
5. Check whether electricity-generation water, onsite power generation, water withdrawal, consumption, and water returned to source are separately counted.
6. Check model verification/validation, uncertainty, sensitivity, code availability and source-data provenance.
7. Update the claim-by-claim matrix only after those materials are inspected.

## Current conclusion

Katakam et al. materially narrows the novelty space: system-scale data-center desalination, RO/MVC/hybrid comparison, brine-management optimization and water-stress assessment are established prior art. The study's stated exclusion of further DC–desalination thermal/operational integration leaves a narrower potential distinction for source-traceable, time-resolved waste-heat-to-MD analysis, but that distinction must still survive full comparison with Kanbur (2020), Wyon (2025), Yang (2026), and other heat-driven MD work. The full-text/SI gate remains open.

## Sources

- Katakam et al., PubMed bibliographic record and abstract: https://pubmed.ncbi.nlm.nih.gov/42731480/
- Katakam et al., Elsevier ScienceDirect publisher record and indexed article text: https://www.sciencedirect.com/science/article/abs/pii/S0043135426014223
- DOI: https://doi.org/10.1016/j.watres.2026.126748
