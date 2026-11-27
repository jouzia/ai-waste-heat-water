# India electricity-generation water factors: CEEW source and derivation audit

**Audit date:** 2026-11-27  
**Purpose:** Determine whether India-specific thermal-power water coefficients can responsibly inform the project's electricity-related water-consumption sensitivity analysis.  
**Decision:** A useful historical, technology-specific Indian benchmark exists. It is suitable only as a labelled sensitivity input, not as a current Tamil Nadu/India grid-average factor or a site-specific marginal factor. The consumption coefficients are partly derived rather than directly measured, and one gas coefficient has a small but material source-to-source inconsistency. No geographic-integration or validation gate is advanced.

## 1. Primary India-specific source

Chaturvedi, V., Nagar Koti, P., Sugam, R., Neog, K., & Hejazi, M. (2017). *Implications of Shared Socio-economic Pathways for India's Long-term Electricity Generation and Associated Water Demands*. CEEW Working Paper 2017/16, September 2017.

- Public report: https://www.ceew.in/sites/default/files/CEEW-Implications-of-Shared-Socio-Economic-Pathways-for-India-Longterm.pdf
- Relevant sections: §2.3, pp. 5–6; §3.1, pp. 7–10; Table 3, p. 9; Appendix 1, pp. 23–25.
- The report compiles an India-specific power-plant inventory. It reports 198 units in the wider inventory and says the sample represents 88% of India's coal capacity as of 31 December 2015.
- The Table 3 withdrawal sample comprises 19 coal cooling-tower (CT) observations, two coal once-through-cooling (OTC) observations, and nine gas CT observations.
- Coal/gas withdrawal intensities are collated from plant-specific official/secondary sources, including water-tariff petitions and other reports. The authors state that the underlying Indian coal/gas source material generally reports withdrawals at the intake point, not measured consumption.
- The paper therefore estimates coal/gas consumption by applying global consumption-to-withdrawal ratios from Macknick et al. (2011) to the India-specific withdrawal values. These are **derived consumption estimates**, not a set of directly metered Indian consumption observations.
- The report explicitly says the Indian water intensities also include uses beyond cooling, including coal ash handling. They should not be described as cooling-tower-only factors.

## 2. Reported technology-specific ranges

The report's Table 3 reports the following min/median/max intensities in m³/MWh. Numerically, **1 m³/MWh = 1 L/kWh**.

| Fuel and cooling | Withdrawal (min / median / max) | Consumption (min / median / max) | Sample size |
|---|---:|---:|---:|
| Coal, CT | 2.31 / 3.79 / 5.16 | 2.19 / 2.59 / 4.80 | 19 |
| Coal, OTC | 171 / 216 / 261 | 0.86 / 1.56 / 1.64 | 2 |
| Gas, CT | 1.24 / 1.62 / 2.00 | 0.86 / 1.17 / 1.60 | 9 |

These values are operational generation-stage factors. They are not full life-cycle factors and do not include a complete upstream fuel-supply inventory. The coal CT sample is the most useful of the three for a historical Indian thermal-generation sensitivity case; the two-observation coal OTC sample is too small to support a stable distribution.

### Appendix-level freshwater-sample reconciliation

A row-level cross-check of CEEW 2017 Appendix 1 helps explain the coal sample sizes:

- The appendix contains freshwater/inland coal CT withdrawal records that, after excluding the three high-use CT outliers explicitly identified by the authors (8.70, 9.84, and 10.36 m³/MWh) and the Simhadri seawater CT record (0.83 m³/MWh), leave **19** CT records—the exact Table 3 sample size.
- The Table 3 coal OTC sample of **two** matches the freshwater Anpara and Obra records (171 and 261 m³/MWh). The seawater Tata Mundra OTC record is not part of that pair.
- This reconciliation strongly suggests that the Table 3 coal CT/OTC withdrawal summaries are based on inland/freshwater observations. However, CEEW does not publish an explicit row-to-summary inclusion crosswalk, so this is a transparent reconstruction rather than an author-confirmed filter.

The coal consumption estimates inherit the apparent freshwater scope of those withdrawal samples, but remain ratio-derived rather than directly metered. Do not generalise the inference to the gas sample: its row-level source-water and gas-cycle mapping needs its own reconciliation.

## 3. Consumption-factor derivation audit

