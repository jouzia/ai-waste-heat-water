# Property-source and solver verification gate (2026-10-28)

## Official source checked

The official MIT Seawater Library page identifies:
- Code version 3.1.5 dated 7 August 2024.
- Property tables version dated 9 December 2023.
- Specific heat capacity as `SW_SpcHeat(T, S, P)`, with documented range 0–180 °C, 0–180 g/kg, 0–12 MPa.
- Latent heat of vaporization as `SW_LatentHeat(T, S)`, with documented range 0–200 °C, 0–240 g/kg at the library's defined reference pressure convention.
- A correction to the Jamieson specific-heat coefficient, explicitly noting the corrected coefficient (b_3=-3.15\times10^{-6}), rather than the positive sign printed in the original source.
- Correlations described in the 2010 Sharqawy et al. review and the 2016 Nayar et al. review with pressure dependence.

Official references:
- MIT library: https://web.mit.edu/seawater/
- Version history: https://web.mit.edu/seawater/Version_History_07Aug24-pdf-3a.pdf
- Sharqawy et al. (2010): https://doi.org/10.5004/dwt.2010.1079
- Nayar et al. (2016): https://doi.org/10.1016/j.desal.2016.02.024

## What this establishes—and what it does not

This independently confirms that the official library exists, identifies function signatures, supported ranges, version dates, and the corrected specific-heat coefficient. It does **not** prove that the public-mirror source transcription in the exploratory solver is byte-identical to the official v3.1.5 archive. The official archive was not checksum-verified in this audit.

The official library's specific-heat function takes pressure, while the latent-heat function does not. A defensible property adapter therefore needs to preserve each function's distinct input contract instead of forcing both through one generic interface.

## Code-review findings for the audit-only solver

The current reference solver correctly keeps the property values explicit and does not silently call the project production thermodynamics. Its tests verify algebraic residuals and expected smoke-test outputs for the selected provisional values. Those tests are regression tests for the implementation under those inputs, not independent physical validation.

One domain restriction needs further source confirmation before broader use: the solver currently requires `minimum_delta_t_h_out_c <= delta_t_h_in_c` and selects roots only within that interval. The SI explicitly gives a minimum `delta_T_h,out >= 0.5 °C`; it does not, in the accessible equation text, establish `delta_T_h,out <= delta_T_h,in` as a universal mathematical constraint. This upper bound may be appropriate for the plotted operating cases but must not be presented as a source-stated general constraint without additional evidence.

## Next verification steps

1. Obtain and checksum the official v3.1.5 archive, or transcribe the exact equations from the official code files and compare them line-by-line against the mirror.
2. Implement a property adapter only after that source comparison, with independent explicit inputs for temperature, salinity, and pressure as required by each function.
3. Remove or justify the upper-root bound against the SI definitions, and test for multiple admissible roots rather than presuming uniqueness.
4. Add tests for input units, function domains, non-finite values, and the two distinct source interpretations of the inlet temperature difference (0.5 °C printed constraint vs 5 °C prose/main text).
5. Keep all anchor comparisons unfitted and labeled as figure-read targets with rounding uncertainty.

## Gate

**Not a reproduction yet.** The official source's existence, version, property ranges, and specific-heat correction are confirmed. Exact implementation provenance, property-call states, the printed constraint discrepancy, and the solver's general root admissibility remain open.
