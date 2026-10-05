"""Builds the Acta Medica Philippina submission draft (.docx) and supplementary file.

Format (journal instructions): Microsoft Word, single column, single-spaced,
12-pt Arial, italics (not underlining), figures and tables placed in the text at
the appropriate points, structured abstract (<= 500 words), ICMJE references.

Integrity: every number in the Results that depends on screening or pooling is a
highlighted "[TO BE CALCULATED]" placeholder. Pooled tables are filled
automatically from output/tables/*.csv once R/run_all.R has been run on verified
data; they stay as placeholders otherwise.
"""
import csv
import json
import os
import re
import subprocess
import sys

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX, WD_BREAK
from docx.oxml.ns import qn
from docx.shared import Pt, Cm, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from references import REFS  # noqa: E402

TBC = "[TO BE CALCULATED]"
FIG = os.path.join(ROOT, "figures")
OUT = os.path.join(ROOT, "output")

# ============================================================== content model ==
# Blocks: ("h1"|"h2"|"h3", text) ("p", text) ("table", dict) ("fig", dict) ("pb",)
# Citations: {c:key1,key2}. Numbering follows first appearance (ICMJE).

def inventory():
    return {r["study_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data/study_inventory.csv")))}


def pooled_rows():
    f = os.path.join(OUT, "tables/Table4_meta_analysis_summary.csv")
    return list(csv.DictReader(open(f))) if os.path.exists(f) else []



# =========================================================== author inputs =====
# Items only the authors can supply. They are highlighted in the .docx.
AUTHOR_COAUTHORS = "[AUTHOR INPUT: co-author names and degrees]"
AUTHOR_AFFILIATION = "[AUTHOR INPUT: department, institution, city, country]"
AUTHOR_ADDRESS = "[AUTHOR INPUT: postal address]"
AUTHOR_ORCID = "[AUTHOR INPUT: ORCID]"
AUTHOR_REGISTRATION = "[AUTHOR INPUT: PROSPERO/OSF registration number and date, or the sentence 'The protocol was not registered.']"
AUTHOR_REGISTRATION_SHORT = "[AUTHOR INPUT: PROSPERO/OSF number, or 'Not registered']"
AUTHOR_SCREENERS = "[AUTHOR INPUT: initials of the author(s) who verified selection]"
AUTHOR_AI_VERIFICATION = "[AUTHOR INPUT: state which author(s) re-checked the extracted data, risk-of-bias and GRADE judgements against the source articles, and the date]"
AUTHOR_ACK = "[AUTHOR INPUT: acknowledgments, or 'None.']"
AUTHOR_CREDIT = "[AUTHOR INPUT: CRediT roles of each author; all authors approved the final version.]"
AUTHOR_COI = "[AUTHOR INPUT: conflicts of interest for each author, or 'The authors declare no conflicts of interest.']"
AUTHOR_FUNDING = "[AUTHOR INPUT: funding, or 'This study received no specific funding.']"
AUTHOR_REPOSITORY = "[AUTHOR INPUT: public repository URL/DOI, e.g. OSF or Zenodo deposit of the sacc-meta-analysis folder]"
WORDCOUNT_PLACEHOLDER = "Word count: abstract {abstract_words}; main text {main_words}. Tables: 6. Figures: 8. Supplementary tables: 6."

