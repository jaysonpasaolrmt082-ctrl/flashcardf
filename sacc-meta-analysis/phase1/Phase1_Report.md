# Phase 1 report: SACC systematic analysis and meta-analysis

Prepared 2026-10-05. **Read the verification note first.**

## Verification note (what was and was not checked)

- The build environment's network policy **blocked PubMed, PMC, Europe PMC, Crossref, OpenAlex and all publisher sites**. Only a general web-search tool was available. Every study below was found through that tool. For each one, the title, journal, and PMID, DOI or PMCID were matched to a PubMed, PMC or publisher index URL that appeared in the search results.
- **No full text was read.** Sample sizes, periods and findings come from the abstract text that the search tool returned. They are marked "abstract-level" and must be re-extracted from the full text.
- Nothing was invented. Where a value could not be found it is recorded as `NR` (not retrieved) or `[TO BE VERIFIED]`.
- No meta-analysis was run on real data (integrity rule 13). The R pipeline was tested only on metafor's published BCG benchmark dataset and on clearly labelled synthetic test rows, inside a temporary folder. None of that output is in this repository.

---

## 1. Final PECO

| Element | Definition |
|---|---|
| **P** | Adults with histologically or clinically confirmed colorectal adenocarcinoma/carcinoma |
| **E** | Current or previous intestinal schistosomiasis. The primary stratum is *S. japonicum*, either confirmed or presumed from an endemic-area cohort. Ascertainment is recorded verbatim (egg histology, pathology report, history, stool, serology, PCR, clinical diagnosis) |
| **C** | CRC without evidence, history or pathological findings of schistosomiasis, from the same source population |
| **O** | Primary: OS (HR); DFS/RFS (HR); stage III–IV vs I–II (OR); lymph-node metastasis (OR); distant metastasis (OR). Secondary: demographics, location, pathology, molecular markers, laboratory markers (exploratory), recurrence |
| Separate analyses | (a) within-SACC prognostic factors (SACC-only cohorts); (b) *S. mansoni* / *S. haematobium* / unspecified species; (c) epidemiological CRC-risk studies, catalogued only |

## 2. Inclusion and exclusion criteria

**Include:** observational comparative studies (retrospective or prospective cohorts, case-control, comparative pathological series) of human CRC that report schistosomiasis-associated CRC with a non-schistosomal comparator and give extractable clinicopathological, molecular or survival data. Any language is accepted.
**Within-SACC set only:** SACC-only cohorts that report prognostic factors (egg location, nodal eggs, hepatic schistosomiasis, CEA, T/N stage, etc.).
**Exclude:** case reports; descriptive case series without comparative data; animal and in-vitro studies; editorials and commentaries; narrative and systematic reviews (used only for citation chasing); duplicate reports of the same population for the same outcome; CRC not separable from other cancers; schistosomiasis status undeterminable.
**Exclusion-reason hierarchy (one per full text):** not CRC → not human → no schistosomiasis status → no comparator → no extractable outcome → duplicate cohort.

## 3. Database search strategies

The full strategies for PubMed, Scopus, Web of Science, Embase, CNKI, Wanfang and SinoMed, plus Google Scholar for citation chasing, are in `manuscript/build_manuscript.py` (`SEARCHES`). They are rendered as **Supplementary Table S1** in `manuscript/SACC_Supplementary_Material.docx`. No outcome terms are required, and no language or date limits are applied. The searches themselves still need to be **run by you**, with the date and hit count recorded for each database, because those databases were not reachable from here.

## 4. Initial inventory of studies (identifiers checked against index entries)

Full machine-readable version: `data/study_inventory.csv`. "Abstract-level" = numbers taken from the abstract only.

