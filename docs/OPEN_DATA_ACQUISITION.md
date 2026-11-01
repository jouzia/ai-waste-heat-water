# Open experimental-data acquisition manifest

Status: acquisition and extraction infrastructure only. No observation is promoted to
validation until the raw file is locally hashed, parsed, independently checked, and
linked to a source row.

## Villa et al. (2018) — GDR/OEDI

Dataset DOI: 10.15121/1452747
Landing page: https://gdr.openei.org/submissions/1016
License indicator on the landing page: Creative Commons. Exact file-level terms must
be recorded before redistribution of adapted data.

The seven source workbooks are:

1. https://gdr.openei.org/files/1016/Countercurrent%20DCMD%203M%200.231m%5E2%201%20LPM%204g%20NaCl_08.11.2017.xls
2. https://gdr.openei.org/files/1016/Countercurrent%20DCMD%20Aquastill%200.231m%5E2%201%20LPM%204g%20NaCl_8.10.17.xls
3. https://gdr.openei.org/files/1016/Countercurrent%20Spiral%20DCMD%20Aquastill%203.6m%5E2%2013.5LPM_4g%20NaCl%2007.27.2017.xls
4. https://gdr.openei.org/files/1016/Countercurrent%20DCMD%20Aquastill%200.692%20m%5E2%201%20LPM%204g%20NaCl_low.xls
5. https://gdr.openei.org/files/1016/Airgap%20CLARCOR%20QL822%200.14m%5E2%201.5LPM_4g%20NaCl%2005.15.2017.xls
6. https://gdr.openei.org/files/1016/Cocurrent%20DCMD%20CLARCOR%20QL822%200.231m%5E2%201.5LPM_4g%20NaCl%2005.15.2017.xls
7. https://gdr.openei.org/files/1016/Countercurrent%20DCMD%20CLARCOR%20QL822%200.231m%5E2%201.5LPM_4g%20NaCl%2005.15.2017.xls

The GDR record states that the workbooks contain theoretical, specification, and raw
data worksheets, and lists configuration-specific membrane area, flow, and salinity.
Those metadata are not substitutes for extracting the measured rows.

## Ali, Orfi & Najib (2020) — PLOS ONE

Article DOI: 10.1371/journal.pone.0230207
Landing page: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0230207
License: CC BY 4.0.

Supporting workbooks:
- https://doi.org/10.1371/journal.pone.0230207.s002
- https://doi.org/10.1371/journal.pone.0230207.s003
- https://doi.org/10.1371/journal.pone.0230207.s004
- https://doi.org/10.1371/journal.pone.0230207.s005
- https://doi.org/10.1371/journal.pone.0230207.s006

The PLOS record states that the supporting files contain the relevant experimental data.
The current repository does not embed those binary workbooks.

## Mandatory extraction record

For every downloaded source file record:

- source URL and landing-page DOI
- retrieval timestamp
- byte size and SHA-256
- original filename
- workbook sheet names
- software/parser version
- selected sheet and exact row/column ranges
- unit transformations
- missing-value handling
- exclusion rules
- independent second extraction or cross-check
- observation uncertainty/provenance
- whether the data are development or held-out

Never reconstruct a numeric observation from a prose summary when the underlying
source file is available. Never infer missing boundary conditions.

## Reproducible local extraction utility

The repository now includes `scripts/extract_open_md_data.py`. It performs a **pre-extraction inventory only**: it discovers local XLS/XLSX workbooks, records file size and SHA-256, inventories workbook sheets, and writes a JSON manifest. It does not select observations, transform values, or label any case as validated. Legacy XLS support is provided through the analysis extra's `xlrd` dependency.

Example after legally downloading the registered source files:

```bash
python scripts/extract_open_md_data.py 02_data/raw/open_md 02_data/raw/open_md_inventory.json
```

The next scientific step remains manual, source-specific column/range mapping followed by an independently checked observation ledger. No validation result may be promoted from the inventory alone.



## 2026-10-06 access verification

The Villa GDR landing page was re-verified: the repository exposes seven downloadable workbooks and explicitly describes the theoretical, Specifications, Data, and temperature-range worksheets. The record is publicly accessible and links a Creative Commons licence. The binary XLS files remain unsuitable for direct ingestion through the research automation environment, so no observations are fabricated from the landing-page metadata.

The Ali et al. (2020) dataset was independently re-verified through the publisher/PMC record: five XLSX supporting datasets are available (S1 Data through S5 Data), and the article states that the study used experimental step-response data from a pilot DCMD plant. The associated dataset catalogue identifies CC BY 4.0 and the Figshare dataset record. Observation extraction remains gated until the actual supporting workbooks are locally available to the extraction script.

### Extraction rule
1. Download the original binary files from the authoritative landing page.
2. Preserve the original filename and SHA-256.
3. Run `python scripts/extract_open_md_data.py <input_dir> <output_json>`.
4. Review worksheet names and select source-defined ranges before any unit transformation.
5. Store raw observations separately from transformed model inputs.
6. Record development/held-out assignment before model fitting.
7. Independently re-extract a sample of observations and reconcile discrepancies.

The inventory tool is now executable for both legacy `.xls` and `.xlsx` workbooks; it does not claim that an inventory is a validation result.
