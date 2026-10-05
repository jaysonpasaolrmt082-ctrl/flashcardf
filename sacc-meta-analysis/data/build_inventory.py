"""Builds the Phase-1 study inventory and overlap matrix.

Every value here was taken from a bibliographic index entry (PubMed/PMC/publisher
URL) or from the published abstract as surfaced by a web search on 2026-10-05.
Direct access to PubMed/PMC/publisher full texts was blocked in the build
environment, so NOTHING here has been checked against a full text. Columns
'verification_ids' and 'verification_numbers' record that status explicitly.
'NR' = not retrieved (not the same as 'not reported').
"""
import csv

FIELDS = ["study_id","first_author","year","title","journal","volume_pages","pmid","doi",
          "pmcid","institution","city_province","recruitment_period","n_SACC","n_NSACC",
          "n_total","species","design","outcomes_reported_in_abstract","overlap_group",
          "analysis_set","eligibility_status","verification_ids","verification_numbers","notes"]

S = []
def add(**k): S.append({f: k.get(f, "NR") for f in FIELDS})

# ---------------- Primary comparative set (SACC vs NSACC) ----------------
add(study_id="Zheng2023", first_author="Zheng N", year=2023,
    title="Changing trends, clinicopathological characteristics, surgical treatment patterns, and prognosis of schistosomiasis-associated versus non-schistosomiasis-associated colorectal cancer: a large retrospective cohort study of 31 153 cases in Shanghai, China (2001-2021)",
    journal="Int J Surg", volume_pages="109(4):772-784", pmid="36999800", doi="10.1097/JS9.0000000000000293",
    pmcid="PMC10389396", institution="Dept of Colorectal Surgery, Changhai Hospital, Naval Medical University",
    city_province="Shanghai", recruitment_period="2001-2021", n_SACC=823, n_NSACC=30330, n_total=31153,
    species="S. japonicum (endemic area; definition to verify)", design="Retrospective single-centre cohort",
    outcomes_reported_in_abstract="Trends; clinicopathological features; comorbidity; KRAS; multiple primary CRC; concomitant polyps; surgical patterns; OS; DFS (schistosomiasis not independent predictor of OS/DFS in multivariable analysis)",
    overlap_group="G1-Shanghai-Changhai", analysis_set="Primary comparative",
    eligibility_status="Eligible (provisional)", verification_ids="PMID/DOI/PMCID matched to PubMed/PMC index URLs",
    verification_numbers="Sample sizes from title/abstract; outcome data require full text",
    notes="Dominant cohort by size: mandatory leave-out sensitivity analysis. Same city as Changzheng genomic study (different hospital) - check.")
add(study_id="WangZ2020", first_author="Wang Z", year=2020,
    title="Comparison of the clinicopathological features and prognoses of patients with schistosomal and nonschistosomal colorectal cancer",
    journal="Oncol Lett", volume_pages="19:2375-2383", pmid="32194737", doi="10.3892/ol.2020.11331", pmcid="PMC7039146",
    institution="Dept of Infectious Diseases, Yijishan Hospital of Wannan Medical College", city_province="Wuhu, Anhui",
    recruitment_period="NR", n_SACC=253, n_NSACC=2885, n_total=3138, species="S. japonicum (endemic area; definition to verify)",
    design="Retrospective cohort", outcomes_reported_in_abstract="Age; sex; faecal occult blood; pT stage; CA19-9; WBC; RBC; PLT; 5-year survival",
    overlap_group="G2-Wuhu-Yijishan", analysis_set="Primary comparative", eligibility_status="Eligible (provisional)",
    verification_ids="PMID/DOI/PMCID matched to index URLs", verification_numbers="n from abstract; NSACC n derived as 3138-253",
    notes="Direction of survival difference must be read from full text (search summaries conflicting).")
