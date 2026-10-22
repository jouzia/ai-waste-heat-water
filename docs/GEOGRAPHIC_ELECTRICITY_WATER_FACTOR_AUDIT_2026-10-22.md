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
- `transformation`, generation-mix weights, conversion arithmetic, and uncertainty
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
W_{electricity} = E_{incremental}, C_{grid}
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
