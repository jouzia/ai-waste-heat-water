# CEA monthly environmental SWC report access log — 2026-11-27

## Question

Can the plant-wise Monthly Environmental Stack Emission Status Reports, which CEA says include Specific Water Consumption (SWC), be retrieved from the public CEA website?

## Official sources checked

1. **CEA Annual Report 2024–25**, section 2.11.3, page 25:
   - https://www.cea.nic.in/api/dashboardReports/download-pdf/en/f60d07cd-b057-42b7-9da8-19d5d559dc2a
   - CEA states that it collects monthly environmental data from thermal power plants through Format 60 and, from June 2022, has published Monthly Environmental Stack Emission Status Reports with plant-wise PM, SO2, NOx, and Specific Water Consumption details.
2. **CEA Clean Energy and Energy Transition division page**:
   - https://www.cea.nic.in/divisionPage/510?lang=en
   - Lists the blank annual water-consumption spreadsheet and monthly Format 60 spreadsheet.
   - Its report-list sections display “No Reports Found”; no populated plant/month SWC observations are linked from this page.
3. **CEA site-wide archive page**:
   - https://cea.nic.in/archive?lang=en
   - The Monthly Reports list includes Coal Reports, EV/PCS reports, Fuel Reports, and Generation Reports. It does not list the Monthly Environmental Stack Emission Status Reports.
4. **CEA Framework for Water Audit of Thermal Power Plants: Standard Operating Procedure (November 2026 release)**:
   - Current official PDF: https://www.cea.nic.in/api/dashboardReports/view-pdf/en/11d5a51e-44a5-4d66-817a-5a1dd76a786d
   - Key locations: SWC definition/formula p. 3; FW/NFW source classes p. 12 and pp. 15–16; water-balance equation p. 17; SWC diagram p. 18; source-input template p. 20; township inclusion/exclusion p. 23; monthly SWC table p. 28; applicability and interpretation FAQs pp. 31–32.
   - This is the current official method/template, not the historical plant/month observation series. It applies to coal/lignite TPPs; the SOP explicitly excludes gas/combined-cycle plants.

## Finding

The existence and intended content of the monthly SWC reports are confirmed by CEA's own Annual Report. However, the two public CEA navigation routes inspected do not expose the populated report series. The division page supplies blank templates, while the site-wide archive does not list the environmental reports among its monthly reports.

This is an **access and publication-indexing gap**, not evidence that the reports were never produced. Do not describe the plant/month data as retrieved, machine-readable, or publicly accessible until an actual report file is obtained and checked.

## Official data-request contact

The CEA division page identifies the Divisional Head (Chief Engineer) for Clean Energy and Energy Transition as **Ms. Manjari Chaturvedi** and lists the official email in obfuscated form:

- Published address: `manjari[dot]chaturvedi[at]gov[dot]in`
- Normalized address: `manjari.chaturvedi@gov.in`
- CEA Civil Design Division (issuer of the November 2026 water-audit SOP): `cecd-cea@gov.in` (listed on the SOP cover page). This is an additional routing contact for the water-audit method and reporting template; it is not confirmed as the custodian of the monthly environmental report archive.

The CE&ET division's stated responsibilities include compilation and analysis of monthly environmental data for the power sector. No email has been sent as part of this audit.

## Exact data request required

Request the monthly Environmental Stack Emission Status Reports or machine-readable plant/unit-level extract from June 2022 onward, specifically:

- plant and unit identifiers, state, fuel, capacity, and cooling-water source/type;
- reporting month and year;
- net generation (MWh) for the same unit and month;
- freshwater-source inputs and reported SWC (m³/MWh), including the exact numerator and denominator definitions;
- township supply inclusion/exclusion;
- source-water classification (surface water, groundwater, mine water, treated effluent, seawater, recycled water);
- audit/verification status and any missing-data or correction flags;
- report version, publication date, and source file.

If the full series cannot be shared, request the latest available monthly report plus the reports for FY 2023–24 and FY 2024–25, and ask for the official download/archive URL.

## Project disposition

- Do not create synthetic plant/month observations from the blank Format 60 template.
- Do not substitute the 3.0/3.5 m³/MWh regulatory ceilings for observed values.
- The current November 2026 SOP defines SWC as `FW ÷ net generation`, where `FW = FW1 + FW2`: surface water and groundwater inputs only. NFW1 (treated external water), NFW2 (harvested rainwater), NFW3 (other external input such as mine water), and internal recycled/reused water are recorded separately and excluded from SWC.
- The SOP separately reconciles total inflow, process use, outflows, losses, storage changes, and unaccounted water. Therefore, despite its name, CEA SWC is a freshwater-input intensity, not automatically a net consumptive-loss factor.
- The source classification is a reporting boundary, not a chemical-quality or basin-scarcity conclusion: mine water being NFW3 does not prove it has zero freshwater content or zero hydrological impact. The SOP also says saline borewell water remains groundwater/FW2, subject to the plant's EC/CTO.
- Do not equate CEA SWC with consumptive use without the water-balance components.
- Keep the factor ledger empty until source files and matching generation denominators are obtained, checked, and checksummed.
- The geographic validation gate remains false.


