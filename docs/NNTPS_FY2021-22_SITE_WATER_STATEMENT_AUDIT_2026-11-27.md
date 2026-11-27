# NNTPS FY2021-22 Site Water Statement — Reconciliation Audit (2026-11-27)

## Source and scope

The official MoEFCC monitoring report dated 28 April 2023 embeds NLC India's Environmental Statement for New Neyveli Thermal Power Station (NNTPS), FY ending 31 March 2022. The NLC letter is GM/CEC/E.S. 21-22/43/2022, dated 28 September 2022.

- Environmental statement / MoEFCC report: https://environmentclearance.nic.in/writereaddata/Monitoring/56803999_NLC%20Thermal%20Power%20plant%202023_compressed.pdf
- NLC India Integrated Annual Report FY2021-22: https://nsearchives.nseindia.com/corporate/NLCINDIA_07092022181900_AnnualReport22.pdf
- Rajya Sabha Unstarred Question No. 480 (6 February 2024), Annexure II: https://sansad.in/getFile/annex/263/AU480.pdf?source=pqars
- Existing reproducible calculation: `scripts/reconcile_nntps_water_intensity.py`
- Regression tests: `tests/test_nntps_water_intensity_reconciliation.py`

The NNTPS station is reported as 1,000 MW (2 × 500 MW). Unit I COD was 28 December 2019; Unit II COD was 10 February 2021. The environmental statement is a site-submitted report embedded in a government monitoring document, not an independently audited water balance.

## Transcribed environmental-statement values

| Item | Reported value | Source locator |
|---|---:|---|
| Process water | 32,712.46 m³/day (unit as printed) | PDF p. 35, Part B |
| Cooling water | 1,165.15 m³/day (unit as printed) | PDF p. 35, Part B |
| Domestic water | 5,597.12 m³/day (unit as printed) | PDF p. 35, Part B |
| Process-water intensity, FY2020-21 | 0.111 L/kWh | PDF p. 35, Part B |
| Process-water intensity, FY2021-22 | 0.069 L/kWh | PDF p. 35, Part B |
| Effluent | 7,984 m³/day | PDF p. 36, Part C |

The report's separate environmental-clearance compliance section says mine water stored in a lake is used and groundwater is not extracted for plant operation. The FY2021-22 statement table does not provide a source-wise split of the reported process, cooling, and domestic quantities.

## Generation denominators

NLC India's FY2021-22 annual report gives NNTPS generation as:

| Financial year | Gross generation | Net generation |
|---|---:|---:|
| FY2020-21 | 3,439.17 MU | 3,176.32 MU |
| FY2021-22 | 6,178.74 MU | 5,758.70 MU |

Rajya Sabha Unstarred Question No. 480, Annexure II, independently reports station-wise generation for NEYVELI NEW TPP of 6,177.93 MU in FY2021-22, 7,156.19 MU in FY2022-23, and 5,151.72 MU for FY2023-24 through December 2023. The FY2021-22 parliamentary value is only 0.81 MU below NLC's annual-report gross figure, so it closely corroborates the gross-generation value. The parliamentary annexure does not label its generation as gross or net.

The existing reconciliation script uses the NLC annual-report **net** generation values (3,176.32 and 5,758.70 MU) for the process-intensity comparison. Do not substitute the gross value without explicitly changing the denominator definition.

## Competing interpretations of the 32,712.46 m³ figure

The environmental statement labels 32,712.46 as m³/day. The same report gives 0.069 L/kWh process-water intensity for FY2021-22. The two values are not reconciled in the source. The repository's existing script deliberately tests both interpretations rather than choosing one.

### Interpretation A — literal daily rate

Using FY2021-22 net generation of 5,758.70 MU:

`32,712.46 m³/day × 1,000 L/m³ ÷ (5,758.70 MU × 1,000,000 kWh/MU ÷ 365 days) = 2.07339 L/kWh`

This is about 30.05 times the reported 0.069 L/kWh.

### Interpretation B — 30-day total

If 32,712.46 m³ is instead a 30-day total:

`32,712.46 m³ × 1,000 L/m³ ÷ (5,758.70 MU × 1,000,000 kWh/MU × 30/365) = 0.0691131 L/kWh`

This reproduces the reported 0.069 L/kWh within approximately 0.2%. The reported intensity itself implies a 30-day process volume close to the printed 32,712.46 m³. The prior-year pair also supports this possibility: 0.111 L/kWh and FY2020-21 net generation of 3,176.32 MU imply a monthly process volume of approximately 29,380.96 m³.

The 30-day-total interpretation is therefore a plausible reconciliation, not a verified correction. The report explicitly prints m³/day; no author clarification has been obtained. Do not silently relabel the value as m³/month or replace the source value.

## Water-accounting boundary

- The environmental statement reports mine-water use, but does not provide a source-wise volume split for the FY2021-22 quantities.
- The CEA 2026 thermal-plant water-audit SOP classifies mine water as NFW3; it is not included in the FW1+FW2 external freshwater-input numerator used for CEA specific water consumption.
- The source does not clarify whether the process/cooling/domestic quantities are fresh intake, mine-water intake, gross circulation, make-up, or another boundary.
- Effluent volume and reuse statements do not establish the site's net consumptive fraction.
- The reported process-water intensity is not automatically a freshwater-consumption factor.

## Required resolution before quantitative use

1. Obtain written NLC clarification of whether 32,712.46 m³ is a daily rate or a 30-day/monthly total, and whether the printed unit is correct.
2. Obtain the source-wise split of FW1, FW2, and NFW3 inputs for the same reporting period.
3. Confirm whether the 0.069 L/kWh denominator is net generation, gross generation, or another output measure.
4. Reconcile process, cooling, domestic, make-up, recycle, effluent, and source-water quantities.
5. Only after reconciliation, calculate a plant-year freshwater withdrawal or consumption factor with a clear numerator, denominator, boundary, and uncertainty.

## Scientific disposition

The source pair is valuable site-specific evidence and the 30-day interpretation is strongly supported by numerical consistency, but the printed unit/period and water-source boundary remain unresolved. Both interpretations remain in the reconciliation script; the factor remains excluded pending operator clarification. No model default or validation gate changes.
