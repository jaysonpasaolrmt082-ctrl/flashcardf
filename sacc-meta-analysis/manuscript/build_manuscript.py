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
    p(abstract_results(pooled))
    _unused = ("**Results.** [TO BE CALCULATED] records were screened and [TO BE CALCULATED] studies ([TO BE CALCULATED] independent cohorts; [TO BE CALCULATED] SACC and [TO BE CALCULATED] NSACC patients) were included. Compared with NSACC, SACC was associated with overall survival HR [TO BE CALCULATED] (95% CI [TO BE CALCULATED]; I² [TO BE CALCULATED]), disease-free survival HR [TO BE CALCULATED], stage III-IV disease OR [TO BE CALCULATED], lymph-node metastasis OR [TO BE CALCULATED], and distant metastasis OR [TO BE CALCULATED]. [Secondary findings and certainty ratings TO BE WRITTEN from verified results.]")
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
    p("Two reviewers independently extracted data into a piloted spreadsheet (Supplementary Table S3) covering study identification (authors, year, PMID, DOI, institution, city, province, department), design and recruitment period, schistosomiasis ascertainment (species, diagnostic method, verbatim definition), patient numbers, demographics, tumour location, pathology, stage, metastasis, molecular and laboratory markers, and survival estimates. [Interim: for this draft, data were extracted from full texts by one AI-assisted extractor and checked programmatically against the source text; independent extraction by a second reviewer is PENDING.] Each value was labelled by origin: reported directly; calculated from reported raw data; estimated from Kaplan-Meier curves; or pooled. When studies reported medians with interquartile ranges, means and standard deviations were estimated with the method of Wan et al.{c:wan2014} and the transformation was recorded. Study authors were contacted for missing data [TO BE CONFIRMED].")
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
    p(search_paragraph())
    B.append(("fig", {"file": "Figure1_PRISMA_flow.png", "w": 15.0,
                      "cap": "**Figure 1.** PRISMA 2020 flow diagram of study selection (interim: PubMed only; the remaining databases are still to be searched). Counts are read from data/analysis_ready/prisma_counts.csv."}))
    h2("Characteristics of included studies")
    p(characteristics_paragraph())
    B.append(("table", table1(inv)))
    B.append(("fig", {"file": "Figure2_landscape_timeline.png", "w": 16.0,
                      "cap": "**Figure 2.** Chronological landscape of identified studies. Bars show recruitment periods where reported; diamonds show publication year. Right column: SACC/NSACC sample sizes (NR, not reported; dash, SACC-only cohort). Labels give city/province."}))
    h2("Schistosomiasis ascertainment")
    p("All analysed comparative cohorts defined schistosomiasis by histological identification of schistosome eggs (often calcified) in the resected colorectal specimen; one series also accepted ova in stool or biopsy.{c:feng2015} No study confirmed the species morphologically or molecularly; all were classified as S. japonicum presumed from endemic-area residence. Two pathologists blinded to clinical data reviewed slides in the Qingpu reports;{c:wangw2020,wangw2023} Zheng et al. noted that egg reporting was not compulsory in routine pathology, so some SACC may have been misclassified as NSACC.{c:zheng2023} The comparison was therefore strictly SACC with egg-proven intestinal involvement versus CRC without eggs in the specimen.")
    h2("Demographic characteristics")
    p(pooled_sentence(pooled, "Male sex", "male sex") + " " + pooled_sentence(pooled, "age", "age (mean difference, years)", md=True) + " " + pooled_sentence(pooled, "Age > 60 years", "age over 60 years") + " Every cohort that reported age found SACC patients to be older or of similar age (Figure 7); the very high heterogeneity reflects the size, not the direction, of the difference.")
    h2("Anatomical distribution")
    p(pooled_sentence(pooled, "Rectal location", "rectal location") + " " + sens_sentence("Rectal location") + " " + pooled_sentence(pooled, "Right-sided colon", "right-sided colon location") + " " + pooled_sentence(pooled, "Sigmoid location", "sigmoid location"))
    h2("Pathological characteristics")
    p(pathology_paragraph(pooled))
    B.append(("table", table2(inv)))
    h2("Tumour stage and metastatic behaviour")
    p(pooled_sentence(pooled, "Stage III-IV", "stage III-IV disease") + " " + sens_sentence("Stage III-IV") + " " + pooled_sentence(pooled, "pT3-T4", "pT3-T4 tumours") + " " + pooled_sentence(pooled, "Lymph-node metastasis", "lymph-node metastasis") + " " + pooled_sentence(pooled, "Distant metastasis", "distant metastasis") + " The largest cohort reported less nodal and distant metastasis in SACC,{c:zheng2023} whereas the Wuhu Second People's Hospital cohort reported more nodal metastasis;{c:wu2021} the pooled estimates show no consistent difference.")
    B.append(("fig", {"file": "Figure3_phenotype_forest.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 3.** Clinicopathological phenotype of SACC versus NSACC: pooled odds ratios (random effects, REML) with 95% confidence intervals for each outcome with at least two independent cohorts. Red, primary outcomes; blue, secondary outcomes. Study-level forest plots are provided in the Supplementary Material."}))
    h2("Molecular characteristics")
    p(molecular_paragraph(pooled))
    B.append(("table", table3()))
    B.append(("fig", {"file": "Figure6_molecular.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 6.** Molecular phenotype. Pooled odds ratios for biomarkers reported by at least two comparable studies, and evidence map for biomarkers that could not be pooled."}))
    h2("Overall survival")
    p(pooled_sentence(pooled, "OS - Adjusted", "overall survival (multivariable-adjusted HRs)", hr=True) + " " + pooled_sentence(pooled, "OS - Unadjusted", "overall survival (unadjusted or derived HRs)", hr=True) + " The unadjusted pool combined three estimates above 1 with one HR below 1 derived from a log-rank P value in a 100-patient follow-up subset;{c:wangz2020,tierney2007} the largest cohort reported no independent effect after adjustment but did not report the adjusted HR.{c:zheng2023}")
    B.append(("fig", {"file": "Figure4_OS_forest.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 4.** Overall survival in SACC versus NSACC. Hazard ratios with 95% CI; multivariable-adjusted and unadjusted/derived estimates are pooled separately. Source column: P1, adjusted HR reported; P2, unadjusted HR reported; P3, derived from survival statistics; P4, reconstructed from Kaplan-Meier curves."}))
    h2("Disease-free and recurrence-free survival")
    p(pooled_sentence(pooled, "DFS - Adjusted", "disease-free survival (adjusted)", hr=True) + " " + pooled_sentence(pooled, "DFS - Unadjusted", "disease-free survival (unadjusted)", hr=True) + " Both cohorts showed shorter disease-free survival in SACC before adjustment and attenuated, non-significant HRs after adjustment.{c:zheng2023,li2024}")
    B.append(("fig", {"file": "Figure5_DFS_forest.png", "w": 16.0, "from_output": True,
                      "cap": "**Figure 5.** Disease-free/recurrence-free survival in SACC versus NSACC (hazard ratios, random effects)."}))
    h2("Within-SACC prognostic factors")
    p(within_paragraph())
    B.append(("table", table5()))
    h2("Risk of bias")
    p(rob_paragraph())
    h2("Sensitivity and subgroup analyses")
    p(sensitivity_paragraph())
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


