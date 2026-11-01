# AGMD latent-heat and recovery mass-basis audit

**Status:** source-supported interpretation of the publisher SI; numerical reproduction remains **NOT REPRODUCED**.

## Scope

This audit follows the equations in Malaguti et al. (2026), *Waste Heat Won't Make Membrane Distillation Cool: Thermodynamic Analysis of Cooling and Pumping Burdens*, Supporting Information, §§1.1–1.2, equations S1–S16. It distinguishes what the SI explicitly defines from consequences of those definitions.

## 1. Recovery definition

The SI defines single-pass water recovery immediately before Eq. S2 as

\[
R = \frac{\dot m_d}{\dot m_{h,in}},
\]

where \(\dot m_d\) is distillate production and \(\dot m_{h,in}\) is hot-channel feed inlet mass flow. Thus R is a distillate-to-hot-feed mass-flow ratio, not a ratio to the cold-channel circulation flow or to makeup flow.

The derivation of S2 also assumes \(\dot m_d\ll\dot m_{h,in}\), and treats hot-channel specific heat as approximately constant, evaluated at hot-channel inlet conditions. This is an approximation stated by the authors, not an exact finite-depletion balance.

## 2. Latent-heat basis in S1–S2

Equation S1 writes the vapour heat rate as

\[
\dot Q_{mass}=\dot m_d h_{vap}.
\]

The SI defines this as the heat rate transferred by water vapour flowing across the membrane. The mass rate multiplying \(h_{vap}\) is the distillate/vapour mass rate \(\dot m_d\). The main article describes complete salt rejection and pure distillate.

**Interpretation:** in this term, \(h_{vap}\) must be the enthalpy/latent-heat quantity on a per-kilogram-of-vapour (pure-water) basis. Sharqawy et al. (2010) Eq. 37, \(h_{fg,sw}=h_{fg,w}(1-S_R/1000)\), is a latent heat per kilogram of saline solution. Applying that seawater-solution mass correction to the \(\dot m_d h_{vap}\) term would mix the solution mass basis with the pure distillate mass flow.

Accordingly, the AGMD solver's S2/S8 \(h_{vap}\) input should use the pure-water latent-heat correlation (Sharqawy et al. Eq. 54, at an explicitly justified evaluation temperature), unless a separate source establishes a different definition. Do not apply Eq. 37 to this term. Eq. 37 remains a valid property correlation for a distinct saline-solution mass basis; it is not the basis of S1's vapour enthalpy flow.

## 3. Heat capacities and stream identities

- S2: \(c_h\) is the hot-channel feed specific heat; the SI says it is selected at hot-channel inlet conditions and treated as approximately constant along that channel.
- S6: the AGMD/gap energy balance explicitly includes \(\dot m_d c_d T_d\), identifying \(c_d\) as the distillate-stream heat capacity.
- S7–S8: the cold-channel stream has its own \(c_c\) term; S7 additionally invokes water makeup before the cold-channel inlet to compensate for distillate leaving the module.
- The main article's configuration-3 description identifies a saline stream circulating through the hot/feed and cold/cooling channels, with makeup water compensating vapour losses. Therefore \(c_h\) and \(c_c\) are seawater-property inputs at their respective inlet states, while \(c_d\) is a pure-water/distillate-property input at the distillate state.

The SI does not provide the numerical salinity or exact temperature evaluation states for these properties in the equations reproduced here. Those inputs must remain explicit assumptions or be recovered from additional source material; they must not be tuned to the rounded recovery anchors.

## 4. What the audit does and does not establish

Established from the SI:
1. \(R=\dot m_d/\dot m_{h,in}\).
2. \(\dot Q_{mass}=\dot m_d h_{vap}\).
3. The S1–S2 vapour enthalpy term uses the distillate/vapour mass basis, so the pure-water latent-heat correlation is the consistent Sharqawy input for this term.
4. \(c_h\) is an inlet-state hot-feed property; S6–S8 distinguish distillate heat capacity and cold-channel heat capacity.
5. The AGMD gap balance includes makeup-water accounting.

Not established:
- The numerical salinity used for the article's property calls.
- Exact evaluation temperatures for \(c_h\), \(c_c\), \(c_d\), and \(h_{vap}\).
- A complete independent reproduction of the four Figure 4 recovery anchors or the article's operating-point metrics.

## 5. Required implementation discipline

- Keep \(h_{vap}\) as pure-water latent heat per kg distillate in S2/S8.
- Keep seawater heat capacities and distillate heat capacity as separate explicit inputs.
- Retain the seawater latent-heat helper as a separately documented correlation, but do not feed it into the S1/S2 vapour term.
- Do not select property states by minimizing error against the article's rounded Figure 4 values.
- Any future sensitivity analysis must predeclare salinity and property-state ranges and report the full envelope, not a best-fit point.

## Sources

- Malaguti et al. (2026), publisher Supporting Information, §§1.1–1.2, Eqs. S1–S16; in particular S1–S2 and S6–S8.
- Malaguti et al. (2026), main article, *Desalination* 628, 120039, DOI: https://doi.org/10.1016/j.desal.2026.120039.
- Sharqawy, Lienhard & Zubair (2010), “Thermophysical properties of seawater: a review of existing correlations and data,” *Desalination and Water Treatment* 16, 354–380, DOI: https://doi.org/10.5004/dwt.2010.1079; Eq. 37 (seawater-solution latent-heat basis) and Eq. 54 (pure-water latent heat).

**Reproduction status: NOT REPRODUCED.** This audit resolves the mass basis of the vapour enthalpy term; it does not recover the article's undisclosed property states or demonstrate numerical reproduction.