| Study | PMID | DOI | Institution | Period | SACC n | NSACC n | Outcomes (abstract) | Overlap group | Status |
|---|---|---|---|---|---|---|---|---|---|
| Zheng 2023, Int J Surg | 36999800 | 10.1097/JS9.0000000000000293 | Changhai Hosp., Shanghai | 2001–2021 | 823 | 30,330 | trends, clinicopath., KRAS, multiple primary, polyps, OS, DFS (not independent) | G1 | Eligible |
| Wang Z 2020, Oncol Lett | 32194737 | 10.3892/ol.2020.11331 | Yijishan Hosp., Wuhu, Anhui | NR | 253 | 2,885* | age, sex, FOBT, pT, CA19-9, WBC/RBC/PLT, 5-y survival | G2 | Eligible |
| Wang W 2020, World J Surg Oncol | 32611359 | 10.1186/s12957-020-01925-5 | Qingpu Branch, Zhongshan Hosp., Shanghai | 2008–2016 | 137 | 214 | age, clinicopath., OS (independent) | G3 (index) | Eligible |
| Wang W 2021, World J Surg Oncol | 34743724 | 10.1186/s12957-021-02433-w | Qingpu Branch | NR | NR | NR (338 total) | CD8, PD-L1, OS | G3 | Overlap: immune markers only |
| Wang W 2023, World J Surg Oncol | 36726115 | 10.1186/s12957-023-02911-3 | Qingpu Branch | NR | NR | NR (349 total) | sTIL, CD3, CD20 | G3 | Overlap: immune markers only |
| Pan 2020, Jpn J Clin Oncol | 32297641 | 10.1093/jjco/hyz210 | Zhongshan/Qingpu (shared authors) | NR | NR | NR (354 total) | c-MYC amplification | G3 | Overlap: c-MYC only |
| BMC Gastroenterol 2023 (authors TBV) | 37277702 | 10.1186/s12876-023-02834-z | NR (suspected G3) | NR | NR | NR | CD4, CD8, CRP, OS | G3? | Check institution |
| Li 2024, Chin Med J | 37920960 | 10.1097/CM9.0000000000002905 | Union Hosp., Wuhan | NR | 30 | 459 | KRAS G12S/D, OS | G4 | Eligible |
| Zhang 2023, Pathol Oncol Res | 38099242 | 10.3389/pore.2023.1611396 | Jingzhou Hosp., Hubei | 2020–2022 | 101 | 240 | sex, TNM, LN, PNI, vascular thrombus, differentiation | G5 | Eligible; **overlaps Zhu 2024** |
| Zhu 2024, BMC Infect Dis | 39054428 | 10.1186/s12879-024-09648-8 | Central China (verify) | 2020–2022 | 95 | 406 | age, site, T stage | G5? | Resolve overlap |
| Wang M 2014, Asian Pac J Cancer Prev | 25422211 | 10.7314/apjcp.2014.15.21.9271 | West China Hosp., Chengdu | NR | 30 | 30 (matched) | OS, DFS | G6 | Survival only (stage-matched) |
| NCG 1986, Zhonghua Zhong Liu Za Zhi (Chinese) | 3021419 | – | Multicentre, China | NR | 430 | NR | 5-y survival | G7 | Needs Chinese full text |
| Madbouly 2007, Int J Colorectal Dis | 16786317 | 10.1007/s00384-006-0144-3 | Univ. Alexandria, Egypt | NR | 40 | 20 | p53, MMR, MSI, stage, synchronous | G8 | ***S. mansoni*** stratum only |
| Yang 2023, Sci Rep | 37704736 | 10.1038/s41598-023-42456-9 | Yijishan Hosp., Wuhu | NR | NR | NR | multi-organ tumours | G2 | Uncertain (CRC separable?) |
| Wang M 2016, Colorectal Dis | 26922912 | 10.1111/codi.13317 | West China (verify) | NR | NR | – | egg site, CEA, pT, OS | G6 | Within-SACC |
| Pan 2023, Eur J Cancer Prev | 37200090 | 10.1097/CEJ.0000000000000811 | NR (verify) | NR | 172 | – | nodal eggs, hepatic schisto., DFS, OS | G3? | Within-SACC |
| Liu 2013, Asian Pac J Cancer Prev | 24083755 | 10.7314/APJCP.2013.14.8.4839 | NR | NR | 32 | – | endoscopy, pathology | – | No comparator → exclude from comparative |
| CT study 2012, Eur J Radiol | 22658847 | NR | NR | NR | 130 | – | multifocality, histology | – | Within-SACC descriptive |
| Genomic 2023, Genes Dis | 37396536 | 10.1016/j.gendis.2022.05.026 | Changzheng Hosp., Shanghai | 2014–2020 | 30 | external | WES, TMB, MSI | – | Molecular map only |
| Xu & Su 1984, Int J Cancer | 6480152 | 10.1002/ijc.2910340305 | – | – | – | – | CRC risk | – | Epidemiological (separate) |
| Qiu 2005, Ann Trop Med Parasitol | 15701255 | NR | – | – | – | – | CRC risk | – | Epidemiological (separate) |
| Liu XF 2023, Front Oncol | 38125940 | 10.3389/fonc.2023.1288197 | – | 2018–2021 | – | – | malignancy in *S. japonicum* pts | – | Check CRC separability |

