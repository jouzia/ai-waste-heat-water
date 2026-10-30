# MIT Seawater Library Source-Version Audit (2026-10-30)

## Official source evidence

The official MIT Seawater Library page identifies:
- Code version: 7 August 2024.
- Tables version: 9 December 2023.
- Downloadable MATLAB, EES, and Excel VBA code archive: version dated 7 August 2024.
- Stated seawater temperature and salinity ranges: 0–120 °C and 0–120 g/kg, with pressure validity varying by property.
- Pressure dependence is incorporated for thermodynamic functions over 0–12 MPa; selected transport/colligative functions use an implicit reference-pressure convention.

Official page: https://web.mit.edu/seawater/

The official version-history PDF identifies code version 3.1.5 dated 2024-08-07. Its listed change is a revision to the MATLAB internal-energy function's handling of non-standard units in calls to density and enthalpy functions. This confirms the version label and release date; it does not independently expose the full source code for every function.

Official version history: https://web.mit.edu/seawater/Version_History_07Aug24-pdf-3a.pdf

## Important version distinction

The publicly indexed MIT property-table PDF identifies itself as library version 3.1.3 (December 21, 2016), with tables updated through December 2023. It is useful as an official tabular reference, but it is **not** the 3.1.5 code archive and must not be described as such.

Official table PDF: https://web.mit.edu/seawater/2017_MIT_Seawater_Property_Tables_r2b_2023c.pdf

Accordingly:
- The public code mirror previously transcribed in this project is not verified against the official 3.1.5 archive.
- The 3.1.3 tables can provide independent reference-point checks only where the property, temperature, salinity, pressure, and units align.
- A match to a 3.1.3 table value does not prove byte-level or equation-level equivalence to the 3.1.5 implementation.
- Do not label the exploratory solver's property layer “MIT v3.1.5”.

## Property implications for this project

The official MIT page requests citation of both Nayar et al. (2016), which includes pressure-dependent correlations, and Sharqawy et al. (2010), the earlier review. Malaguti et al. cite Sharqawy et al. (2010) for their temperature-/salinity-dependent properties. The project must therefore distinguish:
1. the correlation family explicitly cited by Malaguti;
2. the exact MIT library implementation/version used for an independent check; and
3. the actual property evaluation states used in the AGMD coupled equations.

These are related but not interchangeable claims.

## Gate

**Official release identity verified; exact source implementation still unverified.** Do not close the property provenance gate until the official archive has been inspected or the equations have been independently transcribed from the cited literature with matching conventions. The 3.1.3 tables may be used as bounded spot checks, not as a substitute for the 3.1.5 source archive.
