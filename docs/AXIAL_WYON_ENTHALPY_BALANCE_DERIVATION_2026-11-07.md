# Axial DCMD stream enthalpy balance: Wyon reference and finite-volume derivation

**Date:** 2026-11-07  
**Status:** Derivation audit; no solver changes  
**Scope:** Establish what is already supported by Wyon (2025), distinguish the existing lumped outlet implementation from the axial channel solver, and specify a defensible opt-in finite-volume formulation.

## 1. Correction to the preceding audit's scope

The counter-current variable-mass audit correctly identified that the axial channel marchers update temperature with constant-`cp` sensible-heat expressions while updating mass flow separately. However, the repository already contains a separate Wyon-based lumped module outlet implementation that evaluates mass-weighted stream enthalpies and inverts them to outlet temperatures:

- `src/ai_water/wyon_2025_enthalpy.py`: Wyon Appendix A Eqs. (A11)–(A12), plus bracketed inversion;
- `src/ai_water/wyon_2025_module_outlets.py`: Wyon Section 3.2.2 Eqs. (18)–(20), with water and salt mass balances and feed/permeate enthalpy-rate checks;
- `tests/test_wyon_2025_module_outlets.py`: verifies the lumped mass, salt, and enthalpy-rate identities.

Thus it would be inaccurate to say that the repository has no variable-mass enthalpy formulation. It has one at the **lumped one-pass module level**. What remains unestablished is the axial finite-volume extension in `md_channel.py` and `md_channel_countercurrent.py`.

## 2. Source-supported lumped convention

Wyon (2025), Section 3.2.2, Eq. (18), writes the total module heat-transfer rate as the feed enthalpy-rate decrease and permeate enthalpy-rate increase:

```text
Q = H_f,in - H_f,out = H_p,out - H_p,in
H = m_dot * h
```

Eq. (19) relates mass and volumetric flow. Eq. (20) expresses salt conservation. Appendix A Eqs. (A11)–(A12) provide seawater and pure-water specific enthalpy correlations. The current lumped implementation follows this convention:

```text
m_f,out = m_f,in - m_v
m_p,out = m_p,in + m_v

m_f,out * h_f,out = m_f,in * h_f,in - Q
m_p,out * h_p,out = m_p,in * h_p,in + Q
```

It then obtains the feed outlet salinity from salt mass conservation and inverts the two enthalpy correlations for outlet temperatures. In this convention, the mass-weighted outlet enthalpy rates already include the effect of the changing stream mass. Do **not** append a second transferred-water enthalpy term to these same equations: that would double count the mass-transfer energy unless the definition of (Q) were changed to a different, explicitly phase-resolved control-volume convention.

This is an explicit source-based lumped closure. It is not an independent experimental validation of the correlation or of the assumptions used to identify the membrane total heat rate with the stream enthalpy-rate difference.

## 3. Candidate axial finite-volume extension

For cell (i), let (A_i=A_m/N), (J_i) be the local water flux, and (Q_i=q_{tot,i}A_i) be the local total heat-transfer rate. The local interface solution already reports:

```text
q_feed,i = q_latent,i + q_conductive,i
q_permeate,i = q_feed,i
```

Use the same Wyon net-stream-enthalpy convention cell by cell:

```text
m_v,i = J_i * A_i

m_f,out,i = m_f,in,i - m_v,i
m_p,out,i = m_p,in,i + m_v,i

m_f,out,i * h_f,out,i
    = m_f,in,i * h_f,in,i - Q_i

m_p,out,i * h_p,out,i
    = m_p,in,i * h_p,in,i + Q_i
```

Then close the feed salt balance (salt is nonvolatile):

```text
m_salt,i = m_f,in,i * w_f,in,i
w_f,out,i = m_salt,i / m_f,out,i
S_R,out,i = 1000 * w_f,out,i   [g/kg]
```

Recover temperatures from the existing Wyon enthalpy correlations:

```text
T_f,out,i = h_f,Wyon_inverse(h_f,out,i, S_R,out,i)
T_p,out,i = h_pure_water,Wyon_inverse(h_p,out,i)
```

For co-current flow, propagate both stream outlet states to the next cell in the same axial direction. For counter-current flow, the feed sweep propagates from (x=0) to (x=L), while the permeate sweep propagates from (x=L) to (x=0); the two boundary-value profiles must be iterated to convergence. Each cell's permeate inlet/outlet mass-flow states must follow the physical permeate direction, not the feed-coordinate order.

### Why the variable mass matters

