# Geographic electricity–water factor integration audit — 2026-10-22

## Decision

**The electricity-related water-factor join is not yet defensible for the six city-centroid proxies.** Do not calculate a single net-water result by attaching a U.S.-wide factor to Chennai, Hyderabad, Barcelona, Singapore, Frankfurt, or Phoenix. The current geographic layer remains context screening only.

This audit distinguishes three different quantities that must not be substituted for one another:

1. **Data-centre direct water use / WUE** — water used or withdrawn at the facility per unit of IT energy, with operator-specific definitions.
2. **Electricity-generation water intensity** — water consumed or withdrawn upstream to generate electricity, per unit of electricity, dependent on grid mix, year, plant cooling, and accounting boundary.
3. **Basin water-stress indicator** — contextual risk classification; it is not a physical water volume and must never be multiplied into litres.

## Source assessment

| Candidate source | What it can support | What it cannot support by itself | Project disposition |
|---|---|---|---|
| WRI Aqueduct 4.0 | Basin-level baseline/future water-stress context after versioned spatial sampling | Physical water intensity, local water availability, grid water factor | Retain as context only; current coordinates are city-centroid proxies |
| NREL / OpenEI operational electricity-generation water factors | Literature-derived U.S. technology-level withdrawal/consumption scenarios; CC BY 4.0 source is openly catalogued | A location- and year-specific factor for Indian, Spanish, Singaporean, or German electricity supply; not a substitute for grid mix | May be used as a clearly labeled external sensitivity comparator, not the primary factor for non-U.S. sites |
| CEA / Ministry of Power thermal-plant water-consumption reporting and norms | India-specific primary-source evidence about thermal-plant water use, plant reporting formats, and regulatory limits | A national, all-generation, all-year consumption-per-kWh factor without plant output, generation mix, and compatible consumption observations | Preferred India evidence track; retrieve source data and calculate only with matching generation denominators |
| CEEW / peer-reviewed India water-for-electricity modeling | India-specific modelled withdrawal/consumption scenarios and sensitivity to generation mix/cooling technology | A directly observed, current, Chennai-specific marginal factor unless the underlying scenario and boundary actually provide it | Candidate for a sourced scenario range after full methods/data audit |
| Operator-reported data-centre WUE | Facility/portfolio direct-water scenario when the published metric's boundary is explicit | Upstream electricity-generation water or a universal cross-operator factor | Use only in a separate direct-facility ledger; do not merge blindly with grid factors |

## Verified source leads

1. **NREL/OpenEI dataset:** “Operational Water Consumption and Withdrawal Factors for Electricity Generating Technologies.” Public dataset, CC BY 4.0; its scope is explicitly electricity-generation technologies in the United States. Dataset: https://data.openei.org/submissions/390 ; Data.gov catalogue: https://catalog.data.gov/dataset/operational-water-consumption-and-withdrawal-factors-for-electricity-generating-technologi
2. **Central Electricity Authority (India):** environmental-data formats include annual and monthly water-consumption reporting for thermal power stations. Official entry: https://www.cea.nic.in/divisionPage/510?lang=en
3. **Government of India / Ministry of Power:** parliamentary response describes thermal-power-plant water-consumption norms and implementation context. Official press release: https://www.pib.gov.in/PressReleasePage.aspx?PRID=1989804&lang=2&reg=48
4. **CEEW / peer-reviewed India analysis:** Srinivasan et al. (2018), “Water for electricity in India: A multi-model study of future challenges and linkages to climate change mitigation,” *Applied Energy* 210, 673–684, DOI https://doi.org/10.1016/j.apenergy.2017.04.079. Summary page: https://www.ceew.in/publications/water-electricity-india
5. **Data-centre workload water review:** Lei et al. (2025), DOI https://doi.org/10.1016/j.resconrec.2025.108310, finds large variation across workload water use and identifies grid water factors, cooling type, utilization, efficiency, and climate as material determinants. It supports site/year-specific modeling, not a universal factor.

## Required schema for any future factor row