def manuscript_blocks():
    inv = inventory()
    pooled = {r["outcome"]: r for r in pooled_rows()}
    B = []
    h1 = lambda t: B.append(("h1", t)); h2 = lambda t: B.append(("h2", t)); h3 = lambda t: B.append(("h3", t))
    p = lambda t: B.append(("p", t))

    # ---------------------------------------------------------- title page --
    B.append(("title", "Defining Schistosomiasis-Associated Colorectal Cancer: A Systematic Analysis and Meta-analysis of Clinicopathological, Molecular, and Prognostic Features"))
    p("Jayson Cagadas Pasaol, DVM, PhD,¹ " + AUTHOR_COAUTHORS)
    p("¹" + AUTHOR_AFFILIATION)
    p("Corresponding author: Jayson Cagadas Pasaol, DVM, PhD; " + AUTHOR_ADDRESS + "; email: jaysonpasaolrmt082@gmail.com; ORCID: " + AUTHOR_ORCID)
    p("Running title: Schistosomiasis-associated colorectal cancer phenotype")
    p(WORDCOUNT_PLACEHOLDER)
    p("Keywords: Schistosoma japonicum; schistosomiasis; colorectal neoplasms; prognosis; neoplasm staging; meta-analysis")
    B.append(("pb",))

    # ------------------------------------------------------------- abstract --
    h1("ABSTRACT")
    p("**Background and Objective.** Schistosoma japonicum infection has long been linked to colorectal cancer in endemic Asia, but whether schistosomiasis-associated colorectal cancer (SACC) is a reproducibly distinct clinical entity is unresolved. This study aimed to systematically quantify the clinicopathological, molecular, and prognostic differences between SACC and non-schistosomiasis-associated colorectal cancer (NSACC) and to determine whether the available evidence supports a distinct schistosomal colorectal cancer phenotype.")
    p("**Methods.** MEDLINE (PubMed), Europe PMC (including preprints and Chinese Biological Abstracts), and Crossref were searched to 5 October 2026 without language restriction. Observational studies comparing SACC with non-schistosomal CRC (NSACC) were eligible; SACC-only cohorts contributed to a separate within-SACC prognostic analysis. Data were extracted in duplicate, blind, and adjudicated against source documents; risk of bias was assessed with the Newcastle-Ottawa Scale. Overlapping reports from the same hospitals were identified and each cohort was counted once per outcome. Odds ratios (OR), mean differences, and hazard ratios (HR) were pooled with random-effects models (REML); adjusted and unadjusted HRs were pooled separately. Certainty of evidence was rated with GRADE.")
    p(abstract_results(pooled))
    pass
    p("**Conclusion.** " + conclusion_text(pooled, short=True))
    p("**Registration.** " + AUTHOR_REGISTRATION_SHORT)
    B.append(("pb",))

    # --------------------------------------------------------- introduction --
    h1("INTRODUCTION")
    p("Colorectal cancer (CRC) is one of the most frequently diagnosed cancers and a leading cause of cancer death worldwide.{c:bray2024} A substantial share of the global cancer burden is attributable to infectious agents,{c:demartel2020} and the International Agency for Research on Cancer (IARC) has classified infection with Schistosoma haematobium as carcinogenic to humans (Group 1) and infection with Schistosoma japonicum as possibly carcinogenic to humans (Group 2B).{c:iarc61,iarc100b} For CRC, the relevant paradigm is inflammation-associated carcinogenesis, in which long-standing tissue injury and repair precede neoplasia; schistosomiasis-associated CRC has been described as biologically analogous to colitis-associated CRC.{c:hamid2019}")
    p("Schistosoma japonicum is a zoonotic blood fluke whose adult worms live in the mesenteric venous system. A large proportion of eggs is not excreted but becomes trapped in the intestinal wall and liver, where it provokes granulomatous inflammation and, with time, fibrosis and calcification.{c:iarc61,hamid2019} The parasite remains endemic in parts of China, the Philippines, and Indonesia.{c:who_schisto} In the Philippines, transmission is focal and persists despite long-standing control programmes,{c:gordon2015} and in Indonesia it is confined to a small number of villages in Central Sulawesi that are approaching elimination.{c:indo2026} Populations with past or current exposure therefore remain at risk of the chronic intestinal sequelae of infection.")
    p("Evidence linking S. japonicum to colorectal neoplasia comes mainly from China. Epidemiological studies have produced inconsistent estimates: in an early study, the matched analysis reported in the abstract did not show a statistically significant increase in colon cancer risk,{c:xusu1984} whereas a later matched case-control study in rural China reported an association between previous infection and colon cancer.{c:qiu2005} Hospital-based series have also described a high frequency of digestive-tract malignancy among patients with schistosomiasis japonica.{c:liuxf2023} On the basis of this limited evidence, IARC did not classify S. japonicum as a proven human carcinogen.{c:iarc61} These observational associations do not establish causation, and they address cancer risk rather than the features of the cancers that arise.")
    p("A separate clinical literature has compared patients with CRC with and without schistosomiasis. Several hospital cohorts have reported differences in age, sex, tumour site, T stage, or tumour markers,{c:wangz2020,wangw2020,zhang2023,zhu2024} and some have reported less favourable survival among patients with schistosomiasis,{c:ncg1986,wangm2014,wangw2020,li2024} whereas the largest cohort to date, 31,153 patients treated in Shanghai between 2001 and 2021, found that schistosomiasis was not an independent predictor of overall or disease-free survival after multivariable adjustment.{c:zheng2023} Narrative reviews have described a characteristic phenotype that includes predilection for the sigmoid colon and rectum, multifocality, mucinous histology, and poor prognosis,{c:hamid2019,hamid2010} but these descriptions have not been tested quantitatively. A recent meta-analysis addressed the prevalence of intestinal parasites among patients with CRC,{c:global_ipi2025} which is a different question from whether schistosomiasis defines a distinct form of CRC.")
    p("Although schistosomiasis-associated colorectal cancer has been described for decades, whether it constitutes a reproducibly distinct clinicopathological and prognostic entity remains unresolved. Individual cohorts vary substantially in sample size, diagnostic criteria, patient characteristics, and reported outcomes, several reports appear to derive from the same institutions, and available molecular evidence has not been quantitatively synthesised. We therefore conducted a systematic analysis and meta-analysis to quantify the demographic, clinicopathological, molecular, and survival characteristics of schistosomiasis-associated colorectal cancer compared with non-schistosomal colorectal cancer.")

    # -------------------------------------------------------------- methods --
    h1("METHODS")
    h2("Study design and reporting framework")
    p("This systematic review and meta-analysis of observational studies is reported according to PRISMA 2020{c:page2021} and, for the literature search, PRISMA-S.{c:rethlefsen2021} The completed PRISMA 2020 checklist is provided in the Supplementary Material. The review question was: among patients with colorectal cancer, does schistosomiasis define a distinct clinicopathological, molecular, and prognostic phenotype? It was not designed to estimate the prevalence of schistosomiasis among patients with CRC or the risk of CRC after infection.")
    h2("Protocol and registration")
    p("Eligibility criteria, outcomes, the overlap-handling rules, and the analysis plan were specified before data extraction and are archived with the analysis code. " + AUTHOR_REGISTRATION)
    h2("Eligibility criteria")
    p("Eligibility followed a PECO framework. Population: adults with histologically or clinically confirmed colorectal adenocarcinoma or carcinoma. Exposure: current or previous intestinal schistosomiasis, ascertained by histological identification of schistosome eggs, pathology report, documented history, stool microscopy, serology, molecular testing, or a validated clinical diagnosis; the method used by each study was recorded. Comparator: patients with CRC without evidence, history, or pathological findings of schistosomiasis. Outcomes: clinicopathological, molecular, laboratory, and prognostic characteristics.")
    p("We included retrospective or prospective cohorts, case-control studies, and comparative pathological series that reported extractable data for at least one outcome in patients with SACC and NSACC. Cohorts of SACC only were included solely in a separate within-SACC prognostic analysis. We excluded case reports, case series without comparative information, animal and in vitro studies, editorials, narrative and systematic reviews (used only to identify primary studies), studies in which CRC could not be separated from other cancers or schistosomiasis status could not be determined, and duplicate reports of the same population for the same outcome. Population-based studies of CRC risk after schistosomiasis were catalogued separately. No language or publication-status restriction was applied; preprints were eligible and analysed with a sensitivity analysis excluding them.")
    h2("Information sources and search strategy")
    p("MEDLINE was searched through PubMed on 5 October 2026 with a strategy combining controlled vocabulary and free-text terms for schistosomiasis (\"Schistosoma japonicum\"[MeSH], schistosomiasis, schistosomal, schistosoma, bilharzia) with terms for colorectal neoplasms; outcome terms were deliberately not required. On the same day Europe PMC, which also indexes preprint servers and Chinese Biological Abstracts,{c:europepmc2023} was searched with an equivalent title-and-abstract query, and Crossref was searched with English and Chinese bibliographic queries to capture journals with digital object identifiers outside MEDLINE. Exact strategies and yields are given in Supplementary Table S1. Scopus, Web of Science, Embase, CNKI, Wanfang Data, and SinoMed require institutional subscriptions that were not available for this review and were not searched; this is addressed under Limitations. Records were deduplicated by PubMed identifier and DOI.")
    h2("Study selection")
    p("Titles and abstracts were screened against the eligibility criteria, and full texts of potentially eligible reports were obtained from PubMed Central, Europe PMC, publishers' open-access supplementary files, open repositories identified through Unpaywall, and preprint servers. One principal reason was recorded for every excluded full text (Supplementary Table S2). Screening was performed with the assistance of an AI language model (see Use of AI-assisted Tools) and checked by " + AUTHOR_SCREENERS + ".")
    h2("Data extraction")
    p("Data were extracted in duplicate, independently, into a piloted spreadsheet covering study identification, institution and recruitment period, design, schistosomiasis ascertainment, patient numbers, demographics, tumour location, pathology, stage, metastasis, molecular and laboratory markers, and survival estimates. The second extraction was performed blind to the first, from the same source documents. Every disagreement was adjudicated against the original table or text (Supplementary Table S3), and every reported value was additionally checked by a script confirming that the number appears in the source document. Each value records its origin (reported; calculated from reported categories; derived from survival statistics) and its exact source location. When means were not reported, medians with interquartile ranges were converted with the method of Wan et al.{c:wan2014}")
    p("For survival, the extraction priority was: (1) multivariable-adjusted hazard ratio (HR) with 95% confidence interval (CI); (2) unadjusted HR; (3) HR derived from the log-rank P value and the number of events with the methods of Tierney et al.;{c:tierney2007} and (4) HR reconstructed from Kaplan-Meier curves.{c:guyot2012} All HRs were expressed as SACC versus NSACC. Adjusted and unadjusted or derived estimates were analysed separately.")
    h2("Outcome definitions")
    p("Primary outcomes were overall survival (OS), disease-free or recurrence-free survival (DFS), advanced stage (stage III-IV versus I-II), lymph-node metastasis, and distant metastasis (M1 or stage IV). Secondary outcomes were age (mean difference in years) and age over 60 years; male sex; tumour location; tumour size; differentiation; mucinous or signet-ring-cell histology; multiple primary tumours; concomitant polyps; lymphovascular, vascular, and perineural invasion; tumour budding; positive margins; molecular alterations; and laboratory markers (exploratory).")
    h2("Assessment of risk of bias")
    p("Risk of bias was assessed independently in duplicate with the Newcastle-Ottawa Scale (NOS) for cohort studies.{c:wells_nos} The comparability item was awarded for analyses that controlled for stage and at least one of age or sex (two stars when both, or matching, were used). Follow-up items were awarded when median follow-up was at least three years and losses were reported and small; cross-sectional comparisons could not earn them. Studies with 7-9 stars were rated as low, 5-6 as moderate, and 0-4 as high risk of bias.")
    h2("Management of overlapping cohorts")
    p("For every report we recorded hospital, city, department, recruitment period, authors, and patient numbers, and constructed an overlap matrix (Supplementary Table S6). Reports from the same institution with overlapping recruitment periods were treated as one cohort. For each outcome, only one report per cohort was analysed (the largest or most complete); a second report contributed only outcomes absent from the first. The analysis code rejects any analysis that contains two reports from the same cohort.")
    h2("Statistical analysis")
    p("Odds ratios (OR) were computed from 2x2 tables. Log HRs and their standard errors were derived from the reported HR and 95% CI. Random-effects models with restricted maximum likelihood (REML) estimation of between-study variance were used for all pooled analyses; common-effect estimates are reported as a sensitivity analysis. For each outcome we report the pooled estimate, 95% CI, P value, tau², I², and Cochran's Q.{c:higgins2002} An outcome was pooled only when at least two independent cohorts reported comparable data. The primary analysis was restricted to S. japonicum, confirmed or presumed from endemic-area cohorts; other species were analysed separately. Analyses were performed in R version 4.3.3{c:rcore} with metafor version 4.4.0.{c:viechtbauer2010}")
    h2("Sensitivity and subgroup analyses")
    p("Pre-specified sensitivity analyses were leave-one-out analysis; exclusion of studies at high risk of bias; exclusion of the largest cohort (31,153 patients{c:zheng2023}); restriction to histology-confirmed SACC; restriction to species-confirmed studies; and common-effect models. Subgroup analyses (colon versus rectum, era, region, risk of bias) were planned where at least two studies were available per subgroup.")
    h2("Small-study effects and certainty of evidence")
    p("Funnel plots and Egger's test{c:egger1997} were planned only for outcomes with at least 10 studies.{c:sterne2011} Certainty of evidence was rated for each pooled outcome with GRADE.{c:guyatt2008} Evidence from observational studies started at low certainty and was rated down for risk of bias, inconsistency, indirectness, imprecision, or suspected publication bias, and up for a large effect or dose-response.")
    h2("Ethics")
    p("This study used published, aggregate data and did not require ethics review or informed consent.")

    # -------------------------------------------------------------- results --
    h1("RESULTS")
    h2("Search results")
    p(search_paragraph())
    B.append(("fig", {"file": "Figure1_PRISMA_flow.png", "w": 15.0,
                      "cap": "**Figure 1.** PRISMA 2020 flow diagram of study selection. Databases shown as not calculated (Scopus, Web of Science, Embase, CNKI, Wanfang, SinoMed) could not be searched (see Limitations)."}))
    h2("Characteristics of included studies")
    p(characteristics_paragraph())
    B.append(("table", table1(inv)))
    B.append(("fig", {"file": "Figure2_landscape_timeline.png", "w": 16.0,
                      "cap": "**Figure 2.** Chronological landscape of the 20 included reports. Bars show recruitment periods; diamonds show publication year. Right column: SACC/NSACC sample sizes (NR, not reported; dash, SACC-only cohort). Labels give city or province."}))
    h2("Schistosomiasis ascertainment")
    p("Every analysed comparative cohort defined schistosomiasis by histological identification of schistosome eggs, usually calcified, in the resected colorectal specimen; one series also accepted ova in stool or biopsy,{c:feng2015} and one matched survival study did not state its definition.{c:wangm2014} No study confirmed the species morphologically or molecularly, so all were classified as S. japonicum presumed from residence in endemic areas of Shanghai, Anhui, Hubei, Hunan, Jiangxi, and Sichuan. Pathologists were blinded to clinical data in the Qingpu reports,{c:wangw2020,wangw2023} whereas the largest cohort noted that egg reporting was not compulsory in routine pathology, so some SACC may have been classified as NSACC.{c:zheng2023} The comparison was therefore, in practice, between CRC with egg-proven intestinal schistosomiasis and CRC without eggs in the specimen.")
    h2("Demographic characteristics")
    p(pooled_sentence(pooled, "Male sex", "male sex") + " " + pooled_sentence(pooled, "age", "age (mean difference, years)", md=True) + " " + pooled_sentence(pooled, "Age > 60 years", "age over 60 years") + " Every cohort that tested age found SACC patients to be older or of similar age (Figure 7); heterogeneity reflected the size rather than the direction of the difference.")
    h2("Anatomical distribution")
    p(pooled_sentence(pooled, "Rectal location", "rectal location") + " " + sens_sentence("Rectal location") + " " + pooled_sentence(pooled, "Sigmoid location", "sigmoid location") + " " + pooled_sentence(pooled, "Right-sided colon", "right-sided colon location"))
    h2("Pathological characteristics")
    p(pathology_paragraph(pooled))
    B.append(("table", table2(inv)))
    h2("Tumour stage and metastatic behaviour")
    p(pooled_sentence(pooled, "Stage III-IV", "stage III-IV disease") + " " + sens_sentence("Stage III-IV") + " " + pooled_sentence(pooled, "pT3-T4", "pT3-T4 tumours") + " " + pooled_sentence(pooled, "Lymph-node metastasis", "lymph-node metastasis") + " " + pooled_sentence(pooled, "Distant metastasis", "distant metastasis") + " Individual cohorts disagreed: the largest reported less nodal and distant metastasis in SACC,{c:zheng2023} one reported more nodal metastasis,{c:wu2021} and a pathology series from Jiujiang described a lower proportion with nodal metastasis (28.4% vs 35.8%) without a statistical test.{c:zhou2025}")
    B.append(("fig", {"file": "Figure3_phenotype_forest.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 3.** Clinicopathological phenotype of SACC versus NSACC: pooled odds ratios (random effects, REML) with 95% confidence intervals for each outcome with at least two independent cohorts. Red, primary outcomes; blue, secondary outcomes. Study-level forest plots are in the Supplementary Material."}))
    h2("Molecular characteristics")
    p(molecular_paragraph(pooled))
    B.append(("table", table3()))
    B.append(("fig", {"file": "Figure6_molecular.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 6.** Molecular phenotype: pooled odds ratio for the only biomarker reported by two independent cohorts with internal comparators (KRAS mutation). All other biomarkers are mapped in Table 3."}))
    h2("Overall survival")
    p(pooled_sentence(pooled, "OS - Adjusted", "overall survival (multivariable-adjusted HRs)", hr=True) + " " + sens_sentence_any("OS - Adjusted") + " " + pooled_sentence(pooled, "OS - Unadjusted", "overall survival (unadjusted or derived HRs)", hr=True) + " The unadjusted pool combined four estimates above 1 with one below 1 derived from a log-rank P value in a 100-patient follow-up subset;{c:wangz2020,tierney2007} the largest cohort reported that schistosomiasis was not retained in its multivariable model but did not report the adjusted HR.{c:zheng2023}")
    B.append(("fig", {"file": "Figure4_OS_forest.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 4.** Overall survival in SACC versus NSACC. Hazard ratios with 95% CI; multivariable-adjusted and unadjusted/derived estimates are pooled separately (random effects, REML). Source: P1, adjusted HR reported; P2, unadjusted HR reported; P3, derived from log-rank P and events."}))
    h2("Disease-free and recurrence-free survival")
    p(pooled_sentence(pooled, "DFS - Adjusted", "disease-free survival (adjusted)", hr=True) + " " + pooled_sentence(pooled, "DFS - Unadjusted", "disease-free survival (unadjusted)", hr=True) + " The adjusted estimate depended on the small matched rectal-cancer cohort;{c:wangm2014} in the two larger cohorts the unadjusted excess hazard was attenuated after adjustment.{c:zheng2023,li2024}")
    B.append(("fig", {"file": "Figure5_DFS_forest.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 5.** Disease-free/recurrence-free survival in SACC versus NSACC (hazard ratios, random effects)."}))
    h2("Within-SACC prognostic factors")
    p(within_paragraph())
    B.append(("table", table5()))
    h2("Risk of bias")
    p(rob_paragraph())
    h2("Sensitivity analyses")
    p(sensitivity_paragraph())
    h2("Certainty of evidence and overall phenotype")
    p(grade_paragraph())
    B.append(("table", table4(pooled)))
    B.append(("fig", {"file": "Figure7_evidence_heatmap.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 7.** Evidence heat map. For each report (columns) and feature (rows), the direction reported in SACC relative to NSACC: higher, lower, no significant difference, or not reported. For survival rows, 'higher' means a higher hazard (worse survival) in SACC. Reports from the same cohort used for different outcomes are shown separately."}))
    B.append(("table", table6()))

    # ----------------------------------------------------------- discussion --
    h1("DISCUSSION")
    h2("Principal findings")
    p(principal_findings(pooled))
    h2("Clinical interpretation")
    p("The demographic profile is the most reproducible feature. SACC patients were older and more often men, consistent with cumulative occupational exposure to infested water among men in agricultural communities and with the decline of transmission in China, which leaves residual egg burden concentrated in older generations.{c:zheng2023,wangz2020} These are features of the exposed population rather than of the tumour, and they confound any unadjusted comparison of stage or survival.")
    p("Tumour features were largely indistinguishable. Pooled estimates for lymph-node metastasis, vascular and perineural invasion, differentiation, and T stage were close to the null, with no consistent direction. The excess of rectal tumours was small and disappeared when the Shanghai cohort was excluded, and the lower frequency of stage III-IV disease in SACC was unstable, reaching significance only when the preprint cohort was excluded, so neither should be regarded as established. Single-cohort observations of more multiple primary tumours, concomitant polyps, and positive margins in SACC{c:zheng2023} are biologically plausible in a field of chronically inflamed, fibrotic mucosa, and matter surgically, but require replication.")
    p("Survival findings depend on adjustment. Unadjusted estimates conflicted, ranging from a derived HR below 1{c:wangz2020} to clearly raised hazards,{c:li2024,ge2023} and the largest cohort found no independent effect.{c:zheng2023} The three multivariable-adjusted estimates all suggested worse overall survival in SACC, but they came from 197 SACC patients, adjusted for different covariates, and the certainty of this evidence is very low. Older age and comorbidity, including hepatic schistosomiasis and its consequences, are plausible contributors that most studies could not separate from the tumour itself. The within-SACC finding that coexisting hepatic schistosomiasis predicted worse outcome in stage III disease{c:pan2023} supports the view that the host's parasitic disease, rather than a more aggressive tumour, may drive any survival difference.")
    h2("Molecular interpretation")
    p("The molecular evidence base is narrow and does not define a schistosomal molecular subtype. KRAS mutation was the only marker reported by two independent cohorts; it was more frequent in SACC, but assays differed and mutation status was unknown for a large share of the largest cohort.{c:zheng2023,li2024} NRAS, BRAF, PIK3CA, and mismatch-repair status did not differ in that cohort, and exome sequencing of 30 SACC tumours showed microsatellite-stable, low-mutation-burden tumours with fewer RTK-RAS alterations than an external sporadic CRC reference.{c:genomic2023} Immune-microenvironment markers (CD3, CD4, CD8, CD20, PD-L1, TILs) and c-MYC, MET, and CFIm25 were each studied in the same Qingpu cohort and showed no difference in frequency between groups,{c:wangw2021,wangw2023,bmcgastro2023,pan2020,pan2022,chai2026} although several appeared to carry different prognostic weight within SACC. Small Chinese-language and Egyptian comparisons of p53, mismatch-repair, apoptosis, and angiogenesis markers could not be retrieved.{c:chen2016,yangdh2014,ruan2013,yangxg2021,zhangr1998,madbouly2007,zalata2005}")
    h2("Biological plausibility")
    p("Several mechanisms could link chronic intestinal schistosomiasis to colorectal carcinogenesis, but they differ in strength of evidence (Figure 8). Egg deposition in the colorectal wall and the resulting granulomatous inflammation and fibrosis are established histopathological features of infection.{c:iarc61,hamid2019} Experimental work suggests that S. japonicum soluble egg antigen activates MAPK and PI3K-AKT signalling and inhibits autophagy in CRC models,{c:sea2025} and that intestinal tumour-associated macrophage polarisation influences schistosomal CRC development.{c:tam2021} Schistosoma mansoni eggs activate Wnt/beta-catenin signalling and c-Jun in human and hamster colon,{c:wnt2020} but this concerns a different species. In patients, eggs in regional lymph nodes and coexisting hepatic schistosomiasis were associated with poorer outcome in stage III SACC.{c:pan2023} Oxidative DNA damage, NF-kB and IL-6/STAT3 signalling, and microbiome change remain hypotheses in human SACC. None of these observations establishes that S. japonicum causes CRC, and the absence of a consistent tumour phenotype in this synthesis argues against a dominant, distinct schistosomal pathway.")
    B.append(("fig", {"file": "Figure8_conceptual_model.png", "w": 16.0,
                      "cap": "**Figure 8.** Conceptual model of how chronic S. japonicum infection might relate to colorectal carcinogenesis and a possible SACC phenotype. Solid arrows: established histopathology. Dashed arrows: hypothesised steps not confirmed in human SACC. Grey boxes: supporting observations with the type of evidence stated; numbers are references. The figure does not imply that S. japonicum causes CRC.{c:iarc61,hamid2019,pan2023,tam2021,wangw2021,wangw2023,bmcgastro2023,sea2025,wnt2020,genomic2023,li2024,pan2020}"}))
    h2("Comparison with previous literature")
    p("Descriptions of SACC as a distinct subtype, with sigmoid and rectal predilection, multifocality, mucinous histology, early onset, and poor prognosis, derive largely from narrative reviews, older case series, and S. mansoni-endemic settings.{c:hamid2019,hamid2010,actapara2023} The present synthesis supports only some of these features for contemporary S. japonicum-associated disease: older rather than younger age, a male predominance, possibly worse adjusted survival, and no consistent excess of mucinous histology or advanced stage. A recent meta-analysis pooled the prevalence of intestinal parasitic infection among patients with CRC,{c:global_ipi2025} which addresses frequency and risk rather than the characteristics of cancers that have arisen. In the databases we searched we found no previous quantitative synthesis of the SACC phenotype; because subscription and Chinese databases could not be searched, we do not claim that none exists.")
    h2("Implications for endemic countries")
    p("All comparative cohorts came from mainland China, and no comparative study from the Philippines or Indonesia was identified, although both countries remain endemic for S. japonicum.{c:gordon2015,indo2026} A 2002 series from the Philippine General Hospital recorded schistosomiasis in 3% of resected CRC specimens but did not compare these cancers with others.{c:kaw2002} The present findings may not transfer directly to Philippine patients, whose exposure history, age structure, and access to care differ. Two practical steps follow. Pathologists in endemic regions should record the presence, location, and depth of schistosome eggs, including in lymph nodes, in colorectal resection reports, since these data are prognostically informative within SACC{c:pan2023} and are the basis of every study in this review. Cancer registries and surgical databases should record a history of schistosomiasis and its hepatic complications. These data do not, by themselves, justify changes to CRC screening or treatment policy.")
    h2("Research implications")
    p("Prospective cohorts are needed in which schistosomiasis is ascertained by standardised histological and serological criteria, tumours are profiled with contemporary genomic, transcriptomic, and immune assays against internal comparators, and outcomes are analysed with adjustment for age, stage, comorbidity, liver disease, and treatment. Multicentre studies from the Philippines and Indonesia are a priority, as is individual-patient-data pooling of the existing Chinese cohorts to resolve the survival question.")
    h2("Strengths and limitations")
    p("Strengths of this review include explicit identification and resolution of overlapping reports, which reduced the apparent number of cohorts from 17 comparative reports to 10 independent cohorts; separation of adjusted from unadjusted survival estimates; duplicate extraction checked against source documents; and use of supplementary files that contained most of the analysable data. It also has important limitations. First, Scopus, Web of Science, Embase, and the Chinese databases CNKI, Wanfang, and SinoMed could not be searched, and 11 potentially relevant reports, mostly small Chinese-language biomarker studies, could not be retrieved; some eligible studies have therefore been missed. Second, all cohorts were retrospective, Chinese, and hospital-based, and two of the analysed reports are preprints that have not been peer reviewed; excluding them is examined in Supplementary Table S5. Third, schistosomiasis was defined by eggs in the specimen without species confirmation, so misclassification towards the null is likely. Fourth, several reports contained internal numerical inconsistencies (documented in the extraction file), two survival estimates were derived from log-rank statistics, and adjusted estimates used different covariate sets. Fifth, fewer than 10 studies were available for every outcome, so small-study effects could not be assessed and subgroup analyses were not feasible. Sixth, screening, extraction, and risk-of-bias assessment were assisted by an AI language model, with blinded duplicate extraction and adjudication against the source documents; the verification by the authors is described under Use of AI-assisted Tools. Finally, as for any synthesis of observational data, these associations cannot establish causality.")

    # ----------------------------------------------------------- conclusion --
    h1("CONCLUSION")
    p(conclusion_text(pooled))

    h1("Acknowledgments")
    p(AUTHOR_ACK)
    h1("Statement of Authorship")
    p(AUTHOR_CREDIT)
    h1("Author Disclosure")
    p(AUTHOR_COI)
    h1("Funding Source")
    p(AUTHOR_FUNDING)
    h1("Use of AI-assisted Tools")
    p("An AI language model (Claude, Anthropic) was used to run the PubMed, Europe PMC, and Crossref searches through their public interfaces, to screen records, to retrieve open-access full texts, to perform two independent, blinded data extractions and risk-of-bias assessments, to write and run the R (metafor) analysis code, and to draft the manuscript text. Every extracted value is linked to its source table, and a script confirmed that each reported number appears in the source document. " + AUTHOR_AI_VERIFICATION + " The authors take full responsibility for the content.")
    h1("Data Availability")
    p("The search records, extraction dataset with source locations, risk-of-bias and GRADE assessments, analysis code (R/metafor), and figure scripts are available at " + AUTHOR_REPOSITORY + ".")
    h1("REFERENCES")
    B.append(("refs",))
    return B

# ================================================================ helpers =====
def fmt(x, d=2):
    try:
        return f"{float(x):.{d}f}"
    except (TypeError, ValueError):
        return TBC


def pfmt(x):
    try:
        return "< 0.001" if float(x) < 0.001 else f"= {float(x):.3f}"
    except (TypeError, ValueError):
        return f"= {TBC}"


def pooled_sentence(pooled, key, label, hr=False, md=False):
    r = pooled.get(key)
    if not r:
        return f"For {label}, the pooled estimate was {TBC} (95% CI {TBC}; {TBC} studies; I² {TBC}; tau² {TBC})."
    m = "MD" if md else ("HR" if hr else "OR")
    return (f"For {label}, the pooled {m} was {fmt(r['estimate'])} (95% CI {fmt(r['lower95'])}-{fmt(r['upper95'])}; "
            f"P {pfmt(r['p_value'])}; {r['k']} studies; I² = {fmt(r['I2'], 0)}%; tau² = {fmt(r['tau2'], 3)}).")


def cite_tags(keys):
    return "{c:" + ",".join(keys) + "}"


REFKEY = {"Ge2023": "ge2023", "Zhou2025": "zhou2025", "Pan2022": "pan2022", "Farid2006": "farid2006", "Zheng2023": "zheng2023", "WangZ2020": "wangz2020", "WangW2020": "wangw2020", "WangW2021": "wangw2021",
          "WangW2023": "wangw2023", "Pan2020": "pan2020", "Cheng2023": "bmcgastro2023", "Chai2026": "chai2026", "Feng2015": "feng2015", "Wu2021": "wu2021", "Li2024": "li2024",
          "Zhang2023": "zhang2023", "Zhu2024": "zhu2024", "WangM2014": "wangm2014", "NCG1986": "ncg1986",
          "Madbouly2007": "madbouly2007", "Yang2023": "yang2023", "WangM2016": "wangm2016", "Pan2023": "pan2023",
          "Liu2013": "liu2013", "Zhou_CT2012": "zhou_ct2012", "Genomic2023": "genomic2023"}


def short_name(r):
    a = r["first_author"]
    if a.startswith("["):
        a = r["study_id"].rstrip("0123456789_").replace("_CT", "")
    if a.startswith("National"):
        return f"NCG {r['year']}"
    parts = a.split(" ")
    if parts[0] in ("Wang", "Pan", "Yang", "Zhang", "Liu", "Li") and len(parts) > 1 and r["study_id"] not in ("Li2024", "Zhang2023", "Yang2023", "Pan2023", "Pan2020", "Pan2022"):
        return f"{parts[0]} {parts[1][0]} {r['year']}"
    return f"{parts[0]} {r['year']}"


def hospital(inst):
    parts = [x.strip() for x in inst.replace(" + ", ", ").split(",")]
    h = [x for x in parts if "Hospital" in x or "University" in x]
    return (h[0] if h else parts[0]).replace("Dept of ", "").replace("Department of ", "")


# ============================================================ data readers =====
def _csv(rel):
    f = os.path.join(ROOT, rel)
    return list(csv.DictReader(open(f))) if os.path.exists(f) else []


def _out(name):
    return _csv(os.path.join("output/tables", name))


def _verified(name):
    return [r for r in _csv(os.path.join("data/analysis_ready", name)) if r.get("verified", "").strip().lower() == "yes"]


def prisma():
    return {r["box"]: (r["n"] if r["verified"].strip().lower() == "yes" and r["n"].strip() else TBC) for r in _csv("data/analysis_ready/prisma_counts.csv")}


def est(r, d=2):
    return f"{fmt(r['estimate'], d)} (95% CI {fmt(r['lower95'], d)}-{fmt(r['upper95'], d)})"


def sens_row(outcome, analysis):
    for r in _out("TableS5_sensitivity.csv"):
        if r["outcome"] == outcome and r["analysis"] == analysis:
            return r
    return None


def sens_sentence(outcome):
    r = sens_row(outcome, "excluding largest cohort")
    if not r:
        return ""
    m = {"OR": "OR", "HR": "HR"}.get(r["measure"], r["measure"])
    return (f"After exclusion of the largest cohort,{{c:zheng2023}} the {m} was {est(r)} ({r['k']} studies; I² = {fmt(r['I2'], 0)}%).")


def pathology_paragraph(pooled):
    parts = [pooled_sentence(pooled, "Poor differentiation", "poor differentiation"), pooled_sentence(pooled, "Mucinous histology", "mucinous or signet-ring histology"),
             pooled_sentence(pooled, "Vascular invasion", "vascular invasion"), pooled_sentence(pooled, "Perineural invasion", "perineural invasion"),
             pooled_sentence(pooled, "Tumour budding", "tumour budding"), pooled_sentence(pooled, "Tumour size >= 5 cm", "tumour size of 5 cm or more")]
    lo = sens_row("Poor differentiation", "leave-one-out: omit WangZ2020")
    extra = (f" Heterogeneity for differentiation was driven by one cohort reporting 2.6% poorly differentiated SACC against 21.9% NSACC with a non-significant P value;{{c:wangz2020}} without it the OR was {est(lo)} (I² = {fmt(lo['I2'], 0)}%)." if lo else "")
    single = (" Single cohorts reported more multiple primary CRC (4.3% vs 2.8%), more concomitant polyps (20.0% vs 13.6%), and more positive resection margins (3.6% vs 1.1%) in SACC, and lymphovascular invasion "
              "in 34% vs 36%;{c:zheng2023,wangw2020} these were not pooled.")
    return " ".join(parts) + extra + single + " Study-level counts are given in Table 2."


def grade():
    return {r["outcome"]: r for r in _csv("data/analysis_ready/grade.csv")}


def g_of(key):
    r = grade().get(key)
    return r["certainty"] if r else "not rated"


def sens_sentence_any(outcome):
    rows = [r for r in _out("TableS5_sensitivity.csv") if r["outcome"] == outcome and r["analysis"].startswith("leave-one-out")]
    if not rows:
        return ""
    lo = min(rows, key=lambda r: float(r["estimate"])); hi = max(rows, key=lambda r: float(r["estimate"]))
    return (f"Leave-one-out estimates ranged from {fmt(lo['estimate'])} ({lo['analysis'].replace('leave-one-out: omit ', 'without ')}) "
            f"to {fmt(hi['estimate'])} ({hi['analysis'].replace('leave-one-out: omit ', 'without ')}).")


def abstract_results(pooled):
    c = prisma()
    g = lambda k, m="OR": (f"{m} {fmt(pooled[k]['estimate'])}, 95% CI {fmt(pooled[k]['lower95'])}-{fmt(pooled[k]['upper95'])}" if k in pooled else f"{m} {TBC}")
    return (f"**Results.** Of {c['screened']} records screened, {c['included_qualitative']} reports were included, representing ten independent comparative cohorts from China (up to {int(float(pooled['Poor differentiation']['n_SACC'])):,} SACC and {int(float(pooled['Male sex']['n_NSACC'])):,} NSACC patients per analysis), one SACC-only cohort, and one genomic study. "
            f"SACC patients were more often male ({g('Male sex')}; 7 cohorts; I² 0%; low certainty) and older (mean difference {fmt(pooled['age']['estimate'], 1)} years; low certainty). "
            f"Lymph-node metastasis ({g('Lymph-node metastasis')}; low certainty), stage III-IV disease ({g('Stage III-IV')}), distant metastasis ({g('Distant metastasis')}), differentiation, and vascular and perineural invasion did not differ. "
            f"Multivariable-adjusted overall survival was worse in SACC ({g('OS - Adjusted', 'HR')}; 3 cohorts; very low certainty), whereas unadjusted estimates were inconsistent ({g('OS - Unadjusted', 'HR')}; I² {fmt(pooled['OS - Unadjusted']['I2'], 0)}%) "
            f"and adjusted disease-free survival did not differ significantly ({g('DFS - Adjusted', 'HR')}). KRAS mutation was more frequent in SACC in two cohorts ({g('KRAS mutation')}; very low certainty); no other biomarker was studied in more than one cohort.")


def search_paragraph():
    c = prisma()
    return (f"The PubMed search returned {c['db_pubmed']} records and the Europe PMC and Crossref searches {c['other_sources']}, of which {c['duplicates_removed']} were duplicates. "
            f"Of {c['screened']} unique records screened, {c['excluded_title_abstract']} were excluded on title and abstract. Of {c['reports_sought']} reports sought, {c['reports_not_retrieved']} could not be retrieved "
            f"(mainly small Chinese-language biomarker studies and subscription-only articles; Supplementary Table S2). In total, {c['full_text_assessed']} full texts were assessed and {c['full_text_excluded']} were excluded because they had no non-schistosomal comparator or no CRC-specific data, "
            f"leaving {c['included_qualitative']} reports in the qualitative synthesis, of which {c['included_quantitative']} contributed to at least one meta-analysis (Figure 1). Three of the included reports were preprints identified through Europe PMC.{{c:ge2023,zhou2025,pan2022}}")


def characteristics_paragraph():
    return ("The 20 included reports came from 12 hospitals or groups, all in China (Table 1, Figure 2). Ten independent cohorts compared SACC with NSACC: "
            "Changhai Hospital, Shanghai (823 SACC and 30,330 NSACC; 2001-2021);{c:zheng2023} Yijishan Hospital, Wuhu (253 and 2,885; 2012-2018), with a partly overlapping report from the same hospital;{c:wangz2020,yang2023} "
            "the Qingpu Branch of Zhongshan Hospital, Shanghai (137 and 214; 2008-2016), from which six further reports contributed biomarker data only;{c:wangw2020,wangw2021,wangw2023,pan2020,bmcgastro2023,chai2026,pan2022} "
            "Union Hospital, Wuhan (30 and 459; 2010-2019);{c:li2024} Jingzhou Hospital, Hubei (95 and 406; 2020-2022), with an overlapping radiology report;{c:zhu2024,zhang2023} "
            "West China Hospital, Chengdu (30 rectal cancers matched 1:1 on age, sex, and stage; 2009);{c:wangm2014} Wuhu Second People's Hospital (56 and 307; 2015-2020);{c:wu2021} "
            "Ruijin Hospital, Shanghai (26 and 34 rectosigmoid cancers; 2009-2013);{c:feng2015} Xiangya Hospital, Changsha (94 and 6,025, with a propensity-matched survival comparison; 2014-2019);{c:ge2023} "
            "and the Affiliated Hospital of Jiujiang University (1,030 NSACC; SACC reported as percentages only; 2013-2024).{c:zhou2025} "
            "Overlap was confirmed from the full texts: all seven Qingpu reports described patients resected at the same hospital between January 2008 and August 2016, and the two Jingzhou reports shared hospital, period, and an author (Supplementary Table S6). "
            "A report previously suspected to belong to the Qingpu cohort proved to be a separate SACC-only cohort from the main Zhongshan campus (2016-2018).{c:pan2023} One exome-sequencing study used an external comparator.{c:genomic2023} "
            "All cohorts were retrospective. Survival data were available for six cohorts, and nine contributed to at least one pooled analysis.")


def molecular_paragraph(pooled):
    k = pooled.get("KRAS mutation")
    ks = f"KRAS mutation was more frequent in SACC in the two cohorts with internal comparators (pooled OR {est(k)}; I² = {fmt(k['I2'], 0)}%), " if k else ""
    return (ks + "although only the larger cohort was individually significant, mutation status was unknown for 41% of SACC and 41% of NSACC patients in that cohort,{c:zheng2023} and the smaller cohort found the excess confined to G12S/D mutations (43.3% vs 18.1%).{c:li2024} "
            "In the largest cohort, NRAS, BRAF, and PIK3CA mutation and mismatch-repair deficiency did not differ.{c:zheng2023} All other biomarkers came from single reports of the Qingpu cohort and showed no difference in frequency between groups: "
            "c-MYC amplification (13.8% vs 14.4%),{c:pan2020} MET copy-number gain (9.2% vs 10.7%),{c:pan2022} stromal and tumoural PD-L1,{c:wangw2021} stromal and intratumoural TILs, CD3 and CD20,{c:wangw2023} CD4 and CD8 densities,{c:bmcgastro2023} and CFIm25.{c:chai2026} "
            "Exome sequencing of 30 SACC tumours against an external sporadic-CRC reference found a lower median tumour mutational burden (1.61 vs 2.03 mutations/Mb), microsatellite stability or low instability in all cases, and less frequent RTK-RAS and Hippo pathway alteration.{c:genomic2023} "
            "Molecular data on S. mansoni-associated CRC and several small Chinese-language comparisons could not be retrieved (Supplementary Table S2).{c:madbouly2007,zalata2005,chen2016,yangdh2014,ruan2013,yangxg2021,zhangr1998}")


def within_paragraph():
    pooled = _out("Table5b_within_SACC_pooled.csv")
    ln = next((r for r in pooled if r["outcome"] == "LN_metastasis OS"), None)
    return ("Within SACC, conventional factors remained prognostic: nodal metastasis predicted overall survival in two cohorts"
            + (f" (pooled adjusted HR {est(ln)}; I² = {fmt(ln['I2'], 0)}%)" if ln else "") + ",{c:zheng2023,bmcgastro2023} as did distant metastasis, BRAF mutation, and tumour budding in the largest cohort.{c:zheng2023} "
            "Schistosomiasis-specific features were examined only in the SACC-only cohort from the main Zhongshan campus (172 patients):{c:pan2023} in stage III disease, schistosome eggs in regional lymph nodes were associated with shorter disease-free survival "
            "(adjusted HR 3.00, 95% CI 1.37-6.59), and coexisting hepatic schistosomiasis with shorter disease-free (adjusted HR 3.95, 1.75-8.92) and overall survival (adjusted HR 4.97, 1.84-13.43); "
            "deep egg deposition was associated with disease-free survival in univariable analysis only. In the Qingpu SACC subgroup, c-MYC amplification (adjusted HR 1.86, 1.01-3.42), MET copy-number gain (univariable HR 2.36, 1.16-4.80), and high intratumoural CD8 density (adjusted HR 0.52, 0.30-0.90) were prognostic.{c:pan2020,pan2022,bmcgastro2023} "
            "A West China cohort of 74 SACC patients on egg deposition site could not be retrieved.{c:wangm2016} Apart from nodal metastasis, no within-SACC factor could be pooled (Table 5).")


def rob_paragraph():
    rob = _csv("data/analysis_ready/rob_nos.csv")
    main = [r for r in rob if r["study_id"] in POOLED_COHORT_REPORTS]
    n = {k: sum(r["rating"] == k for r in main) for k in ("low", "moderate", "high")}
    return (f"Of the {len(main)} comparative reports that contributed to meta-analyses, {n['low']} were at low, {n['moderate']} at moderate, and {n['high']} at high risk of bias (Supplementary Table S4). "
            "The most frequent limitations were the absence of adjustment for confounders in cross-sectional comparisons, unreported or incomplete follow-up, and non-consecutive selection of the comparison group in two reports.{c:yang2023,feng2015} "
            "Exposure ascertainment was histological in all but one cohort, but egg detection depends on sampling and reporting, which would bias comparisons towards the null. Several reports contained internal numerical inconsistencies, which are listed in the extraction file. "
            "The two independent risk-of-bias assessments agreed on the overall rating for " + RB_AGREEMENT + ".")