REFKEY = {"Zheng2023": "zheng2023", "WangZ2020": "wangz2020", "WangW2020": "wangw2020", "WangW2021": "wangw2021",
          "WangW2023": "wangw2023", "Pan2020": "pan2020", "Cheng2023": "bmcgastro2023", "Chai2026": "chai2026", "Feng2015": "feng2015", "Wu2021": "wu2021", "Li2024": "li2024",
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


def abstract_results(pooled):
    c = prisma()
    g = lambda k, m="OR": (f"{m} {est(pooled[k])}" if k in pooled else f"{m} {TBC}")
    return (f"**Results.** In this interim analysis (PubMed only), {c['screened']} records were screened and {c['included_qualitative']} reports from seven independent Chinese comparative cohorts, one SACC-only cohort, and one genomic study were included; "
            f"{c['reports_not_retrieved']} potentially relevant reports could not be retrieved. SACC patients were more often male ({g('Male sex')}; 6 cohorts; I² 0%) and older. "
            f"Adjusted overall survival was worse in SACC ({g('OS - Adjusted', 'HR')}; 2 cohorts), but unadjusted estimates were inconsistent ({g('OS - Unadjusted', 'HR')}; I² {fmt(pooled['OS - Unadjusted']['I2'], 0) if 'OS - Unadjusted' in pooled else TBC}%) "
            f"and adjusted disease-free survival did not differ ({g('DFS - Adjusted', 'HR')}). Stage III-IV disease was less frequent ({g('Stage III-IV')}), but not after exclusion of the largest cohort; "
            f"lymph-node metastasis ({g('Lymph-node metastasis')}), distant metastasis ({g('Distant metastasis')}), differentiation, and vascular and perineural invasion did not differ. "
            f"KRAS mutation was more frequent in SACC ({g('KRAS mutation')}; 2 cohorts); other biomarkers came from single cohorts. Certainty of evidence [TO BE RATED with GRADE].")


def search_paragraph():
    c = prisma()
    return (f"This is an interim selection based on MEDLINE only. The PubMed strategy in Supplementary Table S1, run on 5 October 2026, returned {c['db_pubmed']} records, "
            f"which contained all {22} reports of the earlier scoping inventory. Titles and abstracts of {c['screened']} records were screened and {c['excluded_title_abstract']} were excluded. "
            f"Of {c['reports_sought']} reports sought, {c['reports_not_retrieved']} could not be retrieved from open sources (mainly Chinese-language articles and subscription journals; Supplementary Table S2). "
            f"{c['full_text_assessed']} full texts were assessed and {c['full_text_excluded']} was excluded, leaving {c['included_qualitative']} reports in the qualitative synthesis and "
            f"{c['included_quantitative']} contributing to at least one meta-analysis (Figure 1). Scopus, Web of Science, Embase, CNKI, Wanfang, and SinoMed [ARE STILL TO BE SEARCHED; counts TO BE ADDED].")


def characteristics_paragraph():
    return ("The 16 included reports came from nine institutions or groups (Table 1). Seven independent comparative cohorts, all from China, compared SACC with NSACC: "
            "Changhai Hospital, Shanghai (823 SACC and 30,330 NSACC; 2001-2021);{c:zheng2023} Yijishan Hospital, Wuhu (253 and 2,885; 2012-2018), with a second, partly overlapping report from the same hospital;{c:wangz2020,yang2023} "
            "the Qingpu Branch of Zhongshan Hospital, Shanghai (137 and 214; 2008-2016), from which five further reports provided biomarker data only;{c:wangw2020,wangw2021,wangw2023,pan2020,bmcgastro2023,chai2026} "
            "Union Hospital, Wuhan (30 and 459; 2010-2019);{c:li2024} Jingzhou Hospital, Hubei (95 and 406; 2020-2022), with an overlapping radiology report;{c:zhu2024,zhang2023} "
            "Wuhu Second People's Hospital (56 and 307; 2015-2020);{c:wu2021} and Ruijin Hospital, Shanghai (26 and 34 rectosigmoid cancers; 2009-2013).{c:feng2015} "
            "Overlap was confirmed from the full texts: all six Qingpu reports described patients resected at the same hospital between January 2008 and August 2016, and the two Jingzhou reports shared the hospital, period, and an author (Supplementary Table S6). "
            "A previously suspected Qingpu report proved to be a separate SACC-only cohort from the main Zhongshan campus (2016-2018).{c:pan2023} One exome-sequencing study used an external sporadic-CRC comparator.{c:genomic2023} "
            "Allowing for overlap, individual meta-analyses included up to 1,383 SACC and 34,328 NSACC patients (Table 4). All cohorts were retrospective; survival data were available for four cohorts.")


def pathology_paragraph(pooled):
    parts = [pooled_sentence(pooled, "Poor differentiation", "poor differentiation"), pooled_sentence(pooled, "Mucinous histology", "mucinous or signet-ring histology"),
             pooled_sentence(pooled, "Vascular invasion", "vascular invasion"), pooled_sentence(pooled, "Perineural invasion", "perineural invasion"),
             pooled_sentence(pooled, "Tumour budding", "tumour budding"), pooled_sentence(pooled, "Tumour size >= 5 cm", "tumour size of 5 cm or more")]
    lo = sens_row("Poor differentiation", "leave-one-out: omit WangZ2020")
    extra = (f" Heterogeneity for differentiation was driven by one cohort reporting 2.6% poorly differentiated SACC against 21.9% NSACC with a non-significant P value;{{c:wangz2020}} without it the OR was {est(lo)} (I² = {fmt(lo['I2'], 0)}%)." if lo else "")
    single = (" Single cohorts reported more multiple primary CRC (4.3% vs 2.8%), more concomitant polyps (20.0% vs 13.6%), and more positive resection margins (3.6% vs 1.1%) in SACC, and lymphovascular invasion "
              "in 34% vs 36%;{c:zheng2023,wangw2020} these were not pooled.")
    return " ".join(parts) + extra + single + " Study-level counts are given in Table 2."


def molecular_paragraph(pooled):
    k = pooled.get("KRAS mutation")
    ks = f"KRAS mutation was more frequent in SACC in the two cohorts with internal comparators (pooled OR {est(k)}; I² = {fmt(k['I2'], 0)}%), " if k else ""
    return (ks + "although only the larger cohort was individually significant,{c:zheng2023} and the smaller one found the excess confined to G12S/D mutations (43.3% vs 18.1%).{c:li2024} "
            "In the largest cohort, NRAS, BRAF, and PIK3CA mutation and mismatch-repair deficiency did not differ.{c:zheng2023} All other biomarkers came from single reports of the Qingpu cohort and showed no difference between groups: "
            "c-MYC amplification (13.8% vs 14.4%),{c:pan2020} stromal and tumoural PD-L1,{c:wangw2021} stromal and intratumoural TILs, CD3 and CD20,{c:wangw2023} CD4 and CD8 densities,{c:bmcgastro2023} and CFIm25.{c:chai2026} "
            "Exome sequencing of 30 SACC tumours against an external sporadic-CRC reference found a lower median tumour mutational burden (1.61 vs 2.03 mutations/Mb), microsatellite stability or low instability in all cases, and less frequent RTK-RAS and Hippo pathway alteration.{c:genomic2023} "
            "Molecular data on S. mansoni (p53, mismatch repair, c-Myc) and several small Chinese-language comparisons (mismatch repair, p53, COX-2, Bax, Bcl-2, VEGF) were identified but their full texts could not be retrieved.{c:madbouly2007,zalata2005,chen2016,yangdh2014,ruan2013,yangxg2021,zhangr1998}")


def within_paragraph():
    pooled = _out("Table5b_within_SACC_pooled.csv")
    ln = next((r for r in pooled if r["outcome"] == "LN_metastasis OS"), None)
    txt = ("Within SACC, the conventional factors remained prognostic: nodal metastasis predicted overall survival in two cohorts"
           + (f" (pooled adjusted HR {est(ln)}; I² = {fmt(ln['I2'], 0)}%)" if ln else "") + ",{c:zheng2023,bmcgastro2023} as did distant metastasis, BRAF mutation, and tumour budding in the largest cohort.{c:zheng2023} "
           "Schistosomiasis-specific features were examined only in the SACC-only cohort from the main Zhongshan campus (172 patients):{c:pan2023} in stage III disease, schistosome eggs in regional lymph nodes were associated with shorter disease-free survival "
           "(adjusted HR 3.00, 95% CI 1.37-6.59) and coexisting hepatic schistosomiasis with shorter disease-free (adjusted HR 3.95, 1.75-8.92) and overall survival (adjusted HR 4.97, 1.84-13.43); "
           "deep (muscularis or full-thickness) egg deposition was associated with disease-free survival in univariable analysis only. c-MYC amplification (adjusted HR 1.86, 1.01-3.42) and high intratumoural CD8 density (adjusted HR 0.52, 0.30-0.90) "
           "were prognostic in the Qingpu SACC subgroup.{c:pan2020,bmcgastro2023} A West China cohort of 74 SACC on egg deposition site could not be retrieved.{c:wangm2016} With these exceptions, none of the within-SACC factors could be pooled (Table 5).")
    return txt


def rob_paragraph():
    rob = _csv("data/analysis_ready/rob_nos.csv")
    main = [r for r in rob if r["study_id"] in ("Zheng2023", "WangZ2020", "WangW2020", "Li2024", "Zhu2024", "Zhang2023", "Yang2023", "Wu2021", "Feng2015")]
    n = {k: sum(r["rating"] == k for r in main) for k in ("low", "moderate", "high")}
    return (f"Of the {len(main)} comparative reports that contributed to meta-analyses, {n['low']} were at low, {n['moderate']} at moderate, and {n['high']} at high risk of bias on the Newcastle-Ottawa Scale (Supplementary Table S4). "
            "The most frequent limitations were the absence of adjustment for confounders in cross-sectional comparisons, unreported or incomplete follow-up, and non-consecutive selection of the non-schistosomal group in two reports.{c:yang2023,feng2015} "
            "Exposure ascertainment was secure (histology) in all, but may under-detect schistosomiasis, which would bias comparisons towards the null. Several reports contained internal numerical inconsistencies, which are documented in the extraction file. "
            "[Interim: risk of bias assessed by one AI-assisted reviewer; second independent assessment PENDING.]")


def sensitivity_paragraph():
    out = []
    for oc, lab in (("Male sex", "male sex"), ("Stage III-IV", "stage III-IV disease"), ("Lymph-node metastasis", "lymph-node metastasis")):
        r = sens_row(oc, "excluding largest cohort")
        if r:
            out.append(f"{lab} {est(r)}")
    lo = sens_row("OS - Unadjusted", "leave-one-out: omit WangZ2020")
    s = ("Excluding the Shanghai cohort of 31,153 patients{c:zheng2023} gave ORs of " + "; ".join(out) + ". The male excess was therefore robust, "
         "whereas the lower odds of stage III-IV disease and the excess of rectal tumours depended on the largest cohort. ")
    if lo:
        s += (f"For unadjusted overall survival, omitting the only cohort with a favourable (derived) HR{{c:wangz2020}} gave an HR of {est(lo)} (I² = {fmt(lo['I2'], 0)}%). ")
    s += ("Restricting to histology-confirmed SACC did not change any estimate because all analysed cohorts used histology; no cohort confirmed the species, so the S. japonicum-confirmed analysis could not be performed. "
          "Pre-specified subgroup analyses were not feasible with two to seven cohorts per outcome. With fewer than 10 studies for every outcome, small-study effects were not assessed. All sensitivity results are in Supplementary Table S5.")
    return s


# =============================================================== tables ======
FOLLOWUP = {"Zheng2023": "NR (survival in 6,537)", "WangZ2020": "Median 78 mo (100 pts)", "WangW2020": "Median 62.4 mo", "WangW2021": "NR (cohort as Wang 2020)",
            "WangW2023": "NR (cohort as Wang 2020)", "Pan2020": "Median 62.4 mo", "Cheng2023": "Median 62.4 mo", "Chai2026": "NR", "Li2024": "NR",
            "Pan2023": "Median 50.1 mo", "Genomic2023": "NR", "Zhang2023": "None", "Zhu2024": "None", "Yang2023": "None", "Wu2021": "None", "Feng2015": "None"}
DEFN = {"Zheng2023": "Calcified eggs in resected colorectal tissue", "Feng2015": "Ova on microscopy (colon, rectum, or stool)",
        "Li2024": "Intact/calcified eggs, granulomas, or worms in CRC tissue", "Genomic2023": "History plus ova in specimen"}


def table1(inv):
    order = ["Zheng2023", "WangZ2020", "Yang2023", "WangW2020", "WangW2021", "WangW2023", "Pan2020", "Cheng2023", "Chai2026", "Li2024",
             "Zhu2024", "Zhang2023", "Wu2021", "Feng2015", "Pan2023", "Genomic2023", "WangM2014", "WangM2016", "NCG1986", "Madbouly2007"]
    rows = []
    for sid in order:
        r = inv[sid]
        nr = lambda v: "NR" if v in ("NR", "") else v
        retrieved = "Full text read" in r["verification_numbers"]
        rows.append([short_name(r) + cite_tags([REFKEY[sid]]), nr(r["city_province"]), nr(r["institution"]).split(" (")[0].split(",")[0],
                     nr(r["recruitment_period"]), r["design"].split(" (")[0], nr(r["n_SACC"]),
                     nr(r["n_NSACC"]) if not r["analysis_set"].startswith("Within") else "-",
                     r["species"].split(" (")[0], DEFN.get(sid, "Eggs on H&E in resected specimen" if retrieved else "NR (full text not retrieved)"),
                     FOLLOWUP.get(sid, "NR"), r["outcomes_reported_in_abstract"].split(" (")[0][:80], r["overlap_group"].split("-")[0],
                     r["analysis_set"].split(" (")[0].split(" -")[0] if retrieved else "Not analysed (no full text)"])
    return {"cap": "**Table 1.** Characteristics of identified studies", "head": ["Study", "Location", "Institution", "Study period", "Design", "SACC n", "NSACC n", "Species",
            "Definition of schistosomiasis", "Follow-up", "Main outcomes", "Overlap group", "Analysis set"], "rows": rows, "font": 6.5, "landscape": True,
            "foot": "Extracted from full texts on 5 October 2026 except where marked 'no full text'. NR, not reported; mo, months; S. japonicum presumed = endemic-area cohort, species not confirmed. Overlap groups are defined in Supplementary Table S6. "
                    "Six further comparative reports identified by the PubMed search could not be retrieved (Supplementary Table S2)."}


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
                         f"{fmt(r['I2'], 0)}%", fmt(r["tau2"], 3), ("<0.001" if float(r["p_value"]) < 0.001 else fmt(r["p_value"], 3)), "[TO BE ASSESSED]"])
        else:
            rows.append([lab, "<2", "-", "-", m, "Not pooled", "-", "-", "-", "-", "-"])
    return {"cap": "**Table 4.** Summary of meta-analyses: SACC versus NSACC", "head": ["Outcome", "Studies", "SACC n", "NSACC n", "Measure", "Pooled effect", "95% CI", "I²", "tau²", "P value", "GRADE certainty"],
            "rows": rows, "font": 7.5, "landscape": True,
            "foot": "Random-effects models with REML estimation; S. japonicum (presumed) cohorts; one report per overlap group per outcome. HR > 1 and OR > 1 indicate higher hazard or higher odds in SACC; MD > 0, older SACC patients. "
                    "Generated from output/tables/Table4_meta_analysis_summary.csv. GRADE ratings require two reviewers and are pending."}