Every row in the factor join must have:

- `factor_id`, `geography`, `country_or_grid_region`, and `year_or_period`
- `generation_technology` or `grid_mix_scope`
- `water_metric`: `consumption` or `withdrawal` (never a generic `water_use`)
- `value`, `unit`, and denominator (e.g. L/kWh generated)
- `source_title`, `source_url`, DOI/report/table/page locator
- `source_type`: measured / reported / modeled / regulatory limit / scenario
- `cooling_technology`, `fuel`, and system boundary when reported
- `transformation`, generation-mix weights, and conversion arithmetic
- `retrieval_date`, dataset version, license, and checksum for downloaded files
- `applicability_note` and `exclusion_reason` where a row is not applicable to a target site

A regulatory maximum (for example, a thermal-plant limit expressed per MWh) is a **compliance threshold**, not observed average consumption and not a grid-average factor. Do not use it as the central estimate. If it is included, it must be labeled as a separate regulatory-bound scenario.

## Calculation rule

For a grid-mix scenario with technology shares (s_i) and compatible technology-specific consumption factors (c_i), a weighted factor may be calculated only if the shares cover the same geography and period, sum to one (within declared rounding tolerance), and all (c_i) use the same water metric and electricity denominator:

[
C_{grid} = sum_i s_i c_i.
]

If the source gives generation-weighted factors, do not weight them again by capacity shares. If only withdrawal factors are available, do not label the result consumption. If a source reports water per thermal plant output but the model needs water per grid kWh, include the generation share and denominator conversion explicitly. Keep the direct data-centre WUE term separate from (C_{grid}).

The electricity-related water term for incremental auxiliary energy should be computed as:

[
W_{electricity} = E_{incremental} × C_{grid}
]

with compatible kWh and L/kWh units and the water metric stated. Apply the same factor convention to baseline and intervention wherever the counterfactual requires it; do not count the entire facility's electricity water as incremental intervention burden.

## Concrete completion sequence

1. Retrieve CEA annual/monthly thermal-plant water-consumption reporting and matching generation output for the same units/period, where public data permit.
2. Inspect CEEW/Srinivasan et al. model inputs and output tables to identify an India-wide scenario with a documented consumption/withdrawal boundary. Treat it as modeled evidence, not a direct measurement.
3. Select a target-year grid mix from an official generation dataset and check that it is generation share, not installed capacity.
4. Build a small provenance table first for India; do not extrapolate it to the other five proxies.
5. Add Spain, Singapore, Germany, and the U.S. only when equivalent country/year/grid evidence is sourced and metric-compatible. If evidence is not comparable, report separate scenario ranges or leave the factor missing.
6. Unit-test that withdrawal and consumption cannot be silently interchanged, weights sum to one, no factor is assigned outside its geography/year scope, and missing factors block quantitative site-level output.
7. Update the geographic gate only after the factor table, source snapshots/checksums, transformation script, tests, and output ledger exist and have been reviewed.

## Current status

- Aqueduct city-proxy sampling: executed previously; contextual screening only.
- Primary facility locations: not established.
- Compatible site/year electricity-generation water factors: not joined.
- This audit: committed source-selection and calculation protocol only; no new factor values were fabricated and no geographic gate was passed.

## References

- NREL/OpenEI, Operational Water Consumption and Withdrawal Factors for Electricity Generating Technologies: https://data.openei.org/submissions/390
- Central Electricity Authority, environmental data formats for thermal power stations: https://www.cea.nic.in/divisionPage/510?lang=en
- Ministry of Power, Government of India, “Steps being taken to reduce water consumption in thermal power plants” (23 December 2023): https://www.pib.gov.in/PressReleasePage.aspx?PRID=1989804&lang=2&reg=48
- Srinivasan, S. et al. (2018), *Applied Energy*, 210, 673–684: https://doi.org/10.1016/j.apenergy.2017.04.079
- Lei, N. et al. (2025), *Resources, Conservation and Recycling*, 219, 108310: https://doi.org/10.1016/j.resconrec.2025.108310

