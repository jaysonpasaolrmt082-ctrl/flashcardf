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


def manuscript_blocks():
    inv = inventory()
    pooled = {r["outcome"]: r for r in pooled_rows()}
    B = []
    h1 = lambda t: B.append(("h1", t)); h2 = lambda t: B.append(("h2", t)); h3 = lambda t: B.append(("h3", t))
    p = lambda t: B.append(("p", t))

    # ---------------------------------------------------------- title page --
    B.append(("title", "Defining Schistosomiasis-Associated Colorectal Cancer: A Systematic Analysis and Meta-analysis of Clinicopathological, Molecular, and Prognostic Features"))
    p("Jayson Cagadas Pasaol, DVM, PhD,¹ [Co-author names and degrees TO BE ADDED]")
    p("¹[Department, Institution, City, Country TO BE ADDED]")
    p("Corresponding author: Jayson Cagadas Pasaol, DVM, PhD; [postal address TO BE ADDED]; email: jaysonpasaolrmt082@gmail.com; ORCID: [TO BE ADDED]")
    p("Running title: Schistosomiasis-associated colorectal cancer phenotype")
    p("Word count: abstract [TO BE CALCULATED]; main text [TO BE CALCULATED]. Tables: 5. Figures: 8. Supplementary tables: 6.")
    p("Keywords: Schistosoma japonicum; schistosomiasis; colorectal neoplasms; prognosis; neoplasm staging; meta-analysis")
    B.append(("pb",))

    # ------------------------------------------------------------- abstract --
    h1("ABSTRACT")
    p("**Background and Objective.** Schistosoma japonicum infection has long been linked to colorectal cancer in endemic Asia, but whether schistosomiasis-associated colorectal cancer (SACC) is a reproducibly distinct clinical entity is unresolved. This study aimed to systematically quantify the clinicopathological, molecular, and prognostic differences between SACC and non-schistosomiasis-associated colorectal cancer (NSACC) and to determine whether the available evidence supports a distinct schistosomal colorectal cancer phenotype.")
    p("**Methods.** MEDLINE/PubMed, Scopus, Web of Science Core Collection, Embase, CNKI, Wanfang, and SinoMed were searched from inception to [SEARCH DATE TO BE ADDED], supplemented by citation searching, without language restriction. Observational studies comparing SACC with NSACC were eligible; SACC-only cohorts contributed to a separate within-SACC prognostic analysis. Two reviewers independently screened records, extracted data, and assessed study quality with the Newcastle-Ottawa Scale. Overlapping cohorts were identified and each patient was counted once per outcome. Odds ratios (OR), mean differences, and hazard ratios (HR) were pooled with random-effects models (restricted maximum likelihood). Species were analysed separately. Certainty of evidence was rated with GRADE.")
    p("**Results.** [TO BE CALCULATED] records were screened and [TO BE CALCULATED] studies ([TO BE CALCULATED] independent cohorts; [TO BE CALCULATED] SACC and [TO BE CALCULATED] NSACC patients) were included. Compared with NSACC, SACC was associated with overall survival HR [TO BE CALCULATED] (95% CI [TO BE CALCULATED]; I² [TO BE CALCULATED]), disease-free survival HR [TO BE CALCULATED], stage III-IV disease OR [TO BE CALCULATED], lymph-node metastasis OR [TO BE CALCULATED], and distant metastasis OR [TO BE CALCULATED]. [Secondary findings and certainty ratings TO BE WRITTEN from verified results.]")
    p("**Conclusion.** [TO BE WRITTEN after analysis, using restrained wording; see Conclusion template.] Prospective molecularly characterised cohorts from contemporary endemic settings are needed to determine whether these clinical differences reflect a biologically distinct form of colorectal carcinogenesis.")
    p("**Registration.** [PROSPERO/OSF registration number TO BE ADDED, or a statement that the protocol was not registered.]")
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
    p("This systematic analysis and meta-analysis of observational studies is reported according to PRISMA 2020{c:page2021} and, for the literature search, PRISMA-S.{c:rethlefsen2021} The completed PRISMA 2020 checklist is provided in the Supplementary Material. The review question was framed as: among patients with colorectal cancer, does schistosomiasis define a distinct clinicopathological, molecular, and prognostic phenotype? It was not designed to estimate the prevalence of schistosomiasis among patients with CRC or the risk of CRC after infection.")
    h2("Protocol and registration")
    p("The protocol, including eligibility criteria, outcomes, and analysis plan, was [registered in PROSPERO (CRDXXXXXXXXX) on DD Month YYYY / deposited on the Open Science Framework (doi:XXXX) on DD Month YYYY] before full-text data extraction. [Deviations from the protocol TO BE LISTED, or state 'There were no deviations from the protocol.']")
    h2("Eligibility criteria")
    p("Eligibility followed a PECO framework. Population: adults with histologically or clinically confirmed colorectal adenocarcinoma or carcinoma. Exposure: current or previous intestinal schistosomiasis, ascertained by histological identification of schistosome eggs, pathology report, documented history, stool microscopy, serology, molecular testing, or a validated clinical diagnosis; the exact method used by each study was recorded. Comparator: patients with CRC without evidence, history, or pathological findings of schistosomiasis. Outcomes: clinicopathological, molecular, laboratory, and prognostic characteristics (see Outcome definitions).")
    p("We included retrospective or prospective cohorts, case-control studies, and comparative pathological series that reported extractable data for at least one outcome in patients with SACC and NSACC. Cohorts of SACC only were included solely in a separate within-SACC prognostic analysis and were never combined with the comparative analysis. We excluded case reports, case series without relevant comparative information, animal and in vitro studies, editorials, commentaries, narrative and systematic reviews (used only to identify primary studies), studies in which CRC could not be separated from other cancers or schistosomiasis status could not be determined, and duplicate reports of the same population for the same outcome. Population-based studies of CRC risk after schistosomiasis were catalogued separately and not combined with the phenotype analyses. No language restriction was applied; Chinese-language reports were assessed by a reviewer fluent in Chinese [NAME/INITIALS TO BE ADDED].")
    h2("Information sources")
    p("We searched MEDLINE (PubMed), Scopus, Web of Science Core Collection, Embase [if accessible: TO BE CONFIRMED], and the Chinese databases CNKI, Wanfang Data, and SinoMed from inception to [SEARCH DATE TO BE ADDED]. Reference lists of included studies and of major reviews were screened, forward citation searching was performed for included studies, and Google Scholar was used only for citation chasing.")
    h2("Search strategy")
    p("The search combined controlled vocabulary and free-text terms for schistosomiasis (\"Schistosoma japonicum\"[MeSH], schistosomiasis, schistosomal, schistosoma, bilharzia, bilharziasis) with terms for colorectal neoplasms (\"Colorectal Neoplasms\"[MeSH], colorectal, colon, colonic, and rectal cancer, carcinoma, or neoplasm). Outcome terms such as survival or prognosis were deliberately not required, to avoid missing comparative studies that report these outcomes only in the full text. Complete database-specific strategies, platforms, dates, and numbers retrieved are reported in Supplementary Table S1. Records were deduplicated in [EndNote/Zotero/Rayyan, version TO BE ADDED] and checked manually.")
    h2("Study selection")
    p("Two reviewers ([INITIALS]) independently screened titles and abstracts and then full texts against the eligibility criteria. Disagreements were resolved by discussion or by a third reviewer ([INITIALS]). One principal reason was recorded for every excluded full text (Supplementary Table S2).")
    h2("Data extraction")
    p("Two reviewers independently extracted data into a piloted spreadsheet (Supplementary Table S3) covering study identification (authors, year, PMID, DOI, institution, city, province, department), design and recruitment period, schistosomiasis ascertainment (species, diagnostic method, verbatim definition), patient numbers, demographics, tumour location, pathology, stage, metastasis, molecular and laboratory markers, and survival estimates. Each value was labelled by origin: reported directly; calculated from reported raw data; estimated from Kaplan-Meier curves; or pooled. When studies reported medians with interquartile ranges, means and standard deviations were estimated with the method of Wan et al.{c:wan2014} and the transformation was recorded. Study authors were contacted for missing data [TO BE CONFIRMED].")
    p("For survival, the extraction priority was: (1) multivariable-adjusted HR with 95% confidence interval (CI); (2) unadjusted HR; (3) HR derived from reported survival statistics with the methods of Tierney et al.;{c:tierney2007} and (4) HR reconstructed from Kaplan-Meier curves with the algorithm of Guyot et al.{c:guyot2012} All HRs were expressed as SACC versus NSACC. Adjusted and unadjusted estimates were analysed separately.")
    h2("Outcome definitions")
    p("Primary outcomes were overall survival (HR), disease-free or recurrence-free survival (HR), advanced stage (stage III-IV versus I-II; OR), lymph-node metastasis (OR), and distant metastasis (OR). Secondary outcomes were age (mean difference in years) and age over 60 years; male sex; tumour location (rectum versus colon, sigmoid colon, right- versus left-sided); tumour size; differentiation; mucinous and signet-ring-cell histology; multiple primary or synchronous tumours; concomitant polyps; lymphovascular, vascular, and perineural invasion; tumour budding; positive margins; molecular alterations (KRAS, NRAS, BRAF, TP53, APC, PIK3CA, microsatellite instability, mismatch-repair proteins, beta-catenin, p53 immunohistochemistry, Ki-67, and any other reported marker); laboratory markers (CEA, CA19-9, haemoglobin, leukocyte and platelet counts, inflammatory indices); and recurrence. Laboratory outcomes were exploratory.")
    h2("Assessment of study quality and risk of bias")
    p("Two reviewers independently assessed each comparative study with the Newcastle-Ottawa Scale (NOS) for cohort studies,{c:wells_nos} chosen before data extraction and applied unchanged to all studies. The comparability item was awarded when analyses accounted for stage and at least one of age or sex. Studies with 7-9 stars were rated as low, 5-6 as moderate, and 0-4 as high risk of bias. Results are summarised in Table S4 and in a risk-of-bias figure.")
    h2("Management of overlapping cohorts")
    p("For every report we recorded hospital, city, province, department, recruitment period, authors, and patient numbers, and constructed an overlap matrix (Supplementary Table S6). Reports from the same institution with overlapping recruitment periods or shared author groups were treated as potentially overlapping. For each outcome, only the largest or most complete report from an overlap group was included; a second report from the same group contributed only to outcomes absent from the first. The analysis code rejects any outcome that contains two reports from the same overlap group.")
    h2("Statistical analysis")
    p("ORs were computed from 2x2 tables, with 0.5 added to all cells of tables containing a zero cell. Log HRs and their standard errors were derived from the reported HR and 95% CI as SE = [ln(upper) - ln(lower)]/(2 x 1.96). Random-effects models with restricted maximum likelihood estimation of between-study variance (tau²) were used for all pooled analyses; fixed-effect (common-effect) estimates are reported only as a sensitivity analysis. For each outcome we report the pooled estimate, 95% CI, P value, tau², I², and Cochran's Q.{c:higgins2002} Heterogeneity was interpreted using all of these statistics and the clinical diversity of the studies, not I² alone. An outcome was pooled only when at least two independent cohorts reported sufficiently comparable data; otherwise, results were tabulated. The primary analysis was restricted to S. japonicum (confirmed, or presumed from cohorts in S. japonicum-endemic regions); studies of S. mansoni, S. haematobium, or unidentified species were analysed separately. Analyses were performed in R version 4.3.3{c:rcore} with metafor version 4.4.0.{c:viechtbauer2010} The analysis code and the extraction dataset are available at [REPOSITORY URL/DOI TO BE ADDED].")
    h2("Subgroup analyses")
    p("Where at least two studies were available per subgroup, we compared histologically confirmed versus other definitions of schistosomiasis, S. japonicum-confirmed versus presumed species, colon versus rectal cancer, earlier versus contemporary cohorts (recruitment ending before versus from 2010), lower versus higher risk of bias, geographic region, and adjusted versus unadjusted survival estimates.")
    h2("Sensitivity analyses")
    p("Pre-specified sensitivity analyses were leave-one-out analysis; exclusion of studies at high risk of bias; exclusion of potentially overlapping cohorts; restriction to histology-confirmed SACC; restriction to S. japonicum-confirmed studies; fixed-effect models; and exclusion of the largest cohort, to determine whether a single study of more than 31,000 patients{c:zheng2023} dominated any pooled estimate.")
    h2("Assessment of small-study effects")
    p("Funnel plots and Egger's regression test{c:egger1997} were planned only for outcomes with at least 10 studies, in line with published recommendations.{c:sterne2011}")
    h2("Certainty of evidence")
    p("Two reviewers rated the certainty of evidence for overall survival, disease-free or recurrence-free survival, advanced stage, lymph-node metastasis, and distant metastasis using GRADE.{c:guyatt2008} Evidence from observational studies started at low certainty and was rated down for risk of bias, inconsistency, indirectness, imprecision, and suspected publication bias, or up when criteria for a large effect or dose-response were met.")
    h2("Ethics")
    p("This study used published, de-identified, aggregate data and did not require ethics review or informed consent.")

    # -------------------------------------------------------------- results --
    h1("RESULTS")
    h2("Search results")
    p("The database searches identified [TO BE CALCULATED] records and other sources [TO BE CALCULATED]. After removal of [TO BE CALCULATED] duplicates, [TO BE CALCULATED] records were screened and [TO BE CALCULATED] full texts were assessed. [TO BE CALCULATED] studies met the eligibility criteria: [TO BE CALCULATED] in the primary comparative analysis, [TO BE CALCULATED] in the within-SACC analysis, and [TO BE CALCULATED] in quantitative synthesis (Figure 1). Excluded full texts and reasons are listed in Supplementary Table S2.")
    B.append(("fig", {"file": "Figure1_PRISMA_flow.png", "w": 15.0,
                      "cap": "**Figure 1.** PRISMA 2020 flow diagram of study selection. Record counts are entered from verified screening logs."}))
    h2("Characteristics of included studies")
    p("Table 1 summarises the reports identified. [Description of study designs, countries/provinces, recruitment periods, sample sizes, and follow-up TO BE WRITTEN after full-text verification.] Reports from the same institutions were grouped into overlap groups (Supplementary Table S6); the number of independent cohorts was [TO BE CALCULATED]. Figure 2 shows the chronological landscape of the evidence.")
    B.append(("table", table1(inv)))
    B.append(("fig", {"file": "Figure2_landscape_timeline.png", "w": 16.0,
                      "cap": "**Figure 2.** Chronological landscape of identified studies. Bars show recruitment periods where reported; diamonds show publication year. Right column: SACC/NSACC sample sizes (NR, not reported; dash, SACC-only cohort). Labels give city/province."}))
    h2("Schistosomiasis ascertainment")
    p("[TO BE WRITTEN: number of studies using histological egg identification, documented history, serology, stool examination, or combinations; number confirming S. japonicum versus presuming species from endemicity.]")
    h2("Demographic characteristics")
    p(pooled_sentence(pooled, "Male sex", "male sex") + " " + pooled_sentence(pooled, "age", "age (mean difference, years)", md=True))
    h2("Anatomical distribution")
    p(pooled_sentence(pooled, "Rectal location", "rectal location") + " [Sigmoid, right- versus left-sided location TO BE REPORTED.]")
    h2("Pathological characteristics")
    p("[Differentiation, mucinous and signet-ring histology, vascular, lymphovascular and perineural invasion, tumour budding, multiple primary tumours, concomitant polyps, and margins TO BE REPORTED from Table 2 and Figure 3.]")
    B.append(("table", table2(inv)))
    h2("Tumour stage and metastatic behaviour")
    p(pooled_sentence(pooled, "Stage III-IV", "stage III-IV disease") + " " + pooled_sentence(pooled, "Lymph-node metastasis", "lymph-node metastasis") + " " + pooled_sentence(pooled, "Distant metastasis", "distant metastasis"))
    B.append(("fig", {"file": "Figure3_phenotype_forest.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 3.** Clinicopathological phenotype of SACC versus NSACC: pooled odds ratios (random effects, REML) with 95% confidence intervals for each outcome with at least two independent cohorts. Red, primary outcomes; blue, secondary outcomes. Study-level forest plots are provided in the Supplementary Material."}))
    h2("Molecular characteristics")
    p("[TO BE WRITTEN from Table 3.] Molecular data were sparse. Reports identified at the screening stage addressed KRAS mutation,{c:li2024,zheng2023} c-MYC amplification,{c:pan2020} whole-exome sequencing of 30 SACC tumours against an external sporadic-CRC reference,{c:genomic2023} immune-cell infiltration and PD-L1,{c:wangw2021,wangw2023,bmcgastro2023} and, in S. mansoni-associated CRC, p53 immunohistochemistry and mismatch-repair proteins.{c:madbouly2007} Biomarkers were pooled only when at least two comparable internal-comparator studies were available.")
    B.append(("table", table3()))
    B.append(("fig", {"file": "Figure6_molecular.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 6.** Molecular phenotype. Pooled odds ratios for biomarkers reported by at least two comparable studies, and evidence map for biomarkers that could not be pooled."}))
    h2("Overall survival")
    p(pooled_sentence(pooled, "OS - Adjusted", "overall survival (multivariable-adjusted HRs)", hr=True) + " " + pooled_sentence(pooled, "OS - Unadjusted", "overall survival (unadjusted or derived HRs)", hr=True))
    B.append(("fig", {"file": "Figure4_OS_forest.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 4.** Overall survival in SACC versus NSACC. Hazard ratios with 95% CI; multivariable-adjusted and unadjusted/derived estimates are pooled separately. Source column: P1, adjusted HR reported; P2, unadjusted HR reported; P3, derived from survival statistics; P4, reconstructed from Kaplan-Meier curves."}))
    h2("Disease-free and recurrence-free survival")
    p(pooled_sentence(pooled, "DFS - Adjusted", "disease-free survival (adjusted)", hr=True) + " " + pooled_sentence(pooled, "DFS - Unadjusted", "disease-free survival (unadjusted)", hr=True))
    B.append(("fig", {"file": "Figure5_DFS_forest.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 5.** Disease-free/recurrence-free survival in SACC versus NSACC (hazard ratios, random effects)."}))
    h2("Within-SACC prognostic factors")
    p("[TO BE WRITTEN from Table 5.] SACC-only cohorts examined the site of egg deposition,{c:wangm2016} eggs in regional lymph nodes and coexisting hepatic schistosomiasis in stage III disease,{c:pan2023} and c-MYC amplification.{c:pan2020} These data are reported separately from the comparative analysis.")
    B.append(("table", table5()))
    h2("Risk of bias")
    p("[TO BE WRITTEN: distribution of NOS ratings; most frequent limitations, e.g., comparability and ascertainment of exposure.] Ratings are given in Supplementary Table S4.")
    h2("Sensitivity and subgroup analyses")
    p("[TO BE WRITTEN from Supplementary Table S5, including the analysis excluding the Shanghai cohort of 31,153 patients.]")
    h2("Certainty of evidence and overall phenotype")
    p("Table 4 summarises all pooled analyses with GRADE ratings. Figure 7 shows, study by study, the reported direction of each feature, including features that could not be pooled. Table 6 integrates these results into a phenotype matrix.")
    B.append(("table", table4(pooled)))
    B.append(("fig", {"file": "Figure7_evidence_heatmap.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 7.** Evidence heat map. For each study (columns) and feature (rows), the reported direction in SACC relative to NSACC: higher, lower, no significant difference, or not reported."}))
    B.append(("table", table6()))

    # ----------------------------------------------------------- discussion --
    h1("DISCUSSION")
    h2("Principal findings")
    p("[TO BE WRITTEN after analysis. Answer directly: does SACC appear phenotypically distinct, for which features, and with what certainty? Use 'associated with', 'more frequently observed', 'pooled evidence suggests'.]")
    h2("Clinical interpretation")
    p("[TO BE WRITTEN: age, sex, tumour location, stage, metastasis, pathology, survival. Interpret survival in light of the separation of adjusted and unadjusted estimates and of the result excluding the largest cohort.]")
    h2("Molecular interpretation")
    p("The molecular evidence base is narrow. At the screening stage, KRAS data came from two cohorts with different assays,{c:li2024,zheng2023} exome data from 30 tumours compared with an external reference,{c:genomic2023} and p53 and mismatch-repair data from a single S. mansoni series that cannot be extrapolated to S. japonicum.{c:madbouly2007} [TO BE WRITTEN with pooled results.] Unless consistent differences are found across several independent cohorts, these data do not support a defined molecular signature of SACC.")
    h2("Biological plausibility")
    p("Several mechanisms could link chronic intestinal schistosomiasis to a distinct form of CRC, but they should be distinguished by the strength of evidence (Figure 8). Egg deposition in the colorectal wall and the resulting granulomatous inflammation and fibrosis are established histopathological features of infection.{c:iarc61,hamid2019} Experimental work suggests that S. japonicum soluble egg antigen activates MAPK and PI3K-AKT signalling and inhibits autophagy in CRC models,{c:sea2025} and that intestinal tumour-associated macrophage polarisation influences schistosomal CRC development.{c:tam2021} Schistosoma mansoni eggs have been shown to activate Wnt/beta-catenin signalling and c-Jun in human and hamster colon,{c:wnt2020} but this concerns a different species. In patients, immune-cell infiltrates and PD-L1 expression appear to carry different prognostic value according to schistosomiasis status,{c:wangw2021,wangw2023,bmcgastro2023} and eggs in regional lymph nodes have been associated with poorer disease-free survival in stage III SACC.{c:pan2023} Other plausible pathways, including oxidative and nitrosative DNA damage, NF-kB and IL-6/STAT3 signalling, and microbiome change, have not, to our knowledge, been demonstrated specifically in human SACC and remain hypotheses. None of these observations establishes that S. japonicum causes CRC.")
    B.append(("fig", {"file": "Figure8_conceptual_model.png", "w": 16.0,
                      "cap": "**Figure 8.** Conceptual model of how chronic S. japonicum infection might relate to colorectal carcinogenesis and a possible SACC phenotype. Solid arrows: established histopathology. Dashed black arrows: hypothesised steps not confirmed in human SACC. Grey boxes: supporting observations with the type of evidence stated; numbers are references. The figure does not imply that S. japonicum causes CRC.{c:iarc61,hamid2019,pan2023,tam2021,wangw2021,wangw2023,bmcgastro2023,sea2025,wnt2020,genomic2023,li2024,pan2020}"}))
    h2("Comparison with previous literature")
    p("Earlier descriptions of SACC as a distinct subtype were based on narrative reviews and single-centre series.{c:hamid2019,hamid2010,actapara2023} A recent meta-analysis pooled the prevalence of intestinal parasitic infection among patients with CRC and its association with CRC,{c:global_ipi2025} which addresses frequency and risk rather than the characteristics of cancers that have arisen. The present analysis differs in asking, among patients who already have CRC, whether schistosomiasis is associated with a different clinicopathological, molecular, and prognostic profile; in separating species, adjusted and unadjusted survival estimates, and SACC-only cohorts; and in explicitly managing overlap among reports from the same institutions. [TO BE COMPLETED: state whether any previous quantitative synthesis of this question was found by the final search; do not claim primacy unless confirmed.]")
    h2("Implications for endemic countries")
    p("Most comparative cohorts came from China. No comparative cohort from the Philippines or Indonesia was identified at the screening stage [TO BE CONFIRMED by the final search], although both countries remain endemic.{c:gordon2015,indo2026} The findings therefore may not transfer directly to these settings. [TO BE WRITTEN after analysis: implications for pathological recognition of schistosome eggs in resection specimens and for recording schistosomiasis history in cancer registries.] These data do not, by themselves, justify changes to CRC screening policy.")
    h2("Research implications")
    p("The evidence calls for prospective cohorts in which schistosomiasis is ascertained by standardised histological and serological criteria, tumours are profiled with contemporary genomic, transcriptomic, and immune assays against internal comparators, and outcomes are analysed with adjustment for stage and treatment. Patient-derived samples and experimental models are needed to test the hypothesised mechanisms. Studies from endemic settings outside China, particularly the Philippines and Indonesia, are a priority.")
    h2("Limitations")
    p("This analysis has several limitations. The evidence is predominantly retrospective and geographically concentrated in China, and several reports appear to come from the same institutions and patient populations; although overlap was managed explicitly, undetected overlap cannot be excluded. Definitions of schistosomiasis ranged from histological identification of eggs to documented history, which may misclassify exposure. Cohorts span several decades with different staging systems and treatment eras. Survival estimates were adjusted for different covariates or not adjusted at all, and confounding by age, stage, and comorbidity is likely. Molecular data were limited, and few studies contributed to some endpoints, which limits precision and precluded formal assessment of small-study effects for most outcomes. Finally, as for any synthesis of observational data, the associations reported here cannot establish causality.")

    # ----------------------------------------------------------- conclusion --
    h1("CONCLUSION")
    p("The available evidence indicates that schistosomiasis-associated colorectal cancer may exhibit a measurable clinicopathological phenotype distinct from non-schistosomal colorectal cancer; however, the magnitude and consistency of these differences vary across outcomes. [The most strongly supported pooled characteristics TO BE STATED from Table 4 and Table 6.] Prospective molecularly characterised cohorts from contemporary endemic settings are needed to determine whether these clinical differences reflect a biologically distinct form of colorectal carcinogenesis.")

    h1("Acknowledgments")
    p("[TO BE ADDED]")
    h1("Statement of Authorship")
    p("[TO BE ADDED, e.g., CRediT roles: conceptualisation, methodology, investigation (screening and extraction), formal analysis, writing - original draft, writing - review and editing; all authors approved the final version.]")
    h1("Author Disclosure")
    p("[TO BE ADDED: conflicts of interest for each author.]")
    h1("Funding Source")
    p("[TO BE ADDED, or 'This study received no specific funding.']")
    h1("Use of AI-assisted Tools")
    p("[AUTHOR DECISION: describe any use of AI-assisted tools in search design, coding, or drafting, as required by the journal's current policy. The authors take full responsibility for the content.]")
    h1("Data Availability")
    p("The extraction dataset, analysis code (R/metafor), and figure scripts are available at [REPOSITORY URL/DOI TO BE ADDED].")
    h1("REFERENCES")
    B.append(("refs",))
    return B


