# Initial Evidence Base

The initial evidence base is deliberately small and high quality. Each source will later receive a stable ID in SOURCES.yaml.

## AI water footprint

1. Li et al. (2023, revised 2025), *Making AI Less Thirsty*. arXiv:2304.03271. Provides a methodology for AI water withdrawal and consumption and emphasizes spatial and temporal variability. citeturn1academia96

2. Lei, Lu, Shehabi & Masanet (2025), *The water use of data center workloads*. Resources, Conservation & Recycling 219, 108310. Identifies server efficiency, grid water intensity, utilization, cooling, infrastructure efficiency and climate as important determinants of workload-level water use. citeturn1search6turn1search14

3. Herrera et al. (2025), *Sustainable AI infrastructure: A scenario-based forecast of water footprint under uncertainty*. Journal of Cleaner Production 526, 146528. Uses probabilistic scenario analysis and explicitly separates operational, electricity-related and embodied water consumption. citeturn1search1

4. *The water footprint of artificial intelligence: Emerging solutions and governance imperatives* (Water Research, 2026). Provides current context on AI water footprint and links technical mitigation to water constraints. citeturn1search4

## Waste heat and AI infrastructure

5. Díaz-Marín & Berquist (2025), *Flipping the switch: carbon-negative and water-positive data centers through waste heat utilization*. Energy & Environmental Science 18, 8403–8413. Treat as a perspective and conceptual source, not as direct proof of universal water positivity. citeturn1search7

## Membrane distillation

6. Gontarek-Castro & Castro-Muñoz (2024), *How to make membrane distillation greener*. Green Chemistry 26, 164–185. Reviews sustainability of membrane materials and operation and identifies low-grade waste heat integration as an energy-efficiency route. citeturn1search0

7. Guo et al. (2024), *Enhancement and optimization of membrane distillation processes*. Desalination 586, 117862. Systematic review of operating conditions, mechanisms, optimization and integration. citeturn1search10

8. Malaguti et al. (2026), *Waste heat won't make membrane distillation cool: Thermodynamic analysis of cooling and pumping burdens*. Desalination 628, 120039, DOI 10.1016/j.desal.2026.120039. This is a critical system-boundary source: it reports that cooling can approach 80–100% of heating in some configurations and identifies pumping penalties, demonstrating why our model must include heat sinks and hydraulics rather than treating waste heat as automatically free. citeturn0search0turn0search3

## Research consequence

The strongest version of this project should therefore be a conditional feasibility framework, not a predetermined demonstration that AI waste heat is water-positive. The model must allow positive, neutral, and negative net-water outcomes and quantify the conditions producing each regime.


## Additional India thermal-water evidence registered — 2026-11-27

9. **NLC India Limited, Integrated Annual Report FY 2021–22** (official company annual report). The 10-year physical-performance table (printed page 17) reports NNTPS gross generation of 6,178.74 MU and net generation of 5,758.70 MU for FY 2021–22. These are company-reported generation denominators, used only to cross-check the plant's environmental statement. [Annual report PDF](https://nsearchives.nseindia.com/corporate/NLCINDIA_07092022181900_AnnualReport22.pdf).

10. **MoEFCC-certified compliance report containing NNTPS Environmental Statement FY 2021–22** (printed pages 35–36). The operator-reported statement lists process water at 32,712.46 m³/day and process-water intensity at 0.069 L/kWh. The same report says mine water stored in a lake is used and groundwater is not extracted. [Compliance report PDF](https://environmentclearance.nic.in/writereaddata/Monitoring/56803999_NLC%20Thermal%20Power%20plant%202023_compressed.pdf).

**Source-quality finding:** if the reported 32,712.46 m³/day is an annual-average daily value, matching it to NLC's net generation of 5,758.70 MU/year implies 2.073 L/kWh, about 30.05 times the reported 0.069 L/kWh. The environmental statement does not define whether the daily volume is an annual average, design/peak rate, or a different boundary. Neither value is accepted as a water factor pending reconciliation. The plant uses mine water, which the CEA 2026 SOP classifies as NFW3 rather than the FW1+FW2 freshwater inputs used for CEA SWC. These documents provide a source-quality cross-check, not a site/grid factor.