def table5():
    inv = inventory()
    ws = _verified("within_sacc_prognostic.csv")
    rows = [[r["factor"].replace("_", " "), short_name(inv[r["study_id"]]) + cite_tags([REFKEY[r["study_id"]]]), r["comparison"], r["outcome"],
             f"{r['hr']} ({r['lower95']}-{r['upper95']})", "Adjusted" if r["adjusted"] == "yes" else "Univariable", r["covariates"] or "-", r["n_SACC_total"]] for r in ws]
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
        s = "Inconsistent" if i2 >= 75 else ("Moderate" if (sig and k >= 3 and i2 < 50) else "Limited")
        if lab == "Older age":
            d, s = "Up (all cohorts older or similar)", "Moderate (direction consistent; magnitude heterogeneous)"
        if key in ("Rectal location", "Stage III-IV"):
            s += " - depends on largest cohort"
        rows.append([lab, d, s])
    return {"cap": "**Table 6.** Phenotype matrix: is SACC distinct? (provisional)", "head": ["Feature", "Pooled direction", "Strength of evidence"], "rows": rows, "font": 8, "landscape": False,
            "foot": "Classified automatically from Table 4 before GRADE: Moderate, >= 3 cohorts, 95% CI excluding no difference, I² < 50%; Limited, fewer cohorts or imprecise; Inconsistent, I² >= 75%. 'Strong' is reserved for findings with moderate/high GRADE certainty and is not yet assigned."}


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
        "rows": [[d, pl, q, "Inception to search date", "2026-10-05" if d == "MEDLINE" else "[SEARCH DATE TO BE ADDED]", prisma()["db_pubmed"] if d == "MEDLINE" else TBC, "None (no language or date limits)"] for d, pl, q in SEARCHES],
        "foot": "Deduplication: [software and version TO BE ADDED], followed by manual check of author, year, title, and DOI. Searches were not peer-reviewed with PRESS [or: were peer-reviewed by NAME TO BE ADDED]."}))
    B.append(("h1", "Supplementary Table S2. Full texts excluded, with reasons"))
    B.append(("table", {"cap": "**Table S2.** Excluded full-text reports", "font": 8,
        "head": ["Study", "PMID / DOI", "Principal reason for exclusion"],
        "rows": S2_ROWS,
        "foot": "One principal reason per report, in the hierarchy: not CRC; not human; no schistosomiasis status; no comparator; no extractable outcome; duplicate cohort for the same outcome."}))
    B.append(("h1", "Supplementary Table S3. Complete extraction data"))
    B.append(("p", "Provided as the Excel workbook SACC_master_extraction.xlsx (sheets: master_wide, binary_outcomes, continuous_outcomes, survival_outcomes, within_sacc_prognostic, molecular_evidence, evidence_direction, rob_nos, inventory, overlap). Every value records its origin (reported, calculated from raw data, Kaplan-Meier-reconstructed, converted from median/IQR) and its source location in the original report."))
    B.append(("h1", "Supplementary Table S4. Risk-of-bias assessments"))
    B.append(("table", {"cap": "**Table S4.** Newcastle-Ottawa Scale assessments", "font": 8,
        "head": ["Study", "Selection (0-4)", "Comparability (0-2)", "Outcome/exposure (0-3)", "Total (0-9)", "Overall risk of bias"],
        "rows": nos_rows(),
        "foot": "Interim: one AI-assisted assessor; second independent assessment PENDING. Comparability awarded for analyses adjusted for stage plus age or sex. Low risk: 7-9 stars; moderate: 5-6; high: 0-4. Follow-up items are not met by cross-sectional comparisons."}))
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
    B.append(("p", "Study-level forest plots for each pooled outcome (output/figures/Fig_forest_<outcome>.pdf) and funnel plots for outcomes with at least 10 studies will be inserted here from the verified analysis. [TO BE INSERTED]"))
    B.append(("h1", "References cited in the Supplementary Material"))
    B.append(("refs",))
    return B


