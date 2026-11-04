# Kanbur et al. (2020) direct-contact MD prior-art audit — 2026-11-04

**Citation:** Baris Burak Kanbur, Chenlong Wu, and Fei Duan, “Multi-criteria thermoeconomic and thermodynamic assessments of the desalination-integrated two-phase liquid-immersion data center cooling system,” *International Journal of Energy Research* 44 (2020), 10453–10470. DOI: [10.1002/er.5677](https://doi.org/10.1002/er.5677). [Publisher record](https://onlinelibrary.wiley.com/doi/abs/10.1002/er.5677).

**Evidence available in this audit:** Wiley publisher record and abstract/summary. The publisher's full-text route redirected to the abstract and the hosted full text was unavailable in this session. No complete article PDF or SI was obtained. Therefore this is a publisher-abstract audit only, not an equation-level reconstruction or validation audit.

## 1. Established system concept

The publisher abstract describes a hybrid data-centre cooling and desalination system:
- Data-centre cooling uses a two-phase liquid-immersion cooling unit.
- Cooling load is investigated over 0.7–1.5 kW.
- Waste heat from the immersion-cooling system heats the feed side of a direct-contact membrane distillation (DCMD) module.
- The reported membrane-area range is 5–75 cm².
- The system is evaluated thermodynamically, economically and thermoeconomically, including a multiobjective optimization.

The publisher reports maximum thermal efficiency of 64.5%, maximum exergy efficiency of 53.7%, and a daily distillate production up to 6.13 kg at the highest cooling load and membrane area. The hybrid system is reported to have higher capital and operating costs than standalone data-centre cooling, with a 3.72-year payback period and levelized product cost reported as 2.69–5.33 SGD/h. The abstract reports a best trade-off at a cooling load of 1.1 kW and membrane area around 5.12–5.19 cm².

These are author-reported model outputs in the abstract. They are not independently reproduced measurements. The unit reported for levelized product cost should be checked in the complete paper before any quantitative comparison.

## 2. Direct overlap with Research 2

Kanbur et al. establish prior art for:
1. Direct-contact membrane distillation driven by data-centre waste heat.
2. Using the data-centre cooling loop as the source of thermal energy for MD feed heating.
3. Evaluating coupled data-centre cooling and MD performance.
4. Joint thermodynamic, economic, thermoeconomic and multiobjective optimization.

Consequently, Research 2 cannot claim the first data-centre waste-heat/DCMD integration, the first use of DCMD for data-centre waste-heat utilization, or the first technoeconomic analysis of this broad system concept.

The fact that Research 2 uses a different data-centre scale, geography, or a different MD configuration would not alone establish a publishable novelty.

## 3. What remains unknown from the accessible publisher record

The abstract does not establish:
- The exact DCMD heat and mass transfer equations.
- Membrane material, thickness, porosity, pore size and wetting assumptions.
- Feed/permeate inlet temperatures, flow rates, salinity and channel geometry.
- Heat-exchanger approach temperature and effectiveness.
- Pump curves, pressure drops, hydraulic efficiency and pumping boundaries.
- Whether the model is steady-state or transient.
- The exact data-centre heat source temperature profile and time variation.
- Validation dataset, calibration procedure, error metrics and independent validation.
- Water withdrawal, consumption, return flow, cooling-water source and brine/concentrate boundaries.
- Electricity-related water consumption or grid-water factors.
- Counterfactual freshwater displacement and product-water end use.
- Water-stress weighting, spatial factors or uncertainty distributions.
- Code and data availability.

Do not infer these details from the abstract or substitute assumptions from other MD studies. Obtain the complete paper/SI through an authorized route before making equation-level or validation claims.

## 4. Comparison with Wyon (2025) and current Research 2

Wyon's 2025 thesis independently models a hypothetical 1.5 MW direct-to-chip data centre in Barcelona with DCMD, a commercial heat exchanger and two commercial pumps, including three product-water end uses. It also reports a model-to-experiment heat-flux comparison with residual discrepancies and acknowledges unresolved causes. That is a distinct and more detailed case-study source, but it still does not establish a validated, general time-resolved net-water framework.

The current Research 2 engine is a reduced-order MD screening model with simplified cooling coefficients, pump/auxiliary terms, factor-based electricity water, and explicit counterfactual freshwater displacement. It is not a reproduction of Kanbur's DCMD design or Wyon's 80-module case. The present implementation must not be described as validated by either paper.

| Dimension | Kanbur (2020) publisher abstract | Research 2 current scope |
|---|---|---|
| MD configuration | DCMD | MD-oriented reduced-order model; configuration-resolved validation incomplete |
| Data-centre cooling | Two-phase liquid immersion | Generic workload/heat scenario |
| Heat use | Immersion cooling waste heat heats MD feed | Recoverable heat supplies simplified MD thermal demand |
| Scale | 0.7–1.5 kW cooling load; 5–75 cm² membrane area | Scenario-level energy/thermal accounting; not Kanbur's geometry |
| Outputs | Thermal/exergy efficiency, distillate, cost, optimization | Conditional energy and water ledger/break-even outcomes |
| Water accounting | Not established in accessible abstract | Direct and electricity-related burden minus explicit freshwater displacement assumptions |
| Time-resolved workload coupling | Not established in accessible abstract | Current workload input is scalar duration/power; not yet time-series validated |
| Independent validation | Unknown from abstract | Research 2's independent validation remains open |

## 5. Revised research-positioning consequence

Kanbur and Wyon together eliminate a broad novelty claim around data-centre waste-heat-driven DCMD/MD. Katakam, Wang, Lei and Herrera further establish prior art around system-scale data-centre desalination, counterfactual water accounting, direct/indirect water burdens, geographic water stress and workload-level water assessment.

A possible remaining question must therefore be much narrower and evidence-led:

> For a specified and independently validated MD configuration, how do source-traceable, time-varying data-centre heat temperature and availability constrain MD production, and under what explicit water withdrawal/consumption, pumping, electricity-factor and freshwater-displacement assumptions does the intervention become net-positive, neutral or net-negative in operational blue-water terms?

This is a research question, not a novelty claim. Before asserting it as novel, compare Kanbur and Wyon full methods/SI, primary MD validation datasets, and any published water-accounting or temporal heat-eligibility analyses.

## 6. Decision and next actions

- [x] Confirm Kanbur's direct DC-waste-heat/DCMD overlap from the publisher abstract.
- [x] Record accessible system scale, outputs and the full-text access limitation.
- [ ] Obtain authorized full article/SI and reconstruct its equations, design parameters, optimization and validation.
- [ ] Compare the Kanbur model line-by-line with Wyon's thesis and the current Research 2 model.
- [ ] Identify primary experimental MD data suitable for independent validation, preserving configuration and operating conditions.
- [ ] Determine whether the Research 2 candidate time-resolved heat eligibility and net operational blue-water question has direct prior art.
- [ ] Keep Issue #16, source reconstruction, independent validation and publication gates open.

**Decision:** Kanbur et al. is direct prior art for data-centre waste-heat-driven DCMD. Research 2 must not claim that broad concept as novel. The accessible abstract does not resolve whether the narrower time-resolved, source-traceable net operational blue-water question is new; that remains unproven.