add(study_id="WangW2020", first_author="Wang W", year=2020,
    title="Comparison of non-schistosomal colorectal cancer and schistosomal colorectal cancer",
    journal="World J Surg Oncol", volume_pages="18:149", pmid="32611359", doi="10.1186/s12957-020-01925-5", pmcid="PMC7330999",
    institution="Qingpu Branch of Zhongshan Hospital, Fudan University", city_province="Shanghai (Qingpu)",
    recruitment_period="2008-01 to 2016-08", n_SACC=137, n_NSACC=214, n_total=351, species="S. japonicum (endemic area; definition to verify)",
    design="Retrospective cohort (resected CRC)", outcomes_reported_in_abstract="Age (older in SACC); other clinicopathological features; OS (KM P=0.0277; schistosomiasis independent predictor in multivariable model); subgroup by stage/LN",
    overlap_group="G3-Shanghai-Qingpu", analysis_set="Primary comparative", eligibility_status="Eligible (provisional) - index study of G3",
    verification_ids="PMID/DOI/PMCID matched", verification_numbers="n from abstract", notes="Likely parent cohort for WangW2021, WangW2023, Pan2020, and possibly BMCGastro2023.")
add(study_id="WangW2021", first_author="Wang W", year=2021,
    title="Correlation between schistosomiasis and CD8+ T cell and stromal PD-L1 as well as the different prognostic role of CD8+ T cell and PD-L1 in schistosomal-associated colorectal cancer and non-schistosomal-associated colorectal cancer",
    journal="World J Surg Oncol", volume_pages="NR", pmid="34743724", doi="10.1186/s12957-021-02433-w", pmcid="PMC8573878",
    institution="Dept of Pathology, Qingpu Branch of Zhongshan Hospital, Fudan University", city_province="Shanghai (Qingpu)",
    recruitment_period="NR", n_SACC="NR", n_NSACC="NR", n_total=338, species="S. japonicum (to verify)", design="Retrospective cohort",
    outcomes_reported_in_abstract="CD8+ TIL; tumoural/stromal PD-L1; OS (schistosomiasis independent predictor)",
    overlap_group="G3-Shanghai-Qingpu", analysis_set="Primary comparative (biomarker/OS only if not superseded)",
    eligibility_status="Eligible - overlapping; use only for outcomes absent from WangW2020",
    verification_ids="PMID/DOI/PMCID matched", verification_numbers="n_total from abstract")
add(study_id="WangW2023", first_author="Wang W", year=2023,
    title="Comparison of the prognostic value of stromal tumor-infiltrating lymphocytes and CD3+ T cells between schistosomal and non-schistosomal colorectal cancer",
    journal="World J Surg Oncol", volume_pages="NR", pmid="36726115", doi="10.1186/s12957-023-02911-3", pmcid="PMC9890788",
    institution="Dept of Pathology, Qingpu Branch of Zhongshan Hospital, Fudan University", city_province="Shanghai (Qingpu)",
    recruitment_period="NR", n_total=349, species="S. japonicum (to verify)", design="Retrospective cohort",
    outcomes_reported_in_abstract="sTILs; CD3; CD20; clinicopathological features (no significant SACC vs NSACC differences per abstract); OS",
    overlap_group="G3-Shanghai-Qingpu", analysis_set="Primary comparative (immune markers only)",
    eligibility_status="Eligible - overlapping; immune markers only", verification_ids="PMID/DOI/PMCID matched", verification_numbers="n_total from abstract")
add(study_id="Pan2020", first_author="Pan W", year=2020,
    title="The prognostic role of c-MYC amplification in schistosomiasis-associated colorectal cancer",
    journal="Jpn J Clin Oncol", volume_pages="50(4):446-455", pmid="32297641", doi="10.1093/jjco/hyz210", pmcid="NR",
    institution="Zhongshan Hospital, Fudan University / Qingpu Branch (co-authors overlap with G3)", city_province="Shanghai",
    recruitment_period="NR", n_total=354, species="S. japonicum (to verify)", design="Retrospective cohort",
    outcomes_reported_in_abstract="c-MYC amplification (14.1%, 50/354 overall); association with age, LN metastasis, stage; OS by schistosomiasis subgroup",
    overlap_group="G3-Shanghai-Qingpu", analysis_set="Molecular evidence table; within-SACC prognostic",
    eligibility_status="Eligible - overlapping; c-MYC only", verification_ids="PMID/DOI matched", verification_numbers="abstract-level")
