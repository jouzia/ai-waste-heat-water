# MIT seawater correlation transcription from a public code mirror

**Audit date:** 2026-10-27  
**Status:** Independent source-code transcription found; not yet an authoritative version match.

## Evidence chain

The official MIT library page identifies code version 3.1.5 (7 August 2024), lists the relevant functions and their validity ranges, and links the official archive:
- Official library: https://web.mit.edu/seawater/
- Official archive URL linked from the page: https://web.mit.edu/seawater/SEAWATER_v3.1.5_07Aug24.zip
- Specific-heat correction note: MIT says the Jamieson coefficient b3 should be negative and gives a corrected Nayar et al. coefficient. That coefficient uses the Nayar equation's own definition and must not be conflated with the variable named B in the implementation below.

The archive download could not be fetched by the current retrieval tools. A public GitHub mirror was inspected as secondary evidence:
- SW_SpcHeat.m: https://github.com/river-shaddock/Honours-Public/blob/b173b7c91527e0695cd483ca7539aee193ec6017/code/misc/mit_seawater_matlab/SW_SpcHeat.m
- SW_LatentHeat.m: https://github.com/river-shaddock/Honours-Public/blob/b173b7c91527e0695cd483ca7539aee193ec6017/code/misc/mit_seawater_matlab/SW_LatentHeat.m

The mirror's exact library-version provenance is not established. It is useful for transcription and cross-checking, but not sufficient to claim an exact match to the official 2024 archive.

## Transcribed equations in the mirrored code

### Specific heat at atmospheric reference pressure

The mirror converts temperature to ITS-90 Celsius and salinity to reference-composition g/kg, then computes:

```text
T68 = 1.00024 * (T90_C + 273.15)
A = 5.328 - 9.76e-2*S + 4.04e-4*S^2
B = -6.913e-3 + 7.351e-4*S - 3.15e-6*S^2
C = 9.6e-6 - 1.927e-6*S + 8.23e-9*S^2
D = 2.5e-9 + 1.666e-9*S - 7.125e-12*S^2
cp_sw_P0 = 1000*(A + B*T68 + C*T68^2 + D*T68^3)  [J/(kg K)]
```

The code adds a pressure correction for non-reference pressures. The target paper's assumed pressure basis must be confirmed before using it. The mirrored function documents approximately 1% accuracy, with some extrapolated subranges; do not generalize the broad nominal range into uniform accuracy.

### Latent heat

The mirror computes pure-water latent heat as:

```text
hfg_w = 2.5008991412e6
      - 2.3691806479e3*T
      + 2.6776439436e-1*T^2
      - 8.1027544602e-3*T^3
      - 2.0799346624e-5*T^4   [J/kg]
hfg_sw = hfg_w*(1 - 0.001*S) [J/kg]
```

Here T is ITS-90 Celsius and S is reference-composition salinity in g/kg. The source function documents a 0–200 °C, 0–240 g/kg range and 0.01% accuracy. The code evaluates latent heat at the supplied temperature; it does not decide which temperature Malaguti et al. intended.

## Required before production implementation

1. Inspect the official 2024 archive when an actual archive download is available, compare file contents against the mirror, and record the license.
2. Establish Malaguti's exact property-evaluation convention: temperature(s), salinity, and pressure used for c_h, c_c, and h_vap.
3. Create unit tests at known table points or against official-library outputs, including a 35 g/kg seawater case and the target temperature range.
4. Keep property tests separate from the coupled AGMD equations; only after the property layer passes should the independent nonlinear solver be attempted.

## Gate status

This source-code transcription narrows the property-model uncertainty but does not close it. No production code has been changed, no AGMD recovery anchor has been reproduced, and no empirical validation or net-water benefit is established.