## Source-access checkpoint (2026-10-22)

Follow-up verification is recorded in [GEOGRAPHIC_FACTOR_SOURCE_ACCESS_CHECKPOINT_2026-10-22.md](GEOGRAPHIC_FACTOR_SOURCE_ACCESS_CHECKPOINT_2026-10-22.md). The official CEA page indexes annual and monthly reporting formats, but one current official URL redirected to a login page during this review; no public observed plant-level dataset was extracted. The Open Government Data station-generation catalog is a possible denominator source, not a factor by itself. The India multi-model paper remains suitable only for source-cited scenario analysis after table-level extraction. The factor ledger therefore remains intentionally empty and the geographic gate remains false.

## Addendum — CEA India thermal-plant water-accounting source audit (2026-11-27)

### Newly verified official source

The Central Electricity Authority's **CEA Framework for Water Audit of Thermal Power Plants: Standard Operating Procedure**, released November 2026, is now accessible as an official CEA PDF:

- Official PDF: https://www.cea.nic.in/api/dashboardReports/view-pdf/en/d88a8d91-e888-42f9-879f-6af6b5788f98
- Official division page listing annual and monthly thermal-plant environmental data formats: https://www.cea.nic.in/divisionPage/510?lang=en
- CEA Annual Report 2024–25, section 2.11.3, states that CEA has published Monthly Environmental Stack Emission Status Reports from June 2022, including plant-wise specific-water-consumption information: https://www.cea.nic.in/api/dashboardReports/download-pdf/en/f60d07cd-b057-42b7-9da8-19d5d559dc2a

### What the CEA SOP actually measures

The SOP defines Specific Water Consumption (SWC) in m³/MWh as freshwater input per unit of net electricity generation. Its accounting rules are unusually useful for separating freshwater-source categories:

- Only raw surface water and groundwater (FW1 + FW2) count in SWC.
- Externally supplied treated sewage/effluent, harvested rainwater, and other non-fresh inputs are separately recorded but excluded from SWC.
- Internal recycled/reused water is recorded as an internal flow and is not added again to total external input.
- The water audit separately records plant outflows, consumption/losses, storage changes, and unaccounted water.

The official definition and formula are on SOP page 3 and pages 18–20. The reporting template asks for net generation and SWC both including and excluding township supply. The monthly SWC table (page 28) requests, by month, net generation (MWh), freshwater input (m³), township water, and SWC including/excluding township.

**Critical metric limitation:** CEA's SWC is a freshwater-input intensity, not automatically a thermodynamic consumptive-use factor. The water balance records discharges and losses separately. It must therefore be stored as a distinct `freshwater_input` or `withdrawal/input` metric unless the plant's audited balance demonstrates which portion is consumed. Do not relabel SWC as `consumption` merely because the SOP uses the term “Specific Water Consumption.”

### Scope limitations

- The November 2026 SOP applies to coal/lignite thermal power plants and excludes plants located on the coast and using seawater for cooling.
- It does not provide a national all-generation factor; it supplies a method and reporting structure.
- The SWC norms of 3.0 or 3.5 m³/MWh are regulatory ceilings, not observed plant means and not a grid-average factor.
- Plant-level reports may be self-reported; the SOP calls for water audits, metering checks, and verification. Provenance and audit status must be retained for each row.
- CEA's Annual Report confirms that monthly plant-wise SWC reporting exists from June 2022, but this review has not yet retrieved a complete machine-readable plant/month series. The public SOP is a template/method source, not the missing observation dataset.

### Implications for this project

1. Add `freshwater_input` as a separate water metric in the evidence schema; do not force CEA SWC into the existing `consumption` or `withdrawal` categories without a documented boundary mapping.
2. Use CEA monthly observations only after retrieving the actual plant/month report and matching the same plant/month net generation denominator.
3. Prefer plant-specific, audited SWC rows for an India thermal-generation scenario; do not use regulatory ceilings as central estimates.
4. Keep the generation-weighted factor separate from the grid-mix weighting step. To obtain a national/grid scenario, combine only compatible plant/technology values and same-period **generation** shares, not installed capacity.
5. Treat the resulting thermal-only estimate as a partial grid component. Hydro, nuclear, solar, wind, imports, and other generation sources need separate compatible evidence before a whole-grid factor can be calculated.
6. Keep Chennai/Hyderabad city-centroid proxies distinct from the national Indian grid scenario. A national factor is not a site-specific marginal factor.

