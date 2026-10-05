# SACC systematic analysis and meta-analysis (Acta Medica Philippina)

**Defining Schistosomiasis-Associated Colorectal Cancer: A Systematic Analysis and Meta-analysis of Clinicopathological, Molecular, and Prognostic Features**

## Status

This is a **submission-formatted draft, not a finished paper**. The Introduction, Methods, Discussion framework, search strategies, figures 1, 2 and 8, the table structures and the analysis code are complete. Every result that depends on screening or pooling is a highlighted `[TO BE CALCULATED]` placeholder. No study-level numbers have been entered or pooled, because full texts could not be accessed from the build environment (see `phase1/Phase1_Report.md`).

## Contents

| Path | What it is |
|---|---|
| `phase1/Phase1_Report.md` | Answers to the 10 first-task items: PECO, criteria, searches, verified inventory, overlap, outcomes feasibility, existing meta-analyses, novelty |
| `manuscript/SACC_Manuscript_ActaMedPhilipp.docx` | Manuscript in journal format (Arial 12, single-spaced, figures and tables in text, ICMJE references) |
| `manuscript/SACC_Supplementary_Material.docx` | Tables S1–S6 and the PRISMA 2020 checklist |
| `manuscript/Cover_Letter.docx`, `Highlights_and_Graphical_Abstract.docx`, `Figure_and_Table_Legends.docx` | Submission extras |
| `data/study_inventory.csv`, `data/overlap_matrix.csv` | Study inventory and overlap matrix |
| `data/SACC_master_extraction.xlsx` | Master extraction workbook |
| `data/analysis_ready/*.csv` | Analysis-ready long-format files (empty, headers only) |
| `R/run_all.R`, `R/sacc_functions.R` | Full metafor pipeline: REML random effects, sensitivity analyses, Egger (k ≥ 10), Figures 3–7, Tables 3–5 and S5 |
| `tests/test_pipeline.R` | Validation against metafor's BCG benchmark and checks on the integrity guards |
| `figures/` | Figures 1, 2 and 8 (PDF, SVG, 600-dpi PNG and TIFF) and their script |

## Workflow after extraction

```bash
# 1. fill data/analysis_ready/*.csv from full texts; set verified = yes after double-checking
Rscript tests/test_pipeline.R          # optional: re-validate the software
Rscript R/run_all.R                    # writes output/tables and output/figures
python3 manuscript/build_manuscript.py # rebuilds the .docx with pooled values and Figures 3-7
```

Requirements: R ≥ 4.3 with `metafor`, `ggplot2`, `svglite` and `ragg`. Python 3 with `python-docx`, `openpyxl` and `matplotlib`.

## Integrity safeguards built into the code

- Only rows with `verified = yes` are analysed.
- Two reports from the same `overlap_group` cannot enter the same outcome; the pipeline stops with an error.
- Nothing is pooled when k < 2. Egger's test and funnel plots run only when k ≥ 10.
- *S. japonicum* is the primary stratum. Other species are never pooled with it.
- Adjusted and unadjusted HRs are pooled separately.
- The PRISMA figure shows `[TO BE CALCULATED]` for any count not marked verified.
