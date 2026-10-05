# Duplicate extraction and adjudication (2026-10-05)

**Reviewer 1** extracted the data, documented in `EXTRACTION_LOG.md`.

**Reviewer 2** was an independent AI extraction run. It was given only the source full texts, a field list and the NOS rules. It had no access to reviewer 1's files. Its raw outputs are archived in `data/second_extraction/`.

Disagreements were resolved against the source table or text.

| Domain | Items compared | Agreement | Disagreements and resolution |
|---|---|---|---|
| Binary counts | 82 rows (4 numbers each) | 78 identical | **Zheng 2023 LN:** Table 1 gives 260 and Table S4 gives 261. This is a source inconsistency; Table S4 kept. **Right-sided location (Wang Z 2020, Zhu 2024):** a definition difference; caecum + ascending + transverse kept, consistent with Li 2024. **Ge 2023 age >60:** changed to the text values 79/94 vs 2973/6025, which match the text's own percentages. |
| Binary rows found by reviewer 2 only | 17 | - | **Feng 2015 distant metastasis (0/26 vs 1/34):** added. **Not used:** Wang M 2014 matched outcomes (matched design); Yang 2023 and Zhang 2023 duplicates of the overlap-group index study; Zhu 2024 LN and stage (internally inconsistent); Zhang 2023 age >50 (different cut-off); Ge 2023 polyps (matched cohort only). |
| Survival HRs | 11 | 11/11 | Inputs for both derived HRs (deaths, log-rank P, n) were identical. |
| Continuous (pooled age) | 4 | 4/4 | |
| Molecular counts | 21 | 21/21 | |
| Within-SACC HRs | 19 | 19/19 | |
| NOS items | 88 (11 studies × 8) | 87/88 | **Wang W 2020 comparability:** changed from 2 to 1 star (adjusted for stage and sex but not age). Total 7; still low risk. |
| NOS overall rating | 11 | 11/11 | |

Reviewer 2 flagged three additional source inconsistencies, now noted in the extraction file:
- **Li 2024:** KRAS G12S/D is given as 12/30 in the text but 13/30 in Supplementary Table S4. The table value is used.
- **Wu 2021:** the printed χ² of 3.827 corresponds to P = 0.050, not the stated P < 0.05.
- **Chai 2026:** P < 0.05 is reported with confidence intervals that include 1.

**Human verification by the authors** is still required before submission. See "Use of AI-assisted Tools" in the manuscript.

## Round 2: reports supplied by the review team (2026-10-05)

Wang M 2016, NCG 1986, Zhang R 1998, Madbouly 2007, Zalata 2005 and Farid 2006 were re-extracted blind by a second AI reviewer, working only from the source texts and page images.

**Agreement.** All numeric values matched for the binary, continuous, molecular, survival-source and within-SACC rows: Madbouly 9/9, Zhang R 5/5, Zalata 3/3, NCG 1/1 and Wang M 2016 CEA 1/1.

**Discrepancies resolved:**
- **Zalata 2005, p53 antibody.** Changed to clone 1801 (Methods, line "antibody (clone 1801)"), with a diffuse threshold of >30% nuclei. Reviewer 2 was correct.
- **Added from reviewer 2:**
  - Zalata 2005 male sex, 16/24 vs 28/59. Calculated from percentages; S. mansoni stratum; not pooled.
  - Madbouly 2007 DCC loss, 16/40 vs 11/20.
- **NCG 1986 overall survival.** Reviewer 2 recorded crude 5-year survival only (45.6% vs 50.9%). The HR used (1.163, 1.007-1.344) is derived from these figures with the Parmar method and is labelled `derived_from_5y_survival`. It enters only the unadjusted pool.
- **NOS ratings.** Reviewer 2's scores were adopted for four items:
  - NCG 1986, O1: 0, because outcome ascertainment is not described. Total 5, moderate.
  - Zhang R 1998, S3: 0, because the method of diagnosing schistosomiasis is not stated. Total 3, high.
  - Madbouly 2007, S1: 0, because the paper does not say patients were consecutive. Total 4, high.
  - Zalata 2005, S1: 1, because the paper reports "eighty-three consecutive patients". Total 5, moderate.
- **Farid 2006.** Both reviewers agree it has no non-schistosomal comparator, so it is excluded at full text.
- **Wang M 2016.** Both reviewers agree it is SACC-only and is used only for the within-SACC CEA estimate.

**Reporting inconsistencies found by reviewer 2.** These are recorded in the row notes:
- Madbouly 2007: the P values for LN involvement and age conflict between sources.
- Zalata 2005: the recalculated p53 P value is 0.37, not the reported 0.073.
- NCG 1986: two different 5-year survival figures are given for tumours >10 cm (26.5% vs 37.5%).
