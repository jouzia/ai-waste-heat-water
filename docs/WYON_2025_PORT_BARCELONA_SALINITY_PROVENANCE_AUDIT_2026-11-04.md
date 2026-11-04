# Wyon (2025): Port of Barcelona salinity provenance check

**Date:** 2026-11-04  
**Scope:** Documentation-only source check. No model code or scenario outputs changed.

## Finding

Wyon's Table 2 gives Barcelona seawater salinity as approximately **38 g/kg**, citing the Port of Barcelona water-quality webpage [48], and says the value is converted from Practical Salinity using Sharqawy et al. (2010) [47]. Wyon does not identify the sampling station, sampling year, or unrounded value used for the DCMD feed.

The Port of Barcelona's official *Water and sediment quality of the Port of Barcelona — Summary 2020* reports station-average salinity in PSU (Table 9). Applying Sharqawy Eq. 3, S_R = 1.00472 S_P, yields:

| Station | Water area | 2020 mean S_P (PSU) | Converted S_R (g/kg) |
|---|---|---:|---:|
| MA20B | Open waters | 37.743 | 37.921 |
| MA36A | Sheltered/internal | 37.548 | 37.725 |
| MA36B1 | Sheltered/internal | 37.569 | 37.746 |
| MA36B2 | Sheltered/internal | 37.820 | 37.999 |
| MA36C | Sheltered/internal | 37.617 | 37.795 |
| MA36D | Sheltered/internal | 37.563 | 37.740 |

All six converted values round to **38 g/kg** at the integer precision used by Wyon. The nominal 38 g/kg is therefore plausible and consistent with the official 2020 station averages. It is not a uniquely identified station-specific input.

The report identifies MA20B as the open-water station and MA36A–MA36D as sheltered/internal stations. This matters because Wyon models a seawater feed but does not specify whether its feed is represented by open-water or internal-port salinity. For a coastal intake, MA20B is a plausible candidate, but it must not be silently assumed.

## Nayar 2016 vapour-pressure sensitivity at the observed salinity values

Using Nayar et al. (2016) Eq. 5, with Reference Salinity in g/kg:

~~~text
p_v,sw / p_v,w = exp(-4.58180e-4*S - 2.04430e-6*S^2)
~~~

The corresponding same-temperature vapour-pressure depressions are:
- MA20B open water, 37.921 g/kg: **2.0109%**
- MA36A–MA36D internal waters, 37.725–37.999 g/kg: **1.9992–2.0156%**

This narrow station range changes the same-temperature pressure-depression estimate by only about 0.016 percentage points. It does not establish the impact on DCMD flux.

The earlier illustrative calculation that treated 38 as a raw Practical Salinity value (giving 38.179 g/kg) is only a convention example, not a recovered Port measurement. The actual 2020 open-water station mean is 37.743 PSU, converting to 37.921 g/kg. Wyon's rounded 38 g/kg remains appropriate as the nominal reproduction input until the exact historical chart observation or station selection is recovered.

## Source trace and limitations

1. Wyon, A. (2025), Table 2 and references [47]–[49]: [official Lund thesis PDF](https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf).
2. Port de Barcelona, *Water quality and sediments* page, cited by Wyon as [48]. The page identifies a salinity chart covering 2000–2020, measured in PSU: [official page](https://www.portdebarcelona.cat/en/sustainability/environmental-sustainability/environmental-actions/water/water-quality-and-sediments).
3. Port de Barcelona, *Water and sediment quality of the Port of Barcelona — Summary 2020*, cited by Wyon as [49]. Table 9 gives the station-average PSU values above; sampling stations and campaigns are described in the report: [official PDF](https://www.portdebarcelona.cat/sites/default/files/content/file/2021/09/28/1/valoracion-aguas_-2020.pdf).
4. Sharqawy, M.H., Lienhard V, J.H., and Zubair, S.M. (2010), Eq. 3: S_R = 1.00472 S_P. [DOI: 10.5004/dwt.2010.1079](https://doi.org/10.5004/dwt.2010.1079).
5. Nayar, K.G. et al. (2016), Eq. 5: natural-seawater vapour-pressure correlation. [DOI: 10.1016/j.desal.2016.02.024](https://doi.org/10.1016/j.desal.2016.02.024).

**Not established:** the exact chart point, station, or date Wyon used for the 38 g/kg input; a time-resolved intake salinity series for the thesis's case study; or any resulting change in DCMD mass flux, water production, or cost.
