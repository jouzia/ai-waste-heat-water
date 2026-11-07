# Expanded 12-point DCMD enthalpy-mode mesh convergence grid

**Experiment ID:** `DCMD-ENTHALPY-EXTENDED-MESH-GRID-2026-11-07`  
**Status:** Reproducible implementation; results are generated and archived by the dedicated workflow.

## Objective

Expand the two-point mesh study to the full 4 × 3 operating grid used in the prior sensible-cp versus Wyon enthalpy sensitivity work. This tests whether the earlier mesh-stability observations generalize across feed temperature and Reference Salinity within the selected numerical scenario.

The study contains 12 operating points × 2 energy-balance modes × 4 mesh sizes = **96 simulations**.

## Operating grid

- Feed inlet temperatures: 40, 50, 60, 70 °C.
- Feed Reference Salinities: 15, 35, 38 g/kg.
- Permeate inlet temperature: 20 °C.
- Mesh sizes: 10, 20, 40, 80 finite-volume cells.
- Energy-balance modes: `sensible_cp`, `wyon_enthalpy`.

The fixed numerical configuration is identical to the preceding paired sensitivity and mesh studies: membrane area 0.23088 m², permeance 100 kg m⁻² h⁻¹ bar⁻¹, latent heat 0.67 kWh/kg, membrane conductivity 0.0551 W/(m K), thickness 110 μm, feed/permeate heat-transfer coefficients 500 W/(m² K), feed/permeate inlet mass flows 600 kg/h, heat capacities 4.18 kJ/(kg K), duration 1 h, counter-current arrangement, and concentration polarization disabled.

Within each operating point and energy mode, **only the cell count changes**.

These are controlled numerical scenarios, not a reproduction of Wyon Table 6 or experimental operating records.

## Outputs and comparisons

The CSV reports outlet temperatures, freshwater production, outlet mass flows, concentrate salinity, hot-side thermal demand, latent duty, conductive heat leak, post-hoc global Wyon enthalpy residual, and maximum combined per-cell algebraic residual where available.

Each 10/20/40-cell result is compared with the 80-cell result for the same operating point and mode. Temperature deviations are absolute °C only; percentages of Celsius temperatures are omitted. The 80-cell solution is a finest-mesh reference, not an exact solution.

## Interpretation constraints

1. This study assesses spatial-discretization sensitivity only. It does not validate membrane permeance, heat-transfer coefficients, vapour-pressure correlations, property models, or the Wyon enthalpy convention.
2. A small difference from the 80-cell result indicates numerical mesh stability for the tested cases, not physical accuracy.
3. Wyon-mode algebraic residuals are implementation diagnostics, not independent experimental validation.
4. The post-hoc global Wyon enthalpy residual for sensible-cp mode is a model-form diagnostic, not experimental error.
5. No universal minimum cell count or empirical convergence order is asserted without supporting analysis.
6. The tested grid is bounded by the stated numerical configuration; conclusions should not be extrapolated to other geometries, membrane parameters, flow regimes, or concentration-polarization settings.

## Reproduction

```bash
python scripts/run_extended_enthalpy_mesh_convergence.py --output-dir artifacts/extended_enthalpy_mesh_convergence
pytest -q tests/test_extended_enthalpy_mesh_convergence.py
```

The dedicated workflow archives the CSV, summary JSON, and hash-bearing manifest for 90 days. Numerical findings will be appended after the artifact is generated and independently inspected.


## Numerical findings (96-run artifact)

The dedicated workflow completed all 96 simulations and passed its matrix, finite-output, residual, and SHA-256 manifest checks. The archived artifact is `extended-enthalpy-mesh-grid` (90-day retention). The artifact manifest records 12 operating points, 96 rows, and the fixed configuration above.

Across all 24 operating-point/mode pairs, the absolute deviations from the 80-cell reference decreased monotonically at each refinement step (10 → 20 → 40 → 80 cells) for every reported comparison output: feed and permeate outlet temperatures, freshwater production, hot-side demand, latent duty, and conductive heat leak.

### Worst-case deviations from the 80-cell reference

| Mesh | Feed outlet temperature | Permeate outlet temperature | Freshwater production | Hot-side demand | Latent duty | Conductive heat leak |
|---:|---:|---:|---:|---:|---:|---:|
| 10 cells | 0.008381 °C | 0.008872 °C | 0.4743% | 0.2885% | 0.4743% | 0.2309% |
| 20 cells | 0.003586 °C | 0.003795 °C | 0.2028% | 0.1234% | 0.2028% | 0.09884% |
| 40 cells | 0.001194 °C | 0.001264 °C | 0.06752% | 0.04111% | 0.06752% | 0.03292% |

Temperature entries are absolute differences in °C, not percentages. Percentage entries are relative deviations in the corresponding non-temperature quantity. Values are maxima across the 12 operating points and both energy modes; maxima need not occur in the same case.

The largest Wyon-mode absolute global enthalpy residual across the 48 Wyon simulations was approximately 4.41 × 10⁻⁷ W. The largest reported combined per-cell algebraic residual was approximately 1.45 × 10⁻¹¹ W. These are numerical implementation diagnostics under the selected enthalpy convention. They do not establish physical or experimental validity. The sensible-cp cases have nonzero post-hoc Wyon residuals by construction because the two modes use different energy conventions.

### Interpretation

Within this tested reduced-order configuration, 40 cells differed from the 80-cell reference by no more than 0.001264 °C in outlet temperature, 0.06752% in freshwater/latent-duty quantities, 0.04111% in hot-side demand, and 0.03292% in conductive heat leak. This supports mesh stability at 40 cells relative to the 80-cell reference for this grid. It does **not** establish that 40 cells are universally sufficient, that the 80-cell result is exact, or that either mode is experimentally accurate. No formal convergence order is inferred.
