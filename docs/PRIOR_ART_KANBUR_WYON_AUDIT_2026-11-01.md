# Prior-art audit: Kanbur et al. (2020) and Wyon (2025)

**Review date:** 2026-11-01  
**Status:** source-grounded abstract/record audit; Wyon open-access full-text retrieval attempted but PDF fetch timed out. This is not a full-text methods audit or novelty clearance.

## 1. Kanbur, Wu & Duan (2020): desalination-integrated data-centre cooling

**Citation:** Kanbur, B. B., Wu, C., & Duan, F. (2020). “Multi-criteria thermoeconomic and thermodynamic assessments of the desalination-integrated two-phase liquid-immersion data center cooling system.” *International Journal of Energy Research*, 44(13), 10453–10470. DOI: https://doi.org/10.1002/er.5677. First published 23 July 2020.

**Accessible records:** Wiley full-record page (abstract and bibliographic metadata): https://onlinelibrary.wiley.com/doi/full/10.1002/er.5677 ; University of Southern Denmark record: https://portal.findresearcher.sdu.dk/en/publications/multi-criteria-thermoeconomic-and-thermodynamic-assessments-of-th/

### What the accessible record supports

- A hybrid two-phase liquid-immersion data-centre cooling and desalination system is proposed.
- The immersion-cooling waste heat heats the feed side of a direct-contact membrane distillation (DCMD) module.
- Reported cooling load range: 0.7–1.5 kW; reported membrane area range: 5–75 cm².
- The analysis is thermodynamic, economic and thermoeconomic, including a multiobjective optimization.
- Abstract-reported maxima/results include thermal efficiency 64.5%, exergy efficiency 53.7%, daily distilled-water production up to 6.13 kg at the highest cooling load and membrane area, and a 3.72-year payback period. These are the authors' reported results and have not been independently reproduced here.
- The abstract says the hybrid has higher capital and operating costs than stand-alone data-centre cooling. It reports levelized product cost in SGD/h; do not silently reinterpret this unit as SGD/m³.

### Comparison to Research 2

| Dimension | Kanbur et al. (2020) | Current Research 2 | Consequence |
|---|---|---|---|
| Heat source | Two-phase liquid-immersion data-centre cooling waste heat | Data-centre waste-heat scenarios | Waste-heat-to-desalination coupling is established prior art |
| Desalination | DCMD | MD/AGMD/DCMD research pathway | DCMD overlap is direct; process label cannot be a novelty claim |
| Coupling | Waste heat heats DCMD feed | Candidate model couples heat availability to MD and a physical water ledger | The integration itself is not novel; only a precisely demonstrated additional accounting/temporal method could distinguish the work |
| Scale | 0.7–1.5 kW cooling load; 5–75 cm² membrane area | Current scenario scale differs and needs normalized comparison | Do not compare output rates without area, feed, temperatures, recovery, and scale normalization |
| Metrics | Thermal/exergy efficiency, water production, economics, payback, product cost | Candidate net operational blue-water impact plus MD performance | Different estimands, but current water ledger is not yet fully validated |
| Cooling/pumping | Abstract identifies immersion cooling and technoeconomic system; detailed pump/cooling terms not extracted | Current model includes explicit cooling/pumping burdens as a key concern | Full methods needed to determine exact overlap and whether burdens are treated comparably |
| Water accounting | Withdrawal/consumption definitions not established from accessible abstract | Intended ledger distinguishes withdrawal, consumption and displacement | No novelty claim until Kanbur full text and SI are checked |
| Validation / uncertainty | Abstract does not establish independent experimental validation or uncertainty protocol | Independent MD validation and evidence calibration remain incomplete | No claim of stronger validation |
| Code/data | Not established in this record audit | Public repository | Verify availability and licenses before reproducibility comparison |

**Interpretation:** Kanbur et al. is a direct antecedent for the combination of data-centre cooling waste heat and DCMD. Research 2 must not claim first integration of data-centre waste heat with membrane distillation. The remaining potential distinction is in a rigorously defined, validated operational water-accounting boundary, not the heat-to-DCMD concept.

## 2. Wyon (2025): data-centre waste-heat desalination thesis

**Citation:** Wyon, A. (2025). “Desalination utilizing data centre waste heat.” Lund University, Environmental and Energy Systems Studies, report LUTFD2/TFEM—25/5229--SE + (1–53). Open-access repository record: https://lup.lub.lu.se/student-papers/record/9198095

### What the accessible institutional record supports

