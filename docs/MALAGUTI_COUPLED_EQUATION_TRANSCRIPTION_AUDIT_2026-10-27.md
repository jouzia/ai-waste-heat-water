# Malaguti SI Equation Audit: Coupled Module Equations (2026-10-27)

## Scope

This audit transcribes the supplied supplementary-information PDF, pages S2–S6, for the coupled recovery/temperature equations. It is an equation transcription and consistency audit, not an independent numerical reproduction.

Source: Malaguti et al., “Waste Heat Won’t Make Membrane Distillation Cool: Thermodynamic Analysis of Cooling and Pumping Burdens,” *Desalination* 628 (2026), 120039, DOI: 10.1016/j.desal.2026.120039. The publisher-hosted article is listed by the authors' institutional research portal: https://vbn.aau.dk/en/publications/waste-heat-wont-make-membrane-distillation-cool-thermodynamic-ana-2/

## Equations as printed in the supplied SI

The SI defines vaporization efficiency as:

\[
\eta = \frac{\dot m_d h_{vap}}{\dot Q_{lost,h}}
\tag{S1}
\]

Under its constant-hot-channel-specific-heat assumption and recovery definition \(R=\dot m_d/\dot m_{h,in}\), it reduces this to:

\[
\eta = \frac{R h_{vap}}{c_h(\Delta T-\Delta T_{h,out})}.
\tag{S2}
\]

For DCMD, the SI gives the module heat balance:

\[
\Delta T_{h,in}\left(1+R\frac{c_c}{c_h}\right)
-\Delta T_{h,out}(1-R)
=R\left(\frac{c_c}{c_h}T_{h,in}-T_{c,in}\right).
\tag{S4}
\]

The printed constraint in Equation S5 is \(\Delta T_{h,out}\ge 0.5\) and \(\Delta T_{h,in}=0.5\). However, the prose immediately below S5 says \(\Delta T_{h,in}\) is fixed at 5 °C and only values of \(\Delta T_{h,out}\ge0.5\) °C are considered. The later main-text description also states \(\Delta T_{h,in}=5\) °C. This is a source-internal discrepancy; the audit does not silently choose one value.

For AGMD, the SI gives:

\[
(R-1)c_h(\Delta T_{h,out}+T_{c,in})
=R c_d T_d + T_{h,in}(c_c-c_h)-c_c(\Delta T_{h,in}+T_{c,in})
\tag{S7}
\]

and

\[
T_d = \frac{T_{h,in}+(T_{c,in}+\Delta T_{h,out})}{2}.
\tag{S8a}
\]

The three-equation AGMD system combines S2, S7, and S8a. The printed constraint line under Equation S8 again states \(\Delta T_{h,in}=0.5\), while the prose on SI page S5 states the inlet transmembrane difference is fixed at 5 °C. Treat this as the same unresolved discrepancy.

## Property-evaluation conventions supported by the SI

- The SI explicitly assumes specific heat does not substantially change along each channel for the coupled module balance and uses inlet-condition specific heat in the derivation (page S2).
- In the reference-system energy analysis, the SI states that the selected specific heat is at the hot-channel inlet for configuration 1 (page S5).
- The SI states seawater is the feed and distillate water is the cold-channel fluid for the reference analysis, with property values based on Sharqawy et al.; cold-channel inlet temperature is 20 °C, and the inlet transmembrane temperature difference is described in prose as 5 °C (page S5).
- The supplied SI excerpt does not fully specify a universal evaluation temperature and salinity for every property in the coupled S2/S4 and S2/S7/S8 systems. Do not infer one global convention beyond what is stated.

## Implementation gate

Before implementing a production solver, independently establish the exact property definitions and evaluation states from the article's cited Sharqawy correlations, and retain both candidate interpretations of the 0.5 °C versus 5 °C discrepancy in an explicit audit test or configuration. A solver must not tune property values to the four plotted recovery anchors. The plotted values can be treated as validation targets only after the equations and property states have been fixed independently.

The recovery anchors discussed in the project are figure-read values, not tabulated ground truth. Any numerical comparison must disclose figure-digitization uncertainty, solver tolerances, property-model version, and which interpretation of the contradictory constraint was used.

## Status

**Open / not independently reproduced.** This document records the printed equations and unresolved source inconsistency. It does not claim that the reported recovery anchors have been reproduced, that the model has been empirically validated, or that the research establishes a net-water benefit.
