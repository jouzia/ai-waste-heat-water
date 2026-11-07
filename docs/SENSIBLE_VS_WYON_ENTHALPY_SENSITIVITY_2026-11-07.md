# Sensible-cp versus Wyon enthalpy sensitivity (2026-11-07)

## Experiment identity

- Experiment: `SENSIBLE-VS-WYON-ENTHALPY-COUNTERCURRENT-2026-11-07`
- Matrix: 4 feed temperatures × 3 Reference Salinities = 12 paired cases
- Feed inlet temperatures: 40, 50, 60, 70 °C
- Feed Reference Salinity: 15, 35, 38 g/kg
- Permeate inlet temperature: 20 °C
- Solver: separate counter-current finite-volume solver, 20 cells
- Reporting duration: 1 h
- Comparison: existing `sensible_cp` versus opt-in `wyon_enthalpy`

The only paired model switch is `energy_balance_mode`. Both modes use identical boundary conditions, geometry, membrane parameters, heat-transfer coefficients, inlet mass-flow rates, salinity, mesh, and local interface closure.

The fixed numerical scenario is: membrane area 0.23088 m²; permeance 100 kg m⁻² h⁻¹ bar⁻¹; latent heat 0.67 kWh kg⁻¹; membrane conductivity 0.0551 W m⁻¹ K⁻¹; thickness 110 µm; feed/permeate heat-transfer coefficients 500 W m⁻² K⁻¹; feed/permeate mass flows 600 kg h⁻¹; baseline heat capacities 4.18 kJ kg⁻¹ K⁻¹. Concentration polarization is disabled. This is an explicit numerical sensitivity case adapted from the repository's counter-current grid-test scale, **not** a reproduction of Wyon Table 6 or an experimental benchmark.

## Paired outcome ranges

All deltas below are Wyon enthalpy mode minus sensible-cp mode.

| Output | Absolute delta range across 12 cases | Relative change range |
|---|---:|---:|
| Feed outlet temperature | −0.0341 to +0.0905 °C | Not reported (Celsius percentage is not meaningful) |
| Permeate outlet temperature | −0.0447 to −0.0108 °C | Not reported (Celsius percentage is not meaningful) |
| Freshwater produced (1 h) | −0.000352 to +0.002184 kg | −0.103% to +0.178% |
| Hot-side thermal demand (1 h) | −0.000466 to +0.003007 kWh | −0.059% to +0.144% |
| Latent duty (1 h) | −0.000236 to +0.001463 kWh | −0.103% to +0.178% |
| Conductive heat leak (1 h) | −0.000281 to +0.001544 kWh | −0.046% to +0.122% |

The permeate outlet is lower in Wyon mode in all 12 cases. Feed outlet temperature changes sign across the matrix, so the comparison does not support a single direction-of-change claim for the feed outlet. Temperature changes are reported only in degrees Celsius, never as percentages of Celsius values. Product-water and duty differences are small in this selected scenario and also change sign.

## Enthalpy residual diagnostics

A post-hoc global residual was independently recomputed for both modes using the same Wyon Appendix A specific-enthalpy correlation and common enthalpy datum:

```text
R_H = (m_f,out h_f,out + m_p,out h_p,out
       - m_f,in h_f,in - m_p,in h_p,in) / 3600
```

This is reported in W. It is a model-form diagnostic applied to both outputs, not an independent experimental error.

- Sensible-cp baseline: absolute residual 6.12–36.68 W across the matrix.
- Sensible-cp residual as a fraction of hot-side duty: 0.408–3.883%.
- Wyon enthalpy mode: maximum absolute post-hoc global residual 1.75 × 10⁻⁷ W.
- Wyon enthalpy mode: maximum absolute combined per-cell algebraic residual 1.25 × 10⁻¹¹ W.

The residual contrast confirms that the opt-in Wyon mode numerically enforces the selected Wyon net-stream-enthalpy convention much more closely than the existing constant-`c_p` approximation in this scenario. It does not demonstrate that the convention itself is experimentally correct or that the local latent-heat/interface model is validated.

## Interpretation

1. In this 12-case scenario, replacing the sensible-`c_p` bulk-stream update with the Wyon enthalpy update changes outlet temperatures by less than 0.1 °C, freshwater production by less than 0.18%, and integrated hot-side duty by less than 0.15%.
2. Small output changes do not make the model-form distinction irrelevant: the post-hoc common-datum enthalpy residual of the sensible-`c_p` baseline reaches 36.68 W, while the Wyon-mode residual is near numerical roundoff.
3. The Wyon-mode residual is expected from the algebraic update and should not be presented as independent physical validation.
4. This is a controlled numerical comparison, not a calibrated operating-point study. Broader conclusions require additional configurations, mesh-convergence checks for this energy mode, independent experimental axial temperature data, and scrutiny of the transferred-water/latent-heat reference convention.

## Reproducibility

Run:

```bash
python scripts/run_sensible_vs_wyon_enthalpy_sweep.py --output-dir artifacts/sensible_vs_wyon_enthalpy_sweep
pytest -q tests/test_sensible_vs_wyon_enthalpy_sweep.py
```

- Workflow: `Sensible versus Wyon enthalpy sensitivity`
- Successful artifact run: `42379580540`
- Artifact ID: `13577150783`
- Artifact SHA-256: `b02342d2c2e55a854f604d18637dfd467bde1e053506a7d93b006d6321333f9f`
- CSV SHA-256: `693466ab3f411f3b0bc1aa2efe21283d344d5e70b98be409cb17e22ac1a5927c`
- Artifact retention: 90 days from 2026-11-07.

The CSV and manifest are archived as a GitHub Actions artifact; the manifest includes the complete fixed configuration and file hash.
