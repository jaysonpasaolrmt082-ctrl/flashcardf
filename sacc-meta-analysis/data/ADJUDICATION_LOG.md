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