### Status after this source audit

- Official method and definitions: verified.
- CEA monthly plant-wise SWC publication history: verified from the CEA Annual Report.
- Actual plant/month SWC observations extracted and checksummed: **not yet done**.
- Matching plant/month net-generation denominators joined: **not yet done**.
- National grid-mix weights and non-thermal technology factors joined: **not yet done**.
- Site-specific electricity-related water factor: **not available**.
- Geographic validation gate: **remains false**.

No numeric factor was inferred or fabricated from the regulatory limits or blank reporting templates. This addendum improves the India source pathway but does not complete geographic integration or support a site-level net-water result.

### Publication-access cross-check (2026-11-27)

The CEA Clean Energy and Energy Transition division page was opened directly. It lists the annual water-consumption spreadsheet and monthly Format 60 spreadsheet templates, but its report-list sections currently display **“No Reports Found”**; it does not expose the plant/month SWC report series from that page. This creates an access discrepancy with the CEA Annual Report's statement that monthly plant-wise SWC reports have been published since June 2022.

- Direct page inspected: https://www.cea.nic.in/divisionPage/510?lang=en
- The page exposes the blank annual water-consumption and monthly Format 60 templates, not populated plant observations.
- The separate monthly report landing page indexed by search engines could not be opened reliably during this audit and did not provide a verifiable downloadable report set.

**Disposition:** do not mark plant/month SWC data as publicly retrieved or accessible. The next step is to locate the actual CEA report archive or request the relevant monthly report dataset from CEA; until then, the CEA SOP and Annual Report establish the method and claimed publication history only. The factor ledger remains empty.

### Historical Tamil Nadu plant-level SWC evidence and source-quality review (2026-11-27)

A second route is available through the Centre for Science and Environment (CSE) 2021 report, **_Water-Inefficient Power: Implementing Water Norms and Zero Discharge in India’s Coal-Power Fleet_**:

- Full report: https://www.cseindia.org/content/downloadreports/10856
- CSE key findings: https://cdn.cseindia.org/userfiles/water-inefficient-power.pdf
- CSE describes its SWC compilation as plant-reported values from 2017–18, 2018–19, and 2019–20, averaged where all three years were available; if only one year was available, that year's value was used.
- CSE compiled the data from annual environmental statements, field surveys, plant questionnaires, and RTIs to State Pollution Control Boards. It explicitly warns that reporting formats were inconsistent, some values were under-reported or misrepresented, and third-party verification was absent.

CSE Table 3.8 reports the following historical Tamil Nadu values (m³/MWh):

| Plant | Region | Cooling / source | Reported average SWC | CSE status |
|---|---|---|---:|---|
| Neyveli TPS I (Extension), 420 MW | Cuddalore | Cooling tower / freshwater | <3.5 | Complying |
| Neyveli TPS-II, 1,470 MW | Cuddalore | Cooling tower / freshwater | 4.39 | Non-complying |
| Neyveli TPS-II (Extension), 500 MW | Cuddalore | Cooling tower / freshwater | 5.25 | Non-complying |
| TAQA Neyveli, 250 MW | Cuddalore | Cooling tower / freshwater | 3.6 | Non-complying |
| Mettur TPS, 840 MW | Salem | Cooling tower / freshwater | 5.9 | Non-complying |
| Mettur TPS, 600 MW | Salem | Cooling tower / freshwater | 2.56 | Complying |

CSE reports that about 12.16 GW of Tamil Nadu thermal capacity was surveyed, with 67% (about 8.08 GW) seawater-based or air-cooled and exempt from the freshwater SWC norms. The remaining freshwater-based capacity is not representative of the entire Tamil Nadu grid. CSE also notes that a significant share of the non-complying capacity was in the Cuddalore region.

