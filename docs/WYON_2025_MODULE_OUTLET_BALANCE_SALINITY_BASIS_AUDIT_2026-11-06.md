# Wyon 2025 Module Outlet Balances and Salinity Basis Audit

**Date:** 2026-11-06  
**Status:** Lumped one-pass implementation with explicit mass and energy conservation; not an axial module reproduction.

## Source equations

Wyon Section 3.2.2 uses:

- Eq. (18): (q_{tot} A_m = H_{f,in}-H_{f,out}=H_{p,out}-H_{p,in})
- Eq. (19): (H=\dot m h=\dot V\rho h=v A_{channel}\rho h)
- Eq. (20): (\frac{\dot m_{f,in}}{\rho_{f,in}}S_{f,in}=\frac{\dot m_{f,out}}{\rho_{f,out}}S_{f,out})

Appendix A11 explicitly labels its salinity variable (S) in kg/kg. Eq. (20), however, is written in volumetric-flow form ((\dot m/\rho)S). These two salinity bases must not be conflated.

## Dimensional interpretation of Eq. (20)

Let:

- (w_s) be salt mass fraction in kg salt/kg solution;
- (C_s) be salt mass concentration in kg salt/m³ solution;
- (\rho) be solution density in kg/m³;
- (\dot V=\dot m/\rho) be volumetric flow in m³/s.

Then:

[
C_s=\rho w_s
]

and the dimensionally consistent volumetric salt balance is:

[
\dot V_{in} C_{s,in}=\dot V_{out} C_{s,out}
]

Substituting (\dot V=\dot m/\rho) and (C_s=\rho w_s) gives:

[
\dot m_{in} w_{s,in}=\dot m_{out} w_{s,out}
]

Therefore Eq. (20) is consistent if its (S_f) denotes **volumetric salt concentration** (kg/m³). If (S_f) is instead interpreted as the Appendix A11 mass fraction (kg/kg), the displayed volumetric-flow equation is dimensionally inconsistent. The thesis does not explicitly state the Eq. (20) salinity unit next to the equation.

The implementation avoids this ambiguity by conserving salt on a mass-fraction basis and then independently evaluating the equivalent volumetric form using (C_s=\rho w_s).

## Implemented lumped balance

The module inlet mass flow rates follow Eq. (19):

[
\dot m_{f,in}=v_f A_{channel}\rho_{f,in},\qquad
\dot m_{p,in}=v_p A_{channel}\rho_{p,in}
]

The membrane water transfer rate is:

[
\dot m_{tr}=J A_m
]

The feed and permeate outlet mass flows are then:

[
\dot m_{f,out}=\dot m_{f,in}-\dot m_{tr},\qquad
\dot m_{p,out}=\dot m_{p,in}+\dot m_{tr}
]

Feed salt mass is conserved:

[
w_{s,out}=\frac{\dot m_{f,in}w_{s,in}}{\dot m_{f,out}}
]

The total heat-transfer rate is:

[
Q=q_{tot}A_m
]

Outlet specific enthalpies are obtained from:

[
h_{f,out}=\frac{\dot m_{f,in}h_{f,in}-Q}{\dot m_{f,out}}
]

[
h_{p,out}=\frac{\dot m_{p,in}h_{p,in}+Q}{\dot m_{p,out}}
]

The temperatures are recovered by inverting Wyon Appendix A Eqs. (A11) and (A12). The implementation checks both enthalpy-rate balances and both equivalent salt-balance forms.

## Scope and limitations

- This is a **lumped one-pass module calculation**. It treats the local coupled surface solution as representative of the supplied membrane area.
- It does not resolve axial temperature, salinity, velocity, or flux profiles.
- It does not model pressure drop, pump work, heat-exchanger performance, or the downstream plant.
- The model is only evaluated within the implemented 0–100°C and property-correlation salinity domains.
- This is a physically explicit implementation of the conservation balances, not proof that every modelling approximation matches Wyon's unpublished calculation details.

## Reproduction

Run:

```bash
pytest -q tests/test_wyon_2025_module_outlets.py tests/test_wyon_2025_enthalpy.py
```

The tests check water mass transfer, salt conservation, Eq. (20)'s volumetric form, feed/permeate enthalpy rates, and invalid-input handling.

## Source

Annie Wyon (2025), *Desalination utilizing data centre waste heat: A techno-economic study*, Lund University, report LUTFD2/TFEM--25/5229--SE, printed p. 16, Eqs. (18)–(20), and Appendix A, printed p. 43, Eqs. (A11)–(A12).

Official thesis record: https://lup.lub.lu.se/student-papers/record/9198095  
PDF: https://lup.lub.lu.se/student-papers/record/9198095/file/9198100.pdf
