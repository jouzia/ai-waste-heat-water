# AGMD property-state scenario audit (not a reproduction)

**Date:** 2026-11-01  
**Status:** exploratory sensitivity diagnostic only; no scenario is claimed to be the article's hidden reference case.

## Why this audit exists

The Malaguti et al. (2026) article reports recovery anchors for Config. 3 but does not state the seawater salinity or the exact evaluation temperatures used for the hot-stream, cold-stream, distillate, and latent-heat properties. The supplementary equations assume constant heat capacities and use the hot-stream inlet value in Eq. S2. They do not fully document every property state needed to reconstruct the reported calculations.

The Sharqawy (2010) correlations are now implemented in `src/ai_water/sharqawy_2010.py`. This audit asks a narrower question: what does one transparent, deliberately simple property-state choice produce, and how sensitive is the answer to latent-heat mass basis?

## Illustrative scenario definition

This is an **illustrative scenario**, not a source-recovered input set:

- Salinity: (S_R=35) g/kg (representative seawater scenario; not stated by Malaguti et al.).
- Hot and cold saline-stream heat capacities: Eq. (9) at 20°C for both streams. This deliberately uses the same reference temperature for a controlled baseline, not a claim about the authors' choice.
- Distillate heat capacity: pure-water Eq. (51) at 20°C and 0.101325 MPa.
- Latent heat: pure-water Eq. (54) at 60°C.
- A second latent-heat branch multiplies the pure-water value by (1-S_R/1000=0.965), following Eq. (37), to expose the solution-mass basis effect.
- (T_{c,in}=20°C), (Delta T_{h,in}=5°C), and the article's four ((eta,Delta T)) benchmark coordinates.
- The solver's only default outlet constraint is (Delta T_{h,out}geq0.5°C); no unsubstantiated upper bound is imposed.

Computed property values for this illustrative input set:
- (c_{sw}(20°C,35,g/kg)=3999.76) J/(kg K)
- (c_w(20°C,0.101325,MPa)=4189.09) J/(kg K)
- (h_{fg,w}(60°C)=2357.80) kJ/kg
- (h_{fg,sw}(60°C,35,g/kg)=2275.28) kJ/kg

## Results

Recovery fractions from the current S2/S8 solver:

| η | ΔT (°C) | Article anchor | Pure-water latent basis | Seawater-solution latent basis |
|---:|---:|---:|---:|---:|
| 0.5 | 30 | 2.2% | 2.1468% | 2.2256% |
| 0.5 | 50 | 3.9% | 3.9003% | 4.0450% |
| 0.7 | 30 | 3.0% | 3.0206% | 3.1322% |
| 0.7 | 50 | 5.6% | 5.5099% | 5.7164% |

Corresponding (Delta T_{h,out}) values:
- Pure-water latent basis: 4.6904, 4.0165, 4.5625, and 3.5996°C.
- Seawater-solution latent basis: 4.6789, 3.9792, 4.5461, and 3.5457°C.

The pure-water latent-heat branch happens to lie close to the four rounded article anchors for this particular illustrative input set. **This is not evidence that the article used this basis or these property states.** The solution-basis branch changes recovery by roughly 0.08–0.21 percentage points at these points. Since the source SI's mass-flow definitions and latent-heat mass basis must be interpreted together, neither branch is promoted as the definitive reproduction until that accounting is resolved.

## Interpretation and next checks

1. The solver can now be driven by actual Sharqawy correlation outputs rather than the earlier arbitrary constants.
2. The result remains underdetermined: changing salinity, evaluation temperatures, or latent-heat basis changes recovery.
3. The close match in one branch is not used to tune parameters, infer hidden inputs, or claim replication.
4. The next scientific check is a strict mass-basis audit of the publisher SI: trace the definition of recovery (R), feed/makeup/distillate mass flows, and the units of (h_{vap}) through S1–S8. Then construct a small, predeclared salinity/property-state sensitivity grid, and report the envelope rather than selecting the case closest to the figure.

## Provenance

- Malaguti et al. (2026), *Desalination* 628, 120039, DOI: https://doi.org/10.1016/j.desal.2026.120039.
- Sharqawy et al. (2010), *Desalination and Water Treatment* 16, 354–380, DOI: https://doi.org/10.5004/dwt.2010.1079.
- Correlation implementation: `src/ai_water/sharqawy_2010.py`.
- AGMD equation solver: `src/ai_water/malaguti_agmd_reference.py`.

**Reproduction status remains: NOT REPRODUCED.**