# Exploratory AGMD Solver Check — Not a Reproduction (2026-10-27)

## Purpose

This is a deliberately isolated algebra/numerical check of the coupled AGMD equations transcribed from Malaguti et al. (2026) Supporting Information, Eqs. S2, S7, and S8. It is not production code and must not be cited as a reproduction of Figure 4B.

## Candidate assumptions used only to test the equation system

- Cold-stream inlet temperature: 20 °C.
- Overall inlet-stream temperature difference: ΔT = 30 or 50 °C, hence hot inlet temperature set to 20 °C + ΔT for this check.
- Inlet terminal difference: ΔT_h,in = 5 °C, following the main-text statement and SI prose; the printed S8 constraint line instead says 0.5 °C.
- Seawater salinity: 35 g/kg, used as a provisional scenario, not confirmed as the authors' exact solver input in the accessible text.
- Hot-side and cold-side seawater specific heats: MIT seawater-library mirror correlation evaluated at their respective inlet temperatures.
- Distillate specific heat: constant 4182 J kg−1 K−1, used as a simple placeholder rather than a version-verified Sharqawy/MIT call.
- Latent heat: seawater correlation from the same public code mirror evaluated at hot-inlet temperature. This evaluation point is provisional and not established as the authors' convention.
- Coupled equations: S2 and S7, with Td = (Th,in + Tc,in + ΔT_h,out)/2 from S8.

## Numerical result (diagnostic only)

Using a generic nonlinear root solver under the assumptions above yielded the following single candidate root for each case:

| η | ΔT (°C) | ΔT_h,out (°C) | R |
|---:|---:|---:|---:|
| 0.5 | 30 | 4.7557 | 0.02202 |
| 0.5 | 50 | 4.2179 | 0.04087 |
| 0.7 | 30 | 4.6262 | 0.03099 |
| 0.7 | 50 | 3.7873 | 0.05775 |

These are close to the four Figure 4B anchors (2.2%, 3.9%, 3.0%, 5.6%), but this agreement is **not** evidence of reproduction: the result depends on unverified property evaluation choices, a provisional salinity, a placeholder distillate heat capacity, and the unresolved 0.5 °C / 5 °C source discrepancy. Do not tune or promote these results as validated outputs.

## Required follow-up before a defensible reproduction

1. Verify the exact property correlations and units against a versioned source. The official MIT page lists a 2024 library archive, but the code used in this check was transcribed from a public mirror and has not been checksum-matched to that archive.
2. Establish the source-supported temperature/salinity inputs for c_h, c_c, c_d, and h_vap. The SI explicitly selects hot-channel specific heat at inlet conditions for S2 and describes constant channel specific heats, but does not fully specify every AGMD property call.
3. Resolve or explicitly branch the inconsistent printed constraint ΔT_h,in = 0.5 °C versus the prose/main text value 5 °C.
4. Add residual, bounds, multiple-initial-guess, units, and property-domain tests.
5. Compare against the plotted anchors only after assumptions are fixed independently. Report figure-reading uncertainty and do not fit assumptions to those four values.

## Decision

**Exploratory solver: numerically solvable; reproduction gate: still open.** No production thermodynamics code was changed. No empirical validation, novelty, or net-water-benefit claim follows from this check.