# ================================================================ helpers =====
def fmt(x, d=2):
    try:
        return f"{float(x):.{d}f}"
    except (TypeError, ValueError):
        return TBC


def pooled_sentence(pooled, key, label, hr=False, md=False):
    r = pooled.get(key)
    if not r:
        return f"For {label}, the pooled estimate was {TBC} (95% CI {TBC}; {TBC} studies; I² {TBC}; tau² {TBC})."
    m = "MD" if md else ("HR" if hr else "OR")
    return (f"For {label}, the pooled {m} was {fmt(r['estimate'])} (95% CI {fmt(r['lower95'])}-{fmt(r['upper95'])}; "
            f"P = {fmt(r['p_value'], 3)}; {r['k']} studies; I² = {fmt(r['I2'], 0)}%; tau² = {fmt(r['tau2'], 3)}).")


def cite_tags(keys):
    return "{c:" + ",".join(keys) + "}"


REFKEY = {"Zheng2023": "zheng2023", "WangZ2020": "wangz2020", "WangW2020": "wangw2020", "WangW2021": "wangw2021",
          "WangW2023": "wangw2023", "Pan2020": "pan2020", "BMCGastro2023": "bmcgastro2023", "Li2024": "li2024",
          "Zhang2023": "zhang2023", "Zhu2024": "zhu2024", "WangM2014": "wangm2014", "NCG1986": "ncg1986",
          "Madbouly2007": "madbouly2007", "Yang2023": "yang2023", "WangM2016": "wangm2016", "Pan2023": "pan2023",
          "Liu2013": "liu2013", "Zhou_CT2012": "zhou_ct2012", "Genomic2023": "genomic2023"}


