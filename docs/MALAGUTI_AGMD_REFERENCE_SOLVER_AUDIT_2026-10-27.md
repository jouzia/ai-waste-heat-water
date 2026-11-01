# Malaguti AGMD reference solver: equation audit (2026-10-27)

## Purpose and boundary

This is an audit-only, standalone solver for the AGMD/internal-heat-recovery configuration (configuration 3) described by Malaguti et al. (2026), *Desalination* 628, 120039, DOI: [10.1016/j.desal.2026.120039](https://doi.org/10.1016/j.desal.2026.120039). It does not modify the project's production thermodynamics or net-water ledger.

The supplementary information (pp. S2–S4) defines the coupled system:

- **S2:** \(\eta = R h_{vap}/[c_h(\Delta T-\Delta T_{h,out})]\).
- **S7/S8:** AGMD module energy balance, including distillate outlet sensible enthalpy.
- **Distillate outlet estimate:** \(T_d=[T_{h,in}+(T_{c,in}+\Delta T_{h,out})]/2\).
- **Admissibility:** \(\Delta T_{h,out}\ge 0.5\ ^\circ C\).

The source's printed constraint in the S5/S8 blocks says \(\Delta T_{h,in}=0.5\ ^\circ C\), but the same supplement's prose (pp. S3 and S5) and the main article's methods say \(\Delta T_{h,in}=5\ ^\circ C\). This solver requires that value as an explicit argument; the diagnostic run below follows the article/prose value of 5 °C and records the source inconsistency rather than silently resolving it.

## Property assumptions

The paper states that density, latent heat, and specific heat are based on temperature-/salinity-dependent correlations from Sharqawy et al. The official [MIT seawater properties library](https://web.mit.edu/seawater/) lists seawater specific heat, density, and latent heat functions and their validity ranges. It also documents a correction to the Jamieson specific-heat coefficient. The library's availability does not mean its functions have yet been integrated or independently checked in this branch.

The solver requires \(c_h\), \(c_c\), \(c_d\), and \(h_{vap}\) to be passed explicitly. The smoke-test values are provisional (\(c_h=4000\), \(c_c=4000\), \(c_d=4180\) J/(kg K), and \(h_{vap}=2.4\) MJ/kg). The hot and cold channels are saline-water streams in this AGMD configuration; \(c_d\) refers to the distillate. Using 4180 J/(kg K) for the cold saline stream would incorrectly treat it as pure water, so the smoke test does not do that. None of these provisional values is claimed to be retrieved from the official MIT/Sharqawy library.

Property-source matching, salinity basis, pressure convention, temperature at which latent heat is evaluated, and the exact convention for each stream property remain unresolved. Do not label the provisional case a reproduction.

## Provisional numerical diagnostic

Using the provisional values above, with \(T_{c,in}=20\ ^\circ C\), \(\Delta T_{h,in}=5\ ^\circ C\), and the four main-text operating points, the solver returns:

| \(\eta\) | \(\Delta T\) (°C) | \(\Delta T_{h,out}\) (°C) | Recovery (%) | Main-text reported recovery (%) |
|---:|---:|---:|---:|---:|
| 0.5 | 30 | 4.698 | 2.109 | 2.2 |
| 0.5 | 50 | 4.039 | 3.830 | 3.9 |
| 0.7 | 30 | 4.573 | 2.966 | 3.0 |
| 0.7 | 50 | 3.632 | 5.410 | 5.6 |

This is a **numerical diagnostic only**. It uses illustrative values, not source-matched property outputs; it is not an independent reproduction. The 50 °C, \(\eta=0.7\) case is about 0.2 percentage points below the source-reported anchor, so exact property provenance and the figure/readout convention matter.

## Tests and interpretation

Tests verify the coupled equations' residuals, admissible root, basic physical bounds, and invalid-input rejection for the provisional cases. Passing these tests verifies the implementation against the transcribed equations and chosen inputs; it does not establish that the property values match the paper, that the paper's figures were independently reproduced, or that the thermodynamic model is experimentally validated.

## Next gate

1. Use the official MIT/Sharqawy property routines (code version 7 August 2024; tables version 9 December 2023) or an independently checked transcription, with relevant validity ranges recorded.
2. Specify seawater salinity, property evaluation temperatures, pressure convention, and distillate property conventions from the source or a documented sensitivity analysis.
3. Run the four anchors without fitting to the targets and report residuals and rounding-aware error.
4. Keep IAPWS-08 as a separate comparison only; do not substitute it silently into the paper-reproduction path.
5. Leave production code unchanged until the independent benchmark and tests are reviewed.
