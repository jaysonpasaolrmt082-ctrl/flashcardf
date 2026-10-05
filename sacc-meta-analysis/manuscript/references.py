"""Reference registry (ICMJE/Vancouver style, as required by Acta Medica Philippina).

status:
  "ids"     - title, journal, PMID and/or DOI matched to a PubMed/PMC/publisher index
              entry via web search on 2026-10-05 (full text NOT accessed)
  "std"     - standard methods reference
  "verify"  - one or more bibliographic elements (authors/year/pages) still missing;
              shown highlighted in the manuscript and MUST be completed from PubMed
Numbers are assigned in order of first citation by build_manuscript.py.
"""

REFS = {
 # ---------------- background ----------------
 "bray2024": ("Bray F, Laversanne M, Sung H, Ferlay J, Siegel RL, Soerjomataram I, et al. Global cancer statistics 2022: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries. CA Cancer J Clin. 2024;74(3):229-63. doi:10.3322/caac.21834", "std"),
 "demartel2020": ("de Martel C, Georges D, Bray F, Ferlay J, Clifford GM. Global burden of cancer attributable to infections in 2018: a worldwide incidence analysis. Lancet Glob Health. 2020;8(2):e180-90. doi:10.1016/S2214-109X(19)30488-7", "std"),
 "iarc61": ("International Agency for Research on Cancer. Schistosomes, liver flukes and Helicobacter pylori. IARC Monographs on the Evaluation of Carcinogenic Risks to Humans, Vol. 61. Lyon: IARC; 1994.", "ids"),
 "iarc100b": ("International Agency for Research on Cancer. Biological agents. IARC Monographs on the Evaluation of Carcinogenic Risks to Humans, Vol. 100B. Lyon: IARC; 2012.", "ids"),
 "who_schisto": ("World Health Organization. Schistosomiasis [Internet]. Geneva: WHO; [cited YYYY Mon DD]. Available from: https://www.who.int/news-room/fact-sheets/detail/schistosomiasis", "verify"),
 "gordon2015": ("Gordon CA, Acosta LP, Gobert GN, Olveda RM, Ross AG, Williams GM, et al. Real-time PCR demonstrates high prevalence of Schistosoma japonicum in the Philippines: implications for surveillance and control. PLoS Negl Trop Dis. 2015;9(1):e0003483. doi:10.1371/journal.pntd.0003483", "verify"),
 "indo2026": ("[Authors to be verified]. Schistosomiasis japonicum in Indonesia: progress and surveillance needs in verge-of-elimination settings. Trop Med Infect Dis. 2026;11(4):86. doi:10.3390/tropicalmed11040086", "verify"),
 "hamid2019": ("Hamid HKS. Schistosoma japonicum-associated colorectal cancer: a review. Am J Trop Med Hyg. 2019;100(3):501-5. doi:10.4269/ajtmh.18-0807", "ids"),
 "hamid2010": ("Hamid HKS, Mekki SO, Suleiman SH, Ibrahim SZ. Colorectal carcinoma associated with schistosomiasis: a possible causal relationship. World J Surg Oncol. 2010;8:68. doi:10.1186/1477-7819-8-68. PMID: 20704754", "ids"),
 "xusu1984": ("Xu Z, Su DL. Schistosoma japonicum and colorectal cancer: an epidemiological study in the People's Republic of China. Int J Cancer. 1984;34(3):315-8. doi:10.1002/ijc.2910340305. PMID: 6480152", "ids"),
 "qiu2005": ("Qiu DC, Hubbard AE, Zhong B, Zhang Y, Spear RC. A matched, case-control study of the association between Schistosoma japonicum and liver and colon cancers, in rural China. Ann Trop Med Parasitol. 2005;99(1):47-52. PMID: 15701255", "ids"),
 "liuxf2023": ("Liu XF, Ju S, Wang KY, Li Y, Qiang JW. The prevalence rate, mortality, and 5-year overall survival of Schistosoma japonicum patients with human malignancy. Front Oncol. 2023;13:1288197. doi:10.3389/fonc.2023.1288197. PMID: 38125940", "ids"),
 "global_ipi2025": ("[Authors to be verified]. Global prevalence and correlation of intestinal parasitic infections in patients with colorectal cancer: a systematic review and meta-analysis. BMC Gastroenterol. 2025. doi:10.1186/s12876-025-04144-y. PMID: 40804378", "verify"),
 "actapara2023": ("[Authors to be verified]. Schistosoma japonicum associated colorectal cancer and its management. Acta Parasitol. 2023. doi:10.1007/s11686-023-00707-9. PMID: 37594685", "verify"),
 # ---------------- primary studies ----------------
 "zheng2023": ("Zheng N, et al. Changing trends, clinicopathological characteristics, surgical treatment patterns, and prognosis of schistosomiasis-associated versus non-schistosomiasis-associated colorectal cancer: a large retrospective cohort study of 31 153 cases in Shanghai, China (2001-2021). Int J Surg. 2023;109(4):772-84. doi:10.1097/JS9.0000000000000293. PMID: 36999800", "verify"),
 "wangz2020": ("Wang Z, Du Z, Liu Y, Wang W, Liang M, Zhang A, et al. Comparison of the clinicopathological features and prognoses of patients with schistosomal and nonschistosomal colorectal cancer. Oncol Lett. 2020;19:2375-83. doi:10.3892/ol.2020.11331. PMID: 32194737", "ids"),
 "wangw2020": ("Wang W, Lu K, Wang L, et al. Comparison of non-schistosomal colorectal cancer and schistosomal colorectal cancer. World J Surg Oncol. 2020;18:149. doi:10.1186/s12957-020-01925-5. PMID: 32611359", "verify"),
 "wangw2021": ("Wang W, Jing H, Liu J, Bu D, Zhang Y, Zhu T, et al. Correlation between schistosomiasis and CD8+ T cell and stromal PD-L1 as well as the different prognostic role of CD8+ T cell and PD-L1 in schistosomal-associated colorectal cancer and non-schistosomal-associated colorectal cancer. World J Surg Oncol. 2021;19:[pages to verify]. doi:10.1186/s12957-021-02433-w. PMID: 34743724", "verify"),
 "wangw2023": ("Wang W, Zhang Y, Liu J, Jing H, Lu K, Wang L, et al. Comparison of the prognostic value of stromal tumor-infiltrating lymphocytes and CD3+ T cells between schistosomal and non-schistosomal colorectal cancer. World J Surg Oncol. 2023;21:[pages to verify]. doi:10.1186/s12957-023-02911-3. PMID: 36726115", "verify"),
 "bmcgastro2023": ("[Authors to be verified]. The predictive value of CD4, CD8, and C-reactive protein in the prognosis of schistosomal and non-schistosomal colorectal cancer. BMC Gastroenterol. 2023;23:[pages to verify]. doi:10.1186/s12876-023-02834-z. PMID: 37277702", "verify"),
 "pan2020": ("Pan W, Wang W, Huang J, Lu K, Huang S, Jiang D, et al. The prognostic role of c-MYC amplification in schistosomiasis-associated colorectal cancer. Jpn J Clin Oncol. 2020;50(4):446-55. doi:10.1093/jjco/hyz210. PMID: 32297641", "ids"),
 "li2024": ("Li X, Liu H, Huang B, Yang M, Fan J, Zhang J, et al. Schistosoma infection, KRAS mutation status, and prognosis of colorectal cancer. Chin Med J (Engl). 2024;137(2):235-7. doi:10.1097/CM9.0000000000002905. PMID: 37920960", "ids"),
 "zhang2023": ("Zhang F, Wang X, Zhu Y, Xia P. Conjoint analysis of clinical, imaging, and pathological features of schistosomiasis and colorectal cancer. Pathol Oncol Res. 2023;29:1611396. doi:10.3389/pore.2023.1611396. PMID: 38099242", "ids"),
 "zhu2024": ("Zhu Y, et al. A retrospective cross-sectional study: comparison of the clinicopathological features of schistosomal and non-schistosomal colorectal cancer in Central China. BMC Infect Dis. 2024;24:[pages to verify]. doi:10.1186/s12879-024-09648-8. PMID: 39054428", "verify"),
 "wangm2014": ("Wang M, et al. Prognostic analysis of schistosomal rectal cancer. Asian Pac J Cancer Prev. 2014;15(21):9271-5. doi:10.7314/apjcp.2014.15.21.9271. PMID: 25422211", "verify"),
 "ncg1986": ("National Cooperative Group on Pathology and Prognosis of Colorectal Cancer. [Schistosomiasis and its prognostic significance in patients with colorectal cancer]. Zhonghua Zhong Liu Za Zhi. 1986;8(2):149-51. Chinese. PMID: 3021419", "ids"),
 "madbouly2007": ("Madbouly KM, Senagore AJ, Mukerjee A, Hussien AM, Shehata MA, Navine P, et al. Colorectal cancer in a population with endemic Schistosoma mansoni: is this an at-risk population? Int J Colorectal Dis. 2007;22:175-81. doi:10.1007/s00384-006-0144-3. PMID: 16786317", "ids"),
 "yang2023": ("Yang Y, Wang XY, Duan C, et al. Clinicopathological characteristics and its association with digestive system tumors of 1111 patients with Schistosomiasis japonica. Sci Rep. 2023;13:[pages to verify]. doi:10.1038/s41598-023-42456-9. PMID: 37704736", "verify"),
 "wangm2016": ("Wang M, Wu QB, He WB, Wang ZQ. Clinicopathological characteristics and prognosis of schistosomal colorectal cancer. Colorectal Dis. 2016;18:1005-9. doi:10.1111/codi.13317. PMID: 26922912", "ids"),
 "pan2023": ("Pan W, Guo J, Li J, Su J, Zhang X, Liu J, et al. Presence of schistosome eggs in lymph node predict unfavorable prognosis in schistosomal colorectal cancer. Eur J Cancer Prev. 2023;32(6):566-74. doi:10.1097/CEJ.0000000000000811. PMID: 37200090", "ids"),
 "liu2013": ("Liu W, Zeng HZ, Wang QM, et al. Schistosomiasis combined with colorectal carcinoma diagnosed based on endoscopic findings and clinicopathological characteristics: a report on 32 cases. Asian Pac J Cancer Prev. 2013;14(8):4839-42. doi:10.7314/APJCP.2013.14.8.4839. PMID: 24083755", "ids"),
 "zhou_ct2012": ("[Authors to be verified]. CT presentations of colorectal cancer with chronic schistosomiasis: a comparative study with pathological findings. Eur J Radiol. 2012;81(8):e835-43. PMID: 22658847", "verify"),
 "genomic2023": ("[Authors to be verified]. Genomic analysis of schistosomiasis-associated colorectal cancer reveals a unique mutational landscape and therapeutic implications. Genes Dis. 2023. doi:10.1016/j.gendis.2022.05.026. PMID: 37396536", "verify"),
 # ---------------- mechanism ----------------
 "tam2021": ("[Authors to be verified]. Polarization of intestinal tumour-associated macrophages regulates the development of schistosomal colorectal cancer. J Cancer. 2021;12:1033-[pages to verify].", "verify"),
 "sea2025": ("[Authors to be verified]. A hidden \"promoter\": Schistosoma japonicum soluble egg antigen activates MAPK/PI3K-AKT pathways and inhibits autophagy to facilitate colorectal cancer. Infect Immun. [year to verify]. doi:10.1128/iai.00696-25", "verify"),
 "wnt2020": ("[Authors to be verified]. Schistosoma mansoni eggs induce Wnt/beta-catenin signaling and activate the protooncogene c-Jun in human and hamster colon. Sci Rep. [year to verify]. doi:10.1038/s41598-020-79450-4", "verify"),
 # ---------------- methods ----------------
 "page2021": ("Page MJ, McKenzie JE, Bossuyt PM, Boutron I, Hoffmann TC, Mulrow CD, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ. 2021;372:n71. doi:10.1136/bmj.n71", "std"),
 "rethlefsen2021": ("Rethlefsen ML, Kirtley S, Waffenschmidt S, Ayala AP, Moher D, Page MJ, et al. PRISMA-S: an extension to the PRISMA statement for reporting literature searches in systematic reviews. Syst Rev. 2021;10:39. doi:10.1186/s13643-020-01542-z", "std"),
 "wells_nos": ("Wells GA, Shea B, O'Connell D, Peterson J, Welch V, Losos M, et al. The Newcastle-Ottawa Scale (NOS) for assessing the quality of nonrandomised studies in meta-analyses [Internet]. Ottawa: Ottawa Hospital Research Institute; [cited YYYY Mon DD]. Available from: https://www.ohri.ca/programs/clinical_epidemiology/oxford.asp", "std"),
 "tierney2007": ("Tierney JF, Stewart LA, Ghersi D, Burdett S, Sydes MR. Practical methods for incorporating summary time-to-event data into meta-analysis. Trials. 2007;8:16. doi:10.1186/1745-6215-8-16", "std"),
 "guyot2012": ("Guyot P, Ades AE, Ouwens MJ, Welton NJ. Enhanced secondary analysis of survival data: reconstructing the data from published Kaplan-Meier survival curves. BMC Med Res Methodol. 2012;12:9. doi:10.1186/1471-2288-12-9", "std"),
 "wan2014": ("Wan X, Wang W, Liu J, Tong T. Estimating the sample mean and standard deviation from the sample size, median, range and/or interquartile range. BMC Med Res Methodol. 2014;14:135. doi:10.1186/1471-2288-14-135", "std"),
 "viechtbauer2010": ("Viechtbauer W. Conducting meta-analyses in R with the metafor package. J Stat Softw. 2010;36(3):1-48. doi:10.18637/jss.v036.i03", "std"),
 "higgins2002": ("Higgins JPT, Thompson SG. Quantifying heterogeneity in a meta-analysis. Stat Med. 2002;21(11):1539-58. doi:10.1002/sim.1186", "std"),
 "egger1997": ("Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. BMJ. 1997;315(7109):629-34. doi:10.1136/bmj.315.7109.629", "std"),
 "sterne2011": ("Sterne JAC, Sutton AJ, Ioannidis JPA, Terrin N, Jones DR, Lau J, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. BMJ. 2011;343:d4002. doi:10.1136/bmj.d4002", "std"),
 "guyatt2008": ("Guyatt GH, Oxman AD, Vist GE, Kunz R, Falck-Ytter Y, Alonso-Coello P, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. BMJ. 2008;336(7650):924-6. doi:10.1136/bmj.39489.470347.AD", "std"),
 "rcore": ("R Core Team. R: a language and environment for statistical computing. Version 4.3.3. Vienna: R Foundation for Statistical Computing; 2024.", "std"),
}
