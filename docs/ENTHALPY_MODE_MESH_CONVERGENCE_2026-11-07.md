# DCMD enthalpy-mode mesh convergence protocol

**Experiment ID:** `DCMD-ENTHALPY-MESH-CONVERGENCE-2026-11-07`  
**Status:** Reproducible experiment implementation; numerical results are emitted by the linked GitHub Actions artifact.

## Objective

Quantify the spatial-discretization sensitivity of the counter-current finite-volume DCMD channel model for the two bulk-stream energy-balance modes already present in the repository:

- `sensible_cp`: constant-`cp` bulk-stream temperature update.
- `wyon_enthalpy`: mass-weighted Wyon Appendix A stream-enthalpy update.

The mesh is varied over 10, 20, 40, and 80 cells. The same operating inputs, geometry, membrane properties, inlet conditions, and solver tolerances are used at every mesh. Only `cells` changes.

## Operating points

| Case | Feed inlet | Permeate inlet | Feed Reference Salinity |
|---|---:|---:|---:|
| T60_S35 | 60 °C | 20 °C | 35 g/kg |
| T70_S38 | 70 °C | 20 °C | 38 g/kg |

Both cases use the same fixed numerical scenario as the preceding paired sensitivity experiment: membrane area 0.23088 m², permeance 100 kg m⁻² h⁻¹ bar⁻¹, latent heat 0.67 kWh/kg, membrane conductivity 0.0551 W/(m K), thickness 110 μm, feed/permeate heat-transfer coefficients 500 W/(m² K), and inlet mass-flow rates 600 kg/h on each side. Both heat capacities are 4.18 kJ/(kg K), duration is 1 h, and concentration polarization is disabled.

These are controlled numerical scenarios, not reproductions of Wyon Table 6 or experimental operating records.

## Reported quantities

For each case, mode, and mesh, the CSV reports feed/permeate outlet temperatures, freshwater production, outlet mass-flow rates, concentrate salinity, hot-side thermal demand, latent duty, conductive heat leak, post-hoc global Wyon enthalpy residual, and the maximum combined per-cell enthalpy residual where the solver exposes it.

Each 10/20/40-cell result is compared with the 80-cell result for the same case and mode. Temperature differences are reported in °C only. Relative differences are reported for non-temperature quantities only.

The 80-cell solution is a *finest-mesh reference*, not an exact solution. The study should be interpreted through the observed change from 10→20→40→80 cells, not by treating 80 cells as ground truth. A small difference from the 80-cell result is evidence of mesh stability for this model and these cases, not proof of physical accuracy.

## Interpretation constraints

1. Mesh convergence addresses numerical resolution only. It does not validate membrane permeance, heat-transfer coefficients, vapour-pressure correlations, thermodynamic property models, or the selected Wyon enthalpy convention.
2. The Wyon-mode algebraic residual checks the implementation's selected enthalpy update; it is not independent experimental validation.
3. The post-hoc global Wyon enthalpy residual is a model-form diagnostic. It is not experimental error.
4. No empirical convergence order is claimed unless the observed sequence supports it and the assumptions for such an estimate are stated.
5. Do not infer that the 80-cell result is physically correct merely because finer meshes agree.

## Reproduction

```bash
python scripts/run_enthalpy_mesh_convergence.py --output-dir artifacts/enthalpy_mesh_convergence
pytest -q tests/test_enthalpy_mesh_convergence.py
```

The workflow archives `enthalpy_mesh_convergence.csv`, `mesh_convergence_summary.json`, and a hash-bearing `manifest.json` for 90 days. The CSV and manifest are the audit trail; the report should be updated with the artifact's actual numerical results after the workflow completes.