- Techno-economic analysis of membrane distillation driven by data-centre waste heat.
- Hypothetical 1.5 MW direct-to-chip data centre located in Barcelona, Spain.
- Three product-water use cases: data-centre air-cooling, electrolyser feed for backup hydrogen fuel, and sale to the local water grid.
- Python thermodynamic model including literature-based DCMD modules, a commercial heat exchanger and two commercial pumps.
- Economic modelling estimates simplified water cost per cubic metre and space requirement.
- The abstract concludes technical feasibility but economic challenges, particularly pump investment/operation relative to low water production at low data-centre waste-heat temperatures.
- Data-centre and electrolyser use cases are reported as more promising than sale to the water grid, given the latter's estimated cost relative to local water price.

### Comparison to Research 2

| Dimension | Wyon (2025) | Current Research 2 | Consequence |
|---|---|---|---|
| Heat source | Direct-to-chip data-centre waste heat | Data-centre waste-heat scenarios | Direct conceptual overlap |
| Desalination | Literature-based DCMD module model | MD/AGMD/DCMD pathway | MD integration is established prior art |
| Scale/geography | Hypothetical 1.5 MW Barcelona data centre | Current scenario geography/scale must be compared explicitly | A different geography or size alone is not methodological novelty |
| System integration | Heat exchanger and two commercial pumps; three product-water use cases | Candidate time-resolved heat eligibility and net water ledger | Need compare exact heat-exchanger, pump, and product-water equations |
| Pumping | Pump investment and operation materially affect economics | Explicit cooling/pumping burden is central to current net-impact question | Strong overlap in recognizing pump burden; quantify whether accounting boundary differs |
| Water use | Air-cooling, electrolyser, and grid-sale use cases | Intended withdrawal/consumption/displacement counterfactual | Compare each use case and define physical withdrawal vs consumption consistently |
| Electricity water | Not established by accessible abstract | Intended electricity-generation water factor | Possible gap only after full thesis review and evidence-supported factors |
| Validation / uncertainty | Abstract says DCMD modules based on literature; validation/uncertainty details not exposed | Independent primary MD validation remains incomplete | No claim of stronger validation |
| Code/data | Python model is reported; public code availability not established | Public repository | Do not imply Wyon code is unavailable without checking thesis appendices/repository references |

**Access attempt:** the institutional record exposes an “Open Access” PDF link. Opening the PDF through the browser and downloading it in this review session both timed out. Therefore, this audit uses the institutional abstract and metadata only; no chapter, equations, figures, appendices, or numerical tables have been inspected. The full-text criterion in issue #16 remains open.

## 3. Updated claim boundary

The following are now clearly established prior art and must not be claimed as novel by Research 2:

1. Using data-centre cooling waste heat to drive DCMD (Kanbur et al., 2020).
2. Modelling data-centre waste-heat-driven MD with heat exchangers and pumps at data-centre scale (Wyon, 2025).
3. Evaluating alternative uses of the produced water, including data-centre cooling and external supply (Wyon, 2025).
4. Treating pump capital and operating burden as a material feasibility constraint (Wyon, 2025).
5. Thermodynamic, exergy, technoeconomic and multiobjective evaluation of data-centre/DCMD integration (Kanbur et al., 2020).

A candidate Research 2 distinction remains a source-traceable, time-resolved, physically validated operational blue-water ledger that explicitly distinguishes direct withdrawal from consumptive use, cooling/pumping water, electricity-generation water, and defensible counterfactual freshwater displacement. This is not yet established as novel: full-text comparison, complete boundary normalization, and independent empirical MD validation are outstanding.

## 4. Source and access log

- Review date: 2026-11-01.
- Kanbur: Wiley full record and SDU institutional record accessed; abstract and bibliographic details extracted. Full article and supplements not inspected in this pass.
- Wyon: Lund University Publications institutional record accessed; abstract, metadata, and PDF link confirmed. PDF open/download timed out in this session; no full-text extraction claimed.
- Search route: exact DOI/title and institutional repository records.
- No systematic database search, citation-chain screening, or PRISMA-style selection was completed in this pass.

## 5. Required next actions

1. Retrieve and inspect the Wyon PDF through a working institutional download route; extract chapter/page locators, equations, module operating conditions, heat-exchanger and pump assumptions, water-use definitions, uncertainty, and appendices.
2. Obtain Kanbur full text and supplement; extract the DCMD model equations, feed/permeate boundary conditions, thermal integration, pump treatment, optimization constraints, and validation/uncertainty methods.
3. Compare both studies to the exact Research 2 code, experiment manifests, and data—not future planned architecture.
4. Continue full-text extraction for Chen et al. (2026), Yang et al. (2026), and Katakam et al. (2026/2027).
5. Archive reproducible search strings, databases, date ranges, citation-chasing decisions, and a claim-to-evidence matrix.

**Decision:** this audit confirms substantial prior-art overlap and narrows permissible claims. It does not close issue #16, establish novelty, or change the project's reproduction/validation status.