def short_name(r):
    a = r["first_author"]
    if a.startswith("["):
        a = r["study_id"].rstrip("0123456789_").replace("_CT", "")
    if a.startswith("National"):
        a = "NCG"
    return f"{a.split(' ')[0]} {r['year']}"


def table1(inv):
    order = ["Zheng2023", "WangZ2020", "WangW2020", "WangW2021", "WangW2023", "Pan2020", "BMCGastro2023", "Li2024",
             "Zhang2023", "Zhu2024", "WangM2014", "NCG1986", "Yang2023", "Madbouly2007", "WangM2016", "Pan2023",
             "Liu2013", "Zhou_CT2012", "Genomic2023"]
    rows = []
    for sid in order:
        r = inv[sid]
        nr = lambda v: "NR" if v in ("NR", "") else v
        rows.append([short_name(r) + cite_tags([REFKEY[sid]]), nr(r["city_province"]), nr(r["institution"]).split(" (")[0],
                     nr(r["recruitment_period"]), r["design"], nr(r["n_SACC"]),
                     nr(r["n_NSACC"]) if "Within" not in r["analysis_set"] else "-",
                     r["species"].replace(" (to verify)", "*").replace(" (endemic area; definition to verify)", "*").replace(" (presumed; verify)", "*"),
                     TBC.replace("CALCULATED", "EXTRACTED"), TBC.replace("CALCULATED", "EXTRACTED"),
                     r["outcomes_reported_in_abstract"].split(" (")[0][:90], r["overlap_group"].split("-")[0], r["analysis_set"].split(" (")[0].split(" -")[0]])
    return {"cap": "**Table 1.** Characteristics of identified studies",
            "head": ["Study", "Location", "Institution", "Study period", "Design", "SACC n", "NSACC n", "Species",
                     "Definition of schistosomiasis", "Follow-up", "Main outcomes", "Overlap group", "Analysis set"],
            "rows": rows, "font": 6.5, "landscape": True,
            "foot": "Values are from bibliographic records and published abstracts identified on 2026-10-05 and must be confirmed against full texts before submission. NR, not retrieved; *, species presumed from an S. japonicum-endemic setting, to be confirmed; overlap groups G1-G8 are defined in Supplementary Table S6."}