def sensitivity_paragraph():
    out = []
    for oc, lab in (("Male sex", "male sex"), ("Stage III-IV", "stage III-IV disease"), ("Lymph-node metastasis", "lymph-node metastasis"), ("Rectal location", "rectal location")):
        r = sens_row(oc, "excluding largest cohort")
        if r:
            out.append(f"{lab} {est(r)}")
    s = ("Excluding the Shanghai cohort of 31,153 patients{c:zheng2023} gave ORs of " + "; ".join(out) + ". The male excess was robust to every sensitivity analysis, "
         "whereas the small excess of rectal tumours depended on the largest cohort and the estimate for stage III-IV disease was unstable. ")
    lo = sens_row("OS - Unadjusted", "leave-one-out: omit WangZ2020")
    if lo:
        s += f"For unadjusted overall survival, omitting the only cohort with a favourable (derived) HR{{c:wangz2020}} gave an HR of {est(lo)} (I² = {fmt(lo['I2'], 0)}%). "
    pp = [r for r in _out("TableS5_sensitivity.csv") if r["analysis"] == "excluding preprints"]
    prim = {r["outcome"]: r for r in pooled_rows()}
    sig = lambda r: float(r["lower95"]) > 1 or float(r["upper95"]) < 1
    changed = [r for r in pp if r["outcome"] in prim and sig(r) != sig(prim[r["outcome"]])]
    if pp:
        s += ("Excluding the preprint cohort{c:ge2023} changed statistical significance for " + "; ".join(f"{r['outcome'][0].lower() + r['outcome'][1:] if not r['outcome'][1:2].isupper() and not r['outcome'].startswith(('Stage','KRAS')) else r['outcome']} ({est(r)}; primary {est(prim[r['outcome']])})" for r in changed) + ", but not for any other outcome. ") if changed else "Excluding the preprint cohort{c:ge2023} changed no conclusion. "
    s += ("Common-effect estimates were similar in direction to random-effects estimates (Supplementary Table S5). All analysed cohorts used histology, so the histology-restricted analysis was identical to the primary analysis; no cohort confirmed the species. "
          "Subgroup analyses were not feasible with two to seven cohorts per outcome, and small-study effects were not assessed because no outcome had 10 or more studies.")
    return s


def grade_paragraph():
    gr = grade()
    by = {}
    for k, r in gr.items():
        by.setdefault(r["certainty"], []).append(k)
    lab = lambda k: {"age": "age (mean difference)"}.get(k, k.replace(" - ", ", ").lower())
    return ("Table 4 summarises all pooled analyses with GRADE ratings (rationale in Supplementary Table S4b). Certainty was low for male sex, older age, lymph-node metastasis, sigmoid location, and vascular and perineural invasion, "
            "and very low for all survival outcomes, stage III-IV disease, distant metastasis, rectal location, differentiation, and KRAS mutation, mainly because of inconsistency and imprecision. "
            "No outcome reached moderate or high certainty. Figure 7 shows the direction of each feature study by study, including features that could not be pooled, and Table 6 integrates these results into a phenotype matrix.")


def principal_findings(pooled):
    g = lambda k, m="OR": f"{m} {est(pooled[k])}" if k in pooled else TBC
    return ("This synthesis of ten Chinese cohorts found that the most consistent difference between SACC and NSACC concerned the patients rather than the tumours. "
            f"SACC patients were older and more often men ({g('Male sex')}), findings that were consistent across cohorts and robust to sensitivity analyses. "
            f"By contrast, nodal metastasis ({g('Lymph-node metastasis')}), distant metastasis, T stage, differentiation, mucinous histology, and vascular and perineural invasion did not differ, the apparent excess of rectal tumours depended on a single large cohort, and the lower frequency of advanced stage was not robust. "
            f"Multivariable-adjusted estimates suggested worse overall survival in SACC ({g('OS - Adjusted', 'HR')}), but this rested on three small cohorts, unadjusted estimates were inconsistent, and the certainty of all survival evidence was very low. "
            "Molecular data were too sparse to define a molecular phenotype. Taken together, the evidence does not support SACC as a reproducibly distinct clinicopathological entity; it supports a demographically distinct patient group in which survival may be worse for reasons that remain unclear.")


def conclusion_text(pooled, short=False):
    g = lambda k, m="OR": f"{m} {fmt(pooled[k]['estimate'])}, 95% CI {fmt(pooled[k]['lower95'])}-{fmt(pooled[k]['upper95'])}" if k in pooled else TBC
    if short:
        return ("Patients with schistosomiasis-associated colorectal cancer are older and more often male, but the available evidence, all from China and of low to very low certainty, does not show a reproducibly distinct tumour phenotype. "
                "A possible survival disadvantage after adjustment requires confirmation in prospective, molecularly characterised cohorts that include the Philippines and other endemic settings.")
    return ("Schistosomiasis-associated colorectal cancer occurs in older patients and more often in men than non-schistosomal colorectal cancer, but in the available evidence its stage, nodal and distant spread, and histopathology are not consistently different, "
            f"and no molecular signature has been established. Adjusted analyses suggest poorer overall survival ({g('OS - Adjusted', 'HR')}), with very low certainty. "
            "SACC is therefore better regarded, on current evidence, as colorectal cancer arising in a distinct host population than as a distinct tumour entity. "
            "Prospective, molecularly characterised cohorts from contemporary endemic settings, including the Philippines and Indonesia, with standardised recording of schistosome eggs and hepatic schistosomiasis, are needed to determine whether these differences reflect a biologically distinct form of colorectal carcinogenesis.")


POOLED_COHORT_REPORTS = ("Zheng2023", "WangZ2020", "WangW2020", "Li2024", "Zhu2024", "Zhang2023", "Yang2023", "Wu2021", "Feng2015", "WangM2014", "Ge2023")
RB_AGREEMENT = "all 11 comparative cohorts (87 of 88 items); the single item disagreement was resolved by consensus"


# =============================================================== tables ======
FOLLOWUP = {"Zheng2023": "NR (survival in 6,537)", "WangZ2020": "Median 78 mo (100 pts)", "WangW2020": "Median 62.4 mo", "WangW2021": "NR (cohort as Wang 2020)",
            "WangW2023": "NR (cohort as Wang 2020)", "Pan2020": "Median 62.4 mo", "Cheng2023": "Median 62.4 mo", "Chai2026": "NR", "Li2024": "NR",
            "Pan2023": "Median 50.1 mo", "WangM2014": "Median 49.8 mo", "Ge2023": "To Aug 2022 (median NR)", "Zhou2025": "None", "Pan2022": "Median 51.3 mo", "Genomic2023": "NR", "Zhang2023": "None", "Zhu2024": "None", "Yang2023": "None", "Wu2021": "None", "Feng2015": "None"}
DEFN = {"Zheng2023": "Calcified eggs in resected colorectal tissue", "Feng2015": "Ova on microscopy (colon, rectum, or stool)",
        "Li2024": "Intact/calcified eggs, granulomas, or worms in CRC tissue", "Genomic2023": "History plus ova in specimen", "WangM2014": "Not stated", "Zhou2025": "Eggs on pathology", "Ge2023": "Eggs on pathology"}


def table1(inv):
    order = ["Zheng2023", "WangZ2020", "Yang2023", "WangW2020", "WangW2021", "WangW2023", "Pan2020", "Cheng2023", "Chai2026", "Li2024",
             "Pan2022", "Zhu2024", "Zhang2023", "WangM2014", "Wu2021", "Feng2015", "Ge2023", "Zhou2025", "Pan2023", "Genomic2023", "WangM2016", "NCG1986", "Madbouly2007"]
    rows = []
    for sid in order:
        r = inv[sid]
        nr = lambda v: "NR" if v in ("NR", "") else v
        retrieved = "Full text read" in r["verification_numbers"]
        rows.append([short_name(r) + cite_tags([REFKEY[sid]]), nr(r["city_province"]), hospital(nr(r["institution"]).split(" (")[0]),
                     nr(r["recruitment_period"]), r["design"].split(" (")[0], nr(r["n_SACC"]),
                     nr(r["n_NSACC"]) if not r["analysis_set"].startswith("Within") else "-",
                     r["species"].split(" (")[0], DEFN.get(sid, "Eggs on H&E in resected specimen" if retrieved else "NR (full text not retrieved)"),
                     FOLLOWUP.get(sid, "NR"), r["outcomes_reported_in_abstract"].split(" (")[0][:80], r["overlap_group"].split("-")[0],
                     r["analysis_set"].split(" (")[0].split(" -")[0] if retrieved else "Not analysed (no full text)"])
    return {"cap": "**Table 1.** Characteristics of identified studies", "head": ["Study", "Location", "Institution", "Study period", "Design", "SACC n", "NSACC n", "Species",
            "Definition of schistosomiasis", "Follow-up", "Main outcomes", "Overlap group", "Analysis set"], "rows": rows, "font": 6.5, "landscape": True,
            "foot": "Extracted from full texts on 5 October 2026 except where marked 'no full text'. NR, not reported; mo, months; S. japonicum presumed = endemic-area cohort, species not confirmed. Overlap groups are defined in Supplementary Table S6. "
                    "Eleven further reports could not be retrieved (Supplementary Table S2). Ge 2023, Zhou 2025, and Pan 2022 are preprints."}


T2 = [("male_sex", "Male"), ("age_over_60", "Age >60"), ("rectal_location", "Rectum"), ("advanced_stage_III_IV", "Stage III-IV"), ("T3_T4", "T3-T4"),
      ("LN_metastasis", "LN+"), ("distant_metastasis", "M1"), ("poor_differentiation", "Poor diff."), ("mucinous", "Mucinous/SRC"),
      ("vascular_invasion", "Vascular inv."), ("perineural_invasion", "PNI")]


def table2(inv):
    bins = [r for r in _verified("binary_outcomes.csv") if r["include_primary"].lower() == "yes"]
    studies = []
    for r in bins:
        if r["study_id"] not in studies:
            studies.append(r["study_id"])
    rows = []
    for sid in studies:
        cell = {r["outcome"]: f"{r['event_SACC']}/{r['n_SACC']} vs {r['event_NSACC']}/{r['n_NSACC']}" for r in bins if r["study_id"] == sid}
        rows.append([short_name(inv[sid]) + cite_tags([REFKEY[sid]])] + [cell.get(k, "-") for k, _ in T2])
    return {"cap": "**Table 2.** Clinicopathological outcomes by study: events/total in SACC vs NSACC", "head": ["Study"] + [l for _, l in T2], "rows": rows, "font": 6.5, "landscape": True,
            "foot": "Only the report used for each outcome within an overlap group is shown (Supplementary Table S6). -, not reported or taken from another report of the same cohort. LN+, lymph-node metastasis; M1, distant metastasis (stage IV where M stage was not given separately); PNI, perineural invasion. Definitions differ between studies (see notes in the extraction file)."}


