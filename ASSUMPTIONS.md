# Assumptions and Boundary Conditions

This repository is a research model. Values are not automatically empirical just because they are numerically plausible.

## Current model assumptions

1. IT electricity is converted to first-order IT heat on a 1:1 energy basis.
2. Recoverable heat is reduced by recoverable fraction, recovery efficiency, heat-exchanger effectiveness, usable-heat fraction, and any explicit cooling heat penalty.
3. MD mass flux is either a supplied literature/experimental flux or a reduced-order vapor-pressure model.
4. The vapor-pressure model uses NIST SRD 69 pure-water Antoine coefficients within their documented temperature ranges.
5. Saline-feed effects are represented only through an explicitly supplied water activity. feed_salinity_g_kg is retained as metadata until a validated thermodynamic activity model is implemented.
6. Interface temperatures may be supplied directly; otherwise the current symmetric TPC model is a screening approximation.
7. If membrane latent heat is supplied, membrane conductive heat leak can be calculated from Fourier conduction using membrane-specific conductivity and thickness.
8. If pressure drop and pump efficiency are supplied, pumping electricity is derived from hydraulic power. Otherwise the legacy specific pumping-energy input is used.
9. MD cooling duty is a thermal burden and may be assigned electricity and/or water consumption through explicit scenario parameters.
10. Feed withdrawal and concentrate discharge are reported separately from freshwater consumption.
11. Electricity-related water is represented by an explicit grid water factor. This factor is a site/boundary parameter, not a universal constant.
12. No net-water benefit is claimed unless the modeled recovered water is tied to a defined counterfactual freshwater displacement.

## Explicitly not assumed

- All AI heat is recoverable.
- All recovered heat is high enough quality for MD.
- Free waste heat implies free cooling.
- Gross distillate equals net freshwater benefit.
- Withdrawal equals consumption.
- A single membrane flux, permeance, recovery, water activity, grid-water factor, or cooling burden is universal.

## Boundary status

The model is an operational/reduced-order research framework, not a complete ISO-compliant life-cycle assessment. Embodied water, construction, membrane manufacture, replacement, and end-of-life are outside the current operational boundary unless explicitly added.