The CEEW 2017 methods text says that, because India-specific coal/gas consumption observations were unavailable, the authors applied a consumption-to-withdrawal ratio from Macknick et al. (2011) to India-specific withdrawal values.

The central-value arithmetic is reproducible for the two coal cases using the corresponding Macknick generic coal medians:

- Coal CT: 3.79 × (2.60 / 3.80) = **2.59 m³/MWh**.
- Coal OTC: 216 × (1.00 / 138) = **1.57 m³/MWh**, consistent with the reported 1.56 after rounding/source precision.

The gas CT case is not safely reducible to a single correction. Macknick's later 2012 peer-reviewed review distinguishes natural-gas tower cooling into **combined-cycle** and **steam** configurations, with materially different consumption and withdrawal medians. The CEEW 2017 dataset reports one aggregate gas-CT category and does not specify which Macknick subcategory or exact 2011 source-row mapping was used for its conversion. Applying the steam ratio alone (3.1/4.6) gives 1.09 m³/MWh, but that is not a justified universal correction for an unspecified gas-CT sample. Applying the combined-cycle ratio gives a different result.

The CEEW 2017 Table 3 reports **1.17 m³/MWh** for gas CT consumption. The later CEEW report, Chaturvedi et al. (2018), Table 3, reports **1.1 m³/MWh** alongside 1.62 m³/MWh withdrawal. The later report cites Chaturvedi et al. (2017), so this is a follow-on presentation of the same coefficient lineage, not an independent empirical dataset. IRENA's 2018 India power-water methodology table also reproduces the 2017 gas recirculating value of 1.17 and cites CEEW 2017; this is another downstream reuse, not an independent sample. The difference may reflect rounding, a different Macknick category mapping, or an undocumented calculation detail; the available source text does not resolve it.

- Macknick et al. (2012), open-access review: https://doi.org/10.1088/1748-9326/7/4/045802
- CEEW 2018 report: https://www.niti.gov.in/sites/default/files/2023-03/Energy-Water%20Nexus%20and%20Efficient%20Water-Cooling%20Thermal%20Power%20Plants%20in%20IndiaTechnologies%20for%20An%20Analysis%20within%20an%20Integrated%20Assessment%20Modelling%20Framework.pdf
- CEEW 2018 Table 3, pp. 14–15; it cites Chaturvedi et al. (2017).

**Disposition:** retain 1.17 as the value printed in CEEW 2017 and 1.1 as the later rounded presentation. Flag the gas-CT derivation as unresolved because the gas-cycle subtype and exact Macknick mapping are not explicit. Do not silently overwrite 1.17 with the steam-only calculation of 1.09.

## 4. Cross-report lineage and double-counting guardrail

Srinivasan et al. (2018), CSTEP, *Impact of Power Sector Growth on Water Resources*, Table 2, reports coal CT withdrawal/consumption of 3.79/2.6 and coal OTC 216/1.6. It cites CEEW and other sources and adds a footnote stating that coal consumption coefficients were increased by 30% for ash handling.

This presentation should not be treated as an independent confirmation of the CEEW coefficients. The CEEW 2017 paper itself states that its India-specific water intensities include other uses such as coal ash handling. The exact coefficient lineage behind CSTEP's additional 30% note needs reconciliation before combining or applying any further ash-handling uplift. **Do not apply another 30% adjustment to the CEEW 2017 values.**

- CSTEP report: https://icemf.niti.gov.in/sites/default/files/2.%20Impact%20of%20Power%20Sector%20Growth%20on%20Water%20Resouces.pdf
- Relevant sections: §3.1, Table 2, p. 12.

## 5. Relevance to this project's electricity-water factor

The engine's nonzero `grid_water_l_per_kwh` input is explicitly consumption-only. The CEEW coal CT estimate is therefore dimensionally compatible with that field **only in a scenario where the electricity being represented is explicitly assigned to coal generation with cooling-tower technology and the study's operational boundary is accepted**.

It is not a defensible default for the current project because:

