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

22. **Chaturvedi, Nagar Koti, Sugam, Neog and Hejazi (2017), _Implications of Shared Socio-economic Pathways for India’s Long-term Electricity Generation and Associated Water Demands_.** CEEW Working Paper 2017/16. Provides India-specific thermal-plant withdrawal factors, cooling-technology sample sizes, and a plant inventory. The paper applies global consumption-to-withdrawal ratios from Macknick et al. (2011) to Indian withdrawal observations; its coal/gas consumption values are therefore derived estimates, not direct Indian consumption measurements. It states that the Indian intensities include uses such as coal ash handling. [CEEW publication](https://www.ceew.in/publications/implications-shared-socio-economic-pathways-india-long-term-electricity-generation).
23. **Macknick, Newmark, Heath and Hallett (2011), _A Review of Operational Water Consumption and Withdrawal Factors for Electricity Generating Technologies_.** NREL/TP-6A20-50900, DOI 10.2172/1009674. Global technology-level literature review used as the ratio source in CEEW 2017; not an India-specific factor. [NREL report](https://www.nrel.gov/docs/fy11osti/50900.pdf).
24. **Chaturvedi, Sugam, Nagar Koti and Neog (2018), _Energy-Water Nexus and Efficient Water-Cooling Technologies for Thermal Power Plants in India_.** NITI Aayog-sponsored CEEW modelling report. Registered as a follow-on lineage source, not independent confirmation of the 2017 plant survey. [NITI Aayog record](https://www.niti.gov.in/node/698).
25. **Srinivasan, Kanudia, Roshna and Dharmala (2018), _Impact of Power Sector Growth on Water Resources_.** CSTEP Report 2018-02. Table 2 reports coal CT/OTC coefficients and a 30% coal ash-handling adjustment. The report cites CEEW and other sources; this is not an independent plant measurement, and an additional 30% must not be applied to CEEW values without resolving whether ash handling is already included. [NITI Aayog PDF](https://www.niti.gov.in/sites/default/files/2019-06/Final%20Report%20of%20the%20Research%20Study%20on%20Impact%20of%20Power%20Sector%20Growth%20on%20Water%20Resources%20conducted%20by%20C-STEP_Bangalore.pdf).
26. **Zhang, Yang, Urpelainen, Chitkara, Zhang and Wang (2021), “Thermoelectric Power Generation and Water Stress in India: A Spatial and Temporal Analysis.”** _Environmental Science & Technology_ 55(8), 4314–4323, DOI 10.1021/acs.est.0c08724. Provides a national plant-level geodatabase and modeled historical/projection estimates; applies CEEW 2017 factors, so it is not independent validation of those coefficients or a Tamil Nadu grid factor. [ACS article](https://pubs.acs.org/doi/10.1021/acs.est.0c08724).
27. **Reserve Bank of India, _Handbook of Statistics on Indian States_, Table 141: State-wise Electricity Transmission and Distribution Losses.** Reports Tamil Nadu T&D losses of 19.12% for FY 2018–19 (source: CEA). Used only for a conditional delivered-kWh screening gross-up, not as a current marginal loss or state-grid factor. [RBI table](https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=21531).
