# Ali, Orfi & Najib (2020) DCMD supporting-data audit

**Paper:** Emad Ali, Jamel Orfi, and Abdullah Najib, “Developing and validating a dynamic model of water production by direct-contact membrane distillation,” *PLOS ONE* 15(3), e0230207 (2020). DOI: [10.1371/journal.pone.0230207](https://doi.org/10.1371/journal.pone.0230207). The article and supporting files are CC BY 4.0.

**Source:** [PLOS article and supporting information](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230207).

## Reproducible acquisition

- Workflow: [Ali et al. 2020 dynamic DCMD source-data ingestion, run #22](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38437677652).
- Artifact ID: `11833462795`; archive digest: `sha256:a20d3e19b77f1c9d7d8ad09f1b6c1c202fd4b6ba4042cb0c0520715e2b88d7ee`.
- Artifact retention expiry: 2027-01-11 17:19 UTC.
- Five original XLSX supporting objects are retained in the artifact with SHA-256 checksums; extraction code and manifests are in the repository.
- The artifact includes source-linked transient and steady-state ledgers, excluded-row ledger, raw `mw` semantics audit, and a manifest recording file hashes and sheet/row locators.
- Raw worksheet ledger SHA-256: `e24887bb94c1f903d623c4eb9bd19e1798615e5aa6b45776a81a5073d43956f7` (unchanged source export).
- Transient observation ledger SHA-256: `1bc2ca946a9a42034eb13b8d53d6795258b225362140c75d1fa84e69defe7275`.
- Steady-state ledger SHA-256: `87e338a4ac7868d380d6948025ff83b50061212894bb1c35dcf193ac4d363e27`.
- Raw `mw` semantics audit CSV SHA-256: `eaa0d848bc50e7fcd66c2f05fc04508000da3b96f16194d8a0e00c04a15667a3`.

## Extracted material

- **17,385** transient ledger rows across S2–S5.
- **16,837** complete timestamped time-series rows retained as candidates for time-domain analysis.
- **548** temperature-only rows in S5 sheets 50, 60, and 70 have no timestamps and are excluded from time-domain fitting; they remain identified in the manifest.
- **16** steady-state observations from S1, representing nominal flow rates 50, 100, 200, and 300 L/h at hot-inlet setpoints 50, 60, 70, and 80 °C.
- **2** non-condition rows from S1 are explicitly excluded and preserved in an exclusion ledger with original row locators.
- The source paper reports a 10-second sampling interval; the workbook time column is expressed in minutes. Do not assume every worksheet reaches its target setpoint.

## Raw mass-field semantics: blocking issue

The previous tail-slope consistency numbers in this document are **withdrawn from evidentiary use**. They were computed by treating the workbook's `mw` column as accumulated distillate mass. A later source-data audit found that this column decreases between adjacent observations in **14 of 19 complete timed worksheet traces**. That behavior is incompatible with an unqualified cumulative-mass interpretation unless the instrument's reset/measurement protocol explains it.

The current extraction therefore preserves the field as `mw_raw_reading_kg`, leaves `cumulative_distillate_mass_kg` unset, and disables all tail-flux consistency comparisons. The 19-row audit records source file, worksheet, row counts, time span, min/max, monotonicity, and step counts. Neither the monotonic traces nor the nonmonotonic traces are promoted to cumulative-mass observations until the source semantics are verified.

The 16 S1 steady-state mass-flux values remain source-listed observations, but their salinity-column ambiguity and model-form limitations are documented separately. The S1 train/held-out-flow diagnostic is an internal same-paper model-form comparison, not independent validation.

## Data-quality findings to retain

1. **S2 sheet 55:** starts with nonzero cumulative distillate mass and ends below the nominal sheet temperature. Treat it as a partial/nonstandard trace unless the paper's methods resolve the mismatch.
2. **S5 sheets 50/60/70:** include temperature-only rows without time stamps after the timed records. Exclude these rows from dynamic fitting; do not fabricate times.
3. **S5 sheet 80:** the final measured hot-inlet temperature remains below the nominal 80 °C label. Do not treat it as a fully attained 80 °C steady-state observation.
4. **S1 Q=200 and Q=300:** each includes one extra numeric row that does not represent a valid operating condition; preserve the raw row and exclusion reason.
5. **S4 sheet 80R:** keep the replicate/alternate trace distinct. Do not merge it into sheet 80 without a declared replicate policy.
6. **TDS fields:** preserve raw values and uncertainty text (for example, `0.94 ± 0.01`) rather than silently converting to numbers.

## What this data can and cannot establish

This is a useful, open, source-traceable dataset for a future dynamic DCMD module. It does not, by itself, validate the repository's steady-state MD correlations or the proposed data-centre waste-heat-to-freshwater system. Before fitting or comparing any model, document the exact experimental configuration, membrane area, fluid properties, inlet boundary conditions, hot/cold channel mapping, heat-loss treatment, and which time series are held out. Do not fit heat-transfer coefficients to the same traces later reported as validation.

The current main research question remains net operational blue-water impact under an explicit counterfactual. Gross distillate production is not equivalent to avoided freshwater consumption; auxiliary electricity, cooling-system changes, geographic water stress, and actual displacement of freshwater must remain in the system boundary.