The temperature is not updated as (T_{out}=T_{in}pm Q/(dot m_{in}c_p)). Instead, first calculate the outlet specific enthalpy using the **outlet** mass flow, then invert the appropriate fluid enthalpy correlation. This captures the change in both mass flow and feed composition without treating (c_p) as constant.

### No double counting

Under the Wyon Eq. (18) convention above, (Q_i) is the net total stream enthalpy-rate change for the cell. The changing mass is already present in (dot m_{out}h_{out}). Do not add (m_{v,i}h_v) again. A separate phase-resolved formulation is also possible, but it must define liquid and vapour enthalpies at both membrane interfaces, a common datum, and the conductive term, and then derive a different expression for (Q_i). Mixing the two conventions is invalid.

## 4. Global cell identity

Adding the feed and permeate balances gives:

```text
m_f,out,i*h_f,out,i + m_p,out,i*h_p,out,i
  = m_f,in,i*h_f,in,i + m_p,in,i*h_p,in,i
```

This is the cell-level combined-stream enthalpy identity under the Wyon convention. The (+Q_i) and (-Q_i) terms cancel exactly. Across all cells, internal stream enthalpy rates telescope, leaving the module boundary identity:

```text
m_f,in*h_f,in + m_p,in*h_p,in
  = m_f,out*h_f,out + m_p,out*h_p,out
```

The identity is algebraic; implementation tests must still independently check local residuals, salt conservation, positive mass flow, and convergence of the counter-current boundary-value iteration.

## 5. Required implementation safeguards

An opt-in axial Wyon-enthalpy mode should not silently replace the existing generic constant-(c_p) mode. Before implementation:

1. Keep the existing sensible-(c_p) path as the backward-compatible default.
2. Add an explicitly named Wyon enthalpy mode and use Wyon Appendix A domain guards for temperature and salinity.
3. Use the existing `wyon_specific_enthalpy_j_kg` and `wyon_temperature_from_specific_enthalpy_c` functions; do not substitute constant-(c_p) integration.
4. Reject non-finite or non-positive outlet mass flow and enthalpy states outside the inversion bracket.
5. Compute feed salinity after every cell from conserved salt mass and current feed mass flow.
6. In counter-current operation, test the correct permeate inlet and outlet mass-flow indexing at each cell.
7. Preserve reporting-duration invariance: rates and temperatures must not depend on the arbitrary reporting duration; integrated masses and duties scale with duration.
8. Expose per-cell feed, permeate, and combined-stream enthalpy residuals in diagnostics.

## 6. Minimum tests before enabling the mode

- Zero permeation with nonzero conduction: recover the constant-mass Wyon enthalpy balance.
- Nonzero permeation: feed mass decreases, permeate mass increases, salt mass is conserved, and both local stream enthalpy balances close.
- Combined-stream cell residual is near numerical precision.
- Integrated module boundary enthalpy identity closes for co-current and counter-current cases.
- Counter-current permeate indexing reverses correctly and the boundary-value iteration converges.
- Duration invariance for temperatures, fluxes, and mass-flow rates; integrated product mass and heat scale linearly with duration.
- Wyon enthalpy inversion rejects unsupported temperature/salinity states rather than extrapolating.
- Existing default sensible-(c_p) regression tests remain unchanged.

## 7. Important limitations

- Applying Wyon Eq. (18), originally stated for a lumped module, independently to each axial cell is a **finite-volume extension**. It is mathematically conservative under the stated convention, but its physical fidelity requires comparison with a source that reports local axial measurements or a fully specified module model.
- The current surface solver's (q_{tot}=q_{latent}+q_{conductive}) closure and its latent-heat input remain model assumptions. The enthalpy update does not independently validate the chosen latent-heat value or its reference temperature.
- Wyon enthalpy and fluid-property correlations are empirical fits with stated domains. The implementation should preserve those domains and must not imply that the Wyon model has been experimentally validated for all current research cases.
- The generic IAPWS/Nayar paths and Wyon-specific enthalpy mode are distinct model choices. Do not combine a Wyon enthalpy function with another property model without explicitly declaring and justifying the hybrid.

## 8. Decision

The next implementation candidate is an **opt-in axial Wyon enthalpy mode**, derived from the existing Wyon lumped module convention. Do not modify the default channel solver or claim full validation. Implement only after this derivation is reviewed against the thesis equations and the minimum tests above are specified.

## Source

Annie Wyon (2025), *Desalination utilizing data centre waste heat: A techno-economic study*, Lund University, report LUTFD2/TFEM--25/5229--SE, Section 3.2.2, Eqs. (18)–(20), and Appendix A, Eqs. (A11)–(A12).

Official thesis record: https://lup.lub.lu.se/student-papers/record/9198095  
PDF: https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf
