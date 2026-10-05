# Reviewer 2 – internal inconsistencies and cohort overlap

All observations come from the source texts in `reviewer2/sources/`.

## A. Overlapping cohorts

### A1. The Qingpu Branch, Zhongshan Hospital (Fudan University) reports describe the same patients

| Report | Hospital | Period | N (SACC / NSACC) | Notes |
|---|---|---|---|---|
| WangW2020 | Qingpu Branch, Zhongshan Hosp. | Jan 2008 – Aug 2016 | 351 (137 / 214) | Index cohort. Median follow-up 62.4 mo, 146 deaths (41.6%) |
| Pan2020 | same | Jan 2008 – Aug 2016 | 354 (138 / 216) | Same median follow-up of 62.4 mo (0.4–134.4). 148 deaths. TMA for c-MYC |
| WangW2021 | same | Jan 2008 – Aug 2016 | 338 (128 / 210) | TMA subset. "Inclusion criteria as previously described [WangW2020]". Mean/median OS 62.54/62.85 mo, the same values as WangW2020 |
| Pan2022 | same | Jan 2008 – Aug 2016 | 338 (131 / 207) | Cites WangW2020 for its criteria. **Same total N as WangW2021 but a different SACC split (131 vs 128).** Median follow-up 51.3 mo, which differs from the others |
| WangW2023 | same | Jan 2008 – Aug 2016 | 349 (137 SACC overall); 314 with IHC (126 / 188) | Mean/median OS 68/69 mo |
| Cheng2023 | same | Jan 2008 – Aug 2016 | 351 (137 / 214) | Identical to WangW2020: same N, same split, median FU 62.4 mo, 146 deaths. Univariate HR for schistosomiasis 1.399 (1.009–1.940), identical to WangW2020 |
| Chai2026 | same | Jan 2008 – Aug 2016 | 286 (112 / 174) | "351 patients met criteria described previously", then 65 were excluded for tissue detachment |
| Pan2023 | **Zhongshan Hospital main campus** (Fudan) | Jan 2016 – Dec 2018 | 172 SACC only | Different site and a mostly later period. Overlap with the Qingpu cohort is unlikely; only Jan–Aug 2016 coincides, and that is at a different campus |

**Conclusion.** WangW2020, Pan2020, WangW2021, Pan2022, WangW2023, Cheng2023 and Chai2026 come from one cohort: the same single institution, dates and inclusion criteria, with shared authors (Weixia Wang, Weiyu Pan, Junxia Yao, Sinian Huang, Dacheng Bu). The slightly different Ns (286–354) come from TMA or IHC availability. Pool only one of them for any SACC vs NSACC outcome. WangW2020 is the primary report.

Evidence of duplicated or copied analyses:
- Several within-SACC univariate HRs are identical across WangW2021 Table 4 (n=128), WangW2023 Table 3 (n=126) and Cheng2023 Table 4. Examples:
  - age 21.827 (0.139–3436.270)
  - gender 1.311 (0.779–2.207)
  - LNM 3.552 (2.141–5.894)
  - tumour deposit 4.138 (2.205–7.769)
  - differentiation 1.668 (0.991–2.809)
  - perforation 0.506 (0.070–3.657)
  - nervous invasion 1.727 (0.741–4.024)

  These results are reported for n = 126, 128 and 137, which is not possible if the analyses were run separately.
- The CD8 HR in the SCRC set is 0.412 (0.239–0.711) in both WangW2021 (whole-section CD8 density, cut-off 279) and Cheng2023 (intratumoral CD8, cut-off 77). The NSCRC value of 0.459 (0.283–0.745) is also identical across the two papers.
- In Cheng2023, the SCRC "ulceration" HR of 1.008 (0.670–1.514) is identical to the stage III–IV ulceration HR in WangW2020 Table 2.
- In WangW2021 Table 4, the "Schistosomiasis" HR inside the SCRC set, 1.225 (0.703–2.132), is meaningless there. It equals the WangW2020 stage I–II schistosomiasis HR.

The SACC vs NSACC OS HRs from the overlapping Qingpu reports are:

| Report | Univariate HR (95% CI) | Adjusted HR (95% CI) |
|---|---|---|
| WangW2020 | 1.399 (1.009–1.940) | 1.458 (1.049–2.027) |
| Pan2020 | 1.402 (1.014–1.940) | not retained |
| WangW2021 | 1.388 (0.994–1.940) | 1.424 (1.016–1.996) |
| Pan2022 | 1.422 (1.017–1.990) | 1.513 (1.077–2.125) |
| WangW2023 | 1.390 (1.001–1.929) | not retained |
| Cheng2023 | 1.399 (1.009–1.940) | 1.404 (1.007–1.958) |
| Chai2026 | 1.414 (0.982–2.036) | not retained |

### A2. Zhang2023 and Zhu2024 (Jingzhou, Hubei)

- **Zhu2024**: Jingzhou Hospital affiliated to Yangtze University. Jan 2020 – Aug 2022. 95 SACC / 406 NSACC. Ethics approval 2023-106-01 from that hospital.
- **Zhang2023**: "our hospital", with ethics from the Faculty of Medicine, Yangtze University (KY202320). Jan 2020 – Dec 2022. 101 SACC / 240 NSACC (the Group A age range is 45–88).
- **Conclusion:** both are very probably from the same Yangtze University / Jingzhou hospital system over almost the same period. The SACC groups (95 vs 101) are likely largely the same patients. The SACC age ranges, 46–88 in Zhu and 45–88 in Zhang, are almost identical. The hospital is not named explicitly in Zhang2023, so overlap cannot be proven, but it should be assumed. Do not pool both in the same analysis without a sensitivity analysis.

### A3. Other possible overlaps

- **WangZ2020** used Yijishan Hospital (the First Affiliated Hospital of Wannan Medical College, Wuhu) for 2012–2018. **Yang2023** used the First Affiliated Hospital of Wannan Medical College plus Chizhou People's Hospital for 2015–2021. These overlap from 2015 to 2018 at the same hospital.
- **Wu2021** used Wuhu Second People's Hospital (Jun 2015 – Jun 2020). This is a different hospital in the same city, but ethics approval came from Wannan Medical College.
- **Zhu2024** Table 3 cites a "2020 Wang ZJ" Wuhu study with 265 SACC / 3289 NSACC. These figures do not match WangZ2020 (253 / 2885), so they may come from a different or companion report.

## B. Internal inconsistencies by study

### Zheng2023
- The lymph-node data disagree between tables. Table 1 gives SACC pN0 = 491 (N1 178 + N2 82 = 260), while Suppl. Table S4 gives LN-negative 490 / positive 261. NSACC is consistent at 6001.
- Several multivariable HRs in Table 2 (SACC only) have CIs that are implausibly asymmetric on the log scale or barely include the point estimate:
  - OS, age: 1.655 (0.249–2.141)
  - DFS, pN: 1.615 (0.166–2.284)
  - DFS, M1: 1.854 (0.320–4.253)
  - OS, differentiation: 1.610 (0.181–3.765)
  - OS, vascular invasion: 0.313 (0.105–1.931)
- The CEA value is printed as "0.89 1".
- The SACC vs NSACC DFS HR of 1.575 cited in the main text is the univariate value. The adjusted HR is 1.098 (0.774–1.557), from Suppl. Table S6. No adjusted OS HR was reported because schistosomiasis was not retained.
- The abstract says SACRC has "less" LN or distant metastasis, but the pN and pTNM differences were not significant (P=0.060 for pTNM).
- Survival data exist for only 6537 of 16,963 patients (392/808 SACC). The paper reports no follow-up duration.

### WangZ2020
- The Methods give the SACC age SD as "10" (65.32±10), while Table I gives 10.57.
- Differentiation: poorly differentiated was 2.6% (SACC) vs 21.9% (NSACC), yet the reported P is 0.155 (Table IV) or 0.2 (text). A difference of that size with n=253 vs 2885 would be highly significant. There is a reporting error somewhere.
- Survival: 18 of 43 SACC died, yet the reported 5-year survival is 68.9%. For NSACC, 21 of 57 died (63% alive), yet the reported 5-year survival is 46.4%. These figures are hard to reconcile with a Kaplan–Meier analysis that has a median follow-up of 78 months.
- The follow-up cohort is a small, unexplained subset (2012–2013 only).
- In Table VI, the SACC CA19-9 HR is 1.004 (0.152–1.008). The point estimate sits at the edge of its CI.
- The text says the NSACC CRC incidence in 2012 was "1.73/10^6", but Table III gives 17.30/10^5.

### Yang2023
- In the colon table (Table 6), NSACC differentiation sums to 149 (35+86+28), not the stated n of 159.
- Colon LN metastasis and cancer-thrombus data are available for only 55/158 SACC and 60/159 NSACC. This is not explained.
- The rectal-cancer Discussion says the sex difference had "P = 0.005" and differentiation "P = 0.013". Table 7 gives P = 0.061 and P = 0.001; the Discussion values are copied from the colon results.
- The gastric-cancer Discussion gives differentiation P = 0.232, but Table 4 gives P = 0.003.
- NSACC controls were sampled as "almost the same number of patients each year". The design is therefore not a cohort, and the colon/rectal proportions are artificial.

### WangW2020
- Table 1 gives 214 males overall, while the text gives 212 (60.2%) and Table 3 sums to 212. Table 3's 137/214 group sizes may have been copied into the male row.
- The stage III–IV and LN-positive subgroup sex counts in Table 3 do not add up to the whole-cohort counts. For example, NSACC males are 70 + 42 = 112, not 126. In the LNM subgroup, males are 35/36 and females 53/20, which suggests the rows are swapped.
- Table 1 percentages are wrong: nervous invasion "31 (1.0%)", LN >2 "42 (1.2%)", perforation "13 (0.4%)". The nervous-invasion counts are 31 in Table 1 and 32 in Table 3.
- Table 1 gives TNM I+II = 190, but the subgroup N is 192.
- The text says stage IV n=22 is "1.7%" (it is 6.3%) and that 7 patients under 40 are "0.02%".
- The log-rank P is 0.0277 in the Results and 0.0260 in the Discussion.
- OS is defined as "death caused by CRC", so it is really cancer-specific survival.
- In Table 2, the univariate stage III–IV differentiation result is printed as "1.083 (1.083–2.466)", and the LNM subgroup "lymph nodes positive" HR as 0.723 (1.479–3.693). Neither point estimate lies properly within its CI.

### Li2024 (research letter)
- The text says patients with metastatic disease were excluded, but Suppl. Table 1 lists 66 stage IV patients (6 SACC).
- KRAS G12S/D in SACC is "12/30" in the text but 43.3%, which is 13/30. Table S4 gives 13.
- Suppl. Table 5:
  - The title says 230 patients, but only the 40 PSM-matched patients are shown, all of them male.
  - KRAS G12S is listed as "present" in 100%, while the text says G12S was absent.
  - The G12D total is printed as "8 (17.5%)"; 3 + 4 = 7.
- Suppl. Tables 2–3 list covariate n's (e.g., male 869, female 608; total 1477) that far exceed 489.
- The study period is stated as "January 1, 2010 to June 31, 2019". June 31 does not exist.
- Follow-up duration is not reported.

### Zhu2024
- The LN metastasis row gives 6 (10.3%) SACC and 19 (8.2%) NSACC. Those percentages imply denominators of about 58 and 232, not 95 and 406.
- The "T stage I+II / III+IV" row gives 5/90 vs 81/325, and appears to be TNM stage:
  - χ² = 0.861, P = 0.354 is incompatible with 94.7% vs 80.0%.
  - Stage III+IV in 90/95 is incompatible with only 6 LN-positive SACC.
  - The depth-of-invasion data (T1–2 = 17 SACC) do not match "I+II = 5".
  - The abstract nonetheless reports T stage as non-significant, while the conclusion says SACC had a "higher T stage" in the Yangtze basin.
- Histology: adenocarcinoma totals 460 overall but 375 + 89 = 464 by group.
- Intravascular tumour thrombus: the "all patients" total is 209, but 174 + 38 = 212. The SACC percentage of 40.4% implies n = 94.
- The Discussion says Wuhu is in "Hubei"; Wuhu is in Anhui.
- Table 2 lists location P = 0.000 and a total-colon case (footnote b).

### Zhang2023
- The age dichotomy is ≤50 / >50 only, so no ≥60 data are available.
- The T category comes from preoperative imaging ("imaging TNM staging"), not pathology.
- The abstract calls the higher T3 proportion in SACC "certain advantages" and also claims "high tumor differentiation, low malignancy". This is an odd interpretation.
- The hospital is not named.

### Wu2021
- LN metastasis was reported as χ² = 3.827, "P < 0.05". With 1 df, χ² = 3.827 gives P ≈ 0.0504, which is not < 0.05. This is the paper's main finding. Recomputing 35/56 vs 145/307 shows that 3.827 is exactly the Yates-corrected χ² (P = 0.050). The uncorrected χ² is 4.417 (P = 0.036). The result is borderline, and the printed P does not match the printed statistic.
- Differentiation is split only as moderate vs "moderate-poor", which is non-standard.
- Age and sex are reported only as "no difference" or "older", with no group data.

### Feng2015
- The signet-ring and mucinous rows conflict. The table prints "7 (7.7%)" and "3 (30.8%)", while the text gives 8% and 31%, i.e., 2 and 8. Both readings give a combined 10/26.
- The SACC CA19-9 is printed as 10.9 ± 306.5 and CA-125 as 27.4 ± 3.3. Both SDs are implausible, and the markers were available for only 11 and 15 patients respectively, not 26.
- The text gives "31% female" and "69.2% male" (18/26 = 69.2%; 8/26 = 30.8%), which is consistent.
- How the 34 controls were selected is not described.

### WangM2014
- The text says males were "57% in both groups", but 18/30 = 60%.
- TNM-stage DFS P is 0.047 in the abstract but 0.024 in the text and Table 2.
- In the Results text, the pN list ends with "40 pT4 (SRC 21 versus NSRC 19)", a copy error in place of pN2b.
- In Table 2, the smoking OS percentages appear transposed (Yes 69.0±7.1 vs No 77.8±9.8, but with SEs mismatched to group sizes).
- The method for diagnosing schistosomiasis is not described.
- In Table 3 (multivariable Cox), schistosomiasis was the only significant factor, but the HRs for the other covariates are not shown.

### Ge2023 (Research Square preprint)
- For age over 60, the text gives 79 (84.0%) SACC vs 2973 (49.3%) NSACC (≥60, per the Discussion). The Table 1 bands (61–70, 71–80, ≥81) give 78 and 2787, which would be consistent with a ≥61 cut-off. I extracted the ≥60 text values.
- Transverse colon SACC is 0 in Table 1 but 1 in Table 2, with all other SACC location counts the same, so Table 2 sums to 95.
- The conclusion and abstract claim schistosomiasis is "an independent risk factor" for prognosis, but no Cox or multivariable model was fitted. Only a log-rank test on the PSM cohort was reported (35 vs 18 deaths, P = 0.005).
- No HR or follow-up duration is reported.

### Pan2020
- The abstract says c-MYC amplification was associated with "old age". Table 1 (18/84 = 21% if <60 vs 32/270 = 12% if ≥60) and the Results text ("young age") show the opposite.
- Table 1 differentiation: the IHC columns (81/189, 32/52) belong to the opposite rows; Low = 84 does not equal 81 + 189.
- Same cohort as WangW2020, with 354 vs 351 patients and 138 vs 137 SACC.

### Pan2022
- Table 1 differentiation labels are swapped in the group columns. "Low" lists SCRC 97 / NSCRC 160, which are actually the well/high counts. True poor differentiation is SCRC 34/131 and NSCRC 47/207.
- In the SCRC set, MET FISH-positive was not retained in the multivariable model (only stage was). Yet the Discussion says MET copy number "was independent of clinical stage" in SCRC.
- Fig. 2 and Fig. 3 legends and panel references are inconsistent (e.g., stage I–II P is 0.49 in one place and 0.138 in another).
- The SCRC multivariable stage HR is identical to the univariate one, 4.479 (2.618–7.663).

### Pan2023 (SACC-only)
- The OS HR for eggs in the cutting edge in stage III is 1.494 (1.199–11.212). The point estimate lies outside its CI.
- OS is defined as cancer-related death, but "32 patients died, including 15 deaths without evidence of recurrence". This conflicts with the cancer-specific definition.
- The headline result (eggs in LN independent for DFS in stage III) only appears after hepatic schistosomiasis is deliberately removed from the model.
- Presence-site OS P values differ: 0.091 (KM) vs 0.095 (Cox), and 0.044 (KM) vs 0.051 (Cox) in stage III.

### WangW2021
- The schistosomiasis univariate OS result is reported as P = 0.048, but its 95% CI of 0.994–1.940 includes 1.
- The SCRC multivariable CD8 result is reported as P = 0.045, but its CI of 0.337–1.039 includes 1.
- PD-L1 counts disagree. Table 1 gives sPD-L1 positive (≥1%) = 200 (64%), while Table 2 groups 196 negative / 142 positive, which matches the text's ≥2% "high" grouping. Which cut-off Table 2 uses is ambiguous.
- Table 2 has typos. CD8 "Low group 1044" should be 104. The tPD-L1 gender N's are swapped (Male 133 / Female 205). The vessel-invasion N's are 272 and 67.
- The Fig. 4 legend gives panel A as SCRC P = 0.0040, while the text says the significant sPD-L1 effect was in NSCRC.
- In NSCRC, the differentiation CI of 0.991–2.809 is a copy of the SCRC CI.
- The median age of SACC (74) vs NSACC (64.5) is cited in the Discussion.

### WangW2023
- The SCRC multivariable CD3 result is reported as P = 0.045, but its CI of 0.160–1.021 includes 1.
- Table 2 gender appears swapped. Male 79 / 46 means only 125 of 314 are male (40%), but the cohort is 60.7% male.
- The Fig. 4 and Fig. 5 legends contradict themselves: the N = 126 legend describes "without schistosomiasis was 126".
- Table 3 lists the SCRC TNM HR as 4.219 (2.479–7.128); WangW2021 and Cheng2023 give 2.497.

### Cheng2023
- The Table 4 header labels NSCRC N = 137 and SCRC N = 214 (swapped). The SCRC column holds the SCRC results and matches WangW2021.
- The Table 3 schistosomiasis-row sums do not match the column headers for sCD4, iCD8 and sCD8 (e.g., sCD8 low 147 + 96 = 243 vs header 238).
- The Abstract, Discussion and Conclusion contradict the Results:
  - Results: sCD4 is independent in NSCRC, iCD8 in SCRC, and sCD4 and iCD8 in the whole cohort.
  - Discussion: "iCD4, sCD8 … independent in the whole cohort".
  - Conclusion: "iCD4+ and sCD4+ … independent for NSCRC and SCRC respectively".
- The Fig. 4 legend swaps SCRC and NSCRC.
- Stromal CRP positivity is given only as a percentage (30% vs 22%); no counts are reported.
- The SCRC multivariable age HR is printed as 1,669,993.854 (0.000 to 4.66E+255).

### Chai2026
- The text says CFIm25-high in LN-positive was 48/117 and in stage I–II 45/157. Table 3 gives LN-positive high = 69 and stage I–II high = 112. The text appears to report the CFIm25-low counts as "high".
- The Table 3 stage III–IV column headers read Low n = 96, High n = 33 (sum 129). The whole-cohort TNM row gives 51 low / 78 high for stage III–IV.
- The Table 3 LNM column headers read Low 40 / High 77, versus 48 / 69 in the whole-cohort LNM row.
- The schistosomiasis univariate OS result is reported as P = 0.048, but its CI of 0.982–2.036 includes 1.
- The text claims age was "incorporated as a covariate in all multivariate Cox regression analyses", but age does not appear in Table 2's multivariable models.
- The claim that no patient received adjuvant chemotherapy or radiotherapy (only traditional Chinese medicine) across stage III–IV, 2008–2016, is implausible and differs from the companion reports.
- The within-SACC Cox table (Table S3) is not in the supplied text, so within-SACC HRs could not be extracted.

## C. Items not found or not extractable
- **Age as mean ± SD:** not available for WangW2020 (medians only, 74 vs 64), Zhu2024 (means only, no SD), Li2024, Zhang2023 or Wu2021.
- **Not reported in any supplied study:**
  - tumour budding (except Zheng2023 and WangW2020)
  - multiple primary tumours (except Zheng2023)
  - positive margin (except Zheng2023)
  - KRAS (except Zheng2023 and Li2024)
- **Sigmoid location:** only WangZ2020, Yang2023, Zhu2024 and Ge2023 report it.
- **Mucinous histology:** not separately reported in Zheng2023, where it is combined with poor differentiation.
- **Survival data:** no SACC vs NSACC HR was reported by WangZ2020, Ge2023, Zhu2024, Zhang2023, Yang2023, Wu2021 or Feng2015. Only log-rank results are available for WangZ2020 and Ge2023.
- **Chai2026:** Suppl. Tables S2/S3 (group comparison and within-SACC Cox) are not in the supplied text.
- **Pan2020:** Suppl. Table S1 (SACC vs NSACC characteristics) is not in the supplied text.
- **WangW2023:** Supplementary Table 1 is not in the supplied text.
