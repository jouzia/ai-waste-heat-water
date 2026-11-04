# Source-bounded comparison: Katakam et al. (2026) data-centre desalination and SWUI

**Audit date:** 2026-11-04  
**Evidence status:** Publisher indexed full-text/extended introduction and section snippets inspected; PubMed abstract and publisher metadata checked. The complete article PDF, full methods/equations/tables, and supplementary information were not obtained or audited. This is not an independent reproduction.

## Bibliographic record

Vishnu Sree Shanthanu Katakam, Mariam Arzumanyan, Ning Lin, and Vaibhav Bahadur, “System-scale design and analysis of desalination systems for meeting water needs of data centers,” *Water Research* 308 (2027), article 126748; published online 17 August 2026. DOI: [10.1016/j.watres.2026.126748](https://doi.org/10.1016/j.watres.2026.126748).

- Publisher record: https://www.sciencedirect.com/science/article/abs/pii/S0043135426014223
- PubMed record: https://pubmed.ncbi.nlm.nih.gov/42731480/

## What the source establishes

The article models desalination treatment trains for data-centre freshwater quality (TDS <500 ppm). It evaluates two-stage reverse osmosis (RO), mechanical vapour compression (MVC), and hybrid configurations across brackish water (5,000 ppm), seawater (35,000 ppm), and produced water (at least 50,000 ppm). Concentrate pathways include conventional disposal, minimum liquid discharge (MLD), and zero liquid discharge (ZLD).

The abstract reports:
- MLD/ZLD increase freshwater recovery by 4–220% across feed salinities, while input energy and water cost increase by more than 12% and 15%, respectively.
- A seawater hybrid RO–MVC case with MLD: 736 L freshwater per 1,000 kg feed, 9.4 kWh/m³ permeate, and $3.2/m³ permeate.
- A 50,000 ppm produced-water MVC/MLD case: 753 L freshwater per 1,000 kg feed, 36 kWh/m³ permeate, and $10.4/m³ permeate.
- The paper introduces Saline Water Utilization Intensity (SWUI), reported in L/kWh, to connect desalination and data-centre water demand to local water-stress implications. It reports a 40% SWUI reduction from higher MLD recovery in water-stressed settings.

These are published model outputs as reported in the abstract, not independently verified measurements or reproductions.

## Important scope clarification from the publisher's extended text

The article explicitly distinguishes its meaning of “system-scale integration” from physical thermal/operational integration with a data centre. Its final scope statement says that system-level integration refers to coupling the complete desalination treatment train, designed and cost-optimized for data-centre-specific water quality, with an evaluation of the resulting regional water-stress impact through SWUI. Further system-level thermal or operational integration between desalination and the data centre is outside the study's scope. The authors state that facility-specific operational data could later extend this work to mass- and energy-coupling.

This is material: the article is direct prior art for desalination-centered system-scale techno-economic design and water-stress assessment for data-centre water supply, but it does not, on the publisher text inspected, demonstrate an operationally coupled data-centre waste-heat-to-desalination plant.

## Boundary and accounting information visible in the indexed text

The extended introduction describes direct onsite cooling water and indirect electricity-generation water as distinct data-centre water demands. It also notes that where a data centre self-generates electricity using onsite natural gas, the associated generation water may be treated as direct rather than indirect for regulatory/reporting purposes. The paper frames PUE and WUE as energy and freshwater-use ratios relative to IT energy.

The indexed text also describes:
- freshwater quality target below 500 ppm TDS;
- brackish, seawater, and industrial produced-water feed classes;
- conventional, MLD, and ZLD concentrate management;
- pretreatment, post-treatment, and concentrate-management costs in the modeled treatment train;
- water stress as a regional impact of saline-water utilization, rather than considering only freshwater footprint.

However, the full SWUI equation, exact numerator/denominator, source-water withdrawal/consumption treatment, stress-factor data source and spatial resolution, brine impact characterization, and allocation choices were not visible in the retrieved material. These must not be inferred from the metric name or abstract. They require full methods and SI.

## Direct comparison with Research 2

| Dimension | Katakam et al. evidence visible | Research 2 implication |
|---|---|---|
| Data-centre water supply by desalination | Directly modeled for RO, MVC and hybrids | Established prior art; do not claim desalination-for-data-centres itself as novel |
| Feed salinity | Brackish, seawater and produced water | Our scenarios must be compared on a like-for-like feed basis |
| Concentrate management | Conventional, MLD, ZLD | Brine pathway must be explicit, not a generic disposal penalty |
| Treatment train costs | Abstract/extended text says pretreatment, post-treatment and concentrate costs included | Compare cost boundary before claiming broader techno-economic completeness |
| Regional water stress | SWUI introduced; exact equation/data not yet inspected | Direct prior art for a desalination-to-water-stress metric; audit formula before defining any distinction |
| Data-centre cooling water | Direct and indirect water demand discussed | Align site and electricity-related boundaries |
| Physical waste-heat coupling | Explicitly outside scope in the inspected scope statement | A potential technical distinction is actual thermal/operational coupling, but not yet a novelty claim |
| Time-resolved operation | Not established by the inspected text | Need full methods to determine whether dispatch or temporal resolution exists |
| Withdrawal vs consumption | Exact SWUI accounting treatment not established from accessible sections | Do not assume SWUI is a withdrawal metric or a net-water metric |
| Counterfactual freshwater displacement | Not established in the inspected text | Must be tested from full article before asserting absence |

## Research implications and required next checks

1. Obtain the complete article and SI. Extract the exact SWUI definition, equations, source datasets, spatial water-stress factors, time horizon, and all boundary/normalization assumptions.
2. Reconstruct the desalination process train and techno-economic boundary: pretreatment, RO/MVC, energy inputs, post-treatment, concentrate disposal, capital and operating cost basis, and freshwater quality.
3. Determine whether feedwater withdrawals, product-water consumption, brine return/disposal, and electricity-related water are treated as withdrawals, consumption, or stress-weighted volumes. Do not conflate these.
4. Compare SWUI mathematically against the repository's net freshwater impact formulation. A new label or different normalization alone is not a contribution; any proposed distinction must be supported by a materially different, defensible boundary or operational question.
5. Test whether a source-specific waste-heat-driven membrane-distillation system can be compared on equal freshwater quality, source-water, energy, concentrate, and cost boundaries. The paper's RO/MVC systems are not interchangeable with MD.
6. Keep the broader prior-art issue open. The article's explicit exclusion of physical thermal/operational coupling is a useful scope distinction, not proof that no other paper addresses it.

## Bounded prior-art conclusion

Katakam et al. is direct prior art for system-scale, techno-economic desalination design to meet data-centre water-quality needs and for connecting saline-water use/desalination recovery to regional water-stress assessment through SWUI. It therefore rules out broad novelty claims around “desalination for data centres,” “system-scale desalination for data-centre freshwater,” or “a water-stress metric for data-centre desalination.”

The publisher text inspected explicitly places physical thermal/operational coupling between desalination and the data centre outside the study's scope. Research 2 may investigate a different question involving waste-heat-driven membrane distillation and a source-resolved net-water ledger, but the exact distinction remains provisional until Katakam's SWUI methods and other relevant prior art are fully reviewed.

No claim is made that SWUI omits withdrawal accounting or counterfactual displacement; those details are not established by the accessible text inspected here. Issue #16 remains open.

## Access log

| Source | Access | Evidence level |
|---|---|---|
| PubMed record | 2026-11-04 | Bibliographic metadata and abstract |
| ScienceDirect publisher record | 2026-11-04 | Abstract, highlights, extended introduction, visible section snippets, and scope statement |
| Full publisher PDF | Not obtained | Not reviewed |
| Supplementary information | Not obtained | Not reviewed |
| Raw model/code/data | Not obtained | No independent execution or reproduction |
