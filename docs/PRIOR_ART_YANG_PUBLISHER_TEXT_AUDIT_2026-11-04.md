# Yang et al. (2026) publisher-text audit — 2026-11-04

**Citation:** Yang, R., Konstantinou, C., & Hou, Y. (2026). “Enabling grid-interactive data center-desalination coordination through thermo-electric coupling-based waste heat utilization.” *Applied Energy*, 408, article 127428. DOI: [10.1016/j.apenergy.2026.127428](https://doi.org/10.1016/j.apenergy.2026.127428). Published 1 April 2026.

**Primary publisher record:** [ScienceDirect article](https://www.sciencedirect.com/science/article/pii/S0306261926000802)  
**Publisher-indexed PDF route:** [ScienceDirect PDF record](https://www.sciencedirect.com/science/article/pii/S0306261926000802/pdf)  
**Institutional record:** [HKU Scholars Hub](https://hub.hku.hk/handle/10722/379334)

**Audit date:** 2026-11-04  
**Evidence level:** publisher-indexed abstract, introduction, stated research gaps, contribution statement, and section-level snippets. The full article PDF and supplementary information were not obtained. A direct open of the publisher article returned HTTP 403 in this session. This is a substantive publisher-text audit, not a complete methods/equations/SI review.

## 1. Publisher-text findings

### 1.1 System architecture and physical pathway

The article describes a flexible data-centre (DC) and seawater reverse-osmosis (RO) desalination system. Its stated physical chain is:

1. Flexible computing workloads are scheduled, changing data-centre electrical demand and workload-driven heat generation.
2. Server thermal behaviour and heat-recovery equipment determine the recoverable low-grade heat.
3. Recovered heat preheats RO seawater feed.
4. Feedwater temperature interacts with salinity, pressure, membrane transport characteristics, and flux to affect RO specific energy consumption (SEC).
5. The coupled thermal and electrical effects are represented in planning and operational decisions for the data centre and desalination system.

The publisher-indexed introduction specifically identifies the missing prior-art combination as workload flexibility represented as a schedulable electricity-to-heat conversion process, recoverable low-grade heat used as a desalination input, and temperature-dependent RO SEC. The contribution statement describes the physical chain from workload scheduling and server thermal behaviour through recoverable heat and feedwater preheating to RO SEC.

**Technology boundary:** this is reverse osmosis, not membrane distillation. It must not be described as an MD, DCMD, or AGMD study.

### 1.2 Optimization architecture

The publisher text describes a two-stage stochastic mixed-integer nonlinear programming (MINLP) framework:

- Long-term investment/capacity planning is coordinated with short-term operational dispatch.
- The coupled assets include data-centre infrastructure, desalination capacity, renewable generation, and energy storage.
- The physical thermo-electric relationships are intended to remain consistent across planning and operational stages.
- The article identifies renewable availability, electricity prices, and seawater conditions as uncertain inputs.
- The stated solution approach combines Benders decomposition with McCormick-envelope linearization to address the mixed-integer nonlinear and bilinear structure.

The indexed section heading identifies an “improved Benders decomposition” procedure. The accessible text does not expose enough of the algorithm, convergence criteria, recourse structure, or linearization bounds to independently reproduce or assess it.

### 1.3 Case-study claims

The publisher highlights and abstract report:

- an 86.5% reduction in total annualized cost compared with conventional configurations;
- a 17% cost saving attributed to waste-heat synergy.

The publisher-indexed case-study snippet identifies Jubail Industrial City, Saudi Arabia, and says the configuration is inspired by the co-location of the CenterServ Jubail City Data Center and Jubail Desalination Plant, stated to be less than 1 km apart.

These are author-reported model/case-study results. They are not independently reproduced here, and must not be represented as measured operational savings, a verified facility partnership, or transferable performance at another site.

## 2. Explicit contribution claims in the publisher text

The publisher-indexed contribution statement identifies three claims:

1. A unified planning-and-operation framework treating the data centre as both a controllable electrical load and a dispatchable thermal resource, linking workload scheduling, heat recovery, RO preheating, and coordinated capacity/scheduling decisions.
2. A physics-grounded thermo-electric desalination model representing feedwater temperature, salinity, membrane transport characteristics, pump pressure, and RO SEC, connected to workload-driven heat generation and server thermal behaviour.
3. A tractable stochastic co-optimization method using McCormick envelopes and two-stage stochastic Benders decomposition, with case-study cost outcomes.

The paper's own “first”/novelty language is recorded as the authors' claim, not accepted as an independently established priority finding. The introduction's prior-art review and citation chain still require verification.

## 3. Research 2 comparison: source-grounded boundary

| Dimension | Yang et al. (publisher-indexed text) | Research 2 repository status / comparison |
|---|---|---|
| Data-centre heat | Workload-driven heat generation and server thermal behaviour are part of the model | Research 2 investigates time-varying heat eligibility, but source-matched operational workload/heat data are not established by this audit |
| Heat recovery | Recoverable low-grade heat is coupled to seawater feed preheating | Research 2 proposes waste heat as the MD thermal input; heat-source assumptions remain scenario-dependent |
| Desalination process | Temperature-/salinity-/pressure-dependent RO | Research 2 targets MD/AGMD/DCMD physics; the governing transport equations and performance metrics are not interchangeable |
| Physical model | Publisher text claims a high-fidelity thermo-electric RO model including temperature, salinity, pressure, membrane transport and flux | Research 2 has an MD model and ongoing source-validation work; no comparative accuracy or superiority claim is justified |
| Optimization | Joint long-term investment planning and short-term dispatch; two-stage stochastic MINLP | Research 2's scenario/sensitivity and break-even analyses are not equivalent to a stochastic joint capacity-expansion and dispatch optimizer |
| Uncertainty | Renewable availability, electricity prices, and seawater conditions are named in the publisher text | Research 2's illustrative scenario ranges are not calibrated operational probability distributions; do not claim equivalent stochastic treatment |
| Grid interaction | Explicit grid-interactive framing and coordinated renewable/storage decisions | Research 2 accounts for selected incremental electricity-related water burdens; it does not implement an equivalent grid-dispatch/co-planning model |
| Water accounting | The accessible introduction, abstract, highlights, and contribution statement do not establish precise withdrawal, discharge, consumption, or electricity-generation water definitions | Research 2's candidate estimand is a counterfactual operational blue-water ledger; whether its boundaries are distinct must be tested against full Yang methods and tables |
| Cooling and pumping | Pump pressure is named as an RO physical-model variable; complete cooling-water, brine, and auxiliary burden treatment is not visible in the accessible text | Research 2 contains simplified MD cooling/pumping and water-factor assumptions; these must not be presented as directly comparable without boundary normalization |
| Geography | Jubail Industrial City case study; named facilities are reported as less than 1 km apart | Research 2's geographic/basin integration remains incomplete; no site-level transfer claim |
| Validation/data | The accessible publisher text does not reveal the full validation protocol, measured dataset, calibration split, or open code/data status | Research 2 independent primary MD validation remains incomplete; no comparative validation claim |
| Economic output | Annualized-cost case study with reported 86.5% reduction and 17% waste-heat contribution | Research 2's current focus is conditional net operational blue-water impact, not a validated equivalent annualized-cost optimization |

### 3.1 What this paper rules out

Yang et al. is direct prior art against claims that Research 2 is the first to:

- couple data-centre workload/heat behaviour to desalination operation;
- model recoverable data-centre heat as a dispatchable resource for desalination;
- connect waste-heat preheating to temperature-dependent desalination performance;
- coordinate data-centre and desalination planning with operational scheduling;
- use stochastic thermo-electric co-optimization for data-centre/desalination infrastructure;
- combine data-centre flexibility, renewable/storage decisions, and desalination operation.

The RO-versus-MD distinction is a real process-physics distinction, but is not sufficient by itself to establish a novel system contribution.

### 3.2 What remains unknown

The accessible publisher text does **not** establish:

- the exact RO governing equations or constitutive correlations;
- the detailed heat-exchanger model, effectiveness, thermal losses, or recoverable-heat constraints;
- the complete workload-to-server-heat conversion equations and time resolution;
- the exact stochastic scenario construction, probability distributions, and out-of-sample validation;
- the full water withdrawal, discharge, consumption, brine, and electricity-generation water boundaries;
- the cooling-water and auxiliary pumping accounting;
- whether any water-stress metric is used and, if so, its precise definition;
- measured versus modeled inputs, calibration/validation separation, or accessible underlying data/code.

Do not infer these missing details from the abstract or contribution statement. Obtain the full article and SI through an authorized route before marking the full-text comparison complete. No purchase or author contact was made.

## 4. Implications for Research 2's candidate contribution

The only defensible candidate distinction remains conditional and must be assessed against all close prior art, including Kanbur (2020), Wyon (2025), Chen (2026), Yang (2026), Katakam (2026/2027), Wang (2026), and Malaguti (2026):

> A source-traceable, independently validated MD model coupled to time-matched data-centre heat eligibility and a counterfactual operational blue-water ledger that separates withdrawal, discharge, and consumption; accounts for incremental cooling, pumping, and geographically/time-resolved electricity-water burdens; and tests substantiated freshwater displacement and failure/break-even regimes under uncertainty.

This is a research question/candidate scope, not a cleared novelty claim. The present implementation and evidence gates must be audited against the actual code and source data. Do not imply that all elements in this sentence are already implemented or validated.

## 5. Bibliographic and access log

| Date | Route | Result | Evidence classification |
|---|---|---|---|
| 2026-11-04 | ScienceDirect exact-title/DOI indexed record | Abstract, highlights, introduction and contribution statement surfaced | Publisher-indexed text |
| 2026-11-04 | ScienceDirect article page direct open | HTTP 403 | Full page not directly accessible |
| 2026-11-04 | ScienceDirect PDF route | Indexed publisher record surfaced; complete PDF not obtained | No complete PDF/SI inspection |
| 2026-11-04 | HKU Scholars Hub | Bibliographic metadata and abstract | Institutional metadata/abstract |
| 2026-11-04 | Publisher-indexed section snippets | Overall framework, two-stage stochastic optimization, Jubail case study, conclusion and contribution statement | Partial article text |

Search/access route used exact title, DOI 10.1016/j.apenergy.2026.127428, publisher PDF path, and institutional repository record. This is a targeted source audit, not a systematic database search or exhaustive citation-chain review.

## 6. Decision and next actions

1. Add this publisher-text extraction to the claim-by-claim prior-art matrix.
2. Obtain lawful full text/SI if an authorized library route is available; otherwise retain the exact access limitation and do not contact authors or purchase without authorization.
3. Extract Yang's actual equations, parameters, uncertainty distributions, validation protocol, water boundary, cooling/pumping/brine treatment, and code/data status only from the full methods/SI.
4. Recheck the current Research 2 code and experiment manifests before making any implementation comparison stronger than the bounded statements above.
5. Continue the Chen accounting crosswalk and the systematic-search protocol in Issue #16.
6. Keep Issue #16 and all novelty/publication/validation gates open.

**Decision:** the publisher-indexed introduction and contribution statement materially strengthen the Yang prior-art audit. They do not close the full-text comparison, establish novelty, or change any scientific validation gate.
