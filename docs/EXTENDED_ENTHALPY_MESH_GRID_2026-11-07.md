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