\*NSACC n for Wang Z 2020 = 3,138 − 253 (calculated from the abstract totals).

**Not yet searched (blocked or needs institutional access):** CNKI, Wanfang and SinoMed. These are likely to hold several more Chinese-language comparative cohorts. Embase, Scopus and WoS also need formal runs.

## 5. Study-overlap assessment

The full matrix is in `data/overlap_matrix.csv` (Supplementary Table S6). Key findings:

- **G3, Qingpu Branch of Zhongshan Hospital (Fudan), Shanghai: up to six reports** (Wang W 2020/2021/2023, Pan 2020, probably BMC Gastroenterol 2023, and possibly Pan 2023). Their totals of 338–354 patients are almost certainly one cohort. Use Wang W 2020 for clinicopathology and OS. Use each of the others **only** for its own biomarker.
- **G5, Jingzhou/Central China:** Zhang 2023 and Zhu 2024 share an author (Zhu Y) and the identical 2020–2022 period, so the overlap is highly probable. Use one report per outcome.
- **G2, Yijishan Hospital, Wuhu:** Wang Z 2020 and Yang 2023.
- **G6, West China Hospital:** Wang M 2014 (comparative, survival) and Wang M 2016 (SACC-only).
- **Shanghai cross-hospital:** Zheng 2023 (Changhai) and Genomic 2023 (Changzheng) are both Naval Medical University hospitals. The overlap is probably small but should be checked.
- The R code **refuses to pool** two rows from the same overlap group for the same outcome. This is tested.

**Realistic count of independent *S. japonicum* comparative cohorts: about 6** (G1, G2, G3, G4, G5, G6), plus possibly G7 (1986) and any CNKI/Wanfang additions.

## 6. Extraction spreadsheet structure

`data/SACC_master_extraction.xlsx` contains these sheets:
- `master_wide`: every variable you listed (179 columns), grouped by domain and pre-filled with the identifiers above.
- Long, analysis-ready sheets: `binary_outcomes`, `continuous_outcomes`, `survival_outcomes`, `within_sacc_prognostic`, `molecular_evidence`, `evidence_direction`, `rob_nos`, `prisma_counts`. The same files exist as CSVs in `data/analysis_ready/`, and the R pipeline reads those.
- Each row records `data_origin` (reported / calculated_from_raw / KM_reconstructed / converted_median_IQR), `source_location`, two extractors, `overlap_group`, `species_stratum`, `histology_confirmed`, `rob_overall`, and **`verified` (only `yes` rows are ever analysed)**.

## 7. Outcomes likely to support quantitative meta-analysis (provisional, from abstracts)