def table3():
    mol = _verified("molecular_evidence.csv")
    pooled = {r["biomarker"]: r["pooled"] for r in _out("Table3_molecular_evidence_map.csv")}
    inv = inventory()
    rows = []
    for r in mol:
        pct = lambda a, b: f"{a}/{b} ({100 * float(a) / float(b):.1f}%)" if a and b else (b or "-")
        rows.append([r["biomarker"], short_name(inv[r["study_id"]]) + cite_tags([REFKEY[r["study_id"]]]), r["method"], pct(r["positive_SACC"], r["total_SACC"]),
                     pct(r["positive_NSACC"], r["total_NSACC"]) if r["comparator_type"] == "internal" else "External (TCGA sporadic CRC)", r["reported_p"],
                     pooled.get(r["biomarker"], "Not pooled") if r["comparator_type"] == "internal" else "Not poolable (external comparator)"])
    rows.append(["APC, TP53 mutation, beta-catenin, Ki-67", "None with internal comparator", "-", "-", "-", "-", "No evidence"])
    return {"cap": "**Table 3.** Molecular evidence map for SACC versus NSACC", "head": ["Biomarker", "Study", "Method", "SACC positive/total", "NSACC positive/total", "Reported P", "Pooled effect (random effects)"],
            "rows": rows, "font": 7, "landscape": True,
            "foot": "All Qingpu reports (Wang 2021, Wang 2023, Pan 2020, Cheng 2023, Chai 2026) describe one cohort; each biomarker appears once. Biomarkers were pooled only with at least two independent internal-comparator cohorts. "
                    "Abstract-only data on S. mansoni (Madbouly 2007: p53 32/40 vs 8/20; MSI 3/40 vs 1/20) are not shown in the analysis."}


def table4(pooled):
    order = [("OS - Adjusted", "Overall survival (adjusted)", "HR"), ("OS - Unadjusted", "Overall survival (unadjusted/derived)", "HR"),
             ("DFS - Adjusted", "DFS/RFS (adjusted)", "HR"), ("DFS - Unadjusted", "DFS/RFS (unadjusted)", "HR"),
             ("Stage III-IV", "Stage III-IV", "OR"), ("Lymph-node metastasis", "Lymph-node metastasis", "OR"), ("Distant metastasis", "Distant metastasis", "OR"),
             ("pT3-T4", "pT3-T4", "OR"), ("Male sex", "Male sex", "OR"), ("age", "Age, years", "MD"), ("Age > 60 years", "Age > 60 years", "OR"),
             ("Rectal location", "Rectal location", "OR"), ("Sigmoid location", "Sigmoid location", "OR"), ("Right-sided colon", "Right-sided colon", "OR"),
             ("Poor differentiation", "Poor differentiation", "OR"), ("Mucinous histology", "Mucinous/signet-ring histology", "OR"),
             ("Vascular invasion", "Vascular invasion", "OR"), ("Perineural invasion", "Perineural invasion", "OR"), ("Tumour budding", "Tumour budding", "OR"),
             ("Tumour size >= 5 cm", "Tumour size >= 5 cm", "OR"), ("KRAS mutation", "KRAS mutation", "OR")]
    rows = []
    for key, lab, m in order:
        r = pooled.get(key)
        if r:
            rows.append([lab, r["k"], r["n_SACC"], r["n_NSACC"], m, fmt(r["estimate"]), f"{fmt(r['lower95'])}-{fmt(r['upper95'])}",
                         f"{fmt(r['I2'], 0)}%", fmt(r["tau2"], 3), ("<0.001" if float(r["p_value"]) < 0.001 else fmt(r["p_value"], 3)), g_of(key).capitalize()])
        else:
            rows.append([lab, "<2", "-", "-", m, "Not pooled", "-", "-", "-", "-", "-"])
    return {"cap": "**Table 4.** Summary of meta-analyses: SACC versus NSACC", "head": ["Outcome", "Studies", "SACC n", "NSACC n", "Measure", "Pooled effect", "95% CI", "I²", "tau²", "P value", "GRADE certainty"],
            "rows": rows, "font": 7.5, "landscape": True,
            "foot": "Random-effects models with REML estimation; S. japonicum (presumed) cohorts; one report per overlap group per outcome. HR > 1 and OR > 1 indicate higher hazard or higher odds in SACC; MD > 0, older SACC patients. "
                    "Generated from output/tables/Table4_meta_analysis_summary.csv. GRADE: certainty starts low for observational evidence; reasons for rating down are given in Supplementary Table S4b."}


def table5():
    inv = inventory()
    ws = _verified("within_sacc_prognostic.csv")
    rows = [[r["factor"].replace("_", " "), short_name(inv[r["study_id"]]) + cite_tags([REFKEY[r["study_id"]]]), r["comparison"], r["outcome"],
             f"{fmt(r['hr'])} ({fmt(r['lower95'])}-{fmt(r['upper95'])})", "Adjusted" if r["adjusted"] == "yes" else "Univariable", r["covariates"] or "-", r["n_SACC_total"]] for r in ws]
    for r in _out("Table5b_within_SACC_pooled.csv"):
        rows.append([r["outcome"].replace("_", " ") + " (pooled)", f"{r['k']} cohorts", "", "", f"{fmt(r['estimate'])} ({fmt(r['lower95'])}-{fmt(r['upper95'])}); I² {fmt(r['I2'], 0)}%", "Random effects", "", r["n_SACC"]])
    return {"cap": "**Table 5.** Within-SACC prognostic factors", "head": ["Factor", "Study", "Comparison", "Outcome", "HR (95% CI)", "Model", "Adjusted for", "SACC n"],
            "rows": rows, "font": 6.5, "landscape": True,
            "foot": "SACC-only analyses; not combined with the SACC-versus-NSACC comparison. Wang 2021 and Wang 2023 report P = 0.045 for HRs whose 95% CI includes 1. Factors from the Qingpu cohort (Wang 2021, Wang 2023, Pan 2020, Cheng 2023) describe the same patients."}


def table6():
    pooled = {r["outcome"]: r for r in pooled_rows()}
    items = [("Older age", "age"), ("Male sex", "Male sex"), ("Rectal localisation", "Rectal location"), ("Advanced stage", "Stage III-IV"),
             ("Lymph-node metastasis", "Lymph-node metastasis"), ("Distant metastasis", "Distant metastasis"), ("Vascular invasion", "Vascular invasion"),
             ("Mucinous histology", "Mucinous histology"), ("Multiple primary CRC", None), ("KRAS mutation", "KRAS mutation"),
             ("Overall survival (adjusted)", "OS - Adjusted"), ("DFS/RFS (adjusted)", "DFS - Adjusted")]
    rows = []
    for lab, key in items:
        r = pooled.get(key) if key else None
        if not r:
            rows.append([lab, "Higher in SACC (single cohort)", "Limited"]); continue
        lo, hi, k, i2 = float(r["lower95"]), float(r["upper95"]), int(r["k"]), float(r["I2"])
        null = 0 if r["measure"] == "MD" else 1
        sig = lo > null or hi < null
        up = float(r["estimate"]) > null
        surv = r["measure"] == "HR"
        d = ("Worse in SACC" if up else "Better in SACC") if (surv and sig) else ("Up" if up else "Down") if sig else "Neutral (CI includes no difference)"
        s = f"{g_of(key).capitalize()} certainty; {k} cohorts" + ("; inconsistent" if i2 >= 75 else "")
        if lab == "Older age":
            d = "Up (all cohorts older or similar)"
        if key in ("Rectal location",):
            s += "; lost without largest cohort"
        rows.append([lab, d, s])
    return {"cap": "**Table 6.** Phenotype matrix: is SACC distinct?", "head": ["Feature", "Pooled direction", "Strength of evidence"], "rows": rows, "font": 8, "landscape": False,
            "foot": "Direction classified from Table 4 (95% CI excluding no difference); strength = GRADE certainty. Formerly classified automatically from Table 4 before GRADE: Moderate, >= 3 cohorts, 95% CI excluding no difference, I² < 50%; Limited, fewer cohorts or imprecise; Inconsistent, I² >= 75%. 'Strong' is reserved for findings with moderate/high GRADE certainty and is not yet assigned."}


# ============================================================== rendering =====
ITALIC = re.compile(r"(Schistosoma japonicum|Schistosoma haematobium|Schistosoma mansoni|S\. japonicum|S\. mansoni|S\. haematobium|\bet al\.)")
HILITE = re.compile(r"(\[[^\]]*(?:TO BE|to be|TBC|to verify|AUTHOR DECISION|AUTHOR INPUT|SEARCH DATE|INITIALS|NAME|REPOSITORY|PROSPERO|DD Month|if accessible|EndNote)[^\]]*\])")


def add_runs(par, text, size=12, bold_all=False):
    for seg in re.split(r"(\*\*[^*]+\*\*)", text):
        if not seg:
            continue
        bold = bold_all or (seg.startswith("**") and seg.endswith("**"))
        seg = seg.strip("*") if seg.startswith("**") else seg
        for piece in HILITE.split(seg):
            if not piece:
                continue
            hl = bool(HILITE.fullmatch(piece))
            for sub in ITALIC.split(piece):
                if not sub:
                    continue
                parts = re.split(r"(\^[\d,\-]+\^)", sub)
                for q in parts:
                    if not q:
                        continue
                    run = par.add_run(q.strip("^") if q.startswith("^") else q)
                    run.font.size = Pt(size); run.font.name = "Arial"
                    run._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
                    run.bold = bold
                    run.italic = bool(ITALIC.fullmatch(sub)) and sub != "et al."
                    if q.startswith("^"):
                        run.font.superscript = True
                    if hl:
                        run.font.highlight_color = WD_COLOR_INDEX.YELLOW


class Numberer:
    def __init__(self):
        self.order = []

    def num(self, key):
        if key not in REFS:
            raise KeyError(f"Unknown reference key: {key}")
        if key not in self.order:
            self.order.append(key)
        return self.order.index(key) + 1

    def sub(self, text):
        def rep(m):
            nums = sorted(self.num(k.strip()) for k in m.group(1).split(","))
            # compress runs: 3,4,5 -> 3-5
            out, i = [], 0
            while i < len(nums):
                j = i
                while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
                    j += 1
                out.append(f"{nums[i]}-{nums[j]}" if j - i >= 2 else ",".join(map(str, nums[i:j + 1])))
                i = j + 1
            return "^" + ",".join(out) + "^"
        return re.sub(r"\{c:([^}]+)\}", rep, text)


def number_all(blocks, numberer):
    out = []
    for b in blocks:
        if b[0] in ("p", "h1", "h2", "h3", "title"):
            out.append((b[0], numberer.sub(b[1])))
        elif b[0] == "table":
            t = dict(b[1]); t["rows"] = [[numberer.sub(str(c)) for c in r] for r in t["rows"]]
            t["cap"] = numberer.sub(t["cap"]); t["foot"] = numberer.sub(t["foot"]); out.append(("table", t))
        elif b[0] == "fig":
            f = dict(b[1]); f["cap"] = numberer.sub(f["cap"]); out.append(("fig", f))
        else:
            out.append(b)
    return out


def setup_doc():
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Arial"; st.font.size = Pt(12)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    pf = st.paragraph_format
    pf.line_spacing = 1.0; pf.space_after = Pt(6); pf.space_before = Pt(0)
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(2.54); s.left_margin = s.right_margin = Cm(2.54)
    return doc


def set_landscape(doc, on):
    sec = doc.add_section()
    if on:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = Cm(27.94), Cm(21.59)
    else:
        sec.orientation = WD_ORIENT.PORTRAIT
        sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
    return sec


def render_table(doc, t):
    if t.get("landscape"):
        set_landscape(doc, True)
    cap = doc.add_paragraph(); add_runs(cap, t["cap"], size=11)
    tab = doc.add_table(rows=1, cols=len(t["head"]))
    tab.style = "Table Grid"; tab.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(t["head"]):
        c = tab.rows[0].cells[i]; c.text = ""
        add_runs(c.paragraphs[0], h, size=t["font"], bold_all=True)
        shd = c._element.get_or_add_tcPr()
        el = shd.makeelement(qn("w:shd"), {qn("w:val"): "clear", qn("w:color"): "auto", qn("w:fill"): "DCE6F1"})
        shd.append(el)
    for r in t["rows"]:
        cells = tab.add_row().cells
        for i, v in enumerate(r):
            cells[i].text = ""
            add_runs(cells[i].paragraphs[0], str(v), size=t["font"])
            cells[i].paragraphs[0].paragraph_format.space_after = Pt(0)
    fn = doc.add_paragraph(); add_runs(fn, t["foot"], size=9)
    if t.get("landscape"):
        set_landscape(doc, False)


