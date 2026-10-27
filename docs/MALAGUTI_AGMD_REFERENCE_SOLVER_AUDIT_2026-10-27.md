# Malaguti AGMD reference solver: equation audit (2026-10-27)

## Purpose and boundary

This is an audit-only, standalone solver for the AGMD/internal-heat-recovery configuration (configuration 3) described by Malaguti et al. (2026), *Desalination* 628, 120039, DOI: [10.1016/j.desal.2026.120039](https://doi.org/10.1016/j.desal.2026.120039). It does not modify the project's production thermodynamics or net-water ledger.

The supplementary information (pp. S2–S4) defines the coupled system:

- **S2:** \(\eta = R h_{vap}/[c_h(\Delta T-\Delta T_{h,out})]\).
- **S7/S8:** AGMD module energy balance, including distillate outlet sensible enthalpy.
- **Distillate outlet estimate:** \(T_d=[T_{h,in}+(T_{c,in}+\Delta T_{h,out})]/2\).
- **Admissibility:** \(\Delta T_{h,out}\ge 0.5\ ^\circ C\).

The source's printed constraint in the S5/S8 blocks says \(\Delta T_{h,in}=0.5\ ^\circ C\), but the same supplement's prose (pp. S3 and S5) and the main article's methods say \(\Delta T_{h,in}=5\ ^\circ C\). This solver requires that value as an explicit argument; the benchmark run below follows the article/prose value of 5 °C and records the source inconsistency rather than silently resolving it.

## Property assumptions

The paper states that density, latent heat, and specific heat are based on temperature-/salinity-dependent correlations from Sharqawy et al. The current solver deliberately requires \(c_h\), \(c_c\), \(c_d\), and \(h_{vap}\) to be passed explicitly. The initial test case uses provisional values (4000, 4180, 4180 J/(kg K), and 2.4 MJ/kg) solely to verify the numerical implementation and equation residuals. These values are **not** claimed to be retrieved from the official MIT/Sharqawy correlation library.

Property-source matching, salinity basis, temperature at which latent heat is evaluated, and the exact convention for each stream property remain a separate gate. Do not label the provisional case a reproduction.

## Provisional numerical diagnostic

Using the provisional values above, with \(T_{c,in}=20\ ^\circ C\), \(\Delta T_{h,in}=5\ ^\circ C\), and the four main-text operating points, the solver returns:

| \(\eta\) | \(\Delta T\) (°C) | \(\Delta T_{h,out}\) (°C) | Recovery (%) | Main-text reported recovery (%) |
|---:|---:|---:|---:|---:|
| 0.5 | 30 | 3.547 | 2.204 | 2.2 |
| 0.5 | 50 | 1.929 | 4.006 | 3.9 |
| 0.7 | 30 | 3.411 | 3.102 | 3.0 |
| 0.7 | 50 | 1.486 | 5.660 | 5.6 |

This is a **numerical diagnostic only**. Although the results are close to the reported rounded anchors, the 50 °C cases differ by about 0.1 percentage point after rounding. That is sufficient reason not to declare reproduction until source-matched properties and exact figure/readout conventions are verified.

## Tests and interpretation

Tests verify the coupled equations' residuals, uniqueness of the admissible root for the provisional cases, basic physical bounds, and invalid-input rejection. Passing these tests verifies this implementation against the transcribed equations and chosen inputs; it does not establish that the property values match the paper, that the paper's figures were independently reproduced, or that the thermodynamic model is experimentally validated.

## Next gate

1. Retrieve and record the official MIT/Sharqawy property routines and relevant validity ranges.
2. Specify seawater salinity, property evaluation temperatures, and distillate property conventions from the source or a documented sensitivity analysis.
3. Run the four anchors without fitting to the targets and report residuals and rounding-aware error.
4. Keep IAPWS-08 as a separate comparison only; do not substitute it silently into the paper-reproduction path.
5. Leave production code unchanged until the independent benchmark and tests are reviewed.