1. It is a historical 2015-era sample, not a 2026 operating factor.
2. It is a coal/gas technology factor, not a Tamil Nadu, Southern Region, or national grid-average factor.
3. It does not identify the marginal generator supplying the intervention's incremental electricity.
4. It does not resolve electricity imports, regional dispatch, generation shares, or plant-specific cooling/source-water conditions.
5. The consumption values are derived using global ratios rather than directly measured Indian coal/gas consumption.
6. The coal values include ash-handling water and should not be relabelled as cooling-only water.
7. The source denominator is electricity generated (m³/MWh), whereas the engine applies its factor to incremental facility electricity consumption. A defensible implementation would need a compatible delivered-kWh denominator or an explicit transmission/distribution-loss adjustment; using the generation factor directly is only a screening simplification.
8. The source does not provide a year- and region-specific generation mix or a marginal supply factor.



### Permitted use

- Retain the CEEW 2017 coal CT consumption range **2.19–4.80 L/kWh (median 2.59)** as a historical India-specific, technology-conditioned sensitivity benchmark.
- Keep withdrawal and consumption in separate columns and separate scenario families.
- Label the consumption values as ratio-derived estimates.
- If used in a scenario, state explicitly that the assumed marginal supply is coal CT; do not call it a grid-average or site-specific factor.
- Treat the coal OTC and gas CT ranges as secondary sensitivity cases with their small sample sizes and the gas-CT median discrepancy disclosed.

### Prohibited use

- Do not populate a default Tamil Nadu or India grid factor from this source.
- Do not average these values with CSE/CAG plant-specific SWC observations; the source periods, data construction, cooling categories, and boundaries differ.
- Do not combine withdrawal coefficients with the consumption-only net-water estimand.
- Do not treat the CEEW 2018 or CSTEP 2018 tables as independent replications of the CEEW 2017 sample.
- Do not infer a site-specific net-water benefit or advance the geographic-integration gate.

## 6. Reproducibility checks

The arithmetic above is reproducible from the source medians:

```text
Coal CT:  3.79 * (2.60 / 3.80) = 2.5926  -> 2.59
Coal OTC: 216  * (1.00 / 138) = 1.5652  -> 1.56
Gas CT:   no unique recalculation without resolving the gas-cycle subtype and Macknick source-row mapping
```

The report's stated method and the tabulated gas CT median cannot be independently reconciled without identifying the gas-cycle subtype and exact Macknick 2011 source row used. The later CEEW 2018 value of 1.1 is a follow-on rounded value, not independent evidence that resolves the mapping.

## 7. Evidence classification and gate decision

- **India-specific withdrawal data:** source-compiled from plant-specific official/secondary records; historical and heterogeneous.
- **Coal/gas consumption data:** derived estimates using Macknick global consumption/withdrawal ratios; not directly metered India-specific consumption.
- **Technology-specific benchmark:** suitable for sensitivity analysis with explicit provenance and assumptions.
- **Whole-grid/site factor:** not established.
- **Independent validation:** not established.
- **Gate change:** none. Keep geographic integration false, quantitative validation claims false, and publication-ready claim false.

This is a source-method audit and factor-provenance note. It does not calculate a Tamil Nadu grid average, update model defaults, add observations to an experimental ledger, or establish a net-water result.


## 8. Peer-reviewed national thermal-fleet aggregation (Zhang et al., 2021)

A later peer-reviewed study provides a stronger national historical aggregation than a single technology coefficient:

Zhang, C., Yang, J., Urpelainen, J., Chitkara, P., Zhang, J., & Wang, J. (2021). *Thermoelectric Power Generation and Water Stress in India: A Spatial and Temporal Analysis*. Environmental Science & Technology, 55(8), 4314–4323. https://doi.org/10.1021/acs.est.0c08724