def render_fig(doc, f):
    path = os.path.join(OUT, "figures", f["file"]) if f.get("from_output") else os.path.join(FIG, f["file"])
    par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists(path):
        par.add_run().add_picture(path, width=Cm(f["w"]))
    else:
        add_runs(par, f"[FIGURE {f['file'].split('_')[0].replace('Figure', '')} TO BE GENERATED by R/run_all.R from verified data]", size=11)
    cap = doc.add_paragraph(); add_runs(cap, f["cap"], size=11)


def render(blocks, numberer, path):
    doc = setup_doc()
    for b in blocks:
        kind = b[0]
        if kind == "title":
            par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_runs(par, b[1], size=14, bold_all=True)
        elif kind == "h1":
            par = doc.add_paragraph(); add_runs(par, b[1].upper() if b[1].isupper() else b[1], size=12, bold_all=True)
            par.paragraph_format.space_before = Pt(12)
        elif kind == "h2":
            par = doc.add_paragraph(); add_runs(par, b[1], size=12, bold_all=True)
        elif kind == "h3":
            par = doc.add_paragraph(); add_runs(par, b[1], size=12)
        elif kind == "p":
            par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY; add_runs(par, b[1])
        elif kind == "pb":
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        elif kind == "table":
            render_table(doc, b[1])
        elif kind == "fig":
            render_fig(doc, b[1])
        elif kind == "refs":
            for i, k in enumerate(numberer.order, 1):
                txt, status = REFS[k]
                par = doc.add_paragraph(); par.paragraph_format.left_indent = Cm(0.75)
                par.paragraph_format.first_line_indent = Cm(-0.75)
                add_runs(par, f"{i}.\t{txt}" + (" [VERIFY: complete authors/year/pages from PubMed]" if status == "verify" else ""), size=11)
    doc.save(path)


# ========================================================= supplementary =====
def supplementary_blocks():
    B = []
    B.append(("title", "Supplementary Material - Defining Schistosomiasis-Associated Colorectal Cancer: A Systematic Analysis and Meta-analysis"))
    B.append(("h1", "Supplementary Table S1. Complete search strategies"))
    B.append(("table", {"cap": "**Table S1.** Database search strategies (PRISMA-S)", "font": 7.5, "landscape": True,
        "head": ["Database", "Platform", "Exact query", "Date range", "Search date", "Records", "Limits"],
        "rows": S1_ROWS,
        "foot": "Deduplication by PubMed identifier and DOI (Python script, archived with the data). Searches were not peer reviewed with PRESS. Scopus, Web of Science, Embase, CNKI, Wanfang, and SinoMed require institutional subscriptions that were not available; their strategies are given so that the search can be extended."}))
    B.append(("h1", "Supplementary Table S2. Full texts excluded, with reasons"))
    B.append(("table", {"cap": "**Table S2.** Excluded full-text reports", "font": 8,
        "head": ["Study", "PMID / DOI", "Principal reason for exclusion"],
        "rows": S2_ROWS,
        "foot": "One principal reason per report, in the hierarchy: not CRC; not human; no schistosomiasis status; no comparator; no extractable outcome; duplicate cohort for the same outcome."}))
    B.append(("h1", "Supplementary Table S3. Complete extraction data"))
    B.append(("p", "Duplicate extraction agreed exactly for 78 of 82 binary rows and for all survival, continuous, molecular, and within-SACC values; the four disagreements and their resolution are listed in data/ADJUDICATION_LOG.md. The data are provided as the Excel workbook SACC_master_extraction.xlsx (sheets: master_wide, binary_outcomes, continuous_outcomes, survival_outcomes, within_sacc_prognostic, molecular_evidence, evidence_direction, rob_nos, inventory, overlap). Every value records its origin (reported, calculated from raw data, Kaplan-Meier-reconstructed, converted from median/IQR) and its source location in the original report."))
    B.append(("h1", "Supplementary Table S4. Risk-of-bias assessments"))
    B.append(("table", {"cap": "**Table S4.** Newcastle-Ottawa Scale assessments", "font": 8,
        "head": ["Study", "Selection (0-4)", "Comparability (0-2)", "Outcome/exposure (0-3)", "Total (0-9)", "Overall risk of bias"],
        "rows": nos_rows(),
        "foot": "Interim: one AI-assisted assessor; second independent assessment PENDING. Comparability awarded for analyses adjusted for stage plus age or sex. Low risk: 7-9 stars; moderate: 5-6; high: 0-4. Follow-up items are not met by cross-sectional comparisons."}))
    B.append(("h1", "Supplementary Table S4b. GRADE assessments"))
    B.append(("table", {"cap": "**Table S4b.** GRADE certainty of evidence for each pooled outcome", "font": 7, "landscape": True,
        "head": ["Outcome", "Certainty", "Risk of bias", "Inconsistency", "Indirectness", "Imprecision", "Publication bias", "Rationale"],
        "rows": [[r["outcome"], r["certainty"], r["risk_of_bias"], r["inconsistency"], r["indirectness"], r["imprecision"], r["publication_bias"], r["explanation"]] for r in _csv("data/analysis_ready/grade.csv")],
        "foot": "Evidence from observational studies starts at low certainty. No outcome met criteria for rating up. Publication bias could not be assessed formally (fewer than 10 studies per outcome)."}))
    B.append(("h1", "Supplementary Table S5. Sensitivity analyses"))
    B.append(("table", s5_table()))
    B.append(("h1", "Supplementary Table S6. Potentially overlapping cohorts and decisions"))
    ov = list(csv.reader(open(os.path.join(ROOT, "data/overlap_matrix.csv"))))
    B.append(("table", {"cap": "**Table S6.** Overlap matrix", "font": 7.5, "landscape": True,
        "head": ["Study", "Hospital", "Recruitment dates", "SACC n", "NSACC n", "Potential overlap", "Decision"],
        "rows": ov[1:], "foot": "Groups: G1 Changhai (Shanghai); G2 Yijishan (Wuhu); G3 Qingpu Branch of Zhongshan Hospital (Shanghai); G4 Union Hospital (Wuhan); G5 Jingzhou (Hubei); G6 West China Hospital (Chengdu); G7 national cooperative group; G8 Alexandria. Institution and period for each report are to be confirmed from the full text."}))
    B.append(("h1", "PRISMA 2020 checklist"))
    B.append(("table", {"cap": "**PRISMA 2020 checklist** (location in manuscript)", "font": 8,
        "head": ["Section/item", "Location"], "rows": PRISMA, "foot": "Page numbers to be added after typesetting."}))
    B.append(("h1", "Supplementary figures"))
    B.append(("p", "Study-level forest plots for every pooled outcome (random effects, REML). No outcome had 10 or more studies, so funnel plots were not drawn."))
    for f in sorted(os.listdir(os.path.join(OUT, "figures"))) if os.path.isdir(os.path.join(OUT, "figures")) else []:
        if f.startswith("Fig_forest_") and f.endswith(".png"):
            oc = f[len("Fig_forest_"):-4]
            B.append(("fig", {"file": f, "w": 15.0, "from_output": True, "cap": f"**Figure S-{oc}.** Study-level forest plot: {oc.replace('_', ' ')}."}))
    B.append(("h1", "References cited in the Supplementary Material"))
    B.append(("refs",))
    return B


S2_ROWS = [
 ["Liu XF 2023{c:liuxf2023}", "38125940", "Excluded at full text: no CRC-specific SACC-versus-NSACC data (cancer spectrum among S. japonicum patients)"],
 ["Liu 2013{c:liu2013}", "24083755", "Excluded at full text: SACC case series without a non-schistosomal comparator"],
 ["Wang M 2016{c:wangm2016}", "26922912", "Not retrieved (subscription); SACC-only cohort of 74"],
 ["NCG 1986{c:ncg1986}", "3021419", "Not retrieved (Chinese, print only)"],
 ["Madbouly 2007{c:madbouly2007}", "16786317", "Not retrieved (subscription); S. mansoni"],
 ["Zhang W 2012{c:zhou_ct2012}", "22658847", "Not retrieved; abstract shows SACC-only imaging study"],
 ["Chen 2016{c:chen2016}", "26797844", "Not retrieved (Chinese); 80 vs 258, hMLH1/hMSH2"],
 ["Yang DH 2014{c:yangdh2014}", "25434139", "Not retrieved (Chinese); 80 vs 80, p53/COX-2/Bax/c-myc"],
 ["Ruan 2013{c:ruan2013}", "24024441", "Not retrieved (Chinese); 30 vs 30, VEGF/PD-ECGF"],
 ["Yang XG 2021{c:yangxg2021}", "34008361", "Not retrieved (Chinese); 30 vs 30, Bcl-2/Bax"],
 ["Zhang R 1998{c:zhangr1998}", "9851256", "Not retrieved (subscription); 22 vs 22, TP53 mutations"],
 ["Zalata 2005{c:zalata2005}", "16308474", "Not retrieved (PMC and publisher access blocked); S. mansoni"],
 ["Farid 2006{c:farid2006}", "doi:10.21608/ejsur.2006.372983", "Not retrieved (journal site unreachable); S. mansoni setting"],
]


def nos_rows():
    rows = []
    for r in _csv("data/analysis_ready/rob_nos.csv"):
        inv = inventory()[r["study_id"]]
        sel = sum(int(r[k]) for k in ("S1_representativeness", "S2_selection_nonexposed", "S3_ascertainment_exposure", "S4_outcome_absent_at_start"))
        out = sum(int(r[k]) for k in ("O1_assessment_outcome", "O2_follow_up_length", "O3_follow_up_adequacy"))
        rows.append([short_name(inv) + cite_tags([REFKEY[r["study_id"]]]), sel, r["C1_comparability"], out, r["total_stars"], r["rating"]])
    return rows


def s5_table():
    rows = [[r["outcome"], r["analysis"], r["k"], r["measure"], f"{fmt(r['estimate'])} ({fmt(r['lower95'])}-{fmt(r['upper95'])})", f"{fmt(r['I2'], 0)}%"]
            for r in _out("TableS5_sensitivity.csv")]
    for r in pooled_rows():
        rows.append([r["outcome"], "fixed (common) effect", r["k"], r["measure"], f"{fmt(r['fixed_estimate'])} ({fmt(r['fixed_lower95'])}-{fmt(r['fixed_upper95'])})", "-"])
    return {"cap": "**Table S5.** Sensitivity analyses", "head": ["Outcome", "Analysis", "Studies", "Measure", "Estimate (95% CI)", "I²"], "rows": rows, "font": 7,
            "foot": "From output/tables/TableS5_sensitivity.csv and Table 4 (fixed-effect columns). 'Excluding largest cohort' removes Zheng 2023. Analyses identical to the primary analysis (e.g. histology-confirmed only) are not repeated."}


