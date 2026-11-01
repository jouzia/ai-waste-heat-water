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
- specific heat: `SW_SpcHeat(T, S, P)`, with temperature, salinity, and pressure inputs;
- latent heat: `SW_LatentHeat(T, S)`, using the library's reference-pressure convention.

The official documentation also records the corrected Jamieson specific-heat coefficient b₃ = −3.15 × 10⁻⁶. These facts establish the documented API/version context; they do not verify that an independently obtained archive is identical to the official v3.1.5 download.

### Unresolved provenance and state

The official v3.1.5 archive bytes have not been independently obtained and checksum-matched against an official MIT checksum/signature. The inspected public mirror is a lead only: its filename is not proof of byte identity, and its inspected Python rewrite does not supply a verified matched pair of the required specific-heat and latent-heat routines.

The article identifies saline feed, complete salt rejection, pure distillate, a 20 °C cold inlet, and a 5 °C hot-inlet terminal difference. It does not, in the accessible text, unambiguously specify numerical feed salinity and each stream property's evaluation temperature. The cold-channel heat capacity must not be silently treated as pure-water heat capacity; distillate heat capacity is a separate pure-water stream property. The specific-heat pressure input and latent-heat reference-pressure convention must remain distinct.

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