add(study_id="BMCGastro2023", first_author="[first author to verify]", year=2023,
    title="The predictive value of CD4, CD8, and C-reactive protein in the prognosis of schistosomal and non-schistosomal colorectal cancer",
    journal="BMC Gastroenterol", volume_pages="NR", pmid="37277702", doi="10.1186/s12876-023-02834-z", pmcid="PMC10240683",
    institution="NR (suspected Qingpu/Zhongshan group - verify)", city_province="NR", recruitment_period="NR",
    species="S. japonicum (to verify)", design="Retrospective cohort",
    outcomes_reported_in_abstract="Stromal/intratumoural CD4, CD8; CRP; OS (schistosomiasis independent predictor)",
    overlap_group="G3? (suspected)", analysis_set="Primary comparative (immune markers only)",
    eligibility_status="Eligible - suspected overlap", verification_ids="PMID/DOI/PMCID matched", verification_numbers="none retrieved")
add(study_id="Li2024", first_author="Li X", year=2024,
    title="Schistosoma infection, KRAS mutation status, and prognosis of colorectal cancer",
    journal="Chin Med J (Engl)", volume_pages="137(2):235-237", pmid="37920960", doi="10.1097/CM9.0000000000002905", pmcid="PMC10798728",
    institution="Dept of Pathology, Union Hospital, Tongji Medical College, Huazhong University of Science and Technology",
    city_province="Wuhan, Hubei", recruitment_period="NR", n_SACC=30, n_NSACC=459, n_total=489, species="S. japonicum (to verify)",
    design="Retrospective cohort (research letter)", outcomes_reported_in_abstract="KRAS G12S/D (qPCR); OS (univariable HR reported)",
    overlap_group="G4-Wuhan-Union", analysis_set="Primary comparative", eligibility_status="Eligible (provisional)",
    verification_ids="PMID/DOI/PMCID matched", verification_numbers="n from abstract; HR and KRAS % seen only in search summary - MUST re-extract",
    notes="Short research letter: check for full Cox model and covariates.")
add(study_id="Zhang2023", first_author="Zhang F", year=2023,
    title="Conjoint analysis of clinical, imaging, and pathological features of schistosomiasis and colorectal cancer",
    journal="Pathol Oncol Res", volume_pages="NR", pmid="38099242", doi="10.3389/pore.2023.1611396", pmcid="PMC10719402",
    institution="Dept of Radiology, Jingzhou Hospital Affiliated to Yangtze University", city_province="Jingzhou, Hubei",
    recruitment_period="2020-01 to 2022-12", n_SACC=101, n_NSACC=240, n_total=341, species="S. japonicum (to verify)",
    design="Retrospective cohort", outcomes_reported_in_abstract="Sex; TNM stage; LN metastasis; nerve invasion; vascular tumour thrombus; differentiation; CT calcification; CA-125",
    overlap_group="G5-Jingzhou", analysis_set="Primary comparative", eligibility_status="Eligible (provisional)",
    verification_ids="PMID/DOI/PMCID matched", verification_numbers="n from abstract",
    notes="Shares author (Zhu Y) and identical period with Zhu2024 - HIGH overlap risk.")
add(study_id="Zhu2024", first_author="Zhu Y", year=2024,
    title="A retrospective cross-sectional study: comparison of the clinicopathological features of schistosomal and non-schistosomal colorectal cancer in Central China",
    journal="BMC Infect Dis", volume_pages="NR", pmid="39054428", doi="10.1186/s12879-024-09648-8", pmcid="PMC11271061",
    institution="NR (Central China; verify - possibly Jingzhou)", city_province="Hubei (verify)", recruitment_period="2020-2022",
    n_SACC=95, n_NSACC=406, n_total=501, species="S. japonicum (to verify)", design="Retrospective cross-sectional",
    outcomes_reported_in_abstract="Age >60; site (rectum/sigmoid); T stage; comparison with Yangtze basin literature",
    overlap_group="G5-Jingzhou (suspected)", analysis_set="Primary comparative", eligibility_status="Eligible - overlap with Zhang2023 to resolve",
    verification_ids="PMID/DOI/PMCID matched", verification_numbers="n from abstract")
