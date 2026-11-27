# NNTPS FY2021-22 Site Water Statement — Source-Consistency Audit (2026-11-27)

## Source and scope

The Government of India's Ministry of Environment, Forest and Climate Change (MoEFCC) monitoring report for the Neyveli New Thermal Power Project is dated 28 April 2023 and embeds NLC India's Environmental Statement for New Neyveli Thermal Power Station (NNTPS) for the financial year ending 31 March 2022.

- Official PDF: https://environmentclearance.nic.in/writereaddata/Monitoring/56803999_NLC%20Thermal%20Power%20plant%202023_compressed.pdf
- Monitoring report identifies NNTPS as a 1,000 MW (2 × 500 MW) lignite-based station in Cuddalore District, Tamil Nadu.
- Unit I COD: 28 December 2019; Unit II COD: 10 February 2021.
- NLC environmental statement letter: GM/CEC/E.S. 21-22/43/2022, dated 28 September 2022.
- The embedded statement appears at PDF pages 35–37 (printed page labels 35–37).

This is a primary site-submitted environmental statement reproduced in an official government monitoring report. It is not an independently audited plant water balance.

## Transcribed values

| Item | Reported value | Source locator |
|---|---:|---|
| Installed capacity | 1,000 MW (2 × 500 MW) | PDF p. 35, Part A |
| Unit I COD | 28 Dec 2019 | PDF p. 35, Part A |
| Unit II COD | 10 Feb 2021 | PDF p. 35, Part A |
| Process water | 32,712.46 m³/day | PDF p. 35, Part B |
| Cooling water | 1,165.15 m³/day | PDF p. 35, Part B |
| Domestic water | 5,597.12 m³/day | PDF p. 35, Part B |
| Process-water intensity, FY2020-21 | 0.111 L/kWh | PDF p. 35, Part B |
| Process-water intensity, FY2021-22 | 0.069 L/kWh | PDF p. 35, Part B |
| Effluent | 7,984 m³/day | PDF p. 36, Part C |

The monitoring report further records that the station uses mine water stored in a lake, does not extract groundwater for plant operation, adopts closed-cycle cooling with a cooling-cycle concentration (COC) of 5, and uses treated effluent for dust suppression and greenbelt development (PDF pp. 2–4 of the monitoring report's compliance section).

## Internal consistency check

The reported process-water quantity and specific intensity are incompatible if they describe the same NNTPS boundary and period.

Nameplate upper-bound generation:

[
1000 mathrm{MW}	imes24 mathrm{h}
=24{,}000 mathrm{MWh/day}
=24{,}000{,}000 mathrm{kWh/day}
]

Minimum process-water intensity implied by the reported daily process flow, even at continuous 100% nameplate output:

[
rac{32{,}712.46 mathrm{m^3/day}	imes1000 mathrm{L/m^3}}
{24{,}000{,}000 mathrm{kWh/day}}
=1.3630 mathrm{L/kWh}
]

The statement instead prints **0.069 L/kWh**. At the same maximum generation, that printed intensity would correspond to only 1,656 m³/day of process water, about 19.75 times lower than the reported 32,712.46 m³/day.

Conversely, applying 0.069 L/kWh to the reported process volume implies:

[
rac{32{,}712.46	imes1000}{0.069}
=474{,}093{,}623 mathrm{kWh/day}
approx474{,}094 mathrm{MWh/day}
]

That corresponds to an average output of approximately 19,754 MW, or 19.75 times the station's 1,000 MW nameplate capacity.

The discrepancy is not resolved by the source. Potential explanations include a unit/decimal transcription error, different reporting boundaries, or a distinction between gross process circulation and the intensity denominator. None is assumed here.

## Water-accounting limitations

- The statement labels the daily figures as water consumption but does not supply a matched electricity-generation denominator.
- It does not define whether process/cooling quantities represent fresh intake, gross circulation, make-up, or another accounting boundary.
- Effluent of 7,984 m³/day and statements about reuse do not establish the net consumptive fraction.
- The report does not provide a complete source-wise site water balance, nor a verified split between freshwater and mine-water sources for each reported quantity.
- The 0.069 L/kWh value must not be silently corrected to 0.69, 1.36, or another value.

## Required resolution before quantitative use

1. Obtain the underlying NLC Form-V environmental statement or written clarification from NLC's Corporate Environment Cell / NNTPS.
2. Confirm the unit printed in the intensity table and the exact numerator boundary (process only, freshwater only, or another measure).
3. Obtain FY2021-22 gross/net generation and operating days for NNTPS Units I and II, with the same reporting boundary and period as the water data.
4. Reconcile daily process, cooling, domestic, make-up, recycle, effluent, and source-water quantities.
5. Only after reconciliation, calculate a plant-year withdrawal or consumption factor, with the numerator/denominator definitions and uncertainty documented.

## Scientific disposition

Register this as a site-specific primary-source candidate, but quarantine both the reported 0.069 L/kWh intensity and the daily flow values from model calibration or grid-factor calculations. It does not establish a validated NNTPS water-intensity factor, net freshwater consumption, or a Tamil Nadu grid-average factor. No validation gate changes.