**Evidence classification:** these are historical, secondary-source compiled, self-reported SWC observations, not current audited plant factors, not grid-average factors, and not independently verified consumptive-use factors. Retain them only as historical plant-level freshwater-SWC screening evidence. Do not average them into a Tamil Nadu or Indian grid factor; do not assign them to Chennai/Hyderabad; do not treat CSE's regulatory norm values as measured data.

### CAG performance-audit cross-check of existing Neyveli thermal stations (2025)

The Comptroller and Auditor General of India (CAG) Report No. 35 of 2025, section 3.13 (printed page 45), provides annual SWC values for **TPS-IE, TPS-II, and TPS-IIE** over FY 2017–18 to FY 2022–23. The performance audit explicitly states that its thermal-station review covered TPS-IE, TPS-II, and TPS-II Expansion; **it did not cover NNTPS**.

CAG's footnotes report the following values (m³/MWh, numerically equal to L/kWh):

| Station | 2017–18 | 2018–19 | 2019–20 | 2020–21 | 2021–22 | 2022–23 |
|---|---:|---:|---:|---:|---:|---:|
| TPS-IE | 3.45 | 3.44 | 2.97 | 2.78 | 2.94 | 2.89 |
| TPS-II | 5.17 | 5.51 | 5.15 | 5.05 | 4.90 | 4.97 |
| TPS-IIE | 4.02 | 3.32 | 3.98 | 4.00 | 3.90 | 3.97 |
| CEA/2015 norm cited by CAG | 3.50 | 3.50 | 3.50 | 3.50 | 3.50 | 3.50 |

CAG reports that TPS-II and TPS-IIE were above the 3.5 m³/MWh norm, that TPS-II's water-treatment plant was commissioned in December 2022, and that TPS-II remained above the norm after installation. It also states that no corresponding treatment-plant contract had been awarded for TPS-IIE. **Internal source inconsistency:** footnote 57 gives TPS-IIE as 3.32 m³/MWh in 2018–19, below the 3.50 norm in footnote 58, despite the narrative's broad statement that TPS-IIE SWC was higher. Do not classify that individual year as non-compliant without clarification.

For a like-for-like three-year comparison over FY 2017–18 to FY 2019–20 (the period CSE says it averages), the CAG values have arithmetic means of **5.28 m³/MWh for TPS-II** and **3.77 m³/MWh for TPS-IIE**. CSE Table 3.8 reports 4.39 and 5.25 m³/MWh respectively. The CAG-minus-CSE differences are therefore **+0.89 m³/MWh for TPS-II** and **−1.48 m³/MWh for TPS-IIE**. These are material and unresolved. The sources may use different station boundaries, data submissions, or calculation methods; **do not pool or average CSE and CAG values**.

**Evidence classification:** CAG provides a stronger official historical regulatory-SWC record than the CSE secondary compilation, but the values are still management-reported observations reproduced in a performance audit. The report does not provide the water-source composition, withdrawal/return-flow balance, or consumptive fraction for each station. The 2015-rule SWC values therefore cannot be assumed to equal the CEA 2026 FW1+FW2 freshwater-input metric or a blue-water consumption factor. Retain them as historical station-level regulatory-SWC evidence only. They do not apply to NNTPS, which is a separate 1,000 MW station and was outside the CAG review scope.

Source: https://cag.gov.in/uploads/download_audit_report/2026/CAG---NLC-India-Limited-2025-English-FINAL-SIGNATORY-10-12-2025-0698c6a3b5d7e42.69686670.pdf

### New Neyveli Thermal Power Station environmental-statement cross-check

An official environmental-compliance PDF hosted by the Ministry of Environment, Forest and Climate Change includes the New Neyveli Thermal Power Station (NNTPS) environmental statement for FY 2021–22:

