# Malaguti AGMD three-issue audit checkpoint (2026-11-01)

## Scope and current baseline

This note consolidates the three open questions for the audit-only configuration-3 AGMD reference solver. It does not change production thermodynamics, the production net-water ledger, or the provisional property fixture.

Repository baseline: `9fe93b7a3ba7dfe7c906188538d0d5e906c20862` (PR #21 merge commit).

PR #21 restored the counterfactual freshwater-displacement calculation in the production water ledger. Its final commit passed CI: 177 tests passed, 1 skipped, and Ruff passed. That software result is independent of the AGMD reproduction gate.

## Issue 1 — Is ΔT_h,out ≤ ΔT_h,in a universal constraint?

### Finding

The earlier supplementary-equation-only review did not identify a clear upper bound. A subsequent full-text review of the main article adds important configuration-specific evidence: for configuration 3, the authors state that STEC is systematically higher, consistent with ΔT_h,in > ΔT_h,out, and describe single-pass recovery as bounded by the imposed ΔT_h,in = 5 °C and the minimum achievable ΔT_h,out = 0.5 °C. The article defines ΔT_h,in = T_h,in − T_c,out and ΔT_h,out = T_h,out − T_c,in. This supports ΔT_h,out < ΔT_h,in as a paper-domain condition for the analyzed configuration-3 regime, even though it is not a universal inequality for arbitrary heat exchangers.

The implementation therefore:
- enforces the supplied minimum outlet difference (default 0.5 °C);
- enforces the configuration-3 paper-domain ordering ΔT_h,out < ΔT_h,in by default;
- permits a caller to supply `maximum_delta_t_h_out_c` when testing an explicitly declared operating policy;
- checks the algebraic recovery interval 0 < R ≤ 1; and
- rejects zero or multiple roots that survive the selected model-admissibility filter.

A synthetic regression case demonstrates that the equations alone can admit a root above ΔT_h,in when the paper-domain terminal-order filter is disabled. This is an algebraic counterexample only. The case uses independently selected heat capacities and has no source-backed mapping to the same saline loop in the hot and cold channels; it is **not** evidence of a physically admissible point in the paper's configuration-3 operating domain.

### Disposition

Retain the configuration-3 terminal-order filter in paper-domain mode, with ΔT_h,out < ΔT_h,in. Keep an explicit algebraic-diagnostic mode for examining roots outside that domain; do not report those roots as paper-domain or physically admissible solutions. This is configuration-specific, not a universal heat-exchanger law.

## Issue 2 — Are the seawater property inputs source-matched?

### Confirmed source contracts

The official MIT Seawater Library page identifies code version 3.1.5 (7 August 2024), while the separately published property tables are identified as library version 3.1.3 with table updates through 9 December 2023.

The relevant function contracts differ:
- specific heat: `SW_SpcHeat(T, S, P)`, with documented validity range T = 0–180 °C, S = 0–180 g/kg, and P = 0–12 MPa;
- latent heat: `SW_LatentHeat(T, S)`, with documented validity range T = 0–200 °C and S = 0–240 g/kg, evaluated at the library's `P₀` convention rather than an arbitrary caller-supplied pressure.

MIT defines `P₀` as 0.101325 MPa for T ≤ 100 °C and as the vapor pressure of seawater for T > 100 °C. Therefore the latent-heat input state must record temperature and salinity, and the implied pressure convention; it must not be treated as a freely pressure-adjustable function. By contrast, the specific-heat function explicitly accepts pressure. These are different state contracts, not interchangeable calls.

The official documentation states that its atmospheric-pressure seawater specific-heat correlation is based on Jamieson et al. (1969), with the coefficient correction b₃ = −3.15 × 10⁻⁶ (not positive); the pressure-dependent library correlation is exposed through `SW_SpcHeat(T,S,P)`. The MIT note says the typo was corrected in Sharqawy et al. (2010) and in all MIT codes. These facts establish the documented API, ranges, and correlation lineage; they do not verify that an independently obtained archive is identical to the official v3.1.5 download.

The underlying 2010 review makes the latent-heat mass basis explicit. Its recommended ideal-solution relation is `h_fg,sw = h_fg,w × (1 − S/1000)` (Eq. 37), where S is seawater salinity in g/kg: pure-water latent heat is per kg of water, while the seawater value is per kg of total saline solution. The review also gives a non-ideal expression (Eq. 39) with an osmotic-coefficient derivative correction and reports that this correction is small enough to neglect for its recommendation. This is a useful independent check on units and mass basis, but it must not be silently applied twice if the library routine already returns a seawater-basis value.

For specific heat, the 2010 review's Jamieson correlation (Eq. 9, Table 3) is reported in kJ/(kg K), over 0–180 °C and 0–180 g/kg, with maximum deviation ±0.28%; it is expressed in the original temperature/salinity scales shown in that table. The review explains that recommended equations are converted to ITS-90 and reference-composition salinity for comparison and use. The v3.1.5 function's explicit pressure argument is therefore important: a direct evaluation must use the intended pressure-dependent implementation, not simply copy Eq. 9 as though it were a pressure-general formula.

### Unresolved provenance and state

The official v3.1.5 archive bytes have not been independently obtained and checksum-matched against an official MIT checksum/signature. The official MIT page links the archive as `https://web.mit.edu/seawater/SEAWATER_v3.1.5_07Aug24.zip`; a direct retrieval attempt during this checkpoint was unsuccessful, and the browser could not inspect the ZIP MIME payload. This is an access limitation, not evidence that the official archive is missing or corrupt. No official checksum/signature was found in the accessible version-history or download documentation.

The version-history notes add a useful qualification: v3.1.5 (2024-08-07) records a revision to the MATLAB internal-energy routine; v3.1.4 (2017-02-20) records EES unit annotations; v3.1.3 (2016-12-21) records a kinematic-viscosity pressure-unit correction. No specific-heat or latent-heat code change is listed in those release notes between v3.1.3 and v3.1.5. This makes the v3.1.3 property tables potentially useful for carefully scoped spot checks of those functions, but it does not authenticate the v3.1.5 archive, establish complete code/table identity, or replace inspection of the actual routines. The inspected public mirror is a lead only: its filename is not proof of byte identity, and its inspected Python rewrite does not supply a verified matched pair of the required specific-heat and latent-heat routines.

The article identifies saline feed, complete salt rejection, pure distillate, a 20 °C cold inlet, and a 5 °C hot-inlet terminal difference. It does not, in the accessible text, unambiguously specify numerical feed salinity and each stream property's evaluation temperature. The cold-channel heat capacity must not be silently treated as pure-water heat capacity; distillate heat capacity is a separate pure-water stream property. The specific-heat pressure input and latent-heat reference-pressure convention must remain distinct. For configuration 3, the main article further describes the same saltwater stream circulating through the hot/feed and cold/cooling channels in a closed circuit, with make-up water added to compensate for vapor losses. Accordingly, hot- and cold-channel heat capacities are linked evaluations for that saline circuit, not independent arbitrary fluid choices; their evaluation temperatures and exact composition/state mapping still need to be specified. The distillate remains a separate pure-water stream.

The current smoke-test values (cₕ = 4000, c꜀ = 4000, c_d = 4180 J kg⁻¹ K⁻¹; h_vap = 2.4 MJ kg⁻¹) remain provisional and are not claimed to be MIT/Sharqawy outputs.

### Disposition and acceptance evidence

Do not implement or label a source-matched adapter until one of the following is available:
1. the official v3.1.5 archive bytes and a recorded SHA-256 compared with an official checksum/signature or another independently authenticated official copy; or
2. the relevant official MATLAB source files obtained through a verifiable MIT source path, with direct transcription and review of both function implementations.

Then record each property's stream identity, T, S, P/reference-pressure convention, units, validity range, and source line/function. Keep IAPWS-08 as a separate comparison, not a silent replacement.

## Issue 3 — What is the solver's admissible-root domain, and can uniqueness be claimed?

### Algebraic necessary conditions

Let x = ΔT_h,out. From S2 as transcribed in the reference solver:

R = η cₕ (ΔT − x) / h_vap.

For positive η, cₕ, h_vap and the solver's algebraic filter 0 < R ≤ 1, this implies:

- x < ΔT, from R > 0;
- x ≥ ΔT − h_vap/(η cₕ), from R ≤ 1;
- x ≥ 0.5 °C, from the default supplementary minimum;
- ΔT_h,in < ΔT, an input consistency condition enforced by the current function.

Thus the necessary algebraic interval is:

max(0.5 °C, ΔT − h_vap/(η cₕ)) ≤ x < ΔT.

An explicitly supplied `maximum_delta_t_h_out_c` can further truncate this interval. This interval is necessary under the implemented S2 relation and selected algebraic constraints; it is not a complete thermodynamic/physical admissibility proof. Additional physical conditions require source-backed stream definitions and temperature ordering.

### Root count and uniqueness

After substitution of S2 into S8, the current implementation solves a polynomial of degree at most two. Depending on the supplied inputs and admissibility interval, there can be:
- no admissible real root;
- exactly one admissible real root; or
- two admissible real roots.

The code enumerates real roots, filters them, and returns a result only when exactly one survives. Synthetic tests exercise zero-root and two-root rejection. Those adversarial cases test defensive behavior only; they do not establish that zero or multiple roots occur in the paper's physical operating domain.

The four provisional smoke cases each return one admissible root. That observation is not a proof of uniqueness outside those four points, nor over a continuous operating region.

### Required domain study before any uniqueness statement

A defensible domain study still requires source-backed ranges and operating-state definitions for η, ΔT, ΔT_h,in, T_c,in, cₕ, c꜀, c_d, and h_vap. The study should then:
1. publish the exact parameter domain and property-state mapping before running the grid;
2. enumerate all real roots at each point, not rely on a single initial guess;
3. classify roots separately by algebraic admissibility and any independently justified physical constraints;
4. report zero/one/multiple-root counts, boundary cases, and sensitivity to property uncertainty;
5. retain all failed or ambiguous points in the output; and
6. keep figure-anchor comparisons unfitted and account for one-decimal-place reporting/reading uncertainty.

This source-backed domain scan is currently blocked by Issue 2. No claim of global uniqueness or physical validity is warranted.

## Current gate summary

| Issue | Current result | Remaining gate |
|---|---|---|
| Configuration-3 terminal ordering | Enforced as ΔT_h,out < ΔT_h,in in paper-domain mode; disabled only for algebraic diagnostics | Source-matched stream properties and full supplementary-equation audit remain open |
| MIT/Sharqawy property provenance | Official API/version context confirmed; archive identity and stream-state inputs unresolved | Authenticated v3.1.5 source plus explicit property-state mapping |
| Root-domain/uniqueness | Necessary algebraic interval derived; zero/one/two-root behavior handled in code | Source-backed operating/property domain and full root enumeration |

**Reproduction status: NOT YET REPRODUCED.** Passing tests confirms implementation behavior under stated inputs. It does not validate the source property implementation, reproduce the article's four reported recovery anchors, establish physical realizability, or prove global root uniqueness.

## References

- Malaguti et al. (2026), DOI: https://doi.org/10.1016/j.desal.2026.120039
- MIT Seawater Library: https://web.mit.edu/seawater/
- MIT version history: https://web.mit.edu/seawater/Version_History_07Aug24-pdf-3a.pdf
- MIT property tables (library v3.1.3): https://web.mit.edu/seawater/2017_MIT_Seawater_Property_Tables_r2b_2023c.pdf
- Sharqawy et al. (2010), DOI: https://doi.org/10.5004/dwt.2010.1079
- Nayar et al. (2016), DOI: https://doi.org/10.1016/j.desal.2016.02.024
- Exploratory public mirror (not authenticated as byte-identical to MIT): https://github.com/djessop/sw_properties