add(study_id="WangM2014", first_author="Wang M", year=2014, title="Prognostic analysis of schistosomal rectal cancer",
    journal="Asian Pac J Cancer Prev", volume_pages="15(21):9271-9275", pmid="25422211", doi="10.7314/apjcp.2014.15.21.9271", pmcid="NR",
    institution="Dept of Gastroenterological Surgery, West China Hospital, Sichuan University", city_province="Chengdu, Sichuan",
    recruitment_period="NR", n_SACC=30, n_NSACC=30, n_total=60, species="S. japonicum (to verify)",
    design="Retrospective matched (age, sex, stage) cohort; laparoscopic TME",
    outcomes_reported_in_abstract="OS; DFS (schistosomiasis independent factor in multivariable analysis)",
    overlap_group="G6-Chengdu-WestChina", analysis_set="Primary comparative - survival only (matching on stage invalidates stage/sex/age comparisons)",
    eligibility_status="Eligible for survival only", verification_ids="PMID/DOI matched", verification_numbers="n from abstract")
add(study_id="NCG1986", first_author="National Cooperative Group on Pathology and Prognosis of Colorectal Cancer", year=1986,
    title="[Schistosomiasis and its prognostic significance in patients with colorectal cancer]", journal="Zhonghua Zhong Liu Za Zhi",
    volume_pages="8(2):149-151", pmid="3021419", doi="NR", institution="Multicentre (national cooperative group)", city_province="China (multi-province)",
    recruitment_period="NR", n_SACC=430, species="S. japonicum (presumed; verify)", design="Multicentre retrospective cohort (Chinese language)",
    outcomes_reported_in_abstract="5-year survival lower in SACC; regional LN immune response; infiltrating growth pattern",
    overlap_group="G7-national-historical", analysis_set="Primary comparative (if comparator data extractable)",
    eligibility_status="Potentially eligible - Chinese full text required", verification_ids="PMID matched", verification_numbers="SACC n from abstract")
add(study_id="Madbouly2007", first_author="Madbouly KM", year=2007,
    title="Colorectal cancer in a population with endemic Schistosoma mansoni: is this an at-risk population?",
    journal="Int J Colorectal Dis", volume_pages="22:175-181", pmid="16786317", doi="10.1007/s00384-006-0144-3",
    institution="Dept of Surgery, University of Alexandria", city_province="Alexandria, Egypt", recruitment_period="NR",
    n_SACC=40, n_NSACC=20, n_total=60, species="S. mansoni", design="Comparative pathological series",
    outcomes_reported_in_abstract="p53 IHC; DCC; MLH1/MSH2 (MMR); MSI; stage III-IV; synchronous tumours; mucinous histology",
    overlap_group="G8-Alexandria", analysis_set="Separate species stratum (S. mansoni) - not pooled with S. japonicum",
    eligibility_status="Eligible - species-separate", verification_ids="PMID/DOI matched", verification_numbers="counts seen only in search summary - MUST re-extract")
add(study_id="Yang2023", first_author="Yang Y", year=2023,
    title="Clinicopathological characteristics and its association with digestive system tumors of 1111 patients with Schistosomiasis japonica",
    journal="Sci Rep", volume_pages="NR", pmid="37704736", doi="10.1038/s41598-023-42456-9", pmcid="PMC10500003",
    institution="Yijishan Hospital of Wannan Medical College", city_province="Wuhu, Anhui", recruitment_period="NR", n_SACC="NR (1111 schistosomiasis patients, all sites)",
    species="S. japonicum", design="Retrospective pathology series", outcomes_reported_in_abstract="Age, sex, differentiation in schistosomiasis-associated vs non-schistosomiasis tumours (multiple organs)",
    overlap_group="G2-Wuhu-Yijishan", analysis_set="Check whether CRC-specific comparator data are separable",
    eligibility_status="Uncertain - CRC separability and overlap with WangZ2020", verification_ids="PMID/DOI/PMCID matched", verification_numbers="none")
# ---------------- Within-SACC prognostic set ----------------
add(study_id="WangM2016", first_author="Wang M", year=2016, title="Clinicopathological characteristics and prognosis of schistosomal colorectal cancer",
    journal="Colorectal Dis", volume_pages="18:1005-1009", pmid="26922912", doi="10.1111/codi.13317", institution="West China Hospital, Sichuan University (verify)",
    city_province="Chengdu, Sichuan", species="S. japonicum (to verify)", design="Retrospective SACC-only cohort",
    outcomes_reported_in_abstract="Egg deposition site; CEA; pT; pN; resection margin eggs; OS",
    overlap_group="G6-Chengdu-WestChina", analysis_set="Within-SACC prognostic", eligibility_status="Eligible - within-SACC only (no NSACC comparator)",
    verification_ids="PMID/DOI matched", verification_numbers="none")
