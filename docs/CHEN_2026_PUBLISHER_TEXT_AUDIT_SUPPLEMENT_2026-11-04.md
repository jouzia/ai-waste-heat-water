# Chen et al. (2026) publisher-text audit supplement

**Audit date:** 2026-11-04  
**Paper:** Longxiang Chen, Hui Xie, Meina Xie, Liugan Zhang, Kai Ye, Shizhu Li, “A dual-purpose seawater evaporation system for data center cooling and freshwater production: design and performance analysis,” *Applied Thermal Engineering* 287 (2026), article 129458. DOI: [10.1016/j.applthermaleng.2025.129458](https://doi.org/10.1016/j.applthermaleng.2025.129458).

## Evidence level and access

The ScienceDirect indexed publisher page exposed substantially more than the abstract: the introduction, system description headings, methodology assumptions, model platform, selected conclusion text, and bibliographic reference list. This is **publisher-indexed article text**, not a verified complete PDF or supplementary-information audit. The complete methods, equations, parameter tables, figures, and SI were not available in the inspected text. Do not label this as a full-text review or independent reproduction.

Publisher page: https://www.sciencedirect.com/science/article/pii/S1359431125040505  
Abstract page: https://www.sciencedirect.com/science/article/abs/pii/S1359431125040505

## System architecture established by the visible text

The paper's system is more specific than the short description “seawater evaporation” suggests:

1. Low-pressure seawater phase change absorbs data-centre waste heat and provides cooling.
2. The evaporation generates salt-free vapour.
3. A multi-stage compressor maintains the low-pressure evaporation condition and raises vapour pressure/temperature.
4. Compressor discharge vapour is routed into a multi-effect distillation (MED) process, recovering condensation heat to increase freshwater production.
5. Two configurations are modelled:
   - **SEFDS:** basic seawater evaporation system for data centres.
   - **SEFDS-WI:** enhanced configuration with water-injection heat exchange.

This is not described as membrane distillation. It combines low-pressure seawater evaporation with mechanical vapour compression and MED heat recovery. That distinction matters for a fair comparison with Research 2's AGMD/DCMD model.

## Reported system-level results (authors' model outputs)

The abstract reports the following comparisons against conventional standalone systems:

| Metric | SEFDS | SEFDS-WI |
|---|---:|---:|
| Freshwater production | 10,004.20 t/day | 10,744.12 t/day |
| Freshwater production increase | 13.9% | 21.6% |
| Power reduction | 41.5% | 40.0% |
| Reported power | 6,095.49 kW | 6,349.08 kW |
| Capital cost reduction | 13.1% | 9.1% |
| Operating expense reduction | 37.0% | 34.9% |
| CO2 reduction | 41.6% | 40.0% |
| Reported payback | 3.33 years | 3.30 years |

These values are reproduced from the publisher abstract. They are not measured operating data and have not been independently checked against the full paper's tables or baseline definitions. In particular, the stated power reductions should not be interpreted as a reduction in total data-centre electricity consumption without checking the paper's exact comparison boundary.

## Modelling assumptions visible in publisher text

The methodology snippet states:
- Steady-state thermodynamic modelling of each device.
- All components treated as adiabatic.
- Throttling valves treated as isenthalpic.
- The model is implemented in MATLAB.
- Working-fluid properties are computed using REFPROP 9.1.
- The authors say the MVC-MED, IECS, SEFDS, and SEFDS-WI systems are validated, but the visible text does not expose the validation data, error metrics, or validation scope.

The work compares the proposed configurations with an indirect evaporative cooling system for data centres (IECS) and an MVC-MED desalination system. The conclusion characterizes the work as a thermodynamic, economic, and environmental comparison of the integrated systems against conventional cooling and heat-driven MED desalination.

## Prior-art consequence

This is a direct and strong competitor for the proposition that data-centre waste heat can be integrated with seawater processing to co-produce cooling and freshwater. The architecture also recovers compressor condensation heat through MED, so it is not simply a heat-reuse add-on to an independent desalination plant.

The repository must not claim as novel:
- data-centre cooling plus seawater-derived freshwater co-production;
- low-pressure seawater evaporation driven by data-centre waste heat;
- integration of that vapour stream with MED;
- thermodynamic/thermoeconomic evaluation of such a combined system.

The paper's architecture differs from the repository's AGMD/MD focus. That is a process-configuration difference, not by itself a novelty contribution.

## Critical unresolved accounting questions

The visible publisher text does not establish:
- seawater feed flow and total seawater withdrawal;
- the split between evaporated vapour, freshwater product, rejected concentrate, blowdown, and other losses;
- the salt balance and concentrate/brine discharge concentration or fate;
- whether the “salt-free” vapour/product quality is measured, assumed, or modelled;
- source-water withdrawal versus consumptive use;
- auxiliary electricity boundaries and whether data-centre IT electricity is included;
- whether cooling duty and freshwater production are normalized to the same functional unit;
- the baseline configurations and denominator used for the reported power reductions;
- the exact CO2 accounting factors and whether marginal or average grid factors are used;
- geographic water-stress characterization or counterfactual freshwater displacement;
- transient/seasonal operation, workload variation, or time matching of waste heat to water demand.

These omissions are **unknown from the accessible publisher text**, not proof that the paper itself omits them.

## Research 2 comparison requirements

Before positioning Research 2 against Chen et al., extract from the complete article and SI:
1. Full process-flow diagram and all stream labels.
2. Component mass and energy balances, including seawater feed, vapour, freshwater, brine and water injection.
3. Compressor stages, pressure ratios, efficiencies and electricity consumption.
4. MED effects, heat-recovery equations, performance ratio and temperature levels.
5. Data-centre cooling duty, waste-heat temperature/flow and any IT load assumptions.
6. Baseline definitions and functional units for energy, cost, freshwater and emissions comparisons.
7. Validation cases, source datasets, model errors and sensitivity ranges.
8. Water withdrawal, consumption, discharge, brine and freshwater displacement accounting.

Until these are extracted, no quantitative comparison or net-water superiority claim is justified.

## References and access

- ScienceDirect full article landing: https://www.sciencedirect.com/science/article/pii/S1359431125040505
- ScienceDirect abstract/indexed text: https://www.sciencedirect.com/science/article/abs/pii/S1359431125040505
- DOI: https://doi.org/10.1016/j.applthermaleng.2025.129458

No complete PDF/SI, code, or independent reproduction was obtained in this audit.