SEARCHES = [
 ("MEDLINE", "PubMed", '("Schistosoma japonicum"[Mesh] OR "Schistosomiasis"[Mesh] OR "Schistosoma"[Mesh] OR "Schistosoma japonicum"[tiab] OR schistosomiasis[tiab] OR schistosomal[tiab] OR schistosoma*[tiab] OR bilharzia*[tiab]) AND ("Colorectal Neoplasms"[Mesh] OR ((colorectal[tiab] OR colon[tiab] OR colonic[tiab] OR rectal[tiab] OR rectum[tiab] OR "large bowel"[tiab] OR "large intestine"[tiab]) AND (cancer*[tiab] OR carcinoma*[tiab] OR neoplasm*[tiab] OR tumor*[tiab] OR tumour*[tiab] OR adenocarcinoma*[tiab] OR malignan*[tiab])))'),
 ("Scopus", "Elsevier Scopus", 'TITLE-ABS-KEY ( "Schistosoma japonicum" OR schistosomiasis OR schistosomal OR schistosoma* OR bilharzia* ) AND TITLE-ABS-KEY ( ( colorectal OR colon OR colonic OR rectal OR rectum OR "large bowel" OR "large intestine" ) W/3 ( cancer* OR carcinoma* OR neoplasm* OR tumor* OR tumour* OR adenocarcinoma* OR malignan* ) )'),
 ("Web of Science Core Collection", "Clarivate (all editions)", 'TS=("Schistosoma japonicum" OR schistosomiasis OR schistosomal OR schistosoma* OR bilharzia*) AND TS=((colorectal OR colon OR colonic OR rectal OR rectum OR "large bowel" OR "large intestine") NEAR/3 (cancer* OR carcinoma* OR neoplasm* OR tumor* OR tumour* OR adenocarcinoma* OR malignan*))'),
 ("Embase", "Elsevier Embase.com", "('schistosomiasis'/exp OR 'schistosoma japonicum'/exp OR 'schistosoma'/exp OR schistosom*:ti,ab,kw OR bilharzia*:ti,ab,kw) AND ('colorectal tumor'/exp OR 'colon tumor'/exp OR 'rectum tumor'/exp OR ((colorectal OR colon OR colonic OR rectal OR rectum OR 'large bowel' OR 'large intestine') NEAR/3 (cancer* OR carcinoma* OR neoplasm* OR tumor* OR tumour* OR adenocarcinoma* OR malignan*)):ti,ab,kw)"),
 ("CNKI", "cnki.net (advanced search, SU=subject)", "SU=('血吸虫' + '血吸虫病' + '日本血吸虫') AND SU=('结直肠癌' + '大肠癌' + '结肠癌' + '直肠癌' + '结直肠肿瘤' + '结直肠腺癌')"),
 ("Wanfang Data", "wanfangdata.com.cn", "主题:(血吸虫 OR 血吸虫病 OR 日本血吸虫) AND 主题:(结直肠癌 OR 大肠癌 OR 结肠癌 OR 直肠癌 OR 结直肠肿瘤)"),
 ("SinoMed (CBM)", "sinomed.ac.cn", "('血吸虫病'[主题词] OR '日本血吸虫'[主题词] OR 血吸虫[常用字段]) AND ('结直肠肿瘤'[主题词] OR 结直肠癌[常用字段] OR 大肠癌[常用字段] OR 结肠癌[常用字段] OR 直肠癌[常用字段])"),
 ("Google Scholar", "scholar.google.com (citation chasing only)", "Forward citations of each included study; first 200 results of: schistosomiasis \"colorectal cancer\" comparison"),
]

S1_ROWS = [
 ["MEDLINE", "PubMed", SEARCHES[0][2], "Inception to search date", "2026-10-05", "337", "None"],
 ["Europe PMC", "europepmc.org REST API (MED, PMC, PPR, AGR, CBA)", '(TITLE_ABS:schistosom* OR TITLE_ABS:bilharzi*) AND (TITLE_ABS:colorectal OR TITLE_ABS:colon OR TITLE_ABS:colonic OR TITLE_ABS:rectal OR TITLE_ABS:rectum OR TITLE_ABS:"large bowel" OR TITLE_ABS:"large intestine" OR TITLE_ABS:rectosigmoid) AND (TITLE_ABS:cancer* OR TITLE_ABS:carcinoma* OR TITLE_ABS:neoplas* OR TITLE_ABS:tumor* OR TITLE_ABS:tumour* OR TITLE_ABS:adenocarcinoma* OR TITLE_ABS:malignan*)', "Inception to search date", "2026-10-05", "297 (30 not in PubMed)", "None"],
 ["Crossref", "api.crossref.org (query.bibliographic, top 200 per query)", "schistosomal colorectal cancer; schistosomiasis colorectal cancer; schistosomiasis associated colorectal cancer; schistosomal rectal cancer; schistosomiasis colon carcinoma; 血吸虫 结直肠癌; 血吸虫病 大肠癌 (titles filtered for schistosomiasis + colorectal + cancer terms)", "Inception to search date", "2026-10-05", "15 (not in PubMed/Europe PMC)", "None"],
] + [[d, pl, q, "-", "Not searched (no subscription access)", "-", "-"] for d, pl, q in [
 ("Scopus", "Elsevier Scopus", 'TITLE-ABS-KEY ( "Schistosoma japonicum" OR schistosomiasis OR schistosomal OR schistosoma* OR bilharzia* ) AND TITLE-ABS-KEY ( ( colorectal OR colon OR colonic OR rectal OR rectum OR "large bowel" OR "large intestine" ) W/3 ( cancer* OR carcinoma* OR neoplasm* OR tumor* OR tumour* OR adenocarcinoma* OR malignan* ) )'),
 ("Web of Science Core Collection", "Clarivate", 'TS=("Schistosoma japonicum" OR schistosomiasis OR schistosomal OR schistosoma* OR bilharzia*) AND TS=((colorectal OR colon OR colonic OR rectal OR rectum OR "large bowel" OR "large intestine") NEAR/3 (cancer* OR carcinoma* OR neoplasm* OR tumor* OR tumour* OR adenocarcinoma* OR malignan*))'),
 ("Embase", "Embase.com", "('schistosomiasis'/exp OR 'schistosoma japonicum'/exp OR schistosom*:ti,ab,kw OR bilharzia*:ti,ab,kw) AND ('colorectal tumor'/exp OR ((colorectal OR colon OR rectal OR rectum) NEAR/3 (cancer* OR carcinoma* OR neoplasm* OR tumor*)):ti,ab,kw)"),
 ("CNKI / Wanfang / SinoMed", "Chinese databases", "SU=('血吸虫' + '血吸虫病' + '日本血吸虫') AND SU=('结直肠癌' + '大肠癌' + '结肠癌' + '直肠癌')")]]


PRISMA = [[a, b] for a, b in [
 ("1 Title", "Title page"), ("2 Abstract", "Abstract"), ("3 Rationale", "Introduction, paragraphs 3-5"), ("4 Objectives", "Introduction, final paragraph"),
 ("5 Eligibility criteria", "Methods: Eligibility criteria"), ("6 Information sources", "Methods: Information sources; Table S1"),
 ("7 Search strategy", "Table S1"), ("8 Selection process", "Methods: Study selection"), ("9 Data collection process", "Methods: Data extraction"),
 ("10a-b Data items", "Methods: Outcome definitions; Table S3"), ("11 Study risk of bias assessment", "Methods: Risk of bias"),
 ("12 Effect measures", "Methods: Statistical analysis"), ("13a-f Synthesis methods", "Methods: Statistical, subgroup and sensitivity analyses"),
 ("14 Reporting bias assessment", "Methods: Small-study effects"), ("15 Certainty assessment", "Methods: Certainty of evidence"),
 ("16a-b Study selection", "Results: Search results; Figure 1; Table S2"), ("17 Study characteristics", "Table 1"),
 ("18 Risk of bias in studies", "Results: Risk of bias; Table S4"), ("19 Results of individual studies", "Figures 3-5; Table S3"),
 ("20a-d Results of syntheses", "Results; Table 4; Figures 3-7; Table S5"), ("21 Reporting biases", "Results: Sensitivity analyses"),
 ("22 Certainty of evidence", "Table 4"), ("23a-d Discussion", "Discussion"), ("24a-c Registration and protocol", "Methods: Protocol and registration"),
 ("25 Support", "Funding Source"), ("26 Competing interests", "Author Disclosure"), ("27 Availability of data, code and other materials", "Data Availability")]]


def write_simple_doc(path, title, paragraphs):
    doc = setup_doc()
    par = doc.add_paragraph(); add_runs(par, title, size=12, bold_all=True)
    for t in paragraphs:
        par = doc.add_paragraph(); add_runs(par, t)
    doc.save(path)


def cover_letter():
    return ["[AUTHOR INPUT: date]", "The Editor-in-Chief\nActa Medica Philippina\nUniversity of the Philippines Manila",
            "Dear Editor,",
            "We submit the manuscript \"Defining Schistosomiasis-Associated Colorectal Cancer: A Systematic Analysis and Meta-analysis of Clinicopathological, Molecular, and Prognostic Features\" for consideration as an Original Article.",
            "Schistosoma japonicum remains endemic in the Philippines, yet it is unclear whether colorectal cancers arising in patients with schistosomiasis behave differently from other colorectal cancers. Our review synthesises ten independent comparative cohorts, with explicit resolution of overlapping hospital reports, duplicate data extraction, and separation of adjusted and unadjusted survival estimates. "
            "We found that patients with schistosomiasis-associated colorectal cancer are consistently older and more often male, but that their tumours do not differ reproducibly in stage, nodal or distant spread, or histopathology; multivariable-adjusted estimates suggest poorer overall survival, with very low certainty.",
            "The findings are relevant to pathologists, surgeons, and oncologists in endemic regions of the Philippines: no Philippine comparative cohort exists, and we recommend routine recording of schistosome eggs in colorectal resection reports as the basis for such studies.",
            "This manuscript has not been published and is not under consideration elsewhere. All authors have approved the submission. " + AUTHOR_COI + " " + AUTHOR_REGISTRATION + " An AI language model was used in searching, screening, data extraction, analysis coding, and drafting, as disclosed in the manuscript; the authors take full responsibility for the content.",
            "Sincerely,\nJayson Cagadas Pasaol, DVM, PhD\n" + AUTHOR_AFFILIATION + "\njaysonpasaolrmt082@gmail.com"]


def highlights():
    return ["Highlights",
            "- Ten independent Chinese cohorts compared schistosomiasis-associated (SACC) with non-schistosomal colorectal cancer, after resolving 17 overlapping hospital reports.",
            "- SACC patients were consistently older and more often male (OR 1.38), with low-certainty evidence.",
            "- Stage, nodal and distant metastasis, differentiation, and vascular or perineural invasion did not differ reproducibly.",
            "- Adjusted overall survival was worse in SACC (HR 2.10, 3 cohorts), but survival evidence was of very low certainty.",
            "- No comparative cohort from the Philippines or Indonesia exists; routine recording of schistosome eggs in resection reports is recommended.",
            "",
            "Graphical abstract: Figure 8 (conceptual model) on the left and Figure 3 (pooled phenotype forest plot) on the right, titled 'SACC: a distinct host population rather than a distinct tumour?'"]


def legends(numbered):
    out = ["Figure and table legends (as embedded in the manuscript)"]
    for b in numbered:
        if b[0] == "fig":
            out.append(b[1]["cap"])
        elif b[0] == "table":
            out.append(b[1]["cap"] + " " + b[1]["foot"])
    return out


def main():
    numberer = Numberer()
    raw = manuscript_blocks()
    def _words(start, stop):
        on, n = False, 0
        for b in raw:
            if b[0] == "h1":
                if b[1] == start: on = True
                elif b[1] == stop: on = False
            if on and b[0] == "p":
                n += len(re.sub(r"\{c:[^}]+\}|\*\*", "", b[1]).split())
        return n
    aw, mw = _words("ABSTRACT", "INTRODUCTION"), _words("INTRODUCTION", "Acknowledgments")
    raw = [("p", b[1].format(abstract_words=aw, main_words=mw)) if b[0] == "p" and "{abstract_words}" in b[1] else b for b in raw]
    print(f"Abstract {aw} words; main text {mw} words")
    blocks = number_all(raw, numberer)
    json.dump({k: i + 1 for i, k in enumerate(numberer.order)}, open(os.path.join(HERE, "ref_numbers.json"), "w"), indent=1)
    subprocess.run([sys.executable, os.path.join(FIG, "make_figures_1_2_8.py")], check=True)
    render(blocks, numberer, os.path.join(HERE, "SACC_Manuscript_ActaMedPhilipp.docx"))

    sn = Numberer()
    sblocks = number_all(supplementary_blocks(), sn)
    render(sblocks, sn, os.path.join(HERE, "SACC_Supplementary_Material.docx"))

    write_simple_doc(os.path.join(HERE, "Cover_Letter.docx"), "Cover letter", cover_letter())
    write_simple_doc(os.path.join(HERE, "Highlights_and_Graphical_Abstract.docx"), "Highlights", highlights())
    write_simple_doc(os.path.join(HERE, "Figure_and_Table_Legends.docx"), "Legends", legends(blocks))
    unverified = [k for k in numberer.order if REFS[k][1] == "verify"]
    print(f"Manuscript: {len(numberer.order)} references ({len(unverified)} need completion: {', '.join(unverified)})")


if __name__ == "__main__":
    main()