add(study_id="Pan2023", first_author="Pan W", year=2023, title="Presence of schistosome eggs in lymph node predict unfavorable prognosis in schistosomal colorectal cancer",
    journal="Eur J Cancer Prev", volume_pages="32(6):566-574", pmid="37200090", doi="10.1097/CEJ.0000000000000811", pmcid="PMC10538618",
    institution="NR - authors (Pan W, Hou Y) overlap with Zhongshan/Fudan group; one search summary said West China - VERIFY",
    city_province="NR", n_SACC=172, species="S. japonicum (to verify)", design="Retrospective SACC-only cohort",
    outcomes_reported_in_abstract="Eggs in lymph nodes (83 patients); hepatic schistosomiasis; DFS; OS in stage III",
    overlap_group="G3? (suspected, via authors)", analysis_set="Within-SACC prognostic", eligibility_status="Eligible - within-SACC only",
    verification_ids="PMID/DOI/PMCID matched", verification_numbers="n from abstract")
add(study_id="Liu2013", first_author="Liu W", year=2013,
    title="Schistosomiasis combined with colorectal carcinoma diagnosed based on endoscopic findings and clinicopathological characteristics: a report on 32 cases",
    journal="Asian Pac J Cancer Prev", volume_pages="14(8):4839-4842", pmid="24083755", doi="10.7314/APJCP.2013.14.8.4839",
    n_SACC=32, species="S. japonicum (to verify)", design="Case series", outcomes_reported_in_abstract="Endoscopic and clinicopathological description",
    overlap_group="Unknown", analysis_set="Within-SACC descriptive", eligibility_status="Comparator not confirmed - provisionally EXCLUDED from comparative synthesis",
    verification_ids="Citation matched; PMID/DOI as supplied by user and consistent with index", verification_numbers="n from title")
add(study_id="Zhou_CT2012", first_author="[to verify]", year=2012, title="CT presentations of colorectal cancer with chronic schistosomiasis: a comparative study with pathological findings",
    journal="Eur J Radiol", volume_pages="81(8):e835-e843", pmid="22658847", n_SACC=130, species="S. japonicum (calcified ova)",
    design="Imaging-pathology correlation, SACC only", outcomes_reported_in_abstract="Multifocality (21/130 per summary); mucinous histology; calcification",
    analysis_set="Within-SACC descriptive", eligibility_status="No NSACC comparator - descriptive only", verification_ids="PMID matched", verification_numbers="summary-level")
add(study_id="Genomic2023", first_author="[to verify]", year=2023, title="Genomic analysis of schistosomiasis-associated colorectal cancer reveals a unique mutational landscape and therapeutic implications",
    journal="Genes Dis", pmid="37396536", doi="10.1016/j.gendis.2022.05.026", pmcid="PMC10308108", institution="Changzheng Hospital, Naval Medical University",
    city_province="Shanghai", recruitment_period="2014-2020", n_SACC=30, species="S. japonicum (to verify)", design="Whole-exome sequencing, SACC tumours vs external sporadic-CRC data",
    outcomes_reported_in_abstract="TMB (median 1.61/Mb vs 2.03/Mb in sporadic CRC); MSI-L/MSS; recurrently mutated genes",
    analysis_set="Molecular evidence table (external comparator - not poolable)", eligibility_status="Molecular map only",
    verification_ids="PMID/DOI/PMCID matched", verification_numbers="summary-level")
# ---------------- Epidemiological risk set (kept separate) ----------------
add(study_id="XuSu1984", first_author="Xu Z", year=1984, title="Schistosoma japonicum and colorectal cancer: an epidemiological study in the People's Republic of China",
    journal="Int J Cancer", volume_pages="34(3):315-318", pmid="6480152", doi="10.1002/ijc.2910340305", species="S. japonicum",
    design="Ecological / matched analysis", analysis_set="Epidemiological risk (separate)", eligibility_status="Excluded from phenotype synthesis; cited in Introduction",
    verification_ids="PMID/DOI matched", verification_numbers="RR reported in abstract - verify before citing")
