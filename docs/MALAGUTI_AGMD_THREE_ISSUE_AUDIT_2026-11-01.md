# Malaguti AGMD three-issue audit checkpoint (2026-11-01)

## Scope and current baseline

This note consolidates the three open questions for the audit-only configuration-3 AGMD reference solver. It does not change production thermodynamics, the production net-water ledger, or the provisional property fixture.

Repository baseline: `9fe93b7a3ba7dfe7c906188538d0d5e906c20862` (PR #21 merge commit).

PR #21 restored the counterfactual freshwater-displacement calculation in the production water ledger. Its final commit passed CI: 177 tests passed, 1 skipped, and Ruff passed. That software result is independent of the AGMD reproduction gate.

## Issue 1 — Is ΔT_h,out ≤ ΔT_h,in a universal constraint?

### Finding

The accessible main article contains evidence that must be reconciled before imposing a strict upper bound. In its configuration-3 discussion, it says STEC is systematically higher, consistent with ΔT_h,in > ΔT_h,out, and describes the plotted/reported recovery behavior as bounded by ΔT_h,in = 5 °C and the minimum ΔT_h,out = 0.5 °C. However, later in the same discussion it states: “The only imposed physical constraint is that ΔT_h,out ≥ 0.5 °C to ensure a finite driving force for heat transfer.” The article also describes the recovery bound in terms of the inlet difference and minimum outlet difference, but does not explicitly state in the accessible main text that ΔT_h,out < ΔT_h,in is a universal admissibility rule.

These statements are not equivalent. The reported inequality in the plotted regime is an observation about the article's evaluated results; the “only imposed physical constraint” sentence describes the stated model constraint. A result trend does not by itself justify turning that trend into a hard solver filter. The supplementary information is still required to establish the exact S2/S8 derivation, variable definitions, and any additional constraints.

The implementation introduced in PR #26 initially enforced ΔT_h,out < ΔT_h,in by default. Following this source reconciliation, that default is being changed: the strict-order filter is opt-in only, because the article explicitly calls ΔT_h,out ≥ 0.5 °C the only imposed physical constraint. The synthetic regression case above ΔT_h,in demonstrates only that the implemented algebraic equations can admit such a root under independently selected heat capacities; it is neither proof of physical feasibility nor proof that the paper's full supplementary derivation admits it.

### Disposition

Do not expand the solver's physical claims or run a source-backed domain scan until the supplementary PDF is obtained. Reassess the PR #26 default filter against the actual SI. In the meantime, report results with the strict-order filter explicitly identified as a provisional interpretation, and separately report algebraic roots without implying physical admissibility. The 0.5 °C lower bound is explicitly stated in the main article; a strict upper bound requires stronger source support.

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
| Configuration-3 terminal ordering | Strict ΔT_h,out < ΔT_h,in filter is opt-in only; default applies the article's stated lower bound and S2 recovery interval | Obtain SI to complete the equation/constraint audit; passing algebraic filters is not physical validation |
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


## Supplementary-information retrieval checkpoint (2026-11-01)

The publisher's ScienceDirect record for DOI 10.1016/j.desal.2026.120039 explicitly states that all data generated are included in the article and its supplementary-information file. Appendix A of the main article identifies a separate 618 KB supplementary PDF. The accessible IRIS repository record for handle 11583/3009010 lists only the 4.8 MB main article PDF as a deposited file; it does not expose the supplementary PDF as a second repository attachment. The publisher's extracted record confirms a supplementary-data download control but does not expose a stable direct file URL. The likely Elsevier mmc1.pdf asset path was not verified and must not be treated as the file.

An earlier 27-page working-paper version is independently catalogued by Aalborg University's research portal as an SSRN preprint dated 9 January 2026, DOI 10.2139/ssrn.6048961. It is a distinct earlier manuscript, not the publisher's 618 KB supplementary file. Its record establishes a potential secondary source for version comparison, but until the actual preprint PDF is retrieved and compared, it cannot close the SI gate or be assumed to contain the final supplementary derivation and definitions.

The publisher states that the SI contains the full theoretical derivation, mathematical definitions, and comprehensive variable descriptions. The exact SI equations and property-state definitions therefore remain unverified until the 618 KB file itself is obtained and inspected. The absence of a supplementary attachment from the IRIS record is not proof that the publisher's supplement is unavailable.

**Actionable gate:** retrieve the publisher's SI through its ScienceDirect supplementary-data control or directly from the authors/repository; record exact URL, filename, byte size, and SHA-256 before transcription. Separately, if the SSRN preprint PDF becomes accessible, archive it as an earlier-version comparison with its own provenance and version label. Do not substitute guessed URLs or a reconstructed derivation for source evidence.


## SSRN preprint delivery-link audit (2026-11-01)

A targeted search surfaced the SSRN "Download This Paper" delivery endpoint for the separately catalogued 27-page preprint (DOI 10.2139/ssrn.6048961):

`https://papers.ssrn.com/sol3/Delivery.cfm/9bc95f3e-5eef-44ee-8df7-96c56129f90c-MECA.pdf?abstractid=6048961&mirid=1`

The endpoint is a concrete publisher-hosted PDF delivery URL, not a guessed Elsevier supplementary-file path. However, a direct retrieval attempt returned HTTP 403 Forbidden, and the browser's PDF open was also denied. Therefore the PDF bytes, filename as delivered, byte size, SHA-256, and contents remain unverified. The SSRN record independently confirms a 27-page preprint posted 9 January 2026 and identifies two versions; this metadata does not establish which file/version the delivery endpoint would return or that it contains the final article's supplementary derivation.

**Disposition:** preserve the exact delivery URL as a retrieval lead; do not mark the preprint as downloaded, do not cite it as inspected equation evidence, and do not close the supplementary-information gate. The publisher's 618 KB SI PDF remains a separate unresolved retrieval target.


## Terminal-order interpretation reconciliation (2026-11-01)

A further close reading of the publisher-indexed full text identifies a material qualification to the Issue 1 disposition above. The article says that configuration-3 STEC is systematically higher, consistent with ΔT_h,in > ΔT_h,out, and discusses the evaluated recovery behavior as bounded by ΔT_h,in = 5 °C and ΔT_h,out = 0.5 °C. In the same configuration-3 discussion, however, it explicitly says that “the only imposed physical constraint” is ΔT_h,out ≥ 0.5 °C. The first statement describes the reported trend/results; the second describes the stated physical constraint. They do not establish the same thing.

Consequently, PR #26's default strict-order filter (ΔT_h,out < ΔT_h,in) is not source-validated and is being changed to opt-in only. The default solver will apply the explicit lower bound and S2 recovery interval without imposing the additional strict ordering. Do not silently change the solver or claim that roots above ΔT_h,in are physically admissible. The synthetic above-inlet root remains an algebraic diagnostic only. The actual supplementary PDF is needed to inspect S2/S8, definitions, and whether an additional upper bound is imposed elsewhere.

**Required follow-up:** once the publisher's 618 KB SI is obtained, check every stated constraint and the derivation of the recovery bound against the implementation. Then decide whether the default should enforce only the explicit lower bound plus the S2 recovery interval, or retain a separate source-supported upper bound. Until then, preserve both filtered and unfiltered diagnostic results as distinct categories and keep the reproduction status **NOT YET REPRODUCED**.

Source: Malaguti et al. (2026), DOI https://doi.org/10.1016/j.desal.2026.120039, configuration-3 discussion and Section 3.3; publisher-indexed full text consulted 2026-11-01.


## Solver default aligned with explicit main-article constraint (2026-11-01)

Following the terminal-order reconciliation, the solver's `enforce_config3_terminal_order` default is changed to `False`. The main article explicitly says that the only imposed physical constraint for configuration 3 is ΔT_h,out ≥ 0.5 °C. The fact that the evaluated results exhibit ΔT_h,out < ΔT_h,in does not, by itself, justify enforcing that inequality as a universal root filter. The stricter ordering remains available as an opt-in sensitivity filter, clearly labeled provisional until the supplementary PDF is inspected.

A synthetic regression case now confirms that a root above ΔT_h,in is not rejected by the default algebraic filters, while the optional strict-order filter rejects the same root. This is a test of filter semantics only; the synthetic heat-capacity inputs are not source-matched and do not establish physical feasibility. The provisional smoke tests remain non-reproduction fixtures. No production thermodynamics or water-ledger behavior is changed.

The supplementary-information gate remains open: S2/S8 transcription, property-state mapping, and full physical admissibility are not yet verified. Reproduction status remains **NOT YET REPRODUCED**.


## Publisher supplementary-information equation audit (2026-11-01)

### Source identity

The publisher supplementary PDF was obtained in this conversation as
`1-s2.0-S0011916426001955-mmc1(1).pdf`. It is a 9-page PDF, 632,587 bytes.
SHA-256:

`48f57c20bfe220b336e195b1dd356c09cfc8acec289b72d335a6754c0fd4d191`

This is the actual publisher supplementary material, not the separate SSRN
working-paper manuscript. The file's title page identifies it as the Supporting
Information and Supplementary Material for Malaguti et al. (2026).

### Equation transcription

The AGMD derivation is now directly inspectable:

- S1 defines vaporization efficiency as vapor mass enthalpy flow divided by
  total heat transferred across the membrane.
- S2 gives
  `eta = R * h_vap / (c_h * (DeltaT - DeltaT_h_out))`.
  The supplement assumes approximately constant hot-channel specific heat
  along the feed channel and uses its inlet value.
- S6 is the full AGMD module heat balance, including the distillate enthalpy
  term and the saline cold-channel stream.
- S7 is the reduced AGMD heat balance after the stated constant-specific-heat
  and make-up-water assumptions.
- S8 combines S2 and S7 with
  `T_d = (T_h,in + (T_c,in + DeltaT_h,out)) / 2`.
  The solver's polynomial residual is the S8 equation rearranged to zero; its
  signs and stream heat-capacity terms match the printed equation.

The current implementation therefore has a source-backed S2/S8 algebraic
transcription. The four smoke-test property fixtures remain provisional and
are not source-matched Sharqawy evaluations. Equation transcription does not
by itself reproduce the paper's numerical maps.

### Explicit source inconsistency: inlet terminal difference

The SI prints the constraint brace alongside both the no-gap system S5 and
the AGMD system S8 as
`DeltaT_h,out >= 0.5, DeltaT_h,in = 0.5`.
However, the immediately following prose says the analysis fixes
`DeltaT_h,in = 5 °C` and considers values `DeltaT_h,in >= 0.5 °C`.
The main article independently defines `DeltaT_h,in` as the hot-inlet
difference and states it is set to 5 °C; its AGMD discussion identifies
`DeltaT_h,out >= 0.5 °C` as the only imposed physical constraint.

The defensible interpretation for the paper's reported configuration-3
analysis is therefore `DeltaT_h,in = 5 °C`, with
`DeltaT_h,out >= 0.5 °C`. The printed `DeltaT_h,in = 0.5` in the constraint
brace is internally inconsistent with the adjacent prose and main article and
is treated as an apparent typographical error, not silently adopted as the
analysis setting. This does not establish a universal upper bound
`DeltaT_h,out < DeltaT_h,in`; the main article explicitly describes the
0.5 °C outlet lower bound as the only imposed physical constraint.

### What is now closed, and what remains open

- **Closed:** actual publisher SI located; file identity, byte size, and
  SHA-256 recorded; S2, S6, S7, and S8 inspected; current solver S2/S8
  algebraic transcription checked against the SI.
- **Resolved by cross-document evidence:** use 5 °C for the article's
  configuration-3 inlet terminal difference; flag the SI's printed 0.5 °C
  inlet constraint as an apparent typo.
- **Still open:** source-matched Sharqawy property calculations for the hot
  saline stream, cold saline stream, pure distillate stream, and latent heat;
  precise property evaluation states; numerical reproduction of the article's
  recovery/temperature maps; and a full root-count/uniqueness study over the
  paper's operating domain.

The SI states that seawater flows in the feed channel and distillate water in
the distillate channel, and refers to Sharqawy et al. correlations for density,
latent heat, and specific heat. The main article describes configuration 3 as
the same saltwater stream circulating through hot and cold channels, with
complete salt rejection and pure distillate production. The current provisional
heat capacities and latent heat must therefore remain explicitly provisional
until the corresponding Sharqawy evaluations and stream states are
reconstructed and checked.

**Reproduction status: NOT YET REPRODUCED.** The equation transcription gate
is closed; the property-state, numerical reproduction, and domain-uniqueness
gates remain open.


## Property-state audit after direct SI inspection (2026-11-01)

The publisher SI adds one important state-selection detail that was not available in the earlier main-article-only review:

- In the derivation immediately before Eq. S2, the authors state that the hot-channel specific heat is treated as approximately constant along the feed channel (`c_h,in ≃ c_h,out ≃ c_h`) and that **the selected value refers to the hot-channel inlet conditions**. Therefore, the solver's `c_h` should be an inlet-state property, not an arbitrary channel-average value.
- For the AGMD module balance, S6 distinguishes `c_h`, `c_c`, and `c_d`; S7 then uses the constant-specific-heat approximation for the hot and cold channels and includes make-up water to compensate for distillate loss. The main article identifies the hot and cold channels as the same circulating saltwater stream and the distillate as pure water.
- The SI sets `T_c,in = 20 °C`, `DeltaT_h,in = 5 °C`, and defines `T_h,in = T_c,in + DeltaT`. It estimates `T_d = (T_h,in + T_c,in + DeltaT_h,out)/2`.

The SI does **not** state a numerical seawater salinity for the configuration-3 calculations in its text, nor does it unambiguously state the exact evaluation temperature for `c_c`, `c_d`, or `h_vap`. In particular, it does not explicitly say whether `c_c` is evaluated at the cold-channel inlet or another representative state, whether `c_d` is evaluated at the estimated `T_d`, or how the latent-heat correlation's mass basis is mapped to the pure distillate mass flow in S1. These must remain unresolved rather than being filled with a conventional 35 g/kg seawater assumption or a guessed property temperature.

### Consequence for implementation

No source-matched property adapter or numerical map reproduction is justified yet. The next defensible work is to:

1. extract the complete Sharqawy citation and the exact correlation versions used by the article;
2. identify the salinity and property evaluation states from author-supplied code/data, if available;
3. distinguish latent heat per kg of pure vapor/distillate from latent heat per kg of saline solution, and verify the mass basis against S1's `md * h_vap` term;
4. only then implement a versioned property adapter and calculate the four article anchors without fitting to them.

The article's generic reference to Sharqawy correlations is not enough to uniquely reconstruct these missing numerical inputs. A plausible seawater salinity, a modern library implementation, or a match to rounded figure anchors would not independently establish the authors' exact property-state choices.

**Updated disposition:** S2/S8 equation transcription is source-checked. The hot-channel specific-heat evaluation point is now identified as the hot inlet. Numerical salinity and the remaining property-state/mass-basis details are still undocumented in the inspected SI/main text. **Reproduction remains NOT YET REPRODUCED.**


## External source links and author-query plan (2026-11-01)

### Primary sources to use

1. **Malaguti et al. (2026), version of record** — [DOI: 10.1016/j.desal.2026.120039](https://doi.org/10.1016/j.desal.2026.120039); [Politecnico di Torino repository record and open article PDF](https://iris.polito.it/handle/11583/3009010). The article states that seawater is the feed, salt rejection is complete, distillate is pure water, and properties are based on temperature- and salinity-dependent correlations reported by Sharqawy et al. (2010). It does not report a numerical salinity in the inspected main text/SI. The data-availability statement says the data generated are included in the article and SI.
2. **Publisher supplementary information** — linked from the DOI landing page under Supplementary data; local inspected copy: `1-s2.0-S0011916426001955-mmc1(1).pdf`. It contains S1–S8, but does not resolve the missing numerical salinity or all property evaluation states.
3. **The exact cited property reference, Sharqawy, Lienhard & Zubair (2010)** — [DOI: 10.5004/dwt.2010.1079](https://doi.org/10.5004/dwt.2010.1079); [MIT DSpace author-final manuscript (corrected version)](https://dspace.mit.edu/entities/publication/0c55d19d-eb62-4e5f-8a12-a71c2b53f36a); [MIT-hosted PDF](https://dspace.mit.edu/bitstreams/5cef041d-fe22-4e5a-a3a4-e3c81158bfdf/download). The DSpace record identifies the 2010 paper and its corrected author-final manuscript.
4. **MIT seawater property library** — [official library page](https://web.mit.edu/seawater/); [property tables PDF, updated 9 Dec 2023](https://web.mit.edu/seawater/2017_MIT_Seawater_Property_Tables_r2b_2023c.pdf); [version history](https://web.mit.edu/seawater/Version_History_07Aug24-pdf-3a.pdf); [code archive v3.1.5 (7 Aug 2024)](https://web.mit.edu/seawater/SEAWATER_v3.1.5_07Aug24.zip). This is a useful implementation/reference cross-check, **not proof that the 2026 article used this exact code archive**. The MIT page identifies the specific-heat routine as the Jamieson correlation at 1 atm and documents its corrected coefficient. The library's function contracts also distinguish pressure-dependent specific heat from latent heat evaluated at its stated reference pressure convention.
5. **Pressure-dependent follow-up correlation paper** — [Nayar et al. (2016), DOI: 10.1016/j.desal.2016.02.024](https://doi.org/10.1016/j.desal.2016.02.024). This is cited by the current MIT library, but is **not** the reference [22] cited by Malaguti et al. (2026). Do not silently replace the article's cited 2010 correlations with the later 2016 set.
6. **Mass-basis cross-check** — Sharqawy et al. (2010), latent-heat section, especially Eq. 37 and its stated basis. The correlation distinguishes latent heat per mass of saline solution from pure-water latent heat. Before using it in S1, the implementation must show which basis is returned and how that basis is consistent with the distillate mass flow `m_dot_d`. Avoid applying a seawater correction twice.

### What can be resolved now, and what cannot

- The article explicitly says **seawater** is the feed and pure water is the distillate. This is source-backed, but does not supply a numeric salinity.
- The article explicitly cites **Sharqawy et al. (2010)** for the temperature- and salinity-dependent property correlations. The 2010 paper and corrected manuscript are therefore the first property-correlation source to implement, not a later library selected merely because it is convenient.
- MIT's current library is valuable for checking equation coefficients, validity ranges, units, and code behavior. Its version and API contracts must be recorded separately from the article's stated citation.
- The article/SI still do not uniquely specify the numerical salinity or all property evaluation temperatures. A reference-seawater convention such as 35 g/kg must not be promoted to an author-confirmed input without an explicit statement or data/code evidence.
- The SI's estimate for `T_d` provides a possible evaluation state for pure-water `c_d`, but unless the authors explicitly say they evaluate `c_d` there, this remains an implementation hypothesis to test, not a source fact.

### Author clarification request

The article identifies Alberto Tiraferri as corresponding author and gives `alberto.tiraferri@polito.it`. A concise clarification request should ask:

1. What exact feed salinity (g/kg) was used for the seawater property calculations in configuration 3 / Figures 3C, 3F and 4?
2. At what temperatures were `c_h`, `c_c`, and `c_d` evaluated? We have the SI statement that `c_h` is evaluated at hot-channel inlet conditions; please confirm the cold-channel and pure-distillate states.
3. Which exact Sharqawy 2010 equations or code implementation/version were used?
4. Is `h_{vap}` in S1 the latent heat per kg of pure distillate water or per kg of saline feed solution? If seawater-basis, how was it reconciled with `m_dot_d` (pure distillate mass flow)?
5. What pressure convention was assumed for the properties?
6. Are the underlying calculation scripts, numerical arrays, or a table of property inputs available, beyond the article/SI?

No email has been sent. These questions are recorded as the next source-retrieval action.

**Implementation decision:** proceed with a transparent sensitivity framework over explicitly labelled salinity/property-state scenarios if useful, but do not label any scenario as an exact reproduction. Exact reproduction remains blocked pending author clarification or an independently verifiable numerical input source.
