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