## NNTPS FY 2021–22 reconciliation question for the CEA request

The MoEFCC-hosted compliance PDF containing the NNTPS FY 2021–22 environmental statement (printed pages 35–36) labels process water consumption as **32,712.46 m³/day** and reports process-water intensity of **0.069 L/kWh**:
- https://environmentclearance.nic.in/writereaddata/Monitoring/56803999_NLC%20Thermal%20Power%20plant%202023_compressed.pdf

NLC India's FY 2021–22 Annual Report gives NNTPS net generation of **5,758.70 MU** (and 3,176.32 MU in FY 2020–21):
- https://nsearchives.nseindia.com/corporate/NLCINDIA_07092022181900_AnnualReport22.pdf

Using the FY 2021–22 net-generation denominator, the table's literal m³/day interpretation implies about **2.073 L/kWh**. If 32,712.46 m³ is instead a 30-day total, it implies about **0.06911 L/kWh**, within 0.2% of the reported intensity. The reported 0.111 L/kWh for FY 2020–21 implies about 29,381 m³/month when combined with that year's net generation. This is a strong period-label clue, not confirmation: the statement explicitly labels m³/day, and a different source/metric boundary could also explain the difference.

Add these exact questions to the request:
- Is 32,712.46 m³ a daily rate, a monthly total, or another reporting-period aggregate? Please provide the original Format 60 or calculation sheet.
- Does the 0.069 L/kWh numerator include all process-water inputs, or only freshwater (FW1+FW2)? Are mine-water/NFW3 inputs included in the 32,712.46 m³ figure?
- Did the FY 2021–22 statement use the same FW1/FW2/NFW1/NFW2/NFW3 definitions as the November 2026 CEA SOP, or an earlier reporting convention?
- Is mine water chemically fresh, brackish, or otherwise treated, and what is its measured TDS/conductivity? CEA's NFW3 label is a reporting category, not a water-quality result.
- Is net or gross generation used in the 0.069 L/kWh denominator, and is it the same FY/month period as the water volume?
- Can CEA provide the matching FY 2020–21 and FY 2021–22 NNTPS monthly water-source split and net-generation observations?

Do not silently reinterpret the m³/day label or enter either 2.073 or 0.069 L/kWh into the factor ledger before the period, source classes, and denominator are confirmed.

### Official CEA corroboration of the NNTPS FY2021–22 generation denominator

The CEA *Rate of Sale of Power for the Year 2021–22* supplies an independent official denominator:
- The table header defines the generation field as **Net Gen** (Mkw h / MU).
- Row 258, **NEYVELI NEW TPS**, reports installed capacity **1,000 MW** and net generation **5,758.70 MU**.
- Official PDF: https://www.cea.nic.in/api/dashboardReports/view-pdf/en/2e528aa8-4495-4866-bef8-7f4aafe5099c
- The header appears in the introductory table at printed pages 32–33; the NNTPS row is in the Southern Region table on printed page 43. The same 5,758.70 MU value is also listed in NLC's FY2021–22 Annual Report.

Using 5,758.70 MU over 365 days gives average net generation of **15.777 GWh/day**. The NNTPS environmental statement's process-water volume then has two sharply different interpretations:

| Interpretation of 32,712.46 m³ | Implied process-water intensity |
|---|---:|
| Literal **m³/day**, as printed in the statement | **2.07339 L/kWh** |
| **30-day total** mislabeled as m³/day | **0.069113 L/kWh**, which rounds to the reported **0.069 L/kWh** |

The literal-daily interpretation is about **30.05 times** the reported intensity. The monthly-total interpretation reproduces the reported value to its stated three-decimal precision. This is strong evidence for a period/unit-label problem, but it is not proof: the statement explicitly labels the volume m³/day, and a different water-source/metric boundary could also explain the discrepancy.

The current CEA SOP provides a second possible boundary explanation: mine water is NFW3 and excluded from CEA's FW1+FW2 SWC numerator. The NNTPS compliance report states that mine water from the mines is stored in a lake behind TPS-I Expansion and used for plant operation, and that no groundwater is extracted. However, the FY2021–22 environmental statement labels 0.069 as **“process water consumption per unit of product output”**, not as CEA SWC; it does not provide an FW1/FW2/NFW3 split. The November 2026 SOP must not be retroactively assumed to be the reporting method used in FY2021–22.

For context only, adding the statement's process, cooling, and domestic volumes (32,712.46 + 1,165.15 + 5,597.12 = 39,474.73 m³/day) and treating all as daily gives **2.50200 L/kWh**. This is not a validated plant consumption factor because the source classes, reuse, outflows, and reporting-period alignment remain unresolved.

**Disposition:** keep both interpretations provisional and keep the NNTPS factor ledger entry empty. Request the original monthly/annual calculation sheet, source-wise FW1/FW2/NFW1/NFW2/NFW3/RW volumes, the exact averaging period behind 32,712.46, and the net-generation denominator used for 0.069.
