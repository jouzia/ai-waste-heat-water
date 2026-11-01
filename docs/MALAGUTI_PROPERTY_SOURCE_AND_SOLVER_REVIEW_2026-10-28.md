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


## Source-state constraints confirmed from the published article

The accessible main article states that seawater is the feed, salt rejection is complete, and the produced distillate is pure water. It fixes the cold-stream inlet at 20 °C and the hot-inlet terminal difference at 5 °C. It says density, latent heat, and specific heat are evaluated from temperature- and salinity-dependent Sharqawy correlations.

However, the accessible article text does not provide a numerical feed salinity or fully specify the property evaluation temperature for each stream-specific heat capacity and latent heat. Those omissions prevent a defensible numerical property adapter from being selected solely from the main article. Do not assume 35 g/kg or evaluate every property at a single arbitrary temperature without a source-backed convention or a clearly separated sensitivity analysis.

The official MIT library page distinguishes the function contracts: `SW_SpcHeat(T, S, P)` includes pressure, whereas `SW_LatentHeat(T, S)` uses the library's defined reference-pressure convention. The official download is labelled code version 3.1.5 (7 August 2024), but the separately published property-table PDF is labelled library version 3.1.3 (with table updates through 9 December 2023). The latter is not a version-matched substitute for validating the v3.1.5 implementation.

References:
- Malaguti et al. (2026), main article: https://doi.org/10.1016/j.desal.2026.120039
- MIT seawater library and function ranges: https://web.mit.edu/seawater/
- MIT v3.1.5 version history: https://web.mit.edu/seawater/Version_History_07Aug24-pdf-3a.pdf
- MIT property tables (v3.1.3, updated 9 December 2023): https://web.mit.edu/seawater/2017_MIT_Seawater_Property_Tables_r2b_2023c.pdf

## Code-review findings for the audit-only solver

The current reference solver correctly keeps the property values explicit and does not silently call the project production thermodynamics. Its tests verify algebraic residuals and expected smoke-test outputs for the selected provisional values. Those tests are regression tests for the implementation under those inputs, not independent physical validation.

The root-domain policy has been revised after code review. The generic solver now enforces the explicitly reported minimum `delta_T_h,out >= 0.5 °C` and the algebraic recovery domain, but does not impose `delta_T_h,out <= delta_T_h,in` as a universal source constraint. Callers may supply `maximum_delta_t_h_out_c` when they intentionally want to test that additional cap as a policy assumption. A synthetic regression test confirms that a root above the inlet terminal difference is not rejected by default; a companion test confirms that the optional cap is enforced. These tests verify software behavior, not physical realizability.

## Next verification steps

1. Obtain and checksum the official v3.1.5 archive, or transcribe the exact equations from the official code files and compare them line-by-line against the mirror.
2. Implement a property adapter only after that source comparison, with independent explicit inputs for temperature, salinity, and pressure as required by each function.
3. The generic upper-root bound has been removed; the optional cap is explicitly caller-controlled. Continue testing multiple-root and no-root cases across a documented input domain rather than presuming uniqueness.
4. Add tests for input units, function domains, non-finite values, and the two distinct source interpretations of the inlet temperature difference (0.5 °C printed constraint vs 5 °C prose/main text).
5. Keep all anchor comparisons unfitted and labeled as figure-read targets with rounding uncertainty.


## Public-mirror provenance inspection (2026-11-01)

The public GitHub repository `djessop/sw_properties` was inspected as a lead for the MIT archive. Its README describes a Python rewrite based on MATLAB files from the MIT seawater site; the checked-in Python modules document older 2016/2024 edits and expose density/viscosity routines. The repository tree also contains a file named `SEAWATER_v3.1.5_07Aug24.zip`, but the filename and presence alone do not establish that its bytes are identical to the official MIT download.

This inspection therefore does **not** close the archive-provenance gate. No cryptographic checksum comparison against a separately obtained official MIT archive, signed release, or official checksum was established. The mirror's README and Python modules are not a substitute for inspecting the v3.1.5 MATLAB source, and the inspected Python API does not provide the required specific-heat and latent-heat functions as a verified matched pair. Do not build or label a source-matched AGMD property adapter from this mirror inspection.

Evidence inspected:
- Mirror repository: https://github.com/djessop/sw_properties
- Mirror README: https://github.com/djessop/sw_properties/blob/main/README.md
- Mirror Python implementation: https://github.com/djessop/sw_properties/blob/main/sw_properties.py
- MIT official library landing page and archive link: https://web.mit.edu/seawater/

**Disposition:** archive identity and v3.1.5 source-level function comparison remain unresolved. The next acceptable evidence is the official archive bytes plus a recorded SHA-256, or an official MIT-published checksum/signature, followed by direct inspection of the specific-heat and latent-heat implementations and their units/domains.

## Gate

**Not a reproduction yet.** The official source's existence, version, property ranges, and specific-heat correction are confirmed. Exact implementation provenance, property-call states, the printed constraint discrepancy, and the solver's general root admissibility remain open.
