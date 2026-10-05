# Extraction log (2026-10-05)

This log explains where the numbers in `data/analysis_ready/*.csv` came from and why each overlap decision was made. Every row in those files also has its own `source_location` and `notes`.

## Who did the work, and what is still pending

- **One extractor.** Claude (AI-assisted) extracted every value from the full texts listed below. A second human extractor has not checked them yet (`extractor_2 = PENDING human second extractor`).
- **Programmatic cross-check.** Every value marked `data_origin = reported` was checked automatically: the script confirmed the exact number appears in the source text. All rows passed. The only mismatches were caused by trailing zeros (for example 1.280 vs 1.28) and by table cells that ran together in the XML (Cheng 2023). Those cases were checked by hand against the XML table cells.
- **`verified = yes`** means extracted from the full text and cross-checked as above. It does **not** yet mean double-extracted, as the protocol requires. Before submission, a human should re-extract and set `extractor_2`.
- **Risk of bias (NOS).** Rated by the same single AI-assisted assessor. A second assessor is pending.
- **GRADE.** Not yet rated.

## Sources retrieved

| Study | Source | Notes |
|---|---|---|
| Zheng 2023 | PMC10389396 XML + LWW Supplementary Digital Content 2-9 (.docx) | Supplements give the full 2x2 tables and the Cox models (Table S6) |
| Wang Z 2020 | PMC7039146 | |
| Wang W 2020 / 2021 / 2023 | PMC7330999 / PMC8573878 / PMC9890788 | |
| Pan 2020 | PMC7160914 (Europe PMC) | |
| Cheng 2023 (inventory "BMCGastro2023") | PMC10240683 | First author confirmed: Cheng M |
| Chai 2026 | PMC13559566 | New; found by the PubMed search |
| Li 2024 | PMC10798728 + LWW SDC PDF (CM9/B784) | Supplement Tables S1-S4 hold all the data |
| Zhang 2023, Zhu 2024 | PMC10719402, PMC11271061 | |
| Yang 2023 | PMC10500003 | Colon and rectal CRC are reported separately, so CRC data can be separated |
| Pan 2023 | PMC10538618 | |
| Yu 2023 (inventory "Genomic2023") | PMC10308108 | |
| Liu XF 2023 | PMC10731309 | Excluded (no CRC-specific comparison) |
| Feng 2015 | PMC4476884 (PMC HTML) | New |
| Wu 2021 | PMC8732260 (PMC HTML, Chinese) | New |

**Not retrieved** (publisher, KoreaScience/WAOCP or CNKI access needed): Wang M 2014, Wang M 2016, NCG 1986, Madbouly 2007, Liu 2013, Zhang W 2012 (CT), Chen 2016, Yang DH 2014, Ruan 2013, Yang XG 2021, Zhang R 1998 and Zalata 2005. Their abstract-level data are **not** analysed. The two Madbouly 2007 rows in `molecular_evidence.csv` are kept with `verified = no`.

## Overlap decisions (see `overlap_matrix.csv`)