S2_ROWS = [
 ["Liu XF 2023{c:liuxf2023}", "38125940", "Excluded at full text: no CRC-specific SACC-versus-NSACC data (cancer spectrum among S. japonicum patients)"],
 ["Wang M 2014{c:wangm2014}", "25422211", "Not retrieved (journal site unreachable); abstract gives no HR"],
 ["Wang M 2016{c:wangm2016}", "26922912", "Not retrieved (subscription); SACC-only cohort of 74"],
 ["NCG 1986{c:ncg1986}", "3021419", "Not retrieved (Chinese, print only)"],
 ["Madbouly 2007{c:madbouly2007}", "16786317", "Not retrieved (subscription); S. mansoni"],
 ["Liu 2013{c:liu2013}", "24083755", "Not retrieved; abstract shows no comparator (SACC case series)"],
 ["Zhang W 2012{c:zhou_ct2012}", "22658847", "Not retrieved; abstract shows SACC-only imaging study"],
 ["Chen 2016{c:chen2016}", "26797844", "Not retrieved (Chinese); 80 vs 258, hMLH1/hMSH2"],
 ["Yang DH 2014{c:yangdh2014}", "25434139", "Not retrieved (Chinese); 80 vs 80, p53/COX-2/Bax/c-myc"],
 ["Ruan 2013{c:ruan2013}", "24024441", "Not retrieved (Chinese); 30 vs 30, VEGF/PD-ECGF"],
 ["Yang XG 2021{c:yangxg2021}", "34008361", "Not retrieved (Chinese); 30 vs 30, Bcl-2/Bax"],
 ["Zhang R 1998{c:zhangr1998}", "9851256", "Not retrieved (subscription); 22 vs 22, TP53 mutations"],
 ["Zalata 2005{c:zalata2005}", "16308474", "Not retrieved (PMC access challenge); S. mansoni"],
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
