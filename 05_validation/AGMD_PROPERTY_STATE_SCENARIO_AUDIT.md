# AGMD property-state scenario audit (not a reproduction)

**Date:** 2026-11-01  
**Status:** illustrative baseline plus predeclared property-state sensitivity; no scenario is claimed to be the article's hidden reference case.

## Why this audit exists

The Malaguti et al. (2026) article reports recovery anchors for Config. 3 but does not state the seawater salinity or the exact evaluation temperatures used for the hot-stream, cold-stream, distillate, and latent-heat properties. The supplementary equations assume constant heat capacities and use the hot-stream inlet value in Eq. S2. They do not fully document every property state needed to reconstruct the reported calculations.

The Sharqawy (2010) correlations are implemented in `src/ai_water/sharqawy_2010.py`. This audit records one transparent illustrative state and, separately, the predeclared 108-case sensitivity grid added in PR #38.

## Illustrative scenario definition

This is an **illustrative scenario**, not a source-recovered input set:

- Salinity: (S_R=35) g/kg (representative seawater scenario; not stated by Malaguti et al.).
- Hot and cold saline-stream heat capacities: Eq. (9) at 20°C for both streams. This deliberately uses the same reference temperature for a controlled baseline, not a claim about the authors' choice.
- Distillate heat capacity: pure-water Eq. (51) at 20°C and 0.101325 MPa.
- Vapour latent heat: pure-water Eq. (54) at 60°C.
- (T_{c,in}=20)°C, (Delta T_{h,in}=5)°C, and the article's four ((\eta,\Delta T)) benchmark coordinates.
- The solver's default outlet constraint is (Delta T_{h,out}\geq0.5)°C; no unsubstantiated upper bound is imposed.

Computed property values for this illustrative input set:
- (c_{sw}(20°C,35\ g/kg)=3999.76) J/(kg K)
- (c_w(20°C,0.101325\ MPa)=4189.09) J/(kg K)
- (h_{fg,w}(60°C)=2357.80) kJ/kg

### Latent-heat mass-basis correction

The earlier version of this audit also displayed a seawater-solution latent-heat branch, calculated as (h_{fg,w}(1-S_R/1000)), and left both branches unresolved. The subsequent publisher-SI mass-basis audit (PR #37) resolved that ambiguity for the S1/S2 vapour enthalpy term:

- SI S1 defines the vapour heat rate as (\dot m_d h_{vap}).
- SI S2 and the article define recovery using distillate/vapour mass flow relative to hot-feed mass flow.
- The article states complete salt rejection and pure distillate.
- Therefore (h_{vap}) in the S1/S2 term is on a per-kg-vapour (pure-water) basis. The Sharqawy Eq. (37) factor converts latent heat to a per-kg-total-saline-solution basis and **must not be applied to this vapour-mass term**.

The seawater-solution branch is retained only as a historical counterfactual illustrating the effect of mixing mass bases. It is not SI-consistent for the S1/S2 vapour enthalpy term and is not an alternative equally supported interpretation. This correction does not establish the undisclosed evaluation temperature or salinity used by the article.

## Illustrative baseline results

Recovery fractions from the current S2/S8 solver using the illustrative pure-water latent-heat basis:

| η | ΔT (°C) | Article anchor | Illustrative pure-water latent basis | Historical seawater-solution counterfactual |
|---:|---:|---:|---:|---:|
| 0.5 | 30 | 2.2% | 2.1468% | 2.2256% |
| 0.5 | 50 | 3.9% | 3.9003% | 4.0450% |
| 0.7 | 30 | 3.0% | 3.0206% | 3.1322% |
| 0.7 | 50 | 5.6% | 5.5099% | 5.7164% |

The counterfactual column is shown solely to preserve the audit trail; it is not a valid competing S1/S2 interpretation. The illustrative pure-water branch happens to lie close to the four rounded article anchors, but this is **not evidence** that the article used these property states. No inputs were selected by matching the anchors.

## Predeclared 108-case property-state sensitivity

PR #38 added `scripts/agmd_property_sensitivity.py` and tests. The grid spans:

- (S_R=30,35,40) g/kg;
- pure-water distillate (c_d) evaluation temperatures of 35, 42.5, and 50°C;
- pure-water vapour (h_{vap}) evaluation temperatures of 35, 42.5, and 50°C;
- the four published ((\eta,\Delta T)) benchmark coordinates.

The hot saline-stream (c_h) is evaluated at (T_{h,in}=T_{c,in}+\Delta T), the cold saline-stream (c_c) at 20°C, and (T_{c,in}=20)°C and (Delta T_{h,in}=5)°C are held fixed. Distillate cp and vapour latent-heat temperatures are varied independently; this is a declared sensitivity design, not a claim that either temperature equals the solved distillate outlet temperature.

The executable grid produced **108/108 model-admissible solutions** and no no-root cases. Recovery and outlet-temperature-difference envelopes across the 27 property combinations at each benchmark are:

| η | ΔT (°C) | Recovery envelope (%) | (Delta T_{h,out}) envelope (°C) |
|---:|---:|---:|---:|
| 0.5 | 30 | 2.0794–2.1379 | 4.7534–4.7810 |
| 0.5 | 50 | 3.7765–3.8834 | 4.2454–4.3113 |
| 0.7 | 30 | 2.9255–3.0077 | 4.6294–4.6567 |
| 0.7 | 50 | 5.3334–5.4847 | 3.8413–3.9104 |

Across all 108 cases, recovery spans **2.0794–5.4847%** and (Delta T_{h,out}) spans **3.8413–4.7810°C**. These are deterministic scenario ranges, not confidence intervals, probability statements, or bounds on the article's true result. All 108 scenarios pass the solver's algebraic admissibility checks; this does not independently validate the assumed property states or establish that the source's physical system is fully represented.

## Interpretation and remaining limitations

1. The solver uses Sharqawy correlation outputs with explicit property evaluation states rather than arbitrary constants.
2. The SI mass basis supports pure-water latent heat per kg vapour/distillate in S1/S2. The remaining uncertainty is the article's undisclosed salinity and exact property-evaluation temperatures, not whether to apply the saline-solution mass correction to the vapour term.
3. The grid shows modest variation within the declared property ranges, but it cannot establish the source's hidden input state or prove the reported anchors were independently reproduced.
4. Passing the S2/S8 residual checks verifies numerical consistency with the transcribed equations for these inputs; it is not experimental validation or full article reproduction.
5. Reproduction remains **NOT REPRODUCED** until the source's missing property states and any additional implementation details are independently established.

## Provenance

- Malaguti et al. (2026), *Desalination* 628, 120039, DOI: https://doi.org/10.1016/j.desal.2026.120039.
- Sharqawy et al. (2010), *Desalination and Water Treatment* 16, 354–380, DOI: https://doi.org/10.5004/dwt.2010.1079.
- Correlation implementation: `src/ai_water/sharqawy_2010.py`.
- AGMD equation solver: `src/ai_water/malaguti_agmd_reference.py`.
- Executable sensitivity grid: `scripts/agmd_property_sensitivity.py`.
- Publisher-SI mass-basis audit: `05_validation/AGMD_LATENT_HEAT_MASS_BASIS_AUDIT.md`.

**Reproduction status remains: NOT REPRODUCED.**