- **G3 (Qingpu Branch, Zhongshan Hospital, 2008-01 to 2016-08).** Every full text confirms the same hospital and the same period. Wang W 2020 is the index report for clinicopathology and OS. The other five reports contribute biomarkers only: Wang W 2021 (PD-L1), Wang W 2023 (TILs, CD3, CD20), Pan 2020 (c-MYC), Cheng 2023 (CD4, CD8) and Chai 2026 (CFIm25).
- **Pan 2023** is **not** G3. It comes from the main Zhongshan campus, 2016-01 to 2018-12, and is a separate SACC-only cohort (G9).
- **G5 (Jingzhou).** Zhu 2024 is the index report. Zhang 2023 contributes only LN metastasis and perineural invasion. Zhu 2024's LN row is internally inconsistent, and Zhu 2024 does not report perineural invasion. Zhang 2023's other rows are kept with `include_primary = no`.
- **G2 (Yijishan, Wuhu).** Wang Z 2020 is the index report. Yang 2023 contributes only LN metastasis and vascular invasion, which Wang Z 2020 does not report.
- **Wu 2021** (Wuhu Second People's Hospital) is a different hospital in the same city, so it forms its own group (G10).

## Derived or recalculated values

- **Wang Z 2020 OS HR.** Derived with the Tierney (2007) method from the log-rank P (0.026), the total deaths (39) and the group sizes (43/57): HR 0.487 (0.258-0.917). The paper's death counts (18/43 vs 21/57) are hard to reconcile with its 5-year survival figures (68.9% vs 46.4%). This flag is in the row notes.
- **Zheng 2023.** The adjusted OS HR for schistosomiasis was not reported, because the stepwise model did not retain it. The adjusted DFS HR (1.098) is taken from SDC Table S6.
- **Pooled categories.** Where categories were combined (for example stage III + IV, or T3 + T4), `data_origin = calculated_from_raw` and the components are listed in `source_location`.

## Reporting inconsistencies found in source papers

- **Wang Z 2020.** Poor differentiation is 2.6% vs 21.9%, yet the reported P is 0.155.
- **Zhu 2024.** The LN metastasis percentages do not match the group sizes. The "T stage III+IV" row (94.7% vs 80.0%) does not match its P of 0.354.
- **Li 2024.** The text says metastatic disease was excluded, but Table S1 lists 66 patients at stage IV. The "n" column of Tables S2-S3 is also wrong.
- **Wang W 2021 and Wang W 2023.** Within-SACC HRs are reported with P = 0.045, but their 95% CIs include 1.
- **Cheng 2023.** Column totals in Table 3 differ from the body by 1-5 patients. The Table 4 column labels are swapped (NSCRC N = 137).
- **Feng 2015.** The counts and percentages for the signet-ring and mucinous rows disagree with each other.

## PubMed search (interim PRISMA)

- **Search.** Run on 2026-10-05 with the exact MEDLINE strategy in Supplementary Table S1. It returned 337 records, including all 22 inventory records.
- **Screening.** One AI-assisted reviewer screened the titles, then abstracts for candidate records. 29 reports were sought, 12 could not be retrieved, 17 were assessed and 1 was excluded. That leaves 16 included reports, of which 10 contribute to at least one meta-analysis.
- **Other databases.** Scopus, Web of Science, Embase, CNKI, Wanfang and SinoMed have **not** been searched.
- **Other excluded records.** These were also excluded on abstract:
  - Qin 2021: CRC occurrence in an endoscopy cohort.
  - Zhou LN 2022 and Yi 2016: no non-schistosomal comparator.
  - Kaw 2002: a Philippine CRC series with no schistosomiasis comparison.
  - Noeman 1994: S. mansoni laboratory markers, with mixed groups.

## Second pass (2026-10-05)

- **Additional searches.**
  - Europe PMC title/abstract search: 297 records, 30 not in PubMed.
  - Crossref bibliographic search: 15 relevant titles not found elsewhere.
  - OpenAlex was rate-limited and not used. Scopus, WoS, Embase, CNKI, Wanfang and SinoMed were inaccessible.
- **Newly retrieved.**
  - Wang M 2014: KoreaScience OA PDF. Adjusted OS HR 3.661 (1.458-9.193) and DFS HR 3.147 (1.359-7.290), Table 3; matched on age, sex and stage.
  - Liu 2013: no comparator; excluded.
  - Ge 2023: Research Square preprint, Xiangya Hospital, 94 vs 6025. OS HR 2.16 (1.26-3.71) derived from the matched cohort (35 vs 18 deaths, log-rank P=0.005).
  - Zhou 2025: preprint, Jiujiang. Percentages only, so qualitative.
  - Pan 2022: preprint, Qingpu. MET FISH-positive 12/131 vs 22/207.
- **Still not retrieved.**
  - Wang M 2016 (Wiley).
  - NCG 1986 (print only).
  - Madbouly 2007 (Springer).
  - Zhang W 2012 (Elsevier).
  - Zhang R 1998 (Elsevier).
  - Zalata 2005 (PMC/Hindawi access blocked).
  - Farid 2006 (site unreachable).
  - Four Chinese-language reports (CNKI/Wanfang).
- **Duplicate extraction and adjudication.** See `ADJUDICATION_LOG.md`.

## Third pass (2026-10-05): reports supplied by the review team

- **Extracted from the supplied PDFs.** Only the extracted data are stored in this repository; the PDFs themselves are not.
  - **Wang M 2016.** Within-SACC; CEA HR 4.053.
  - **NCG 1986.** Chinese; pages read as images. Male sex, T3-T4 direction, and an OS HR derived from 5-year survival with the Parmar method.
  - **Zhang R 1998.** Male sex, differentiation, mucinous histology, age, p53 and TP53.
  - **Madbouly 2007** and **Zalata 2005.** S. mansoni stratum; not pooled with S. japonicum.
  - **Farid 2006.** Excluded: no comparator.
- **Not obtained, so excluded:** Chen 2016, Yang DH 2014, Ruan 2013, Yang XG 2021 and Zhang W 2012. They are listed in Table S2 only.
- **Blinded second extraction.** Completed for all six reports; see ADJUDICATION_LOG.md, round 2.
- **The "Not retrieved" section above is superseded** by this pass.
