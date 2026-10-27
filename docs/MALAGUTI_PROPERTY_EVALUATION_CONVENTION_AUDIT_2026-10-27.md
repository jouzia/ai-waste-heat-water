# Malaguti property-evaluation convention audit

**Audit date:** 2026-10-27  
**Status:** Source methods narrowed; evaluation points remain unresolved.

## What the paper explicitly specifies

The main article states that seawater is the feed, salt rejection is complete, and distillate is pure water. It says density, enthalpy of vaporization, and specific heat capacity are based on temperature- and salinity-dependent correlations from Sharqawy et al. The declared boundary conditions are cold-stream inlet temperature 20 °C, hot-inlet terminal difference ΔT_h,in = 5 °C, and heat-exchanger pinch ΔT_HX = 5 °C. The paper defines ΔT_h,in = T_h,in − T_c,out and ΔT_h,out = T_h,out − T_c,in. For the AGMD recovery analysis, it states the 5 °C input difference and a minimum ΔT_h,out of 0.5 °C.

Source: Malaguti et al. (2026), *Desalination* 628, 120039, DOI 10.1016/j.desal.2026.120039. https://doi.org/10.1016/j.desal.2026.120039

## What is not explicit in the accessible text

The main article and the available supplementary equation transcription do not yet establish, with sufficient certainty, the exact evaluation temperature for every property symbol in the AGMD configuration-3 coupled system. In particular, the source must be checked for whether c_h and c_c are evaluated at stream inlet temperatures, outlet temperatures, representative/mean temperatures, or separate stream-specific temperatures, and whether h_vap is evaluated at the hot-side temperature or another representative temperature. The property method must not choose these points merely to improve agreement with Figure 4B.

The main text explicitly uses ΔT_h,in = 5 °C, while the supplementary S5/S8 constraint transcription appears to state 0.5 °C in one place. This is recorded as a source inconsistency. It should not be conflated with the separate stated minimum ΔT_h,out = 0.5 °C.

## Implementation decision

Do not yet write a production property function that silently chooses a representative temperature. First extract the full definitions around Eqs. S6–S8 directly from the supplement image/PDF and compare them with the paper's symbol definitions. Then document each property call as a table with columns: symbol, fluid stream, temperature argument, salinity argument, pressure assumption, cited correlation, units, and evidence location.

Once these are pinned down, implement the property layer as a pure, independently tested function. Tests should check units, expected physical ranges, reference outputs from the official MIT library or a version-matched implementation, and domain failures. Solver tests should separately check equation residuals, positivity, recovery bounds, and sensitivity to initial guesses. The four Figure 4B recoveries are validation targets, not parameters for tuning.

## Current conclusion

The paper supports the correlation family and boundary conditions, but the exact property-evaluation convention is not yet independently established. The source-code mirror helps transcribe the MIT functions but does not replace verification against the official archive. No numerical reproduction, empirical validation, net-water benefit, or novelty claim is established by this audit.