- The authors compiled a bottom-up geodatabase for India's coal-, natural-gas-, and nuclear-fired plants; historical generation was assembled from CEA monthly reports, while cooling types were identified using WRI plant data, environmental-clearance documents, and satellite imagery.
- They applied fuel/cooling-specific water factors (their Table 1, sourced from CEEW 2017) to plant-level generation and aggregated estimated water use at national, state, and catchment levels.
- Their Table 2 reports **1,106 TWh** of thermoelectric generation and **2,393.4 million m³** of freshwater consumption in 2018. Summing the freshwater-source consumption rows gives 72 + 11 + 2,212 + 51 + 46 + 1 + 0.4 = 2,393.4 million m³. Dividing by 1,106 TWh gives **2.164 L/kWh**, rounded to **2.16 L/kWh**.
- The same table yields approximately **2.14 L/kWh** for 2009 (1,315.3 million m³ / 615 TWh) and **2.36 L/kWh** for the 2027 SWITCH-India projection (3,817.4 million m³ / 1,617 TWh).
- The 2027 value is a least-cost, current-policy model projection, not an observation.
- The 2018 thermal fleet was coal-dominated (about 92% of the study's thermoelectric generation); it also included natural gas and nuclear generation and multiple cooling systems.

### Interpretation

The 2.16 L/kWh value is a **national thermal-fleet freshwater-consumption intensity**, not an all-grid factor. The numerator includes freshwater consumption only; seawater consumption is excluded. The denominator includes the study's coal, gas, and nuclear thermoelectric generation. Hydropower, wind, solar PV, and other non-thermoelectric generation are outside this study's thermal-fleet denominator and boundary.

This is a modelled estimate, not direct metering. Its water-intensity inputs are the CEEW 2017 factors audited above, so it is a spatially explicit application of that coefficient lineage—not an independent validation of those coefficients. The study's value is the plant-level generation/cooling inventory and national/state/catchment aggregation.

The study reports that freshwater consumption exceeded 200 million m³ in 2018 in Uttar Pradesh, Chhattisgarh, Madhya Pradesh, and Maharashtra, and that these four states accounted for nearly half of thermoelectric freshwater consumption. It provides state- and catchment-level spatial analysis, but the article text does not report an exact Tamil Nadu-specific consumption intensity. It therefore does not supply a Tamil Nadu grid factor.

### Permitted use

- Retain **2.16 L/kWh (2018)** as a historical, national, thermal-only freshwater-consumption benchmark.
- Retain **2.14 (2009)** and **2.36 (2027 projection)** as contextual time-series values, clearly distinguishing historical estimates from the projection.
- Use the 2018 value only in an explicitly labelled all-thermoelectric-supply sensitivity case or as the thermal component of a separately constructed grid-mix scenario.
- If constructing a total-grid factor, combine thermal and nonthermal generation with matched-year generation shares and defensible nonthermal water factors; do not simply relabel 2.16 as a grid average.
- Preserve the generation-side denominator. The project engine applies its factor to incremental facility electricity consumption; a compatible delivered-kWh factor or explicit transmission/distribution-loss adjustment is required before direct use.

### Exclusions and gate decision

- Not a current 2026 factor, not Tamil Nadu-specific, and not a marginal-generator factor.
- Not a full-grid factor; hydropower and non-thermoelectric generation are outside the study boundary.
- Not independent factor validation because Table 1 uses CEEW 2017 inputs.
- Do not use as the engine default or as a site-specific net-water claim.
- Geographic integration remains **false**; quantitative validation and publication-readiness gates remain unchanged.



### Delivered-kWh screening gross-up using Tamil Nadu T&D losses

The project engine applies its electricity-water factor to incremental facility kWh, so a generation-side factor needs a delivery-basis adjustment before direct use.

RBI Table 141 (source: CEA) reports Tamil Nadu T&D losses of **19.12% for FY2018-19**. The relevant table header is 2012-13 through 2019-20; the Tamil Nadu row is 14.5, 10.8, 11.1, 10.8, 12.6, 15.94, **19.12**, and 17.39. The 13.5 value appearing in the preceding table belongs to an earlier year, not FY2018-19.

Using the 2018 national thermoelectric factor as a conditional all-thermal supply case:

```text
F_generation = 2393.4 million m3 / 1106 TWh = 2.164 L/kWh
F_delivered  = F_generation / (1 - 0.1912)
             = 2.6756 L/kWh
             ≈ 2.68 L/kWh delivered
```

This is a **screening gross-up**, not a Tamil Nadu grid factor. It assumes all incremental facility electricity is supplied by the national thermoelectric fleet; it does not apply a Tamil Nadu generation mix or marginal dispatch weights. The T&D loss statistic is a state-wide accounting measure and is not a pure marginal technical-loss factor; it may include unaccounted/commercial losses. The study's "2018" generation year and the RBI FY2018-19 loss year are plausibly aligned through CEA monthly data, but the article does not explicitly state the fiscal-year convention. Keep the 2.68 value as a separately labelled sensitivity case only.

- RBI Table 141 (published 19 November 2022; source CEA): https://www.rbi.org.in/Scripts/PublicationsView.aspx?id=21531
- CEA national T&D series is not substituted for the state value; the adjustment uses the Tamil Nadu row only.

No engine default is changed. The result does not establish a Tamil Nadu grid-average, marginal factor, or site-specific net-water outcome; the geographic-integration gate remains false.


## 9. National non-hydropower grid factors from WRI/IRENA (2018)

A more complete national non-hydro generation benchmark is published in the WRI/IRENA report *Water Use in India's Power Generation: Impact of Renewables and Improved Cooling Technologies to 2030* (2018).

- Main report: https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2018/Jan/IRENAIndiapowerwater2018pdf.pdf?rev=8c0edce7c68643529763377b3076f9d9
- Methodology and data sources: https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2018/Jan/IRENA_power_water_2018_methodology.pdf?hash=C1726E07286F34010EB878321F72C471F0C4427C&la=en
- Main report Figure 3, p. 6; methodology Tables 1–3, pp. 2–6.

The study reports freshwater consumption intensity for India's **non-hydropower** generation:
- 2014 baseline: **2.09 m³/MWh**.
- IRENA Reference 2030: **1.94 m³/MWh**.
- IRENA REmap 2030: **1.70 m³/MWh**.
- CEA Scenario 1 (2027, high coal/low hydro): **1.63 m³/MWh**.
- CEA Scenario 2 (2027, low coal/high hydro): **1.57 m³/MWh**.

Numerically, 1 m³/MWh = 1 L/kWh. The report defines consumption as freshwater consumed while producing 1 MWh of electricity. The baseline is 2014 because that was the latest year with complete disaggregated generation/capacity data in the cited IEA and CEA datasets.

### Independent reproduction of the 2014 baseline

The 2.09 L/kWh baseline is reproducible from the methodology tables:

```text
I_2014 = Σ_f [G_f × Σ_c (freshwater_share_f,c × C_f,c)] / Σ_f G_f
       = 2.0865 L/kWh
       ≈ 2.09 L/kWh
```

Here, generation by fuel is taken from methodology Table 1, freshwater consumption factors by fuel/cooling from Table 2, and freshwater/seawater cooling shares from Table 3. Seawater-cooled generation contributes no freshwater cooling consumption in this boundary; hydropower is excluded. The independent reconstruction agrees with the published Figure 3 value after rounding.

### Scope and source quality

- This is a national non-hydro generation average, not a thermal-only factor. It includes thermal generation, nuclear, biomass, solar PV, CSP, geothermal, and wind (wind is assumed to require no operational water).
- Hydropower reservoir evaporation is explicitly excluded because attribution to electricity is ambiguous for multipurpose reservoirs.
- Fuel extraction/processing and equipment manufacturing are excluded.
- The model combines heterogeneous factor sources: CEEW 2017 for several coal/gas/nuclear/oil/CSP categories; NREL 2012 for biomass and geothermal; IGES 2013 for gas/oil dry cooling; IRENA 2016 for coal dry cooling; CSE 2015 for CSP dry cooling; and Indian solar-PV developer information for PV cleaning.
- Generation and cooling/source-water shares are national and are not disaggregated by state. The report's methodology states that the IRENA scenarios are national and do not provide state-level generation deployment.
- Future values are scenario outputs, not observations or probability distributions. The 2027 CEA cases depend on the Draft National Electricity Plan assumptions; 2030 cases depend on IRENA Reference/REmap pathways and cooling-policy assumptions.

### Permitted use

- Retain the **2014 baseline 2.09 L/kWh** as a historical national non-hydropower freshwater-consumption benchmark.
- Retain **1.57–1.63 L/kWh** as the two 2027 CEA scenario projections and **1.70–1.94 L/kWh** as the two 2030 IRENA scenario projections; do not treat these as a measured confidence interval.
- These values are closer to a national grid-generation factor than the thermal-only Zhang et al. 2021 factor, but remain non-hydro and generation-side.
- Before use in the engine, convert to a delivered-kWh basis using a compatible transmission/distribution-loss treatment. Do not apply a national factor as a Tamil Nadu or marginal-supply factor without additional evidence.

### Gate decision

This source provides a credible historical national non-hydro benchmark and transparent future scenarios, but it does not provide a current Tamil Nadu grid factor or marginal generation factor. Hydropower remains outside the boundary. Geographic integration remains **false**; no model default, validation gate, or publication claim is changed.
