# Wyon 2025 Baseline: Feed-Salinity Sensitivity Audit

**Date:** 2026-11-06  
**Status:** Source-faithful numerical sensitivity check; not a salinity-corrected physical model.

## Question

Termpiyakul et al. (2005), cited by Wyon as reference [55], tested feed NaCl concentrations from 5,000 to 35,000 mg/L and reports that flux decreased with increasing feed concentration. Its accessible conclusion reports an empirical membrane-distillation coefficient of 0.0024 kg/(m² h Pa) from pure-water data and 0.0021 kg/(m² h Pa) from 35,000 mg/L data, approximately 12% lower.

Wyon's Appendix A Eq. (A9), however, is a **pure-water vapour-pressure correlation**, and the thesis applies it to both the seawater feed and pure-water permeate. This audit measures how much the implemented source-faithful baseline responds to feed salinity through its fluid-property correlations alone.

## Method

The coupled surface solver was evaluated at feed temperatures 40, 50, 60, and 70°C, permeate temperature 20°C, and the initial PVDF geometry:

- PVDF, thickness 126 µm, porosity 0.75, membrane conductivity 0.041 W/(m K);
- pore radius 0.11 µm, provisionally supported by the matching PVDF/GVHP supplier specification;
- channel hydraulic diameter 0.003 m, length 0.1 m;
- feed/permeate velocities 1.85/2.92 m/s;
- total pore pressure 100 kPa.

Only feed reference salinity was changed, from 5 to 35 g/kg. These are approximate mass-based equivalents for the 5,000–35,000 mg/L NaCl range in Termpiyakul et al.; they are not an exact density conversion of the paper's mg/L values.

## Results

| Feed bulk (°C) | Heat flux at 5 g/kg (kW/m²) | Heat flux at 35 g/kg (kW/m²) | Heat-flux change | Mass flux at 5 g/kg (kg/m² h) | Mass flux at 35 g/kg (kg/m² h) | Mass-flux change |
|---:|---:|---:|---:|---:|---:|---:|
| 40 | 10.316 | 10.301 | −0.14% | 6.055 | 6.044 | −0.18% |
| 50 | 17.583 | 17.552 | −0.18% | 12.096 | 12.068 | −0.23% |
| 60 | 27.122 | 27.062 | −0.22% | 21.381 | 21.319 | −0.29% |
| 70 | 39.833 | 39.722 | −0.28% | 35.173 | 35.047 | −0.36% |

Across the tested range, changing feed salinity from 5 to 35 g/kg changes local heat flux by only 0.14–0.28% and mass flux by 0.18–0.36%.

## Interpretation

1. The implemented Wyon baseline has very weak salinity sensitivity because salinity affects the channel properties, but the vapour-pressure driving force is still calculated from pure-water saturation pressure on both interfaces.
2. Termpiyakul et al. report a roughly 12% difference between empirical coefficients obtained from pure-water and 35,000 mg/L data. This is not directly comparable to the current model's 0.2–0.4% sensitivity: the empirical coefficient is a different quantity and the paper attributes high-concentration deviations to concentration polarization and reduced water-vapour pressure.
3. The result identifies a **model-form limitation in the Wyon source baseline**, not a code defect in the source-faithful transcription. Adding water-activity or concentration-polarization corrections would be a separate model variant and must not be silently mixed into the baseline.
4. The 38 g/kg Barcelona case-study salinity is therefore not a decisive input for reproducing Figure 9 within this pure-water vapour-pressure baseline. The exact validation salinity still matters for a physically salinity-aware model and for interpreting the Termpiyakul data.

## Reproduction

Run:

```bash
pytest -q tests/test_wyon_2025_coupled_channel_surface.py
```

The parameterized regression `test_wyon_pure_water_vapour_baseline_has_weak_salinity_sensitivity` checks all four feed temperatures and both salinity endpoints.

## Sources

Annie Wyon (2025), *Desalination utilizing data centre waste heat: A techno-economic study*, Lund University, Appendix A Eq. (A9), Section 3.2.2, and Figure 9.  
PDF: https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf

P. Termpiyakul, R. Jiraratananon & S. Srisurichan (2005), “Heat and mass transfer characteristics of a direct contact membrane distillation process for desalination,” *Desalination* 177, 133–141, DOI 10.1016/j.desal.2004.11.019.  
ScienceDirect abstract: https://www.sciencedirect.com/science/article/abs/pii/S0011916405001864

Secondary accessible abstract/conclusion transcription of the pure-water and 35,000 mg/L empirical coefficients: https://www.lenntech.com/abstracts/1434/heat-and-mass-transfer-characteristics-of-a-direct-contact-membrane-distillation-process.html.
