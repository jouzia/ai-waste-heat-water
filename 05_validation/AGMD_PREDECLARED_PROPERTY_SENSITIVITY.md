# Predeclared AGMD property-state sensitivity grid

**Status:** executable scenario analysis; not a source-recovered property set. Numerical reproduction remains **NOT REPRODUCED**.

## Purpose

The publisher SI establishes the stream/mass basis used by the AGMD balances, but the article does not disclose the salinity and all property-evaluation temperatures required to reproduce the Figure 4 recovery anchors. This grid quantifies the effect of a finite, declared set of plausible property-state scenarios without selecting the scenario that best matches the paper.

## Predeclared design

The script `scripts/agmd_property_sensitivity.py` evaluates the Cartesian product below for all four published (η, ΔT) benchmark coordinates:

| Input | Values / rule | Rationale and boundary |
|---|---|---|
| Reference salinity (S_R) | 30, 35, 40 g/kg | Declared seawater scenario bracket; not attributed to the article |
| (T_{c,in}) | 20°C | Article operating condition |
| (Delta T_{h,in}) | 5°C | Article condition; SI's printed 0.5°C inconsistency remains documented |
| Hot-stream (c_h) evaluation | (T_{h,in}=T_{c,in}+Delta T) | Follows SI statement that hot cp is evaluated at hot-channel inlet |
| Cold-stream (c_c) evaluation | 20°C | Explicit cold inlet state |
| Distillate (c_d) evaluation | 35, 42.5, 50°C | Declared property-state bracket; not asserted to be the exact (T_d) |
| Vapour latent-heat evaluation | 35, 42.5, 50°C | Declared pure-water property-state bracket; not asserted to be the exact interface temperature |
| Vapour latent-heat mass basis | Pure water, kg vapour / kg distillate | Required by SI S1-S2 mass-flow term; no seawater Eq. 37 correction |
| Outlet constraint | (Delta T_{h,out}geq0.5°C) | Article's stated physical constraint; no unsubstantiated upper bound |

The grid contains (3\times3\times3\times4=108) scenario/benchmark evaluations. Heat capacities use Sharqawy et al. (2010) Eq. 9 for seawater and Table 11 Eq. 51 for pure water; vapour latent heat uses pure-water Eq. 54. All temperatures and salinities are explicit in the output CSV.

## Reproduction and interpretation limits

- This is a deterministic scenario envelope, **not** a probability distribution, confidence interval, or uncertainty quantification of the article's hidden inputs.
- The (c_d) and (h_{vap}) evaluation temperatures are varied independently as a controlled sensitivity design. The grid does not claim they are equal to each other or to the solved distillate outlet temperature.
- The script reports no-admissible-root cases rather than silently dropping constraints or inventing a fallback.
- The grid does not tune inputs against the article's rounded recovery anchors.
- A close result in any cell is not evidence that the authors used those property states.
- A fully source-matched reproduction still requires recovery of the exact property-state conventions (or author clarification) and independent validation of the model's assumptions.

## Reproduction

From the repository root, with the project environment installed:

```bash
python scripts/agmd_property_sensitivity.py --output 06_results/agmd_property_sensitivity.csv
```

The output contains one row per predeclared scenario/benchmark combination, including property inputs, solver status, recovery, outlet temperature difference, distillate outlet temperature, and S2/S8 residuals.

## Sources

- Malaguti et al. (2026), *Desalination* 628, 120039, DOI: https://doi.org/10.1016/j.desal.2026.120039; publisher Supporting Information S1-S8.
- Sharqawy, Lienhard & Zubair (2010), DOI: https://doi.org/10.5004/dwt.2010.1079; Eq. 9, Eq. 51, Eq. 54.
- SI mass-basis interpretation: [AGMD latent-heat mass-basis audit](AGMD_LATENT_HEAT_MASS_BASIS_AUDIT.md).

**Reproduction status: NOT REPRODUCED.**
