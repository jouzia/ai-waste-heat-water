# Wyon (2025) Figure 9 benchmark and reconstruction boundary

**Audit date:** 2026-11-06  
**Primary source:** Annie Wyon, *Desalination utilizing data centre waste heat: A techno-economic study*, Lund University, June 2025, report LUTFD2/TFEM--25/5229--SE.  
**Repository implementation:** `src/ai_water/wyon_2025_surface_reference.py`

## Source trace

The official Lund University record identifies the thesis and links the open-access PDF:

- Record: https://lup.lub.lu.se/student-papers/record/9198095
- PDF: https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf

Relevant source locations in the PDF:

- Printed page 15, Section 3.2.2: Eqs. (9)–(16), including the film coefficient, turbulent Nusselt correlation, membrane heat flux, combined Knudsen/molecular mass-transfer coefficient, mean membrane temperature, pore-air partial pressure, 1-bar total pore pressure, and tortuosity.
- Printed page 16: Eq. (17), enthalpy of vapour, Eq. (18) module enthalpy-rate balance, Eq. (19) stream enthalpy flow, and Figure 9.
- Printed pages 14–16: local DCMD model and its stated validation context.

## Figure 9: what it does and does not validate

Figure 9 plots Wyon's **total DCMD-system heat flux** against feed inlet temperature for four experimental/model comparison points. The plotted relative discrepancy labels are:

| Feed inlet temperature | Model-versus-experiment label in Figure 9 |
|---:|---:|
| 40 °C | +6.5% |
| 50 °C | −8.1% |
| 60 °C | −11.0% |
| 70 °C | −8.4% |

These percentages are transcribed from the figure labels, not recalculated from underlying raw observations. The thesis states that a small but significant discrepancy remains, suspects the mass-flux calculation, says the exact cause is unidentified, and notes that the experimental temperature range differs from the range used for subsequent results (printed p. 16).

**Important benchmark boundary:** Figure 9 is not a direct numerical validation target for the repository's isolated surface solver by itself. The figure is the total heat flux of Wyon's DCMD system. Reproducing it requires the matching full-module calculation and source conditions, including stream-side heat-transfer coefficients, mass flux, latent and conductive heat transfer, and the corresponding experimental reference values. The current local solver returns a membrane-surface heat flux for specified bulk temperatures and film coefficients; it does not calculate the full module outlet states or stream enthalpy rates.

The figure's four labels are therefore a **published system-level comparison target**, not evidence that the isolated solver has reproduced Wyon's Figure 9.

The benchmark setup is also materially different from the parameter set used in the repository's representative local-solver test. Wyon's initial validation setup (printed p. 14, Table 6) uses a PVDF membrane with 126 µm thickness, 75% porosity, 0.22 µm pore size, 0.041 W/(m·K) thermal conductivity, and 0.0003 m² area. The later case-study setup (printed p. 17, Table 7) uses PTFE, 77 µm, 89%, 0.45 µm, 0.031 W/(m·K), and 0.1 m². The current isolated solver's regression example uses the latter parameter set. It is therefore not even parameter-matched to the Figure 9 validation configuration. The benchmark reconstruction must first use the initial validation geometry and operating conditions before comparing outputs.

Wyon identifies Termpiyakul, Jiraratananon and Srisurichan (2005), *Desalination* 177, 133–141, DOI 10.1016/j.desal.2004.11.019, as reference [55]. That study reports a flat-sheet PVDF membrane with 0.22 µm pores, feed temperatures 40–70 °C, feed velocities 1.85–3.7 m/s, and a receiving distillate at 20 °C and 2.92 m/s. It also describes calibrating the membrane distillation coefficient from pure-water flux data; the accessible abstract and secondary reproduction report a coefficient of 0.0024 kg/(m²·h·Pa) from pure-water data. This coefficient should not be silently substituted for Wyon's Eq. (14) mechanistic coefficient: the definitions, units, and modelling route must be reconciled first.


## Equation-level implementation status

The current isolated module transcribes the following source-defined elements:

- Wyon Eq. (9): convective film coefficient, \(\alpha = Nu\,k/d_h\).
- Wyon Eq. (10): turbulent-channel Nusselt correlation.
- Wyon Eq. (13): membrane heat flux as latent plus conductive components.
- Wyon Eq. (14): combined Knudsen/molecular diffusion expression.
- Wyon Eq. (15): pore-air partial pressure, \(p_{air}=p_{tot}-p_{vapour}\), with pore vapour pressure evaluated at mean membrane temperature.
- Wyon Eq. (16): tortuosity correlation.
- Wyon Eq. (17): vapour enthalpy correlation.

The implementation's mean-temperature pore-pressure convention is source-faithful: Wyon explicitly states that membrane temperature is approximated by the arithmetic mean of the two interface temperatures and evaluates pore vapour pressure at that mean temperature. The default total pore pressure is 1 bar, as in the thesis.

## Remaining validation work

1. Recover and document the exact source conditions and experimental dataset behind Figure 9, including the cited reference [55], rather than digitizing the plotted curves as if they were raw data.
2. Reconstruct the full local module calculation needed to calculate Wyon's total heat flux on the same basis as Figure 9.
3. Compare model and experimental values at matched conditions and report pointwise errors; retain Wyon's reported discrepancies as historical context, not as acceptance thresholds.
4. Establish an explicit numerical operating envelope and test bracket existence, convergence, and root sensitivity throughout it.
5. Keep model-level, system-level, and experimental validation claims separate.

## Interpretation

The present implementation is an equation-level local membrane-interface reconstruction with internal numerical closure tests. It is not an independent reproduction of Wyon's DCMD module, Figure 9, heat exchanger, pumps, 80-module plant, annual production, or techno-economic results. No experimental validation claim is supported until the remaining steps above are completed.
