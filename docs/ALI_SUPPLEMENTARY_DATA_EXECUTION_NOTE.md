# Source acquisition execution note

## Ali, Orfi & Najib (2020) supplementary data

The article is open access and its supporting information lists five XLSX datasets (S1 Data through S5 Data). The article record is https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230207 and the Europe PMC/PMC record is https://pmc.ncbi.nlm.nih.gov/articles/PMC7092998/ .

Use the original workbook files, not values copied from plots or the article's summary error table. For each file, preserve the publisher-provided filename and SHA-256, inventory all worksheets, identify raw measured data versus model/theoretical worksheets, record native units and sampling interval, and independently check extracted rows. Do not merge records across operating conditions without preserving their condition identifiers.

## Current evidence boundary

The repository's Table 1 transcription records reported model–plant relative errors only. It is not the raw experimental time series and must not be used as a substitute for the supporting XLSX files. No numeric time-series observation should be entered until the original source row or a clearly labelled digitized-figure record exists.

## Execution sequence

1. Retrieve the five XLSX files from the publisher's supporting-data links.
2. Record retrieval date, byte size, SHA-256, original filename, and sheet names.
3. Map each sheet's variables, units, timestamps, and operating condition from its headers and the paper's methods.
4. Create a raw, immutable observation ledger with source file, sheet, row, and column provenance.
5. Independently verify a sample of rows and reconcile unit conversions.
6. Predeclare development versus held-out assignments before model fitting.
7. Run the unfitted comparison and retain every failure or exclusion with a reason.

A successful download or workbook inventory is an acquisition milestone, not scientific validation.