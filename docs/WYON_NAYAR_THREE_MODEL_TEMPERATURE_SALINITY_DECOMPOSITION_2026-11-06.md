# Nayar–Wyon DCMD surface sensitivity: three-model decomposition

**Experiment:** `NAYAR-WYON-TEMP-SALINITY-DECOMPOSITION-2026-11-06`  
**Main commit:** `7a6bc0dc10eadd3891216903e4181f7a1ee89631`  
**Artifact:** `nayar-wyon-temperature-salinity-sweep` (GitHub Actions run `42236544618`)

## Research question

How much of the local DCMD flux difference between Wyon (2025) and Nayar et al. (2016) comes from (a) the different pure-water vapour-pressure correlations and (b) the Nayar natural-seawater salinity correction?

A two-model comparison cannot distinguish these effects. The sweep therefore evaluates three pressure formulations at each identical operating point.

## Three-model design

1. **Wyon baseline:** Wyon Appendix A Eq. (A9) pure-water vapour pressure for feed interface, permeate interface, and mean-pore pressure. This remains the default source-faithful implementation.
2. **Nayar pure-water diagnostic:** Nayar Eq. (6) pure-water vapour pressure on all three terms. This is a diagnostic counterfactual, not a seawater model. Its contrast against Wyon isolates the pure-water reference-correlation change.
3. **Nayar natural seawater:** Nayar Eq. (6) pure-water pressure on the permeate side and Nayar Eq. (5) natural-seawater pressure on the feed-interface and mean-pore terms. Its contrast against the Nayar pure-water diagnostic isolates the salinity correction while holding channel salinity and the other inputs constant.

The Nayar seawater mode uses the supplied bulk Reference Salinity as a proxy for both feed-side membrane-interface salinity and salinity associated with the mean-pore vapour pressure. The model does not solve concentration polarization or a local membrane-interface salinity field.

## Fixed configuration and sweep

The calculation uses Wyon's initial PVDF validation configuration and operating conditions:

- Feed bulk temperatures: 40, 50, 60, and 70 °C
- Permeate bulk temperature: 20 °C
- Feed Reference Salinity: 15, 35, and 38 g/kg
- Feed/permeate velocities: 1.85/2.92 m/s
- Hydraulic diameter: 0.003 m; channel length: 0.1 m
- Membrane: PVDF, 126 µm thick, porosity 0.75, pore radius 0.11 µm
- Membrane thermal conductivity: 0.041 W/(m·K)

The pore radius is 0.11 µm, corresponding to the 0.22 µm nominal pore diameter interpreted with the related GVHP PVDF membrane literature. All three models use the same geometry and channel-property inputs within each case.

## Results across all 12 cases

Percent changes below are calculated relative to the immediately named comparison model, not relative to an arbitrary temperature scale.

| Metric | Nayar pure-water vs Wyon | Nayar seawater vs Nayar pure-water | Nayar seawater vs Wyon |
|---|---:|---:|---:|
| Mass flux | −4.95 to −5.27% | −0.79 to −3.03% | −5.93 to −7.83% |
| Total local heat flux | −1.97 to −3.20% | −0.42 to −1.30% | −2.38 to −4.45% |
| Latent heat flux | −4.95 to −5.27% | −0.79 to −3.03% | −5.93 to −7.83% |
| Conductive heat flux | +0.16 to +0.37% | +0.03 to +0.14% | +0.20 to +0.51% |

The first contrast shows that the different pure-water equations already account for a substantial part of the combined flux difference. The second contrast isolates the additional reduction introduced by Nayar's salinity correction under the stated bulk-salinity proxy.

### Example: 60 °C feed

At 60 °C and 38 g/kg Reference Salinity:

- Nayar pure-water diagnostic vs Wyon: mass flux −5.159%; total heat flux −2.782%.
- Nayar natural seawater vs Nayar pure-water diagnostic: mass flux −2.304%; total heat flux −1.212%.
- Nayar natural seawater vs Wyon overall: mass flux −7.344%; total heat flux −3.961%.

At 60 °C, increasing salinity from 15 to 38 g/kg increases the isolated Nayar salinity-correction effect from −0.836% to −2.304% in mass flux and from −0.440% to −1.212% in total local heat flux.

These are sequential, nonlinear contrasts; their percentages should not be added as if the model were linear.

## Numerical checks

- All 12 operating points converged in all three modes.
- All returned local energy-balance residuals were within the test tolerance of 1e-7 W/m².
- The automated test suite and Ruff passed on the PR.
- The post-merge main test/Ruff workflow passed.
- The post-merge sweep workflow generated, hash-verified, and uploaded the 12-row CSV and manifest.

CSV SHA-256: `568af82b669428bfb21513bbe71d947fefd04d0b36e2db6d00ef1f8afe8e6b40`.

## Interpretation and limitations

1. This is a local, steady membrane-surface model sensitivity, not experimental validation.
2. The Nayar pure-water diagnostic is used only to decompose the correlation effects; it is not presented as a seawater operating model.
3. Bulk feed salinity is assumed to represent feed-interface salinity and the mean-pore salinity term. Concentration polarization is not resolved.
4. The calculation does not solve Wyon's axial module stream enthalpy balances, outlet temperatures, or module production (Eqs. 18–20).
5. It does not reproduce or revalidate Wyon Figure 9. The exact Termpiyakul et al. Figure 9 experimental concentration and full numerical reference dataset remain unresolved.
6. The reported flux changes are conditional on the fixed PVDF geometry, velocities, and temperature/salinity grid. They should not be generalized to the later PTFE case-study configuration or the full plant.

## Conclusion

The paired Nayar natural-seawater formulation predicts lower local mass and total heat flux than Wyon's source-faithful baseline over this grid. The three-model decomposition shows that the difference is not attributable to salinity alone: the pure-water correlation change is the larger contribution in this configuration, while the seawater correction adds a further salinity-dependent reduction. This distinction is necessary for scientifically defensible interpretation of the sensitivity results.

## References

- Nayar, K. G., Sharqawy, M. H., Banchik, L. D., & Lienhard V, J. H. (2016). Thermophysical properties of seawater: A review and new correlations that include pressure dependence. *Desalination, 390*, 1–24. https://doi.org/10.1016/j.desal.2016.02.024
- Wyon, A. (2025). *Desalination utilizing data centre waste heat: A techno-economic study*. Lund University, report LUTFD2/TFEM--25/5229--SE.
- Srisurichan, S., Jiraratananon, R., & Fane, A. G. (2006). Mass transfer mechanisms and transport resistances in direct contact membrane distillation process. *Journal of Membrane Science, 277*, 186–194. https://doi.org/10.1016/j.memsci.2005.10.028
