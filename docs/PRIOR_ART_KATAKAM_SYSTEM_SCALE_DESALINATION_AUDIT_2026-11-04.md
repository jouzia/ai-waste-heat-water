# Katakam et al. (2026 online / 2027 issue) system-scale desalination prior-art audit — 2026-11-04

**Citation:** Vishnu Sree Shanthanu Katakam, Mariam Arzumanyan, Ning Lin, and Vaibhav Bahadur, “System-scale design and analysis of desalination systems for meeting water needs of data centers,” *Water Research* 308, Part B, article 126748. DOI: [10.1016/j.watres.2026.126748](https://doi.org/10.1016/j.watres.2026.126748). PubMed records online-ahead-of-print publication on 17 August 2026; ScienceDirect assigns the article to the issue dated 1 January 2027. Cite as online-first (2026; issue 2027) until final bibliographic formatting.

**Publisher record:** https://www.sciencedirect.com/science/article/abs/pii/S0043135426014223  
**PubMed record:** https://pubmed.ncbi.nlm.nih.gov/42731480/  
**Additional publisher-indexed text:** ScienceDirect indexed article record, including introduction and section snippets.

**Audit date:** 2026-11-04  
**Evidence level:** publisher-indexed abstract, highlights, introduction, stated research gaps, selected methodology/results/conclusion snippets. Direct ScienceDirect open returned HTTP 403 in this session. Complete PDF, SI, all equations, detailed input tables, and validation data were not obtained. This is a publisher-text audit, not a complete methods/SI review or independent reproduction.

## 1. System boundary and technologies

The study models desalination systems designed to supply data-centre freshwater meeting a stated product quality of less than 500 ppm total dissolved solids (TDS). It evaluates:

- Two-stage reverse osmosis (RO).
- Mechanical vapour compression (MVC).
- Hybrid desalination configurations.
- Brackish feedwater, approximately 5,000 ppm.
- Seawater feedwater, approximately 35,000 ppm.
- Produced water at or above 50,000 ppm, with conclusion snippets identifying 50,000 and 90,000 ppm cases.
- Conventional concentrate disposal, minimum liquid discharge (MLD), and zero liquid discharge (ZLD).

The accessible introduction states that the study integrates the desalination treatment train, including pretreatment, post-treatment and concentrate management costs, with costs updated for present-day conditions. It examines freshwater recovery, energy consumption, second-law efficiency and water cost across feed salinities and brine-management strategies.

**Critical scope statement from the publisher text:** the authors explicitly state that further system-level thermal or operational integration between the desalination system and the data centre is beyond the study's scope. Their system-level integration refers to the complete desalination treatment train designed for data-centre freshwater quality and an evaluation of the resulting water-stress implications—not time-resolved physical coupling of data-centre workload/heat to desalination operation.

This scope statement is particularly important for comparison with Research 2.

## 2. Water-accounting and water-stress contribution

### 2.1 Direct and indirect water use

The publisher introduction distinguishes:
- Direct onsite water use associated with data-centre cooling.
- Indirect water use associated with electricity generation.
- For onsite power generation (for example, natural-gas generation), the associated water consumption may be classified as direct use for regulatory/reporting purposes rather than indirect use.

It defines data-centre WUE in L/kWh as total facility freshwater use divided by IT energy consumption, and contrasts water-intensive direct evaporative cooling with air-cooled systems that can shift burden toward electricity-related water use.

**Implication:** Research 2 cannot claim that separating direct cooling water from electricity-related water is itself a new contribution. The precise definitions and boundaries in the current model still need stronger factor metadata, but the conceptual direct/indirect split is established prior art.

### 2.2 Saline Water Utilization Intensity (SWUI)

The article introduces a named metric, **Saline Water Utilization Intensity (SWUI)**, with stated units of L/kWh. The publisher abstract describes it as quantifying the impact of data-centre desalination on local water stress. It is evaluated for three representative data-centre deployment case studies through 2030 and combines the effects of cooling technique, local saline-water conditions, geographic water stress and brine-disposal strategy.

Publisher-reported findings include:
- SWUI increases from 2023 to 2030 across representative conditions, spanning mild to substantial stress impacts.
- Higher recovery through MLD reduces SWUI by 40% in water-stressed settings.
- A publisher highlight states that evaporative cooling can cause severe water stress, with SWUI above 7.

**Do not reproduce or infer the SWUI equation from its unit or abstract description.** The exact formula, reference water-stress data, spatial/temporal aggregation, normalization, and sensitivity/uncertainty treatment require the complete article and SI. Do not describe SWUI as equivalent to Research 2's net-water ledger or as an empirical measurement.

### 2.3 Publisher-reported desalination results

| Case | Freshwater recovery | Energy input | Water cost |
|---|---:|---:|---:|
| Seawater hybrid RO-MVC with MLD | 736 L / 1,000 kg feed | 9.4 kWh/m³ permeate | $3.2/m³ permeate |
| 50,000 ppm produced-water MVC with MLD | 753 L / 1,000 kg feed | 36 kWh/m³ permeate | $10.4/m³ permeate |

The abstract also reports that moving from conventional disposal to MLD/ZLD increases freshwater recovery by 4–220% across feed salinities, while energy input and water cost rise by more than 12% and 15%, respectively.

These are author-reported model/optimization results. They are not independently reproduced measurements. The full baseline definitions, exact case inputs and SI tables were not available in this audit.

## 3. The paper's own prior-art positioning

The publisher-indexed introduction explicitly names several data-centre/desalination studies:
- Waste-heat-integrated thermally driven systems: Kanbur et al. (2020), Sondur et al. (2018), Wyon (2025), and Chen et al. (2026).
- Thermoelectrically coupled RO: Yang et al. (2026).

The authors argue that earlier work often focuses on waste-heat integration or thermo-electric RO, and that some prior models have simplifying assumptions involving process/property models, salt rejection, constant area-normalized flux, restricted feed salinity, limited recovery conditions, and incomplete pretreatment/brine/post-treatment economics.

These are the authors' literature-review assessments. They are not accepted as independently verified criticisms of every cited paper in this audit. Each cited work must be checked individually before repeating a methodological criticism in the manuscript.

The authors' stated contribution is a detailed process/thermodynamic/techno-economic assessment across brackish-to-hypersaline feed salinities and conventional-to-MLD/ZLD concentrate management, together with SWUI and representative geographic case studies.

## 4. Research 2 comparison

| Dimension | Katakam et al. publisher text | Research 2 current implementation / scope | Decision |
|---|---|---|---|
| Desalination technology | Two-stage RO, MVC and hybrids | MD/AGMD/DCMD-oriented model | Different process physics; not a direct numerical comparison |
| Feed salinity | Brackish, seawater and hypersaline produced water | Salinity is an input to MD calculations; the inspected break-even runner uses 5 g/kg feed salinity and fixed water activity | Current scenario is not a representative seawater/hypersaline treatment-train analysis |
| Freshwater quality | Data-centre product target below 500 ppm TDS | No product TDS acceptance/quality model in the inspected engine schema | Research 2 cannot claim equivalent product-water specification |
| Pretreatment/post-treatment | Explicitly included in system-level treatment train and costs | Auxiliary electricity coefficient exists; no complete pretreatment/post-treatment treatment train or cost model | Major scope difference |
| Brine management | Conventional disposal, MLD and ZLD | Feed and concentrate volumes/salinity are simplified outputs; no MLD/ZLD process model | No equivalent brine-management optimization |
| Recovery | Optimized across feed salinities and concentrate conditions | User-specified MD feed recovery fraction; no cost-optimal MLD/ZLD recovery optimization | Different purpose and model boundary |
| Energy | RO/MVC/hybrid system energy, including desalination treatment train | MD thermal demand, simplified cooling electricity and pump/auxiliary electricity | Not equivalent system energy boundary |
| Water metrics | WUE framing and SWUI water-stress metric | Conditional net operational water ledger: direct cooling + electricity-related water − counterfactual freshwater displacement | Direct/indirect water accounting and local water-stress metrics are prior art; Research 2's precise net ledger remains a candidate distinction only |
| Geography | Three representative data-centre deployment cases, local saline conditions and water stress | No basin-resolved water-stress factor in inspected core engine schema | Research 2 does not implement equivalent geographic stress assessment |
| Workload/heat coupling | Explicitly outside scope for further system-level thermal/operational integration | Workload duration, IT power and recoverable-heat fractions feed the reduced-order MD screening model | This is a potential scope distinction, but the Research 2 inputs and time matching remain illustrative and unvalidated |
| Waste heat | Introduction reviews waste-heat-driven thermal systems and Yang's thermoelectric RO | Research 2 models recoverable heat as MD thermal input | Broad use of data-centre waste heat is prior art; exact time-varying operational coupling requires careful comparison |
| Uncertainty | Full scenario and uncertainty method not visible in indexed text | Conditional scenario sweeps; values are explicitly not empirical probability distributions | Do not claim superior uncertainty treatment |
| Validation | Publisher says system-level modelling/optimization; detailed validation evidence unavailable in accessible text | Independent MD validation/source reconstruction remains incomplete | No predictive-validation comparison or superiority claim |
| Code/data | Open code/data status not established by accessible text | Research 2 repository is public | Do not infer the paper is closed or Research 2 is independently reproducible solely from repository availability |

## 5. What this paper rules out for Research 2

Research 2 must not claim:
- the first desalination framework designed for data-centre freshwater needs;
- the first system-scale RO/MVC/hybrid desalination assessment for data centres;
- the first assessment spanning brackish, seawater and hypersaline produced-water feeds;
- the first consideration of conventional, MLD and ZLD concentrate management for data-centre desalination;
- the first use of a data-centre-specific saline-water/water-stress metric;
- the first recognition of direct cooling and electricity-generation water burdens;
- the first geographic comparison of desalination choices and data-centre water stress.

The article does not, based on its own explicit scope statement, resolve time-dependent thermal or operational coupling between data-centre workload/heat and the desalination train. That is a potential distinction for Research 2, but not a cleared novelty claim: other sources (including Yang, Chen, Wyon and Kanbur) already cover parts of workload/heat/desalination integration, and the Research 2 implementation has not yet passed source reconstruction or independent validation.

## 6. Narrow candidate gap after Katakam, Yang and Chen

The defensible candidate question is now more specific:

> Under what source-traceable operating conditions does time-varying, temperature-eligible data-centre waste heat support MD water production while the incremental cooling, pumping, electricity-related water and demonstrable freshwater-displacement terms produce a net change in operational blue-water consumption?

This is a falsifiable research question, not a novelty conclusion. Its possible contribution would need to be shown through:
1. A validated configuration-specific MD model.
2. Time-matched, provenance-backed workload/heat availability rather than a generic recoverable-heat fraction.
3. Explicit direct withdrawal, consumptive loss, returned water and electricity-related water boundaries.
4. A counterfactual showing which freshwater demand is actually displaced.
5. A transparent comparison with SWUI and other local water-stress metrics, without claiming those metrics are new.
6. Independent validation and source-backed uncertainty ranges.

If the available evidence cannot support these requirements, narrow the paper to a benchmark/screening-method study rather than claiming an integrated operational framework.

## 7. Unresolved full-text/SI extraction

The following remain unknown from the accessible publisher-indexed text:
- Exact SWUI equation, component terms, normalization and water-stress data source.
- Exact geographic data and case-study inputs for the three deployments.
- Full water withdrawal/consumption accounting and treatment of onsite generation.
- Full WUE and SWUI time horizon and annualization.
- Detailed RO/MVC/hybrid process equations and optimizer formulation.
- Full pretreatment/post-treatment and MLD/ZLD cost equations.
- Feed/brine stream balances and disposal assumptions for every case.
- Exact validation cases, data, calibration/validation separation and errors.
- Uncertainty distributions, scenario generation and sensitivity analysis.
- Code/data availability and supplementary parameter provenance.

The publisher page's direct access returned HTTP 403. No complete PDF or SI was obtained. Do not infer the missing equation or implementation details from the abstract. No purchase or author contact was made.

## 8. Bibliographic/access log

| Date | Route | Result | Evidence level |
|---|---|---|---|
| 2026-11-04 | PubMed record | Ahead-of-print date, DOI, authors, abstract and indexing metadata | Bibliographic metadata + abstract |
| 2026-11-04 | ScienceDirect indexed record | Abstract, highlights, introduction, explicit scope limitation, section snippets and selected conclusions | Publisher-indexed article text |
| 2026-11-04 | ScienceDirect direct open | HTTP 403 | Full page not directly accessible |
| 2026-11-04 | JoVE Visualize | Abstract and metadata | Secondary abstract record |
| 2026-11-04 | UT Austin news release | Public summary of SWUI and case-study context | Institutional press summary, not methods evidence |

Searches used the exact title, DOI 10.1016/j.watres.2026.126748, publisher PII S0043135426014223, and the exact phrase “Saline Water Utilization Intensity”. This is a targeted audit, not a reproducible systematic review; full search strings, screening and citation-chain coverage still need archiving.

## 9. Decision and next actions

1. Add Katakam as a direct prior-art row in the claim-by-claim matrix and manuscript introduction.
2. Explicitly remove any proposed claim that Research 2 is the first data-centre desalination/water-stress framework.
3. Extract the exact SWUI formula and case inputs from an authorized full-text/SI route before comparing metrics.
4. Audit Wang et al. (2026), Lei et al. (2025), and Herrera et al. (2025) against the precise net operational water claim.
5. Continue the claim-by-claim comparison of Kanbur, Wyon, Chen, Yang and Malaguti.
6. Keep Issue #16 and every source-reconstruction, independent-validation and publication gate open.

**Decision:** Katakam et al. materially narrows Research 2's candidate contribution. It establishes prior art for system-scale data-centre desalination, direct/indirect water-use framing, and geographic saline-water stress assessment, while explicitly leaving detailed thermal/operational integration outside its scope. It does not validate Research 2 or establish that the remaining time-varying MD/net-blue-water question is novel.
