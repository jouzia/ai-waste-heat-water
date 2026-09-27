# Assumptions and Boundary Conditions

This repository is a research model. Values are not automatically empirical just because they are numerically plausible.

## Current model assumptions

1. IT electricity is converted to first-order IT heat on a 1:1 energy basis.
2. Recoverable heat is reduced by recoverable fraction, recovery efficiency, heat-exchanger effectiveness, usable-heat fraction, and any explicit cooling heat penalty.
3. MD mass flux is either a supplied literature/experimental flux or a reduced-order vapor-pressure model.
4. The vapor-pressure model uses NIST SRD 69 pure-water Antoine coefficients within their documented temperature ranges.
5. The primary saline-feed pathway uses IAPWS-08 standard seawater thermodynamics. For single-pass recovery, ideal salt retention increases concentrate salinity and a water-removal-weighted bulk salinity is used for the lumped activity calculation.
6. This single-pass salinity treatment is not concentration polarization. Local concentration boundary-layer effects remain a separate model-form uncertainty.
7. Interface temperatures may be supplied directly; otherwise the current symmetric TPC model is a screening approximation.
8. If membrane latent heat is supplied, membrane conductive heat leak can be calculated from Fourier conduction using membrane-specific conductivity and thickness.
9. If pressure drop and pump efficiency are supplied, pumping electricity is derived from hydraulic power. Otherwise the legacy specific pumping-energy input is used.
10. MD cooling duty is a thermal burden and may be assigned electricity and/or water consumption through explicit scenario parameters.
11. Feed withdrawal and concentrate discharge are reported separately from freshwater consumption.
12. Electricity-related water is represented by an explicit grid water factor. This factor is a site/boundary parameter, not a universal constant.
13. The primary screening metric is Delta_W_net = W_additional_consumption - W_recovered. It does not by itself establish avoided freshwater consumption without an explicit counterfactual.
14. IAPWS-08 validity limits are treated as model constraints; scenarios outside the documented range must not be silently extrapolated.

## Explicitly not assumed

- All AI heat is recoverable.
- All recovered heat is high enough quality for MD.
- Free waste heat implies free cooling.
- Gross distillate equals net freshwater benefit.
- Withdrawal equals consumption.
- Single-pass bulk concentration represents concentration polarization.
- A single membrane flux, permeance, recovery, water activity, grid-water factor, or cooling burden is universal.

## Boundary status

The model is an operational/reduced-order research framework, not a complete ISO-compliant life-cycle assessment. Embodied water, construction, membrane manufacture, replacement, and end-of-life are outside the current operational boundary unless explicitly added.