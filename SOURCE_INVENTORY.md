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


11. **Martínez-Díez and Vázquez-González (1999), “Temperature and concentration polarization in membrane distillation of aqueous salt solutions,” *Journal of Membrane Science* 156, 265–273.** This is the primary experimental source underlying the 2020 paper's saline validation paragraph. Publisher-indexed experimental text is accessible, but the original figures/raw observations have not been retrieved or independently extracted. The 2020 Figure 3 caption has a verified reference mismatch; see [the source-provenance audit](docs/SECONDARY_FIG3_CAPTION_REFERENCE_VERIFICATION_2026-11-27.md). [DOI](https://doi.org/10.1016/S0376-7388(98)00349-4).

12. **Abdel-Rahman (2008), “Modeling Temperature and Salt Concentration Distributions in Direct Contact Membrane Distillation,” *Journal of Engineering Sciences, Assiut University* 36(5), 1167–1188.** This independent DCMD modelling paper explicitly compares its predictions with the 1999 experimental study and reproduces a pure-water subset at three feed/permeate velocities and ΔTb = 10 °C. It is a secondary reproduction, not the primary raw dataset; no new points were digitized. [Full PDF](https://jesaun.journals.ekb.eg/article_118726_da32ffe17fd391f214e6e2c75cb91678.pdf).

13. **Keshavarzzadeh (2020), “Design and bio-inspired optimization of direct contact membrane distillation for desalination based on constructal law,” *Scientific Reports*.** Open-access method and secondary Figure 3 source. Its validation paragraph cites the 1999 experiment (reference 37), while the Figure 3 caption cites unrelated reference 25; the discrepancy is documented as a high-confidence probable caption miscitation, not a publisher-corrected erratum. [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC7545101/).


14. **Central Electricity Authority (2026), _Framework for Water Audit of Thermal Power Plants: Standard Operating Procedure_.** This is the official accounting method for thermal-plant specific water consumption. It distinguishes FW1/FW2 freshwater inputs from non-fresh external inputs and internal reuse; mine water is categorized as NFW3. It defines a freshwater-input intensity and does not itself supply the missing plant/month observation series. [Official PDF](https://www.cea.nic.in/api/dashboardReports/view-pdf/en/d88a8d91-e888-42f9-879f-6af6b5788f98).

15. **Central Electricity Authority, Annual Report 2024–25.** Section 2.11.3 states that CEA has published plant-wise Monthly Environmental Stack Emission Status Reports with specific-water-consumption information from June 2022. The actual monthly report files were not located through the public division page or archive. [Annual report PDF](https://www.cea.nic.in/api/dashboardReports/download-pdf/en/f60d07cd-b057-42b7-9da8-19d5d559dc2a).

16. **Centre for Science and Environment (2021), _Water-Inefficient Power: Implementing Water Norms and Zero Discharge in India’s Coal-Power Fleet_.** Table 3.8 provides historical Tamil Nadu plant-level SWC values compiled from plant-reported data (2017–2020). CSE documents inconsistent reporting and lack of third-party verification; these values are historical screening evidence, not current audited grid factors. [Report](https://www.cseindia.org/content/downloadreports/10856).

17. **Macknick et al. (2012), “Operational water consumption and withdrawal factors for electricity generating technologies: a review of existing literature,” _Environmental Research Letters_ 7, 045802.** The associated NREL/OpenEI dataset is explicitly US technology-level literature-derived factors, with separate withdrawal and consumption values. It is suitable only as a US sensitivity comparator, not as a factor for the India, Spain, Singapore, or Germany proxies. The OpenEI dataset is CC BY 4.0 and was last updated 7 October 2025; the original report carries a separate CC BY-NC-SA 3.0 notice. [OpenEI dataset](https://data.openei.org/submissions/390) · [DOI](https://doi.org/10.1088/1748-9326/7/4/045802).

18. **CEA Clean Energy and Energy Transition division page and public report archive.** The division page exposes blank annual water-consumption and monthly Format 60 templates but its report lists show “No Reports Found”; the CEA public archive's monthly-report list does not list the environmental SWC report series. This is an access gap, not proof that the reports were never produced. [Division page](https://www.cea.nic.in/divisionPage/510?lang=en) · [Public archive](https://cea.nic.in/archive?lang=en).


19. **Comptroller and Auditor General of India, Report No. 35 of 2025, _Operational Performance of NLC India Limited_.** Section 3.13 (printed page 45) reports annual SWC values for TPS-IE, TPS-II and TPS-IIE from FY 2017–18 to FY 2022–23 and audits compliance with the 3.5 m³/MWh norm. CAG states that TPS-II remained above the norm after its water-treatment plant was commissioned in December 2022; TPS-IIE had no corresponding treatment-plant contract. The report's TPS-IIE footnote gives 3.32 m³/MWh in 2018–19, below the 3.50 norm despite the narrative's broad statement that TPS-IIE was above the norm. CAG's 2017–20 means also materially differ from CSE Table 3.8; the series are not pooled. CAG did not review NNTPS, and its SWC values do not specify source-water composition or consumptive fraction, so they are historical regulatory-SWC evidence rather than blue-water factors. [Official CAG PDF](https://cag.gov.in/uploads/download_audit_report/2026/CAG---NLC-India-Limited-2025-English-FINAL-SIGNATORY-10-12-2025-0698c6a3b5d7e42.69686670.pdf).


20. **Martínez-Díez, Florido-Díaz and Vázquez-González (2000), “Study of Polarization Phenomena in Membrane Distillation of Aqueous Salt Solutions,” _Separation Science and Technology_ 35(10), 1485–1501.** The publisher abstract describes experiments with water and aqueous NaCl feeds and measured flux/polarization results across different temperatures, recirculation rates, and feed concentrations. This is a candidate additional primary experimental source, but the full text/figures/tables are not verified and its overlap with the 1999 benchmark is unknown. It is not extracted or used for validation. [Publisher record and abstract](https://www.tandfonline.com/doi/abs/10.1081/SS-100100237) · [DOI](https://doi.org/10.1081/SS-100100237).