| Outcome | Likely independent cohorts | Comment |
|---|---|---|
| Overall survival HR | 3–5 (G1, G3, G4, G6, ±G2/G7) | Adjusted and unadjusted must be pooled separately; G1 adjusted vs others |
| DFS/RFS HR | 2–3 (G1, G6, ±G3) | Borderline |
| Stage III–IV | 3–5 | Wang M 2014 is excluded because it was stage-matched |
| Lymph-node metastasis | 3–4 | |
| Distant metastasis | 2–3 | Borderline |
| Male sex, age | 4–5 | Age may need the median/IQR conversion |
| Rectal / sigmoid location | 3–4 | |
| T3–T4 | 3–4 | |
| Differentiation / mucinous | 2–3 | Borderline |
| Vascular / perineural invasion | 2–3 | Borderline |

## 8. Outcomes that should stay qualitative

- KRAS: two cohorts with different assays (G12S/D qPCR vs [TO BE VERIFIED]). Pool only if the definitions match.
- Multiple primary CRC and concomitant polyps: Zheng 2023 only. *S. mansoni* synchronous tumours stay separate.
- c-MYC, TMB/WES, immune infiltrates (CD3/CD4/CD8/PD-L1/CRP): one institution or an external comparator.
- p53 IHC, MLH1/MSH2, MSI: *S. mansoni* only.
- NRAS, BRAF, TP53 mutation, APC, PIK3CA, β-catenin, Ki-67: no comparative data found.
- Laboratory markers (CEA, CA19-9, CBC): exploratory, mostly one cohort each.
- All within-SACC factors (egg site, nodal eggs, hepatic schistosomiasis): definitions differ, so tabulate them in Table 5.

## 9. Existing meta-analyses overlapping this question

- **Global prevalence and correlation of intestinal parasitic infections in patients with CRC** (BMC Gastroenterol 2025; PMID 40804378; DOI 10.1186/s12876-025-04144-y). It addresses prevalence and the parasite–CRC association. It reports a pooled Schistosoma prevalence among CRC patients and a pooled OR; those values were seen only in a search summary and must be checked before citing. This is **a different question** from ours.
- A Zenodo record titled "Parasitic infections, antiparasitic drug exposure, and cancer risk: a systematic review and meta-analysis" was seen in search results. It looks like a preprint or dataset about cancer risk. Check its status.
- Narrative reviews (not meta-analyses): Hamid 2019 Am J Trop Med Hyg; Acta Parasitol 2023 (PMID 37594685); J Public Health Emerg review.
- **No meta-analysis comparing the SACC and NSACC phenotype or prognosis was found.** The web-search tool is not a systematic search, though, so do **not** claim "first" until the formal PubMed/Scopus/WoS/Embase/CNKI searches confirm it.

## 10. Novelty and publishability (2026–2027)

- **Novelty: moderate and real but narrow.** The specific question (phenotype and prognosis among patients who already have CRC) appears unaddressed by any quantitative synthesis. The newer cohorts (2020–2024) and the explicit overlap handling add value.
- **Main threats:**
  - The evidence base is small, about 6 independent cohorts, all Chinese.
  - The Zheng 2023 cohort (n = 31,153) dominates every analysis it enters, and its conclusion (no independent survival effect) differs from the smaller cohorts.
  - Molecular data are too sparse to claim a "molecular phenotype". The title may need to keep "molecular" only as something that was examined, not as a finding.
- **Fit for Acta Medica Philippina:** good, because *S. japonicum* is endemic in the Philippines. The paper's strongest message for this journal is the evidence gap for Philippine and Indonesian patients.
- **Recommendation:** register the protocol on **PROSPERO now**. It accepts reviews until data extraction is complete. Then run the formal searches, including CNKI and Wanfang, before extracting anything.

## Next actions for you

1. Run the searches in Table S1. Record dates and counts in `data/analysis_ready/prisma_counts.csv` and set `verified = yes`.
2. Screen (two reviewers). Log the exclusions for Table S2.
3. Extract from the full texts into the workbook or CSVs, with two extractors. Set `verified = yes` only after cross-checking.
4. Run `Rscript R/run_all.R`, then `python3 manuscript/build_manuscript.py`. Tables 4 and 6, Figures 3–7 and the Results sentences fill in automatically from the verified output.
5. Complete the 18 references flagged `[VERIFY]` from PubMed.
