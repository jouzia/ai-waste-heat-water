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
4. **CEA 2026 thermal-plant water-audit SOP**:
   - https://www.cea.nic.in/api/dashboardReports/view-pdf/en/d88a8d91-e888-42f9-879f-6af6b5788f98
   - Provides the reporting/accounting method and a blank monthly SWC template, not the historical plant/month observation series.

## Finding

The existence and intended content of the monthly SWC reports are confirmed by CEA's own Annual Report. However, the two public CEA navigation routes inspected do not expose the populated report series. The division page supplies blank templates, while the site-wide archive does not list the environmental reports among its monthly reports.

This is an **access and publication-indexing gap**, not evidence that the reports were never produced. Do not describe the plant/month data as retrieved, machine-readable, or publicly accessible until an actual report file is obtained and checked.

## Official data-request contact

The CEA division page identifies the Divisional Head (Chief Engineer) for Clean Energy and Energy Transition as **Ms. Manjari Chaturvedi** and lists the official email in obfuscated form:

- Published address: `manjari[dot]chaturvedi[at]gov[dot]in`
- Normalized address: `manjari.chaturvedi@gov.in`

The division's stated responsibilities include compilation and analysis of monthly environmental data for the power sector. No email has been sent as part of this audit.

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
- Is net or gross generation used in the 0.069 L/kWh denominator, and is it the same FY/month period as the water volume?
- Can CEA provide the matching FY 2020–21 and FY 2021–22 NNTPS monthly water-source split and net-generation observations?

Do not silently reinterpret the m³/day label or enter either 2.073 or 0.069 L/kWh into the factor ledger before the period, source classes, and denominator are confirmed.
