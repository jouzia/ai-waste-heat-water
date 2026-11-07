# Axial Wyon enthalpy mode implementation (2026-11-07)

## API

The axial channel model now exposes an opt-in energy-balance choice:

```python
ChannelConfig(
    ...,
    energy_balance_mode="wyon_enthalpy",
)
```

The default remains `energy_balance_mode="sensible_cp"` to preserve existing results and compatibility. The Wyon option is supported by both:

- `simulate_dcmd_channel` for co-current and fixed-point counter-current operation;
- `simulate_countercurrent_dcmd_channel` for the separate counter-current solver.

## Cell update

For each cell, with mass transfer rate `m_v = J * A_cell` and total membrane heat rate `Q = q_feed * A_cell`:

```text
m_f,out = m_f,in - m_v
m_p,out = m_p,in + m_v

h_f,out = (m_f,in*h_f,in - Q*3600) / m_f,out
h_p,out = (m_p,in*h_p,in + Q*3600) / m_p,out
```

Mass rates are kg/h, specific enthalpies J/kg, and Q is W. The factor 3600 converts W to J/h. Feed salinity is recomputed after each cell from conserved salt mass. Feed and permeate temperatures are recovered with Wyon Appendix A enthalpy correlations and their bracketed inverse.

The implementation follows Wyon Section 3.2.2 Eq. (18)'s net stream enthalpy-rate convention. It does not add a second transferred-vapour enthalpy term. The sensible-cp path is unchanged.

## Diagnostics

When Wyon mode is enabled, each `ChannelCellResult` includes:

- `feed_enthalpy_balance_residual_w`
- `permeate_enthalpy_balance_residual_w`
- `combined_enthalpy_balance_residual_w`

These are algebraic residuals for the two stream updates and their combined cell identity. They are not independent experimental validation metrics. For the fixed-point counter-current solver, the module-wide boundary identity is also affected by the configured profile convergence tolerances.

## Tests

```bash
pytest -q tests/test_channel_wyon_enthalpy.py
```

The tests cover the constant-mass conduction limit, nonzero permeation with salt retention, co-current and both counter-current solver paths, duration invariance, and an independently recomputed module enthalpy identity. The full repository suite and Ruff must pass before merge.

## Scope limitations

- Wyon enthalpy mode is an explicitly selected property/energy model; it must not be silently mixed with the generic IAPWS/Nayar property paths.
- The local interface solver still uses the configured latent-heat value and its existing reduced membrane closure. This change does not validate that latent-heat parameter or independently validate the local surface model.
- The cellwise application of Wyon's lumped Eq. (18) is a finite-volume extension. Numerical conservation checks establish internal consistency, not experimental validation of axial profiles.
- Unsupported Wyon enthalpy inversion states raise errors; the correlations are not extrapolated.
