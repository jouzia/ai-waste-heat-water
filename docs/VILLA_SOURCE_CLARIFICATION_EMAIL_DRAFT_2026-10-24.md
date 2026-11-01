# Email draft: clarification request for Villa et al. (2018) DCMD workbook

**Suggested recipients:** the dataset contact listed on the GDR landing page and, if needed, GDR curation support. Verify current contact details on the official landing page before sending.

**Dataset:** Villa, D. et al. (2018), *Membrane Specifications for Multi-Configuration Membrane Distillation Model*, DOI 10.15121/1452747  
**Landing page:** https://gdr.openei.org/submissions/1016  
**Workbook:** `3M 0.2 Micron Plate and Frame Countercurrent DCMD.xls`

---

**Subject:** Clarification request for measurement channels and provenance in GDR dataset 10.15121/1452747

Dear Dr. Akar and dataset team,

I am conducting a reproducibility audit of the publicly available Villa et al. (2018) membrane-distillation dataset (DOI 10.15121/1452747), specifically the workbook named “3M 0.2 Micron Plate and Frame Countercurrent DCMD.xls.” I am using the data for a methodological assessment of transport-model validation and am trying to avoid making unsupported assumptions about sensor semantics or calculated fields.

The workbook has several points that I cannot resolve from the published files alone:

1. **Equipment identity:** the workbook filename and Specifications sheet identify a 3M membrane, while the “Theoretical” worksheet narrative refers to “CLARCOR QL822.” Is that narrative copied from a different module/workbook, or does it describe any of the measurements in the 3M file?
2. **Active area:** is 0.23088 m² the effective installed membrane area used for the tests, including the effects of seals/gaskets, or only the nominal area?
3. **Flow channels:** the finite values in “MD Feed Flowrate (High) [LPM]” and “MD Cooling Flowrate [LPM]” are negative throughout the retained raw traces; both “MD … Flowrate (Low)” columns contain `Inf`. Could you clarify the channel mapping, sign convention, units, and meaning of these values?
4. **Temperature channels:** is there a channel map identifying the physical locations of the MD and preheater (PH) inlet/outlet temperature sensors?
5. **Flux and timing:** what are the exact semantics, units, time basis, and sampling/reset behavior of cumulative distillate volume and runtime? Is the constant 42.0 LMH value a nominal setpoint or a measured result, and how was flux calculated in the “Theoretical” worksheet?

A short written clarification, a sensor/channel map, a test protocol, or a reference to the relevant source documentation would be extremely helpful. I would preserve any answer with its source and provenance and would not alter the original dataset.

I have prepared a concise list of the questions and the current audit findings here:
https://github.com/jouzia/ai-waste-heat-water/blob/main/docs/VILLA_PRIMARY_SOURCE_CLARIFICATION_REQUEST_2026-10-24.md

Thank you for making the dataset publicly available and for any guidance you can provide.

Best regards,  
Researcher  
Project: “From AI Waste Heat to Water: A Net-Water-Impact Framework for Sustainable AI Infrastructure”
