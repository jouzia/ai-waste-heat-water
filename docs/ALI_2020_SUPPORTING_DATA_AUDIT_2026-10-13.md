# Ali, Orfi & Najib (2020) DCMD supporting-data audit

**Paper:** Emad Ali, Jamel Orfi, and Abdullah Najib, “Developing and validating a dynamic model of water production by direct-contact membrane distillation,” *PLOS ONE* 15(3), e0230207 (2020). DOI: [10.1371/journal.pone.0230207](https://doi.org/10.1371/journal.pone.0230207). The article and supporting files are CC BY 4.0.

**Source:** [PLOS article and supporting information](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230207).

## Reproducible acquisition

- Workflow: [Ali et al. 2020 dynamic DCMD source-data ingestion, run #12](https://github.com/jouzia/ai-waste-heat-water/actions/runs/38427509655).
- Artifact ID: `11829695926`; archive digest: `sha256:1a12fadca90d89452c11f0f7cc5bcbc6b7804e5c16c78528c5a5f70723e15224`.
- Artifact retention expiry: 2027-01-11 16:04 UTC.
- Five original XLSX supporting objects are retained in the artifact with SHA-256 checksums; extraction code and manifests are in the repository.
- The artifact includes source-linked transient and steady-state ledgers, excluded-row ledger, tail-flux diagnostic table, and a manifest recording file hashes and sheet/row locators.
- Raw worksheet ledger SHA-256: `e24887bb94c1f903d623c4eb9bd19e1798615e5aa6b45776a81a5073d43956f7`.
- Transient observation ledger SHA-256: `ee31a5604a01eb33683672b7ace2bae817273976425dc79509923b92647ec35c`.
- Steady-state ledger SHA-256: `87e338a4ac7868d380d6948025ff83b50061212894bb1c35dcf193ac4d363e27`.
- Tail consistency CSV SHA-256: `0fcbd73063027d9c1fb0f981b1b69411caee23d1274b8aeb102a41b62687b76b`.

## Extracted material

- **17,385** transient ledger rows across S2–S5.
- **16,837** complete timestamped time-series rows retained as candidates for time-domain analysis.
- **548** temperature-only rows in S5 sheets 50, 60, and 70 have no timestamps and are excluded from time-domain fitting; they remain identified in the manifest.
- **16** steady-state observations from S1, representing nominal flow rates 50, 100, 200, and 300 L/h at hot-inlet setpoints 50, 60, 70, and 80 °C.
- **2** non-condition rows from S1 are explicitly excluded and preserved in an exclusion ledger with original row locators.
- The source paper reports a 10-second sampling interval; the workbook time column is expressed in minutes. Do not assume every worksheet reaches its target setpoint.

## Cross-check performed

For each timestamped transient series, the extraction pipeline compares linear slopes over the final 25% and final 10% of rows against the corresponding S1 steady-state flux. This is a **within-paper consistency diagnostic**, not independent validation: the transient and steady-state data come from the same publication and may share experimental/systematic errors.

For 15 traces whose final measured hot-inlet temperature is within 2 °C of the sheet's nominal setpoint:
- Final-25% tail slope: median absolute difference **2.78%**, mean absolute difference **3.64%**, range **−5.14% to +9.61%**.
- Final-10% tail slope: median absolute difference **2.83%**, mean absolute difference **4.15%**, range **−12.87% to +11.27%**.

The tails are not guaranteed to be statistically steady merely because they are the final rows. These values must not be presented as validation accuracy or as a model-versus-experiment error metric.

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