def table2(inv):
    feats = [("Age", "Age"), ("Sex", "sex"), ("Site", "site|rectum|location"), ("T stage", "pT|T stage|TNM"), ("LN", "LN|lymph|N stage"),
             ("Invasion", "invasion|thrombus"), ("Differentiation", "differentiation|mucinous"), ("Multiple/polyps", "multiple|polyp|synchronous"),
             ("Markers", "CA19|CEA|CA-125|WBC"), ("OS", "OS|survival"), ("DFS", "DFS")]
    rows = []
    for sid, r in inv.items():
        if not r["analysis_set"].startswith(("Primary", "Separate")):
            continue
        o = r["outcomes_reported_in_abstract"]
        rows.append([short_name(r) + cite_tags([REFKEY[sid]])] + ["A" if re.search(f, o, re.I) else "?" for _, f in feats])
    return {"cap": "**Table 2.** Clinicopathological outcomes available by study (screening stage)",
            "head": ["Study"] + [f for f, _ in feats], "rows": rows, "font": 7.5, "landscape": True,
            "foot": "A, outcome mentioned in the abstract; ?, availability to be determined from the full text. This table will be replaced by extracted SACC and NSACC counts (Supplementary Table S3) after full-text extraction."}


def table3():
    mol_out = os.path.join(OUT, "tables/Table3_molecular_evidence_map.csv")
    rows = [
        ["KRAS mutation", "Li 2024{c:li2024}; Zheng 2023{c:zheng2023}", TBC, TBC, "To be extracted", TBC, "Anti-EGFR eligibility; MAPK signalling", "Limited (2 cohorts, assays differ)"],
        ["c-MYC amplification", "Pan 2020{c:pan2020}", TBC, TBC, "Prognostic within SACC only (abstract)", "Not poolable (k = 1)", "Oncogene; proliferation", "Limited (single cohort)"],
        ["TMB / exome", "Genomic 2023{c:genomic2023}", "30", "External", "Lower TMB; MSS/MSI-L (abstract)", "Not poolable (external comparator)", "Immunotherapy responsiveness", "Very limited"],
        ["MSI / MMR (MLH1, MSH2)", "Madbouly 2007{c:madbouly2007} (S. mansoni)", "40", "20", "To be extracted", "Not poolable (other species)", "DNA mismatch repair", "Very limited; species differs"],
        ["p53 IHC", "Madbouly 2007{c:madbouly2007} (S. mansoni)", "40", "20", "To be extracted", "Not poolable (other species)", "Genome maintenance", "Very limited; species differs"],
        ["CD3/CD8/CD4 TILs, PD-L1, CRP", "Wang 2021{c:wangw2021}; Wang 2023{c:wangw2023}; BMC Gastroenterol 2023{c:bmcgastro2023}", TBC, TBC, "To be extracted", "One overlap group (G3): not poolable", "Tumour immune microenvironment", "Limited (single institution)"],
        ["NRAS, BRAF, TP53 mutation, APC, PIK3CA, beta-catenin, Ki-67", "None identified at screening", "-", "-", "-", "-", "-", "No evidence"],
    ]
    return {"cap": "**Table 3.** Molecular evidence map for SACC versus NSACC",
            "head": ["Biomarker", "Studies", "SACC n", "NSACC n", "Direction", "Pooled effect", "Biological relevance", "Evidence strength"],
            "rows": rows, "font": 7.5, "landscape": True,
            "foot": "Screening-stage map; sample sizes and directions are to be verified from full texts. Pooled effects are computed only for biomarkers with at least two comparable internal-comparator studies." +
                    (" Updated pooled results: output/tables/Table3_molecular_evidence_map.csv." if os.path.exists(mol_out) else "")}