- MoEFCC-certified compliance report and embedded FY 2021–22 environmental statement (printed pages 35–36): https://environmentclearance.nic.in/writereaddata/Monitoring/56803999_NLC%20Thermal%20Power%20plant%202023_compressed.pdf
- NLC India Integrated Annual Report FY 2021–22, physical performance table (printed page 17; NNTPS gross/net generation): https://nsearchives.nseindia.com/corporate/NLCINDIA_07092022181900_AnnualReport22.pdf
- The report identifies the 1,000 MW NNTPS (2 × 500 MW), with units commissioned on 28 December 2019 and 10 February 2021.
- The statement lists process water at 32,712.46 m³/day, cooling water at 1,165.15 m³/day, and domestic water at 5,597.12 m³/day. It reports 7,984 m³/day of effluent discharge.
- It separately reports process water consumption per unit of electrical power as 0.069 L/kWh for FY 2021–22 (0.111 L/kWh for FY 2020–21).
- A separate environmental-clearance compliance table earlier in the same PDF (not the FY 2021–22 statement table itself) says groundwater is not extracted and that mine water stored in a lake behind Thermal Station-I Expansion is used for NNTPS operations. The FY 2021–22 statement table does not break out its process-water volume by source category.

**Annual-generation and period reconciliation:** NLC India's FY 2021–22 Integrated Annual Report reports NNTPS net generation of 5,758.70 MU for the same financial year, equivalent to an annual-average 15.777 million kWh/day. The reported process-water volume has two very different interpretations:

| Interpretation of the reported 32,712.46 m³ | Implied process-water intensity | Comparison with reported 0.069 L/kWh |
|---|---:|---:|
| Literal table label: 32,712.46 m³/day | **2.073 L/kWh** | 30.05× |
| Hypothesis: 32,712.46 m³ per 30-day month (1,090.42 m³/day) | **0.06911 L/kWh** | 1.0016× (0.16% higher) |
| Annualize 12 monthly totals against annual net generation | **0.06817 L/kWh** | 1.2% lower |

The 30-day-total interpretation nearly reproduces the stated 0.069 L/kWh. This is a strong clue that the value may be a monthly total mislabeled as m³/day, or that the volume and intensity use different source/metric boundaries. It is **not confirmation**: the source table explicitly labels the values m³/day, and the document does not define the period basis or the source classes included in the 0.069 L/kWh numerator. The report's separate compliance section says mine water is used, while the FY 2021–22 statement table provides no source-wise volume split. The discrepancy could therefore be a period-label error, a freshwater/non-fresh source-boundary difference, or another accounting mismatch.

The nameplate-only check gives a lower-bound ratio of 1.363 L/kWh if 32,712.46 m³ is truly an average daily volume and the 1,000 MW plant runs at full output. Do not silently relabel the source data or promote either interpretation to a factor. The operator must confirm whether 32,712.46 is a daily rate or monthly total, the period represented by the figure, the source categories included, and the denominator used for 0.069 L/kWh.

**Water-source boundary:** the compliance section says mine water is used, but the FY 2021–22 statement does not give a source-wise volume split. Under the November 2026 CEA SOP, mine water received from another source is categorized as NFW3 (other external non-fresh input), which is recorded but excluded from CEA SWC. Therefore, the 32,712.46 m³/day process-water volume cannot be mapped directly to CEA's FW1+FW2 freshwater-input metric. The 0.069 L/kWh value is not accepted into the factor ledger.

### Geographic-source disposition after historical evidence review

- CSE 2021 supplies a useful historical Tamil Nadu plant-level SWC screening table, with material self-reporting and verification limitations.
- The NNTPS FY 2021–22 statement provides official water-volume and intensity values but contains a large internal consistency discrepancy and identifies mine water as an input source.
- Neither source yields a defensible, current, whole-grid electricity-water factor.
- Do not populate the factor ledger, calculate a site-level net-water result, or change the geographic validation gate from these sources.
- A future usable row requires a consistent period, a defined freshwater/withdrawal/consumption metric, plant-level generation denominator, cooling/source classification, and independent or audited water balance.
