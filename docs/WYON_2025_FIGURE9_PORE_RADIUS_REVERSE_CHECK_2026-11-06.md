# Wyon Figure 9: Pore-Radius Reverse-Consistency Check

**Date:** 2026-11-06  
**Status:** Strong diagnostic hypothesis; not a raw-data reproduction.

## Finding

The coupled local model's **0.22 µm radius** run is visually much closer to the dashed model series in Wyon Figure 9 than the **0.11 µm radius** run. This suggests Wyon's Figure 9 calculation may have used the tabulated 0.22 µm pore-size value directly as the radius in Eq. (14).

That interpretation conflicts with a closely matching PVDF/GVHP experimental setup in Srisurichan et al. (2006), which explicitly reports an **average pore radius of 0.11 µm** for a 0.22 µm pore-size membrane. The result is a likely source-parameter convention mismatch worth resolving before claiming a source-matched reproduction.

## Matched local calculation

The two runs use the same Wyon initial PVDF configuration and operating assumptions:

- PVDF membrane, thickness 126 µm, porosity 0.75, membrane conductivity 0.041 W/(m K)
- Tabulated pore size 0.22 µm; tested radius interpretations 0.11 and 0.22 µm
- Channel hydraulic diameter 0.003 m and length 0.1 m
- Feed/permeate velocities 1.85/2.92 m/s
- Feed bulk temperatures 40, 50, 60, 70°C; permeate bulk temperature 20°C
- Representative feed salinity 38 g/kg, taken from Wyon's Barcelona case study; the exact Figure 9 validation salinity remains unconfirmed
- Total pore pressure 100 kPa
- Wyon Appendix A properties and the coupled mean-bulk/interface-temperature iteration

| Feed bulk (°C) | Heat flux, r = 0.11 µm (kW/m²) | Heat flux, r = 0.22 µm (kW/m²) | Increase when radius doubles |
|---:|---:|---:|---:|
| 40 | 10.300 | 11.235 | 9.1% |
| 50 | 17.548 | 19.458 | 10.9% |
| 60 | 27.056 | 30.497 | 12.7% |
| 70 | 39.710 | 45.469 | 14.5% |

The 0.22 µm-radius series lies near the dashed model curve's visual range in Figure 9 (approximately 11–12, 19–20, 30–31, and 45–46 kW/m²). The 0.11 µm-radius series is systematically lower, increasingly so at higher feed temperatures.

This is a **visual consistency check**, not a digitized raw-data comparison. Wyon does not publish the numerical Figure 9 data points in the thesis, and the underlying reference data/code have not yet been recovered.

## Independent membrane evidence

Srisurichan, Jiraratananon & Fane (2006) describe a flat-sheet PVDF membrane (GVHP, Millipore) and state that the supplier-provided properties were:

- porosity 0.75;
- average pore radius 0.11 µm;
- thickness 125 µm;
- membrane thermal conductivity 0.041 W/(m K).

Their turbulent module also reports effective area 3.0 × 10⁻⁴ m² and hydraulic diameter 0.003 m. These values closely match Wyon Table 6, which lists a 0.22 µm pore size, 75% porosity, 126 µm thickness, 0.041 W/(m K), 0.0003 m² area, and 0.003 m hydraulic diameter.

The match strongly supports the conventional interpretation (0.22\ \mu m) pore size → (0.11\ \mu m) radius for this membrane family. However, Srisurichan et al. (2006) is a corroborating related experiment, not one of Wyon's cited validation references [55] or [56]. Wyon cites Termpiyakul et al. (2005) and Phattaranawik et al. (2003).

## What the cited Termpiyakul study establishes

The accessible ScienceDirect abstract for Wyon reference [55] confirms a flat-sheet PVDF membrane with nominal pore size 0.22 µm, feed NaCl concentrations of 5,000–35,000 mg/L plus brackish/seawater cases, feed temperatures of 40–70°C, feed crossflow velocities of 1.85–3.7 m/s, and permeate at 20°C and 2.92 m/s. It does not identify which feed concentration was used for the particular Figure 9 comparison.

A secondary accessible abstract/conclusion transcription reports an empirical membrane-distillation coefficient of 0.0024 kg/(m² h Pa) from pure-water flux data and 0.0021 kg/(m² h Pa) from the 35,000 mg/L data, a difference of about 12%. This coefficient is not dimensionally or conceptually interchangeable with Wyon's mechanistic Eq. (14) coefficient in kg/(m² s Pa); it is evidence that the effective mass-transfer response can depend on feed concentration, not a parameter to substitute into the current solver.

## Interpretation and limits

1. The Figure 9 dashed model curve is numerically more consistent with the 0.22 µm-radius case. A plausible explanation is that the model used nominal pore size as radius in Eq. (14).
2. The independent supplier-property report supports 0.11 µm as the physical average radius for a closely matching PVDF/GVHP membrane.
3. If Wyon used 0.22 µm as the radius, that choice raises the local model heat flux by about 9–15% and mass flux by about 23–24% relative to the 0.11 µm case.
4. Correcting the radius to 0.11 µm would lower the model heat flux further. It would not automatically remove Wyon's published Figure 9 discrepancies; at 50–70°C it could make the model underprediction larger.
5. The 38 g/kg salinity is a representative case-study input, not a verified Figure 9 experimental condition. The original Termpiyakul data include several feed concentrations, so the precise validation condition remains unresolved.
6. No fitting was performed. The pore radius was not selected to minimize Figure 9 error.

## Required next evidence

- Recover the full Termpiyakul et al. (2005) paper and establish the exact PVDF membrane pore-radius convention and Figure 9 operating concentration.
- Determine whether Wyon's own calculation used 0.22 µm or 0.11 µm as (r).
- Recover the original numerical Figure 9 values or digitize the figure with an explicit uncertainty estimate before reporting benchmark error.
- Keep 0.11 µm as the physically better-supported provisional radius unless primary evidence from Wyon's cited experiment contradicts it.

## Sources

Annie Wyon (2025), *Desalination utilizing data centre waste heat: A techno-economic study*, Lund University, report LUTFD2/TFEM--25/5229--SE, Table 6, Section 3.2.2, Eq. (14), Figure 9.  
Official PDF: https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf

S. Srisurichan, R. Jiraratananon & A.G. Fane (2006), “Mass transfer mechanisms and transport resistances in direct contact membrane distillation process,” *Journal of Membrane Science* 277, 186–194, DOI 10.1016/j.memsci.2005.10.028.  
Accessible full text: https://digital.library.tu.ac.th/tu_dc/digital/api/DownloadDigitalFile/dowload/76312

P. Termpiyakul, R. Jiraratananon & S. Srisurichan (2005), “Heat and mass transfer characteristics of a direct contact membrane distillation process for desalination,” *Desalination* 177, 133–141, DOI 10.1016/j.desal.2004.11.019. Abstract: https://www.sciencedirect.com/science/article/abs/pii/S0011916405001864

Secondary accessible abstract/conclusion transcription of the reported pure-water and 35,000 mg/L empirical membrane-distillation coefficients: https://www.lenntech.com/abstracts/1434/heat-and-mass-transfer-characteristics-of-a-direct-contact-membrane-distillation-process.html.