def table4(pooled):
    order = [("OS - Adjusted", "Overall survival (adjusted)", "HR"), ("OS - Unadjusted", "Overall survival (unadjusted)", "HR"),
             ("DFS - Adjusted", "DFS/RFS (adjusted)", "HR"), ("DFS - Unadjusted", "DFS/RFS (unadjusted)", "HR"),
             ("Stage III-IV", "Stage III-IV", "OR"), ("Lymph-node metastasis", "Lymph-node metastasis", "OR"),
             ("Distant metastasis", "Distant metastasis", "OR"), ("Male sex", "Male sex", "OR"), ("age", "Age, years", "MD"),
             ("Rectal location", "Rectal location", "OR"), ("Vascular invasion", "Vascular invasion", "OR"),
             ("Perineural invasion", "Perineural invasion", "OR"), ("Mucinous histology", "Mucinous histology", "OR"),
             ("Poor differentiation", "Poor differentiation", "OR"), ("KRAS mutation", "KRAS mutation", "OR")]
    rows = []
    for key, lab, m in order:
        r = pooled.get(key)
        if r:
            rows.append([lab, r["k"], r["n_SACC"], r["n_NSACC"], m, fmt(r["estimate"]), f"{fmt(r['lower95'])}-{fmt(r['upper95'])}",
                         f"{fmt(r['I2'], 0)}%", fmt(r["tau2"], 3), fmt(r["p_value"], 3), "[TO BE ASSESSED]"])
        else:
            rows.append([lab, TBC, TBC, TBC, m, TBC, TBC, TBC, TBC, TBC, "[TO BE ASSESSED]"])
    return {"cap": "**Table 4.** Summary of meta-analyses: SACC versus NSACC",
            "head": ["Outcome", "Studies", "SACC n", "NSACC n", "Measure", "Pooled effect", "95% CI", "I²", "tau²", "P value", "GRADE certainty"],
            "rows": rows, "font": 7.5, "landscape": True,
            "foot": "Random-effects models with REML estimation. HR > 1 and OR > 1 indicate higher hazard or higher odds in SACC. Rows are filled automatically from output/tables/Table4_meta_analysis_summary.csv; outcomes with fewer than two independent cohorts are reported narratively."}


