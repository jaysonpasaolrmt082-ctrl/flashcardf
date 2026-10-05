# SACC systematic analysis and meta-analysis (Acta Medica Philippina)

**Defining Schistosomiasis-Associated Colorectal Cancer: A Systematic Analysis and Meta-analysis of Clinicopathological, Molecular, and Prognostic Features**

## Status (updated 2026-10-05, third pass)

The manuscript is a **complete draft**: Results, GRADE, Discussion and Conclusion are written and generated from the verified data. Only items that the authors alone can supply remain, highlighted in yellow as `[AUTHOR INPUT: ...]`: co-authors, affiliations, address, ORCID, registration, funding, conflicts, CRediT roles, acknowledgments, repository DOI, and the names of the authors who verified the AI-assisted work.

**Searches**
- PubMed, Europe PMC (including preprints and Chinese Biological Abstracts) and Crossref were searched on 2026-10-05.
- Scopus, Web of Science, Embase, CNKI, Wanfang and SinoMed could **not** be searched, because there was no subscription or login access. The manuscript states this as a limitation; Table S1 gives ready-to-run strategies for all six.

**Full texts**
- 28 full texts were assessed and 25 reports included: 12 S. japonicum comparative cohorts, 2 SACC-only cohorts, 1 genomic study and 2 S. mansoni series. 15 reports contribute to at least one meta-analysis.
- The review team supplied six PDFs: Wang M 2016, NCG 1986, Zhang R 1998, Madbouly 2007, Zalata 2005 and Farid 2006. All six were extracted; Farid 2006 was excluded because it has no comparator. The PDFs are not stored in this repository.
- Five reports could not be obtained, so they were **excluded** and listed in Supplementary Table S2 and the PRISMA "not retrieved" box. Four are Chinese-language biomarker studies and one is an imaging study. They are not cited anywhere else in the manuscript.

**Duplicate extraction**
- A second, independent extraction was blinded to the first; it was done by an AI agent working only from the source texts, not by a human (`data/second_extraction/`).
- Disagreements were adjudicated against the source (`data/ADJUDICATION_LOG.md`).
- Agreement: 78/82 binary rows; 100% for survival, continuous, molecular and within-SACC values; 87/88 NOS items.
- Round 2 covered the six supplied reports. All doubly extracted values agreed. Four NOS item disagreements were resolved in favour of the source text: NCG 1986 is now 5 (moderate), Zhang R 1998 3 (high), Madbouly 2007 4 (high) and Zalata 2005 5 (moderate).

**Figures**
- Figure 1 (PRISMA) shows only the sources actually searched.
- In Figures 4 and 5, heterogeneity statistics now sit below each pooled diamond, so there is no overlap.
- Figure 7 was redesigned as a domain-grouped evidence map with direction symbols, sample sizes and per-feature tallies.

**GRADE**
- Ratings are in `data/analysis_ready/grade.csv` (Supplementary Table S4b).

**Before submission**
- An author must check the extraction and judgements against the source articles and complete the AUTHOR INPUT fields.
- If institutional access is available, run the six remaining database searches and re-run `R/run_all.R` and `manuscript/build_manuscript.py`.

## Contents

| Path | What it is |
|---|---|
| `phase1/Phase1_Report.md` | Answers to the 10 first-task items: PECO, criteria, searches, verified inventory, overlap, outcomes feasibility, existing meta-analyses, novelty |
| `manuscript/SACC_Manuscript_ActaMedPhilipp.docx` | Manuscript in journal format (Arial 12, single-spaced, figures and tables in text, ICMJE references) |
| `manuscript/SACC_Supplementary_Material.docx` | Tables S1–S6 and the PRISMA 2020 checklist |
| `manuscript/Cover_Letter.docx`, `Highlights_and_Graphical_Abstract.docx`, `Figure_and_Table_Legends.docx` | Submission extras |
| `data/study_inventory.csv`, `data/overlap_matrix.csv` | Study inventory and overlap matrix |
| `data/SACC_master_extraction.xlsx` | Master extraction workbook |
| `data/analysis_ready/*.csv` | Analysis-ready long-format files (extracted data, `verified = yes`) |
| `data/EXTRACTION_LOG.md` | Sources, overlap decisions, derived values and source-paper inconsistencies |
| `output/tables/` | Pooled results (Table 4), sensitivity (Table S5), within-SACC and molecular tables, analysis log; figures are regenerated into `output/figures/` (git-ignored) |
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
