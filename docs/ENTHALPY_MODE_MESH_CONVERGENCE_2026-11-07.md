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


## Results — completed run (2026-11-07)

The dedicated workflow completed successfully for all 16 combinations (2 operating points × 2 energy modes × 4 meshes). For each of the four case/mode combinations, the absolute deviation from the 80-cell result decreased monotonically from 10→20→40 cells for every reported output metric.

### Maximum deviation from the 80-cell reference across both cases and both modes

| Mesh | Outlet-temperature deviation (max absolute °C) | Freshwater production (max absolute relative %) | Hot-side duty (max absolute relative %) | Latent duty (max absolute relative %) | Conductive duty (max absolute relative %) |
|---:|---:|---:|---:|---:|---:|
| 10 cells | 0.008824 | 0.4743% | 0.2878% | 0.4743% | 0.1950% |
| 20 cells | 0.003775 | 0.2028% | 0.1231% | 0.2028% | 0.0835% |
| 40 cells | 0.001257 | 0.0675% | 0.0410% | 0.0675% | 0.0278% |

At 40 cells, the maximum observed outlet-temperature difference from the 80-cell reference is approximately 0.00126 °C. The maximum freshwater-production difference is 0.0675%, and the maximum hot-side-duty difference is 0.0411% across the selected cases and modes. These are numerical mesh differences only.

### Enthalpy residual diagnostics at 80 cells

- Wyon-enthalpy mode: absolute post-hoc global Wyon enthalpy residuals were 4.55×10⁻⁸ W (T60_S35) and 1.63×10⁻⁷ W (T70_S38). Maximum combined per-cell algebraic residuals were 6.21×10⁻¹² W and 1.45×10⁻¹¹ W, respectively.
- Sensible-cp mode: absolute post-hoc global Wyon enthalpy residuals were 29.01 W (T60_S35) and 21.17 W (T70_S38). This is expected as a diagnostic difference between the sensible-cp update and the Wyon enthalpy convention; it is not experimental error.

### Difference between energy-balance modes at the 80-cell mesh

| Case | Feed outlet ΔT (Wyon − sensible) | Permeate outlet ΔT | Freshwater change | Hot-side duty change |
|---|---:|---:|---:|---:|
| T60_S35 | −0.01121 °C | −0.03080 °C | −0.00536% | +0.02373% |
| T70_S38 | +0.01487 °C | −0.04446 °C | +0.04740% | +0.06243% |

The small mode-to-mode differences remain after mesh refinement and are not artifacts of using the original 20-cell mesh. The sign of the feed outlet temperature difference changes between cases; no single directional claim is warranted.

### Reproducibility record

- Pull request: [#102](https://github.com/jouzia/ai-waste-heat-water/pull/102)
- Dedicated successful PR workflow run: [42380566446](https://github.com/jouzia/ai-waste-heat-water/actions/runs/42380566446)
- Artifact ID: `13576738906` (90-day retention)
- Artifact SHA-256: `1e072d3ccb107985d1ce46babd294d9ef249174ad087401c706295990687be07`
- CSV SHA-256: `422da5eefd66250e0fb6cdb6f39ef1a6cba751f0f93bba136ba0cfc530ce2f36`
- Summary JSON SHA-256: `efa1fc071165f6ea2484d065969373141ec227b0e36dd5eb352de052ba3b8768`

**Conclusion:** For these two fixed operating points and this reduced-order model, 40 cells are already close to the 80-cell reference for the reported integral outputs and outlet temperatures. This supports a mesh-stability statement for these cases; it does not establish a universal minimum cell count or physical validation.