def table5():
    rows = [["Egg deposition site", "Wang 2016{c:wangm2016}", "OS", TBC, "Associated with OS in univariable but not multivariable analysis (abstract)", TBC],
            ["Eggs in regional lymph nodes (stage III)", "Pan 2023{c:pan2023}", "DFS; OS", TBC, "Independent factor for DFS (abstract)", TBC],
            ["Hepatic schistosomiasis (stage III)", "Pan 2023{c:pan2023}", "DFS; OS", TBC, "Independent factor for DFS and OS (abstract)", TBC],
            ["CEA level", "Wang 2016{c:wangm2016}", "OS", TBC, "Independent factor for OS (abstract)", TBC],
            ["pT stage", "Wang 2016{c:wangm2016}", "OS", TBC, "Independent factor for OS (abstract)", TBC],
            ["c-MYC amplification", "Pan 2020{c:pan2020}", "OS", TBC, "Independent poor-prognosis factor in SACC (abstract)", TBC],
            ["CD8+ TIL density", "Wang 2021{c:wangw2021}", "OS", TBC, "Independent factor in SACC (abstract)", TBC]]
    return {"cap": "**Table 5.** Within-SACC prognostic factors",
            "head": ["Factor", "Study", "Outcome", "HR (95% CI)", "Reported finding", "Adjusted for"],
            "rows": rows, "font": 7.5, "landscape": True,
            "foot": "SACC-only analyses; not combined with the SACC-versus-NSACC comparison. 'Reported finding' paraphrases the published abstract and must be checked against the full text; HRs are to be extracted."}


