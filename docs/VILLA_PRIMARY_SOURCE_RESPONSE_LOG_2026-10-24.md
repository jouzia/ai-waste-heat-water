# Villa Primary-Source Clarification Response Log

**Created:** 2026-10-24  
**Status:** Awaiting external clarification; no response received or contact sent by this repository automation.  
**Dataset:** Villa et al., *Membrane Specifications for Multi-Configuration Membrane Distillation Model*, GDR submission 1016, DOI 10.15121/1452747.  
**Repository:** `jouzia/ai-waste-heat-water`

## Purpose

Maintain a traceable record of unresolved source questions before changing any Villa-derived model assumptions. This log is an evidence-control document, not evidence that the authors have been contacted.

## Contact state

- [ ] Verify the current contact route on the official GDR landing page.
- [ ] Researcher reviews and sends the email draft, if appropriate.
- [ ] Record sent date, recipient/official route, and message copy in a private research record; do not publish private correspondence without permission.
- [ ] Record any response date and the source of the response.
- [ ] Link any public correction, workbook revision, manufacturer document, or author-approved clarification.
- [ ] Re-run source reconstruction and validation only after documenting which fields the evidence resolves.

Email draft: [VILLA_SOURCE_CLARIFICATION_EMAIL_DRAFT_2026-10-24.md](VILLA_SOURCE_CLARIFICATION_EMAIL_DRAFT_2026-10-24.md)  
Question checklist: [VILLA_PRIMARY_SOURCE_CLARIFICATION_REQUEST_2026-10-24.md](VILLA_PRIMARY_SOURCE_CLARIFICATION_REQUEST_2026-10-24.md)  
Existing audit: [VILLA_GEOMETRY_FLOW_PROVENANCE_AUDIT_2026-10-23.md](VILLA_GEOMETRY_FLOW_PROVENANCE_AUDIT_2026-10-23.md)

## Questions that remain open

| ID | Question | Current handling | Closure evidence required |
|---|---|---|---|
| V-01 | Which membrane/device was actually used for the 3M-labelled counter-current DCMD workbook, given the conflicting CLARCOR QL822 narrative? | Device identity unresolved; do not harmonize labels by assumption. | Author confirmation or authoritative device/source record tied to this workbook/run. |
| V-02 | Is 0.23088 m² the correct active membrane area for the reported observations, and does it represent nominal, geometric, or effective area? | Use only as a nominal reported specification in explicitly labelled sensitivity analyses. | Definition, geometry, and provenance for active area. |
| V-03 | What do the negative MD feed and cooling flow values mean? | Preserve signed values; do not take absolute values or silently reinterpret direction. | Channel/orientation map, sign convention, and units/offset explanation. |
| V-04 | Why are the MD Feed Flowrate (Low) and MD Distillate Flowrate (Low) columns `Inf` across retained rows? | Treat as unusable as finite measured flow observations. | Explanation of export/calculation semantics and recoverable raw values, if any. |
| V-05 | Which temperature channels are direct observations versus derived/theoretical values? | Keep the Theoretical worksheet out of the independent observation ledger; avoid target leakage. | Workbook field definitions and measurement/derivation provenance. |
| V-06 | What exactly do cumulative distillate volume, runtime, and reported flux represent? | Treat slope-derived flux as a derived quantity, not an independent measurement. | Definition of volume units, timing, collection method, and flux calculation. |
| V-07 | Why do condition-sheet metadata rows repeat the same “20C/40C 0.4LMH” label? | Treat repeated labels as a metadata inconsistency; do not use them to overwrite sheet-specific identity. | Author explanation or corrected metadata. |

## Decision rules

1. Do not silently correct, absolute-value, interpolate, or reinterpret source fields.
2. Keep raw observations immutable; document any transformation in code and the provenance ledger.
3. Distinguish direct measurements, derived values, nominal specifications, and model outputs.
4. Do not describe the six-condition holdout as independent external validation. The existing fit is diagnostic and must remain labelled accordingly.
5. Do not claim net-water benefit, field validity, or publication readiness based on software tests or conditional scenario outputs.
6. Do not mark source reconstruction, unfitted validation, held-out validation, model-form comparison, or final publication gates complete without a reproducible artifact and provenance record.
7. If no response is received, record the follow-up attempts and retain the unresolved status. Lack of response is not evidence that an assumption is correct.

## Change log

- 2026-10-24: Initial log created. No source-author response is documented; no email has been sent by this workflow.
