# Yang et al. (2026) publisher-text and novelty-claim audit

**Audit date:** 2026-11-04  
**Paper:** Ruizhang Yang, Charalambos Konstantinou, Yunhe Hou, “Enabling grid-interactive data center-desalination coordination through thermo-electric coupling-based waste heat utilization,” *Applied Energy* 408 (2026), article 127428. DOI: [10.1016/j.apenergy.2026.127428](https://doi.org/10.1016/j.apenergy.2026.127428).

## Access status and evidence boundary

The ScienceDirect indexed article page exposes the abstract, highlights and a substantial portion of the introduction, including the authors' literature-gap framing, claimed novelty and first contribution. HKU Scholars Hub provides the bibliographic record and abstract. Its record explicitly reports **“There are no files associated with this item”** and links to the publisher, which requires organizational access or purchase. The HKU metadata carries a CC BY-NC-ND 4.0 rights statement, but no full-text file is attached to the record.

This is therefore a publisher-indexed text audit, **not** a full-text methods/equations/SI review. The article PDF, supplementary information, datasets and source code were not obtained. No independent reproduction was performed.

Access records:
- ScienceDirect article: https://www.sciencedirect.com/science/article/pii/S0306261926000802
- ScienceDirect PDF endpoint (access restricted): https://www.sciencedirect.com/science/article/pii/S0306261926000802/pdfft
- HKU Scholars Hub record: https://hub.hku.hk/handle/10722/379334
- DOI: https://doi.org/10.1016/j.apenergy.2026.127428

## What the article demonstrably claims

The abstract states that the authors:
1. develop a high-fidelity thermo-electric model connecting data-centre waste heat, seawater preheating, and temperature- and salinity-dependent RO efficiency;
2. embed that model in an integrated planning and operational optimization model;
3. co-optimize long-term investment planning and short-term operational dispatch;
4. formulate the problem as a two-stage stochastic MINLP;
5. solve it using Benders decomposition and McCormick envelope linearization.

The publisher abstract describes the contribution as the first model to directly embed the stated waste-heat/seawater-preheating/temperature-salinity-dependent RO physics within an integrated planning-and-operational optimization model. It reports an 86.5% reduction in total annualized cost relative to conventional configurations, with waste-heat synergy accounting for 17% savings. These are the authors' case-study results, not independently validated performance.

The introduction's gap framing is more specific:
- Existing power-system/desalination coordination often represents desalination as a simplified electric load and omits the physical pathway from feedwater preheating to RO SEC.
- Some RO demand-response work accounts for thermal sensitivity but abstracts the physical thermo-electric path.
- Existing data-centre flexibility research focuses on electrical demand, workload scheduling, microgrids and grid services; it does not co-optimize waste heat with RO process physics and desalination production scheduling.
- Heat-reuse literature includes data-centre integration with district heating, but the authors argue that an end-to-end planning-plus-dispatch framework with consistent thermo-electric dynamics is missing.
- The paper's stated novelty is the combination of workload-driven electricity-to-heat conversion, recoverable waste heat, temperature-dependent RO SEC, joint investment and operational scheduling, uncertainty, and a tractable solution procedure.

This is an important direct competitor. It already covers integrated data-centre waste-heat-assisted desalination planning/operation and a coupled thermo-electric optimization framework. Research 2 must not claim those contributions as novel.

## What remains unknown without full text/SI

The indexed text does not establish:
- exact data-centre workload-to-electricity-to-heat equations, utilization/IT load profiles, or server cooling assumptions;
- heat recovery fraction, heat exchanger effectiveness, approach temperatures, flow rates, heat losses, or temperature/pressure ranges;
- exact seawater RO membrane transport/flux/rejection equations and calibration sources;
- RO temperature and salinity dependence, pressure/flux equations, and validated operating envelope;
- whether RO preheating changes recovery, SEC, membrane area, pumping, fouling/scaling or lifetime;
- stochastic scenario construction, probability weights, temporal resolution, forecast errors and scenario reduction;
- complete investment variables, constraints, objective decomposition and baseline definitions;
- whether data-centre QoS/latency constraints and workload migration are modelled in detail;
- water withdrawal versus consumption, cooling-tower evaporation/blowdown, electricity-generation water factors, concentrate/brine fate, and freshwater displacement;
- whether regional water stress is modelled;
- source code, input data, solver tolerances, computational scaling and independent validation.

These are unknown from the accessible text, not evidence that the full article omits them.

## Direct consequence for Research 2

The following claims are not defensible:
- first integrated planning and operational coordination of data centres and desalination;
- first physical coupling of data-centre waste heat to seawater RO;
- first use of data-centre workload flexibility and waste heat as coupled energy/thermal resources;
- first co-optimization of waste-heat-assisted desalination and grid flexibility;
- first application of stochastic MINLP/Benders/McCormick methods to this integration.

A distinction based only on using MD rather than RO would be a technology-configuration difference, not a sufficient novelty argument. Kanbur (2020) and Wyon (2025) already threaten waste-heat-to-MD/DCMD claims; Chen (2026) threatens cooling/freshwater co-production claims through evaporation/MED.

A possible remaining direction for Research 2 is a transparent, source-resolved water-accounting/benchmarking study that separates withdrawal from consumption, explicitly accounts for the water implications of marginal electricity, cooling and concentrate management, and tests counterfactual freshwater displacement under regional and temporal conditions. This is only a candidate gap. It cannot be claimed until Yang and Katakam full methods are checked and the same boundary is searched across the wider literature.

The strongest potential value may be independent cross-technology benchmarking and boundary harmonization rather than proposing another integrated thermo-electric planning framework. If the complete literature already covers the candidate water ledger, reposition as a replication/benchmark or methods comparison.

## Claim-by-claim comparison checklist for full-text acquisition

| Dimension | Yang paper: established from indexed text | Research 2 comparison still required |
|---|---|---|
| Data-centre heat source | Workload-driven electricity-to-heat conversion | Compare workload/IT load and recoverable heat assumptions |
| Heat recovery | Waste heat used for seawater preheating | Extract heat exchanger equations, temperatures, losses |
| Desalination | Temperature- and salinity-dependent seawater RO | Compare RO against AGMD/DCMD equations and validation |
| Operational scheduling | Short-term dispatch jointly optimized | Compare time resolution and demand/heat matching |
| Capacity planning | Long-term investment jointly optimized | Compare investment scope and asset constraints |
| Uncertainty | Two-stage stochastic MINLP | Extract scenarios, probabilities and uncertainties |
| Optimization | Benders decomposition + McCormick linearization | Check formulation, relaxations, convergence and bounds |
| Cooling water | Not established by indexed text | Extract direct site withdrawal/consumption |
| Electricity water | Not established by indexed text | Extract generation withdrawal/consumption and avoid double counting |
| Brine | Not established by indexed text | Extract concentrate quantity, salinity and disposal |
| Net freshwater displacement | Not established by indexed text | Define counterfactual source and displacement factor |
| Water stress | Not established by indexed text | Check location-specific scarcity factors |
| Validation/code/data | Not established by indexed text | Extract validation and reproducibility artifacts |

## Literature claims requiring caution

The article's introduction makes broad statements about what prior work does not combine. These are the authors' literature-gap claims, not independently established facts. Research 2 must test them against the cited references and independent searches rather than repeating them uncritically.

The paper's abstract says “for the first time” for its particular integrated thermo-electric model. Do not generalize that phrase to all data-centre/desalination integration. The article itself is one primary source in a fast-moving field, and its claim requires checking its own cited prior art.

## Next steps

1. Obtain the complete publisher PDF and SI through institutional access or a user-provided copy. No purchase or author contact has been made.
2. Extract the full mathematical model, data, validation, system boundary, and objective.
3. Follow all 29 cited references in the article and screen the closest studies on RO temperature sensitivity, flexible desalination, data-centre waste heat, and planning/dispatch.
4. Compare the article's actual water boundary against Lei et al. (2025), Katakam et al. (2026/27), and the Research 2 ledger.
5. Update Issue #16's claim matrix only after full-text source comparisons.
6. Keep Issue #16 open. No novelty conclusion is justified from abstract/indexed text alone.