add(study_id="Qiu2005", first_author="Qiu DC", year=2005, title="A matched, case-control study of the association between Schistosoma japonicum and liver and colon cancers, in rural China",
    journal="Ann Trop Med Parasitol", volume_pages="99(1):47-52", pmid="15701255", species="S. japonicum", design="Matched case-control",
    analysis_set="Epidemiological risk (separate)", eligibility_status="Excluded from phenotype synthesis; cited in Introduction", verification_ids="PMID matched")
add(study_id="LiuXF2023", first_author="Liu XF", year=2023, title="The prevalence rate, mortality, and 5-year overall survival of Schistosoma japonicum patients with human malignancy",
    journal="Front Oncol", pmid="38125940", doi="10.3389/fonc.2023.1288197", pmcid="PMC10731309", n_total=5866, species="S. japonicum",
    design="Hospital-based retrospective (all malignancies)", analysis_set="Epidemiological / background", eligibility_status="Check whether CRC-specific SACC vs NSACC data are separable",
    verification_ids="PMID/DOI/PMCID matched")

with open("data/study_inventory.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(S)

OV = [
 ("Zheng2023","Changhai Hospital, Shanghai","2001-2021","823","30330","Genomic2023 (Changzheng Hospital, Shanghai; different hospital, same health system)","Retain; confirm no shared patients with Genomic2023"),
 ("WangZ2020","Yijishan Hospital, Wuhu","NR","253","2885","Yang2023 (same hospital)","Retain WangZ2020 for CRC outcomes; use Yang2023 only if CRC data are separable and non-duplicative"),
 ("WangW2020","Qingpu Branch, Zhongshan Hospital, Shanghai","2008-2016","137","214","WangW2021, WangW2023, Pan2020, BMCGastro2023, Pan2023 (shared authors/institution)","Index study for clinicopathological and OS outcomes of group G3"),
 ("WangW2021","Qingpu Branch, Zhongshan Hospital","NR","NR","NR (338 total)","WangW2020","Use only for CD8/PD-L1; never re-enter OS or clinicopathology"),
 ("WangW2023","Qingpu Branch, Zhongshan Hospital","NR","NR","NR (349 total)","WangW2020","Use only for sTIL/CD3/CD20"),
 ("Pan2020","Zhongshan Hospital (Fudan) / Qingpu","NR","NR","NR (354 total)","WangW2020","Use only for c-MYC"),
 ("BMCGastro2023","NR (suspected Qingpu)","NR","NR","NR","WangW2020 (suspected)","Use only for CD4/CD8/CRP after institution check"),
 ("Li2024","Union Hospital, Wuhan","NR","30","459","None identified","Retain"),
 ("Zhang2023","Jingzhou Hospital, Hubei","2020-2022","101","240","Zhu2024 (shared author, identical period)","Choose larger/more complete per outcome after full-text check; never pool both for same outcome"),
 ("Zhu2024","Central China (verify)","2020-2022","95","406","Zhang2023","See Zhang2023"),
 ("WangM2014","West China Hospital, Chengdu","NR","30","30 (matched)","WangM2016 (same group; within-SACC)","Survival only in primary set; WangM2016 kept in within-SACC set"),
 ("NCG1986","Multicentre, China","NR","430","NR","None identified (historical)","Retain if comparator data extractable"),
 ("Madbouly2007","Alexandria, Egypt","NR","40","20","None","S. mansoni stratum only"),
 ("Pan2023","NR (verify)","NR","172","0","G3 (suspected via authors)","Within-SACC only"),
 ("WangM2016","West China Hospital, Chengdu","NR","NR","0","WangM2014","Within-SACC only"),
]
with open("data/overlap_matrix.csv","w",newline="") as f:
    w = csv.writer(f); w.writerow(["study_id","hospital","recruitment_dates","SACC_n","NSACC_n","potential_overlap","decision"]); w.writerows(OV)
print(len(S), "inventory rows;", len(OV), "overlap rows")
