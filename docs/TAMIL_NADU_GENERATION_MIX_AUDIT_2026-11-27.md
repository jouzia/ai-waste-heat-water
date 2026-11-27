# Tamil Nadu State-Wise Generation Mix Audit (FY2020-21 to FY2025-26)

**Audit date:** 2026-11-27  
**Primary source:** Ministry of Power, Government of India, Rajya Sabha Unstarred Question No. 4143, answered 30 March 2026, Annexure I.  
**Dataset:** `data/geography/tamil_nadu_generation_mix_2020_21_to_2025_26.csv`  
**Reproducible summary:** `scripts/summarize_tamil_nadu_generation_mix.py`

## 1. Scope and source interpretation

Annexure I reports state-wise source-wise generation for Tamil Nadu for FY2020-21 through FY2024-25, plus FY2025-26 through February 2026. The table reports thermal, nuclear, and large-hydro generation from stations of **25 MW and above**. Its renewable total includes wind, solar, biomass, bagasse, small hydro, and large hydro.

The source does not explicitly label the generation values as gross or net. The station-level NNTPS value in the 2024 Rajya Sabha answer (6,177.93 MU in FY2021-22) is close to NLC's reported gross generation (6,178.74 MU) and distinct from CEA net generation (5,758.70 MU). This supports a gross-generation interpretation for NNTPS, but the aggregate dataset is therefore retained as **reported generation** rather than relabelled gross or net.

All values are MU (million kWh). The FY2025-26 row covers April 2025–February 2026 only (11 months).

## 2. Tamil Nadu generation mix

| Period | Total generation (MU) | Thermal (MU) | Thermal share | Nuclear (MU) | Nuclear share | Renewable incl. hydro (MU) | Renewable share |
|---|---:|---:|---:|---:|---:|---:|---:|
| FY2020-21 | 91,736.53 | 51,200.05 | 55.81% | 13,664.72 | 14.90% | 26,871.76 | 29.29% |
| FY2021-22 | 106,081.37 | 61,182.76 | 57.68% | 15,625.26 | 14.73% | 29,273.35 | 27.60% |
| FY2022-23 | 116,688.02 | 67,083.23 | 57.49% | 16,012.57 | 13.72% | 33,592.22 | 28.79% |
| FY2023-24 | 123,311.63 | 75,333.82 | 61.09% | 14,811.22 | 12.01% | 33,166.59 | 26.90% |
| FY2024-25 | 130,124.92 | 74,221.36 | 57.04% | 17,493.39 | 13.44% | 38,410.17 | 29.52% |
| FY2025-26 (Apr–Feb) | 120,963.23 | 59,863.82 | 49.49% | 14,008.30 | 11.58% | 47,091.11 | 38.93% |

The FY2021-22 grand total differs by only 0.03 MU from the station-wise total in the 2024 parliamentary answer (106,081.40 MU); the source-reported 2026 answer value is retained in the CSV.

### Fuel composition

Thermal generation comprises coal, lignite, natural gas, and any reported diesel/HSD or naphtha generation. The main fuel pattern is:

- Coal share of total generation rose from **35.25%** in FY2020-21 to **41.02%** in FY2024-25, peaking at **43.84%** in FY2023-24.
- Lignite share was **18.11%** in FY2020-21, peaked at **21.35%** in FY2021-22, and was **14.78%** in FY2024-25.
- Natural-gas generation remained a small share, declining from **2.47%** in FY2020-21 to **1.24%** in FY2024-25.

### Non-hydropower mix

IRENA's non-hydropower factor boundary excludes hydropower. For a comparable generation denominator, the script subtracts both small- and large-hydro generation from the reported grand total and from the renewable total.

| Period | Non-hydro generation (MU) | Thermal share of non-hydro | Nuclear share of non-hydro | Non-hydro renewables share |
|---|---:|---:|---:|---:|
| FY2020-21 | 86,279.05 | 59.34% | 15.84% | 24.82% |
| FY2021-22 | 100,576.13 | 60.83% | 15.54% | 23.63% |
| FY2022-23 | 110,425.54 | 60.75% | 14.50% | 24.75% |
| FY2023-24 | 119,542.35 | 63.02% | 12.39% | 24.59% |
| FY2024-25 | 125,265.60 | 59.25% | 13.97% | 26.78% |
| FY2025-26 (Apr–Feb) | 115,249.87 | 51.94% | 12.15% | 35.90% |

This non-hydro mix is a useful input for a generation-side scenario using non-hydro water-intensity factors. It is not itself a water factor. The FY2025-26 partial-period shares must not be treated as a completed annual mix.

## 3. Generation is not the consumption mix

The state-wise table describes generation located in Tamil Nadu. It does not provide the electricity consumed in Tamil Nadu after accounting for imports, exports, central-station allocations, transmission losses, and dispatch.

The 2024 Rajya Sabha Question No. 480, Annexure III, separately reports firm allocations from central generating stations located in Tamil Nadu to Tamil Nadu and other states for April 2021–December 2023:

| Central station group | Allocated to Tamil Nadu (MU) | Total listed allocation (MU) | Tamil Nadu share | Other-state share |
|---|---:|---:|---:|---:|
| NLC power plants | 30,435.00 | 59,780.00 | 50.91% | 49.09% |
| NTECL Vallur | 15,984.91 | 22,425.70 | 71.28% | 28.72% |
| Nuclear | 21,043.89 | 37,058.56 | 56.79% | 43.21% |

These are **firm allocations**, not measured hourly dispatch or actual consumption. They nevertheless demonstrate that geographic generation in Tamil Nadu cannot be substituted directly for the state's electricity-consumption mix. A full state supply balance still needs imports, exports, actual dispatch, and losses.

## 4. Water-accounting implications

No water factor is calculated or added to the factor ledger in this change.

A defensible Tamil Nadu electricity-water factor still requires:
1. A generation or consumption denominator with a clearly stated gross/net and import/export boundary.
2. Technology- and cooling-system-specific water intensities, with withdrawal, consumption, and freshwater-input metrics kept separate.
3. Plant-level source-water information, including the treatment of mine water and seawater.
4. A clear decision on whether hydropower reservoir evaporation is inside or outside the water-accounting boundary.
5. A reconciliation between state generation, central-station firm allocations, imports, exports, and electricity delivered to consumers.

The nuclear share should not automatically be assigned a freshwater intensity: Kudankulam and Madras Atomic Power Station are coastal facilities, and the relevant cooling-water source must be verified before assigning a freshwater factor. Likewise, CEA's reporting classification of mine water as NFW3 is not by itself a conclusion about the water's hydrological origin or basin-scarcity impact.

## 5. Reproducibility and disposition

Run:

```bash
python scripts/summarize_tamil_nadu_generation_mix.py
pytest -q tests/test_tamil_nadu_generation_mix.py
```

The summary reports source totals, total-generation shares, and non-hydropower shares. Regression tests check category reconciliation, the FY2021-22 source values, the FY2024-25 non-hydro calculation, and the incomplete FY2025-26 period.

**Disposition:** accept this as a source-qualified Tamil Nadu generation-mix dataset for generation-side scenario analysis. Do not call it a consumption mix, do not calculate a water factor from generation shares alone, and do not change any validation gate or engine default.