def table6():
    feats = ["Older age", "Male sex", "Rectal localisation", "Advanced stage", "Lymph-node metastasis", "Distant metastasis",
             "Vascular invasion", "Mucinous histology", "Multiple primary CRC", "KRAS mutation", "Overall survival", "DFS/RFS"]
    return {"cap": "**Table 6.** Phenotype matrix: is SACC distinct?",
            "head": ["Feature", "Pooled direction (up / down / neutral; better / worse for survival)", "Strength of evidence (strong / moderate / limited / inconsistent)"],
            "rows": [[f, "[TO BE COMPLETED after analysis]", "[TO BE COMPLETED after analysis]"] for f in feats], "font": 8, "landscape": False,
            "foot": "Strong: >= 3 independent cohorts, consistent direction, low-moderate risk of bias, moderate/high GRADE. Moderate: >= 2 cohorts, consistent direction, low GRADE. Limited: single cohort or imprecise pooled estimate. Inconsistent: cohorts disagree in direction."}


# ============================================================== rendering =====
ITALIC = re.compile(r"(Schistosoma japonicum|Schistosoma haematobium|Schistosoma mansoni|S\. japonicum|S\. mansoni|S\. haematobium|\bet al\.)")
HILITE = re.compile(r"(\[[^\]]*(?:TO BE|to be|TBC|to verify|AUTHOR DECISION|SEARCH DATE|INITIALS|NAME|REPOSITORY|PROSPERO|DD Month|if accessible|EndNote)[^\]]*\])")


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
        "rows": [[d, pl, q, "Inception to search date", "[SEARCH DATE TO BE ADDED]", TBC, "None (no language or date limits)"] for d, pl, q in SEARCHES],
        "foot": "Deduplication: [software and version TO BE ADDED], followed by manual check of author, year, title, and DOI. Searches were not peer-reviewed with PRESS [or: were peer-reviewed by NAME TO BE ADDED]."}))
    B.append(("h1", "Supplementary Table S2. Full texts excluded, with reasons"))
    B.append(("table", {"cap": "**Table S2.** Excluded full-text reports", "font": 8,
        "head": ["Study", "PMID / DOI", "Principal reason for exclusion"],
        "rows": [["Liu 2013{c:liu2013}", "24083755 / 10.7314/APJCP.2013.14.8.4839", "Provisional: no non-schistosomal comparator identified (case series); retained for within-SACC description only - confirm on full text"],
                 ["Zhou 2012 (CT){c:zhou_ct2012}", "22658847", "Provisional: SACC-only imaging-pathology study; no NSACC comparator"],
                 [TBC, TBC, "[Remaining exclusions TO BE ADDED from screening log]"]],
        "foot": "One principal reason per report, in the hierarchy: not CRC; not human; no schistosomiasis status; no comparator; no extractable outcome; duplicate cohort for the same outcome."}))
    B.append(("h1", "Supplementary Table S3. Complete extraction data"))
    B.append(("p", "Provided as the Excel workbook SACC_master_extraction.xlsx (sheets: master_wide, binary_outcomes, continuous_outcomes, survival_outcomes, within_sacc_prognostic, molecular_evidence, evidence_direction, rob_nos, inventory, overlap). Every value records its origin (reported, calculated from raw data, Kaplan-Meier-reconstructed, converted from median/IQR) and its source location in the original report."))
    B.append(("h1", "Supplementary Table S4. Risk-of-bias assessments"))
    B.append(("table", {"cap": "**Table S4.** Newcastle-Ottawa Scale assessments", "font": 8,
        "head": ["Study", "Selection (0-4)", "Comparability (0-2)", "Outcome/exposure (0-3)", "Total (0-9)", "Overall risk of bias"],
        "rows": [[f"{n}{{c:{k}}}", TBC.replace("CALCULATED", "ASSESSED")] + [TBC.replace("CALCULATED", "ASSESSED")] * 4
                 for n, k in [("Zheng 2023", "zheng2023"), ("Wang Z 2020", "wangz2020"), ("Wang W 2020", "wangw2020"), ("Li 2024", "li2024"),
                              ("Zhang 2023", "zhang2023"), ("Zhu 2024", "zhu2024"), ("Wang M 2014", "wangm2014"), ("NCG 1986", "ncg1986"),
                              ("Madbouly 2007", "madbouly2007")]],
        "foot": "Two independent assessors; disagreements resolved by consensus. Low risk: 7-9 stars; moderate: 5-6; high: 0-4."}))
    B.append(("h1", "Supplementary Table S5. Sensitivity analyses"))
    B.append(("p", "Generated by R/run_all.R as output/tables/TableS5_sensitivity.csv: leave-one-out; excluding the largest cohort; excluding high risk of bias; histology-confirmed SACC only; S. japonicum-confirmed only; fixed-effect estimates. [TABLE TO BE INSERTED from verified analysis output.]"))
    B.append(("h1", "Supplementary Table S6. Potentially overlapping cohorts and decisions"))
    ov = list(csv.reader(open(os.path.join(ROOT, "data/overlap_matrix.csv"))))
    B.append(("table", {"cap": "**Table S6.** Overlap matrix", "font": 7.5, "landscape": True,
        "head": ["Study", "Hospital", "Recruitment dates", "SACC n", "NSACC n", "Potential overlap", "Decision"],
        "rows": ov[1:], "foot": "Groups: G1 Changhai (Shanghai); G2 Yijishan (Wuhu); G3 Qingpu Branch of Zhongshan Hospital (Shanghai); G4 Union Hospital (Wuhan); G5 Jingzhou (Hubei); G6 West China Hospital (Chengdu); G7 national cooperative group; G8 Alexandria. Institution and period for each report are to be confirmed from the full text."}))
    B.append(("h1", "PRISMA 2020 checklist"))
    B.append(("table", {"cap": "**PRISMA 2020 checklist** (location in manuscript)", "font": 8,
        "head": ["Section/item", "Location"], "rows": PRISMA, "foot": "Page numbers to be added after typesetting."}))
    B.append(("h1", "Supplementary figures"))
    B.append(("p", "Study-level forest plots for each pooled outcome (output/figures/Fig_forest_<outcome>.pdf) and funnel plots for outcomes with at least 10 studies will be inserted here from the verified analysis. [TO BE INSERTED]"))
    B.append(("h1", "References cited in the Supplementary Material"))
    B.append(("refs",))
    return B


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
    return ["[Date]", "The Editor-in-Chief\nActa Medica Philippina\nUniversity of the Philippines Manila",
            "Dear Editor,",
            "We submit the manuscript \"Defining Schistosomiasis-Associated Colorectal Cancer: A Systematic Analysis and Meta-analysis of Clinicopathological, Molecular, and Prognostic Features\" for consideration as an Original Article.",
            "Schistosoma japonicum remains endemic in the Philippines, yet it is unclear whether colorectal cancers arising in patients with schistosomiasis behave differently from other colorectal cancers. Our study synthesises the comparative evidence on demographic, pathological, molecular, and survival features of schistosomiasis-associated colorectal cancer, with explicit handling of overlapping hospital cohorts and separation of adjusted and unadjusted survival estimates. [Principal findings TO BE ADDED in one or two sentences after analysis.]",
            "The findings are relevant to pathologists, surgeons, and oncologists in endemic regions of the Philippines, and the analysis identifies the absence of Philippine comparative cohorts as a research priority.",
            "This manuscript has not been published and is not under consideration elsewhere. All authors have approved the submission and declare [no conflicts of interest / conflicts as listed]. The protocol was [registered as ... / not registered].",
            "Sincerely,\nJayson Cagadas Pasaol, DVM, PhD\n[Affiliation]\njaysonpasaolrmt082@gmail.com"]


def highlights():
    return ["Highlights (to be finalised after analysis)",
            "- Systematic synthesis comparing schistosomiasis-associated and non-schistosomal colorectal cancer, with S. japonicum analysed separately from other species.",
            "- Overlapping hospital cohorts identified and each patient counted once per outcome; the largest cohort (31,153 patients) assessed in leave-out analyses.",
            "- [Primary pooled finding on survival TO BE ADDED]",
            "- [Primary pooled finding on stage/metastasis TO BE ADDED]",
            "- Molecular data are sparse; no comparative cohort from the Philippines or Indonesia was identified [TO BE CONFIRMED].",
            "",
            "Graphical abstract: use Figure 8 (conceptual model) on the left and Figure 3 (pooled phenotype forest plot) on the right, with the title and one-sentence conclusion. To be assembled once Figure 3 exists."]


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
    blocks = number_all(manuscript_blocks(), numberer)
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
