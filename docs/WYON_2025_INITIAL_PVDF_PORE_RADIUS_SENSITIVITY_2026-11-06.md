# Wyon 2025 Initial PVDF Setup: Pore-Radius Interpretation Sensitivity

**Date:** 2026-11-06  
**Status:** Numerical sensitivity audit; not an experimental validation or Figure 9 reproduction.

## Question

Wyon's initial DCMD setup lists a PVDF membrane pore size of 0.22 µm (Table 6, printed p. 15), while the membrane mass-transfer equation (Eq. 14) uses the **average pore radius** (r). The thesis does not explicitly state in Table 6 whether the listed pore-size value is a diameter or a radius.

This matters because the Knudsen contribution to the membrane mass-transfer coefficient is directly proportional to (r). The two plausible interpretations were therefore tested without selecting one as source-correct:

- **Diameter interpretation:** (r = 0.11 µm)
- **Radius interpretation:** (r = 0.22 µm)

The underlying experimental membrane convention must be confirmed from Wyon's reference [55] before either value is used for a benchmark claim.

## Configuration and assumptions

The calculation uses the initial model geometry in Wyon Table 6:

| Input | Value |
|---|---:|
| Membrane | PVDF |
| Membrane thickness | 126 µm |
| Membrane porosity | 0.75 |
| Tabulated pore size | 0.22 µm |
| Membrane thermal conductivity | 0.041 W/(m K) |
| Membrane area | 0.0003 m² (not used by this local flux solver) |
| Channel hydraulic diameter | 0.003 m |
| Channel length | 0.1 m |
| Feed velocity | 1.85 m/s |
| Permeate velocity | 2.92 m/s |
| Permeate bulk temperature | 20°C |
| Feed bulk temperatures | 40, 50, 60, 70°C |
| Feed salinity | 38 g/kg |
| Total pore pressure | 100 kPa |

**Salinity qualification:** 38 g/kg is taken from Wyon Table 2 for the Barcelona case study. It is a representative seawater input here, not a confirmed Figure 9 validation-run salinity. The validation experiment's exact feed salinity still needs to be recovered from reference [55].

The calculation uses the Wyon Appendix A property correlations, the Wyon pure-water vapour-pressure correlation on both membrane interfaces, and the coupled channel/surface fixed-point solver. Feed and permeate properties are evaluated at the arithmetic mean of each stream's bulk and membrane-surface temperatures, as described in Section 3.2.2.

## Results

Mass flux is reported in kg/(m² h); heat flux is the local membrane-surface model result in W/m².

| Feed bulk (°C) | Assumed radius (µm) | Mass flux (kg/m² h) | Heat flux (kW/m²) |
|---:|---:|---:|---:|
| 40 | 0.11 | 6.043 | 10.300 |
| 40 | 0.22 | 7.424 | 11.235 |
| 50 | 0.11 | 12.065 | 17.548 |
| 50 | 0.22 | 14.869 | 19.458 |
| 60 | 0.11 | 21.313 | 27.056 |
| 60 | 0.22 | 26.339 | 30.497 |
| 70 | 0.11 | 35.034 | 39.710 |
| 70 | 0.22 | 43.403 | 45.469 |

Doubling the assumed pore radius changes the calculated mass flux by **+22.9% to +23.9%** across the tested feed-temperature range. The local heat flux changes by **+9.1% to +14.5%**.

All eight cases converged in 27–29 fixed-point iterations. The maximum reported fixed-point temperature residual was below (1.0\times10^{-8}\ ^\circ\mathrm{C}). Regression tests lock the displayed mass- and heat-flux values to the implementation.

## Interpretation

1. The pore-size/radius convention is a first-order uncertainty for the local mass-flux prediction. It cannot be treated as a cosmetic unit conversion.
2. The two cases are **alternative interpretations**, not lower/upper confidence bounds and not evidence that either convention is correct.
3. The 38 g/kg salinity is a case-study input. It must not be represented as the measured Figure 9 feed salinity until reference [55] is checked.
4. These are local surface-model heat fluxes. Wyon Figure 9 compares total heat flux for the DCMD system; reproducing it also requires the module stream enthalpy balances and outlet-state calculations (Eqs. 18–20). No Figure 9 match is claimed here.
5. The calculations retain Wyon's source-faithful pure-water vapour-pressure assumption for both seawater and pure-water interfaces. No seawater activity correction is added.

## Next evidence required

- Obtain the full Termpiyakul et al. (2005) reference [55] and confirm whether 0.22 µm denotes a pore diameter, radius, or another nominal pore-size measure.
- Recover the exact salinity and operating conditions associated with the Figure 9 validation data.
- Only then select a source-matched pore radius and feed salinity for a parameter-matched Figure 9 reconstruction.

## Reproduction

Run:

```bash
pytest -q tests/test_wyon_2025_coupled_channel_surface.py
```

The parameterized regression `test_initial_pvdf_setup_pore_radius_interpretation_sensitivity` covers all eight cases.

## Source

Annie Wyon (2025), *Desalination utilizing data centre waste heat: A techno-economic study*, Lund University, report LUTFD2/TFEM--25/5229--SE. See Table 2, Table 6, Section 3.2.2, Eqs. 7–17, and Figure 9.  
Official thesis record: https://lup.lub.lu.se/student-papers/record/9198095  
PDF: https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf

Reference [55]: Termpiyakul, Jiraratananon & Srisurichan (2005), “Heat and mass transfer characteristics of a direct contact membrane distillation process for desalination,” *Desalination* 177, 133–141, DOI: 10.1016/j.desal.2004.11.019.
