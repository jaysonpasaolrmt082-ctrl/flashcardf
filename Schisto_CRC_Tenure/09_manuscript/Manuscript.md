<!--
SUBMISSION-READY TEMPLATE. Every value shown as ⟦R: …⟧ is a result slot.
Fill it ONLY from the file named in the slot, after running 04_R_scripts/run_all.sh.
Search for "⟦" before submission — zero matches must remain.
Paragraphs marked ⟦ADAPT⟧ contain interpretation that must be checked against the
actual direction of the findings (e.g., if DNA_REPAIR is not enriched, rewrite that paragraph).
Target: Acta Medica Philippina (Original Article; structured abstract ≤ 250 words; Vancouver/AMA refs).
-->

# Cross-Species Transcriptomic Analysis Identifies Colorectal Cancer-Associated Molecular Pathways Induced by *Schistosoma japonicum* Infection

**Running title:** *S. japonicum* colon signature and colorectal cancer

**Jayson Cagadas Pasaol, DVM, PhD**¹\*

¹ ⟦Department⟧, ⟦College⟧, University of the Philippines Manila, Manila, Philippines

\* **Corresponding author:** Jayson Cagadas Pasaol · ⟦institutional address⟧ · jaysonpasaolrmt082@gmail.com (⟦replace with up.edu.ph address⟧) · ORCID ⟦0000-0000-0000-0000⟧

**Word count:** abstract ⟦n⟧; main text ⟦n⟧ · **Figures:** 6 · **Tables:** 3 · **Supplementary files:** 6

---

## ABSTRACT

**Background and Objective.** *Schistosoma japonicum* remains endemic in the Philippines, China and Indonesia. Chronic intestinal infection has been associated epidemiologically and histopathologically with colorectal neoplasia, but the molecular overlap between parasite-induced colonic host responses and human colorectal carcinogenesis is poorly characterized. We asked whether *S. japonicum* infection induces colonic transcriptional programs that overlap with those of human colorectal adenocarcinoma, with emphasis on inflammation, oxidative stress and the DNA-damage response (DDR).

**Methods.** An infection-associated signature from *S. japonicum*-infected versus uninfected mouse colon (8 weeks post-infection) was mapped to one-to-one human orthologues and integrated with differential expression of TCGA colon (COAD; ⟦R: n tumour/n normal — 05_results/03_TCGA-COAD_summary.txt⟧) and rectal (READ) adenocarcinoma versus normal mucosa. Overlap, directional concordance, Hallmark and pre-specified DDR gene-set enrichment, STRING protein–protein interaction analysis and exploratory clinical and immune-infiltration associations were evaluated under a pre-registered analysis plan.

**Results.** Of ⟦R⟧ infection-associated orthologues, ⟦R⟧ were also dysregulated in COAD (⟦R⟧-fold over expectation; hypergeometric *P* = ⟦R⟧), of which ⟦R⟧% changed in the same direction (binomial *P* = ⟦R⟧). ⟦R: list of pathways enriched in the same direction in both — 05_results/05_gsea_all.tsv⟧ were shared. Network analysis identified ⟦R: hub genes — 05_results/06_hubs.tsv⟧ as candidate hub genes; ⟦R⟧ of ⟦R⟧ concordant genes replicated in READ.

**Conclusion.** ⟦ADAPT⟧ *S. japonicum* infection induces a colonic host-response program that partially recapitulates inflammatory, oxidative-stress and genome-maintenance features of human colorectal cancer. These candidate pathways warrant prospective validation in *S. japonicum*-endemic populations.

**Keywords:** schistosomiasis japonica; colorectal neoplasms; transcriptome; DNA repair; inflammation; comparative genomics

---

## INTRODUCTION

Schistosomiasis is a neglected tropical disease that, according to the World Health Organization, required preventive chemotherapy for an estimated 253.7 million people in 2024.¹ *Schistosoma japonicum*, the zoonotic Asian species, remains endemic in the Philippines, the People's Republic of China and Indonesia.¹⁻³ In the Philippines, transmission persists in provinces of the Visayas and Mindanao, where infection is sustained by a broad mammalian reservoir and the amphibious snail host *Oncomelania hupensis quadrasi*.³ Unlike *S. mansoni*, adult *S. japonicum* pairs inhabit the superior mesenteric venous system and release large numbers of eggs, a substantial proportion of which become trapped in the intestinal wall and liver, where they provoke chronic granulomatous inflammation and fibrosis.²,⁴

Chronic inflammation is an established enabling characteristic of cancer.⁵,⁶ Inflammatory cells generate reactive oxygen and nitrogen species that oxidize DNA, induce strand breaks and impair DNA-repair fidelity, and inflammatory cytokine signalling through NF-κB and IL-6/STAT3 promotes epithelial survival and proliferation.⁷,⁸ Inflammatory bowel disease-associated colorectal cancer is the clearest clinical example of this inflammation–genome instability axis in the colon.⁹ Several helminths are recognized carcinogens: the International Agency for Research on Cancer (IARC) classifies *S. haematobium*, *Opisthorchis viverrini* and *Clonorchis sinensis* as Group 1 carcinogens and *S. japonicum* as Group 2B ("possibly carcinogenic to humans").¹⁰,¹¹ Proposed mechanisms of helminth-associated malignancy include chronic inflammation, oxidative DNA damage, parasite-secreted mitogens and immunomodulation.¹²

Evidence linking *S. japonicum* specifically to colorectal cancer (CRC) comes from ecological correlations between schistosomiasis and CRC mortality in endemic regions of China,¹³ and from clinicopathological series describing schistosomal CRC as a distinct entity with egg deposition in tumour tissue and differing clinical features.¹⁴ Colorectal cancer itself is the third most common cancer worldwide,¹⁵ and its molecular landscape has been comprehensively characterized by The Cancer Genome Atlas (TCGA).¹⁶ Nonetheless, this association has not been shown to be causal, and the host molecular programs through which chronic intestinal infection could create a pro-tumorigenic colonic environment remain incompletely characterized.

Recently, Lin et al. generated transcriptomic profiles of colon and small intestine from mice infected with *S. japonicum* for eight weeks and reported 1,693 differentially expressed genes in infected colon, enriched for NF-κB, Th17-differentiation, natural-killer-cell and B-cell signalling pathways.¹⁷ That study focused on the effects of a probiotic intervention and did not relate the infection-induced colonic response to human colorectal carcinogenesis.

We therefore integrated an experimental *S. japonicum*-infected colon transcriptomic signature with human colorectal cancer transcriptomic data to identify conserved molecular pathways potentially connecting chronic parasitic infection with colorectal carcinogenesis. We specifically tested, under a pre-specified analysis plan, whether infection-associated genes overlap with and change in the same direction as genes dysregulated in human colorectal adenocarcinoma, and whether shared programs involve inflammation, oxidative stress and the DNA-damage response.

---

## METHODS

### Study design and analytical framework

This was a secondary, cross-species integrative analysis of publicly available transcriptomic data (Figure 1). The research question, datasets, thresholds, primary and secondary outcomes and sensitivity analyses were specified in an analysis plan frozen before the human overlap analyses were run (Supplementary File 1; ⟦deposit date and DOI/OSF link⟧). Analyses not pre-specified are labelled exploratory. The study was reported in accordance with ⟦e.g., the relevant items of the STREGA/TRIPOD guidance as applicable to secondary omics analyses⟧.

### Public transcriptomic datasets

Datasets are summarized in **Table 1**. The infection dataset was generated by Lin et al.¹⁷ from C57BL/6 ⟦verify strain from source paper⟧ mice percutaneously infected with *S. japonicum* cercariae (SI group) and uninfected controls (NG group); colon tissue was collected at eight weeks post-infection. Raw reads are deposited in the NCBI Sequence Read Archive (SRR15682843–SRR15682848). A third arm treated with *Bacillus subtilis* (SIBS) was excluded from all analyses, because the question concerned infection versus no infection. Accompanying 16S rRNA data (SRR15694234–SRR15694269) were not analysed.

Human data were TCGA colon adenocarcinoma (TCGA-COAD; primary discovery) and rectal adenocarcinoma (TCGA-READ; replication) RNA-seq gene-level counts (GDC harmonized "STAR – Counts" workflow, GENCODE v36), comprising primary tumours and adjacent solid-tissue normal samples.¹⁶

### *S. japonicum* infection-associated gene signature

The primary infection signature was the published DESeq2 comparison of SI versus NG colon (Supplementary Table S5 of Lin et al.¹⁷). Genes with adjusted *P* < 0.05 and |log₂ fold change| ≥ 1 were classified as up- or down-regulated. ⟦If full table available:⟧ For ranked analyses, genes were ranked by the signed statistic sign(log₂FC) × −log₁₀(*P*). We first confirmed that the table reproduced the published counts of 1,693 DEGs (598 up, 1,095 down) (⟦R: 05_results/01_mouse_signature_summary.txt⟧).

For independent re-processing (sensitivity analysis), raw reads were quality-trimmed with fastp¹⁸ and quantified against the Ensembl release 112 GRCm39 transcriptome with Salmon (selective alignment with genomic decoys, GC-bias correction),¹⁹ summarized to gene level with tximport²⁰ and analysed with DESeq2.²¹ ⟦ADAPT — choose one:⟧ (a) Agreement with the published fold-changes was assessed by Spearman correlation (ρ = ⟦R: 05_results/01_reprocessing_agreement.txt⟧). / (b) Because the deposited runs comprise ⟦R: n⟧ colon libraries per group, which is insufficient for dispersion estimation, re-processing was used for quality control and fold-change concordance only, and statistical inference relied on the published signature.

### Mouse-to-human orthologue conversion

Mouse genes were mapped to human orthologues with Ensembl BioMart (release 112) via biomaRt.²² The primary analyses used only one-to-one orthologues. Genes with one-to-many or many-to-many relationships were flagged and not resolved arbitrarily; they were included only in sensitivity analysis 1 (Supplementary Table S2).

### TCGA colorectal cancer data acquisition and differential expression

TCGA data were retrieved with TCGAbiolinks.²³ One aliquot per sample was retained, and analysis was restricted to protein-coding and lncRNA genes with ≥ 10 counts in ≥ 10 samples. Differential expression of primary tumour versus solid-tissue normal was estimated with DESeq2 (Wald test, design ~ condition),²¹ and log₂ fold changes were shrunk with apeglm for display and ranking.²⁴ Human DEGs were defined as Benjamini–Hochberg FDR < 0.05 and |log₂FC| ≥ 1. A paired analysis restricted to patients contributing both tumour and normal samples (design ~ patient + condition) was performed as sensitivity analysis 3.

### Cross-species integrative analysis

The analysis universe consisted of genes that had a one-to-one orthologue and were tested in both datasets. Over-representation of infection-associated DEGs among COAD DEGs was assessed with a one-sided hypergeometric test. Overlapping genes were classified as concordant up (up in infection and tumour), concordant down, or discordant; the proportion concordant was compared with 50% by an exact one-sided binomial test, and fold-change agreement was summarized by Spearman's ρ. Concordant genes were tested for replication in TCGA-READ (same direction, FDR < 0.05). Pre-specified sensitivity analyses comprised (1) inclusion of one-to-many orthologues, (2) a human fold-change threshold of 1.5 (|log₂FC| ≥ 0.58), (3) the paired tumour–normal subset and (4) the re-processed mouse signature.

### Functional enrichment and gene-set enrichment analysis

Gene-set enrichment analysis (GSEA)²⁵ was performed with fgsea²⁶ on Wald-statistic-ranked gene lists using the MSigDB Hallmark collection²⁷ (minimum 15, maximum 500 genes) for COAD, READ and ⟦the mouse signature in orthologue space⟧. Over-representation analysis of up- and down-regulated infection-associated genes was performed with clusterProfiler²⁸ against the same collections using the analysis universe as background, and GO Biological Process and KEGG enrichment was performed on the concordant genes. Sixteen Hallmark pathways covering inflammation (inflammatory response, TNF-α/NF-κB, IL-6/JAK/STAT3, interferon-γ), oxidative stress (reactive oxygen species), genome maintenance and proliferation (DNA repair, p53, E2F targets, G2/M checkpoint, MYC targets), and oncogenic signalling (apoptosis, epithelial–mesenchymal transition, hypoxia, PI3K/AKT/mTOR, TGF-β, WNT/β-catenin) were pre-specified as focus pathways. FDR < 0.05 was considered significant and FDR < 0.25 suggestive.

### DNA-damage-response gene-set analysis

A DDR and genome-stability gene set of 93 genes was defined *a priori* from canonical pathway membership (Supplementary Table S1), comprising DNA-damage sensing (e.g., *ATM*, *ATR*, *H2AX*), checkpoint signalling (*CHEK1*, *CHEK2*, *TP53*), homologous recombination (*BRCA1*, *BRCA2*, *RAD51*, *PALB2*), PARP-dependent single-strand break repair (*PARP1*, *PARP2*, *XRCC1*), mismatch repair (*MLH1*, *MSH2*, *MSH6*, *PMS2*), base and nucleotide excision repair (*OGG1*, *APEX1*, *ERCC* family), non-homologous end joining, replication stress (*RPA1–3*, *WEE1*, *CLSPN*), Fanconi anaemia genes and oxidative-stress generation and defence (*NOS2*, *DUOX2*, *NFE2L2*, *HMOX1*). The full set and each module containing ≥ 5 genes were tested by GSEA and over-representation analysis as above. Individual DDR genes were not required to be DEGs; the question was whether the infection signature as a whole is enriched for genome-maintenance programs.

### Protein–protein interaction network

Concordant genes (up to 150, ranked by the product of absolute mouse and human log₂ fold changes) were mapped to STRING v12 (*Homo sapiens*, combined score ≥ 0.700).²⁹ Degree, normalized betweenness and Maximal Clique Centrality (MCC, as implemented in cytoHubba³⁰) were computed in igraph,³¹ and the ten genes with the best mean rank across the three metrics were designated *candidate hub genes*. Modules were detected with the Louvain algorithm.³² Network centrality was interpreted as a prioritization criterion, not as evidence of causal importance.

### Human CRC validation (exploratory)

For candidate hub genes and concordant DDR genes, variance-stabilized expression was compared between tumour and normal samples (Wilcoxon rank-sum test) in COAD and READ. Discrimination between tumour and normal was described by single-gene ROC area under the curve (AUC) with DeLong 95% confidence intervals (pROC³³); no multivariable classifier was built. Association with AJCC pathological stage (I–IV) was tested with Spearman correlation and with overall survival with Cox proportional-hazards models adjusted for age, sex and stage (expression standardized per SD), supplemented by Kaplan–Meier curves. *P* values were BH-adjusted within each dataset.

### Immune infiltration analysis (exploratory)

Abundances of eight immune and two stromal populations in COAD tumours were estimated with MCP-counter,³⁴ and an M2-like macrophage score was calculated as the mean expression of *CD163*, *MRC1*, *MSR1*, *CD209* and *F13A1*, given the type 2 immune environment characteristic of schistosome egg granulomas.³⁵ Spearman correlations between candidate genes and cell scores were BH-adjusted.

### Statistical analysis and reproducibility

All analyses were performed in R ⟦version⟧ with Bioconductor ⟦version⟧. Multiple testing was controlled with the Benjamini–Hochberg procedure. The random seed was fixed (20261005). Code, package versions (sessionInfo) and intermediate tables are available at ⟦GitHub URL⟧ and archived at ⟦Zenodo DOI⟧.

### Ethics statement

This study used only publicly available, de-identified data and did not involve recruitment of human participants or the use of experimental animals by the author. TCGA data were generated under the consent and governance of the TCGA program, and the animal data under the approvals reported by the original investigators.¹⁷ ⟦Insert UP Manila REB exemption / non-human-subject determination reference number, if obtained.⟧

---

## RESULTS

### *S. japonicum* infection induces a distinct colonic transcriptional response

The SI-versus-NG colon signature comprised ⟦R⟧ differentially expressed genes (⟦R⟧ up, ⟦R⟧ down), ⟦reproducing / differing from⟧ the 1,693 reported by the original authors (Figure 2A; ⟦R: 05_results/01_mouse_signature_summary.txt⟧). The most strongly up-regulated genes included ⟦R: top 5–8 up — 03_processed_data/mouse_signature.tsv⟧ and the most strongly down-regulated included ⟦R⟧ (Figure 2B). ⟦If 01c ran: Principal component analysis separated infected from control colon along PC1 (⟦R⟧% variance; Figure 2C), and re-processed fold-changes agreed with the published estimates (ρ = ⟦R⟧).⟧

### Cross-species mapping identifies infection-associated human orthologues

Of ⟦R⟧ mouse genes in the signature, ⟦R⟧ (⟦R⟧%) had a one-to-one human orthologue, including ⟦R⟧ of the infection DEGs (⟦R⟧ up, ⟦R⟧ down); ⟦R⟧ genes with ambiguous orthology were flagged (Supplementary Table S2; ⟦R: 05_results/02_orthologue_summary.txt⟧).

### A subset of infection-associated genes is dysregulated in human colorectal cancer

TCGA-COAD comprised ⟦R⟧ primary tumours and ⟦R⟧ normal samples, with ⟦R⟧ DEGs (⟦R⟧ up, ⟦R⟧ down) among ⟦R⟧ genes tested (⟦R: 05_results/03_TCGA-COAD_summary.txt⟧). Within the shared universe of ⟦R⟧ genes, ⟦R⟧ infection-associated genes were also COAD DEGs, ⟦R⟧-fold more than expected by chance (hypergeometric *P* = ⟦R⟧; Figure 3A). Of these, ⟦R⟧ (⟦R⟧%) were directionally concordant — ⟦R⟧ concordant up and ⟦R⟧ concordant down — exceeding the 50% expected under independence (binomial *P* = ⟦R⟧), and mouse and human fold-changes were ⟦positively⟧ correlated (Spearman ρ = ⟦R⟧, *P* = ⟦R⟧; Figure 3B; all from ⟦05_results/04_overlap_stats.tsv⟧). The leading concordant genes are listed in **Table 2**. Of the concordant genes, ⟦R⟧ (⟦R⟧%) were replicated in TCGA-READ. Results were ⟦robust / sensitive⟧ to inclusion of one-to-many orthologues, a relaxed fold-change threshold and the paired tumour–normal design (Supplementary Table S5).

### Shared pathways converge on inflammatory and carcinogenic signalling

⟦ADAPT⟧ Among the 16 pre-specified Hallmark pathways, ⟦R⟧ were enriched in the same direction in the infection signature and in both COAD and READ (Figure 4A; ⟦R: 05_results/05_gsea_all.tsv, 05_ora_mouse_hallmark_ddr.tsv⟧). Inflammatory programs — ⟦TNF-α signalling via NF-κB (NES = ⟦R⟧, FDR = ⟦R⟧), inflammatory response (⟦R⟧) and IL-6/JAK/STAT3 signalling (⟦R⟧)⟧ — were ⟦R⟧. ⟦Discordant pathways, e.g. those reflecting proliferation in tumours but not infected mucosa, should be reported here.⟧ GO Biological Process analysis of the concordant genes highlighted ⟦R: top 5 terms — 05_results/05_concordant_GO_BP.tsv⟧ (Figure 4B).

### DNA-damage-response and oxidative-stress programs are altered

⟦ADAPT⟧ The pre-specified DDR set was ⟦R: enriched/not enriched⟧ in the infection signature (NES = ⟦R⟧, FDR = ⟦R⟧) and ⟦R⟧ in COAD (NES = ⟦R⟧, FDR = ⟦R⟧). At module level, ⟦R: modules significant in both, e.g. oxidative-stress generation (*NOS2*, *DUOX2*), base excision repair⟧ (Figure 4C). Concordantly dysregulated DDR genes were ⟦R: genes⟧ (Table 3).

### Network analysis prioritizes candidate hub genes

The STRING network of ⟦R⟧ concordant genes contained ⟦R⟧ nodes and ⟦R⟧ edges (score ≥ 0.700), organized into ⟦R⟧ modules (Figure 5). The candidate hub genes were ⟦R: 10 genes — 05_results/06_hubs.tsv⟧ (Table 3). ⟦Describe dominant module(s), e.g. chemokine/cytokine module, cell-cycle module.⟧

### Candidate conserved genes show clinical associations in human CRC

In exploratory analyses, ⟦R⟧ of ⟦R⟧ candidate genes differed between tumour and normal tissue in both COAD and READ after correction (Figure 6A; ⟦05_results/07_validation.tsv⟧), with single-gene AUCs ranging from ⟦R⟧ to ⟦R⟧ (Figure 6B). ⟦R⟧ genes were associated with stage and ⟦R⟧ with overall survival after adjustment (⟦gene: HR per SD = ⟦R⟧, 95% CI ⟦R⟧, FDR = ⟦R⟧⟧). In COAD tumours, ⟦R: genes⟧ correlated with ⟦R: cell types, e.g. M2-like macrophage score (ρ = ⟦R⟧)⟧ (Figure 6C; ⟦05_results/08_immune_correlations.tsv⟧).

---

## DISCUSSION

⟦ADAPT — rewrite the first paragraph strictly from the results.⟧ By integrating an experimental *S. japonicum*-infected colon transcriptome with large human colorectal cancer cohorts, we found that infection-associated genes overlapped with tumour-associated genes more than expected by chance and changed predominantly in the same direction. The shared program was characterized by ⟦inflammatory (NF-κB, IL-6/JAK/STAT3), oxidative-stress and genome-maintenance⟧ signatures, and network analysis prioritized ⟦hub genes⟧ as candidate conserved nodes, ⟦several⟧ of which were associated with clinical features of human CRC. To our knowledge ⟦verify by systematic search immediately before submission⟧, this is among the first studies to relate the colonic host response to *S. japonicum* directly to human colorectal cancer transcriptomes and to interrogate DDR pathways in this context.

These findings fit the established model in which chronic inflammation creates a permissive environment for colorectal carcinogenesis.⁵⁻⁹ In colitis-associated cancer, sustained NF-κB and STAT3 activation in epithelial and myeloid cells promotes epithelial survival and proliferation, and inflammatory oxidants generate oxidative base lesions and strand breaks.⁷⁻⁹ Schistosome eggs deposited in the intestinal wall provoke granulomatous inflammation that persists for as long as egg deposition continues,²,⁴ offering a plausible source of chronic, focal inflammatory and oxidative stress in colonic mucosa. ⟦ADAPT: relate to which specific inflammatory genes/pathways were concordant.⟧

The DDR component is, in our view, the most informative aspect of the analysis. ⟦ADAPT: If DDR/ROS enrichment was observed —⟧ Concordant dysregulation of ⟦genes⟧ suggests that the infected colon experiences genotoxic and replication stress of a kind also present in colorectal tumours. Because colorectal cancers frequently show defects in mismatch repair or chromosomal stability,¹⁶ an inflammation-driven DDR burden in non-malignant mucosa could plausibly favour mutation accumulation. ⟦If not observed —⟧ The absence of strong DDR enrichment in the infection signature indicates that, at eight weeks, the host response is dominated by inflammatory and immune programs rather than by a transcriptional DNA-repair response; DNA damage itself (e.g., γH2AX, 8-oxo-dG) may nonetheless occur without detectable transcriptional change and should be measured directly. In either case, PARP-dependent repair is of particular interest: PARP1 is central to base-excision and single-strand-break repair of oxidative lesions, and tumours with impaired homologous recombination are sensitive to PARP inhibition.³⁶ Whether parasite-associated colorectal lesions show distinctive DDR states that create therapeutic vulnerabilities is an open, testable question.

Helminth infections induce type 2 immunity, with alternatively activated (M2-like) macrophages that drive granuloma formation and fibrosis.³⁵ M2-like tumour-associated macrophages are in turn associated with immunosuppression and tumour progression. ⟦ADAPT: report whether candidate genes correlated with M2-like or Treg scores.⟧ This suggests a hypothesis in which parasite-induced immune remodelling contributes, alongside genotoxic stress, to a pro-tumorigenic host state (Figure 7, conceptual model): *S. japonicum* egg deposition → chronic intestinal inflammation → macrophage and immune remodelling → oxidative stress and DDR perturbation → pro-oncogenic molecular state.

This study has important limitations. First, the infection signature derives from a mouse model at a single time point (eight weeks), which reflects the early chronic phase rather than the decades-long exposure of endemic human populations, and the number of deposited libraries is small; we therefore relied on the published signature, pathway-level inference and large human cohorts rather than re-estimating significance from the raw mouse data alone. Second, cross-species comparison is restricted to conserved one-to-one orthologues, which excludes species-specific immune genes and may underestimate overlap. Third, comparing infected non-neoplastic mucosa with tumours conflates inflammation-related and transformation-related changes; overlapping genes may reflect shared inflammation rather than a carcinogenic program, and TCGA tumours are from patients whose schistosomiasis status is unknown and who are largely from non-endemic populations. Fourth, adjacent normal tissue in TCGA is not truly normal, and bulk tissue expression is influenced by cell composition. Fifth, all clinical and immune analyses were exploratory, and single-gene ROC curves do not indicate diagnostic utility. Above all, the design identifies associations and cannot establish that *S. japonicum* causes colorectal cancer.

These results define a set of candidate pathways and genes for prospective validation. The most direct next steps are to measure the candidate genes and DNA-damage markers (e.g., γH2AX, PARP1 activity, RAD51 foci, 8-oxo-dG) in colorectal tissue from patients with and without *S. japonicum* infection in endemic areas of the Philippines, and to test experimentally whether egg antigens or parasite-derived extracellular vesicles induce DNA damage in colonic epithelial cells.

## CONCLUSION

⟦ADAPT⟧ *S. japonicum* infection induces a colonic transcriptional program that partially overlaps, in a directionally concordant manner, with that of human colorectal adenocarcinoma, converging on inflammatory, oxidative-stress and genome-maintenance pathways. These candidate pathways and biomarkers provide a rationale for prospective validation in *S. japonicum*-endemic populations.

---

## STATEMENTS

**Acknowledgments.** The author thanks Lin et al. for making their data publicly available, and The Cancer Genome Atlas Research Network. The results shown here are in part based upon data generated by the TCGA Research Network: https://www.cancer.gov/tcga.

**Statement of Authorship.** The author contributed to the conceptualization, methodology, software, formal analysis, data curation, visualization and writing (original draft, review and editing) of this work and approved the final version submitted (CRediT).

**Author Disclosure.** The author declares no conflict of interest.

**Funding Source.** ⟦None / grant details⟧.

**Data Availability.** All data are public: SRA SRR15682843–SRR15682848; GDC projects TCGA-COAD and TCGA-READ; MSigDB; STRING v12. Code and intermediate results: ⟦GitHub URL; Zenodo DOI⟧.

---

## REFERENCES

<!-- Verify every reference (volume, pages, DOI) against PubMed before submission; renumber if text order changes. -->

1. World Health Organization. Schistosomiasis: key facts [Internet]. Geneva: WHO; ⟦year⟧ [cited ⟦date⟧]. Available from: https://www.who.int/news-room/fact-sheets/detail/schistosomiasis
2. McManus DP, Dunne DW, Sacko M, Utzinger J, Vennervald BJ, Zhou XN. Schistosomiasis. Nat Rev Dis Primers. 2018;4(1):13.
3. Olveda RM, Gray DJ. Schistosomiasis in the Philippines: innovative control approach is needed if elimination is the goal. Trop Med Infect Dis. 2019;4(2):66.
4. Colley DG, Bustinduy AL, Secor WE, King CH. Human schistosomiasis. Lancet. 2014;383(9936):2253–64.
5. Hanahan D. Hallmarks of cancer: new dimensions. Cancer Discov. 2022;12(1):31–46.
6. Coussens LM, Werb Z. Inflammation and cancer. Nature. 2002;420(6917):860–7.
7. Grivennikov SI, Greten FR, Karin M. Immunity, inflammation, and cancer. Cell. 2010;140(6):883–99.
8. Kay J, Thadhani E, Samson L, Engelward B. Inflammation-induced DNA damage, mutations and cancer. DNA Repair (Amst). 2019;83:102673.
9. Ullman TA, Itzkowitz SH. Intestinal inflammation and cancer. Gastroenterology. 2011;140(6):1807–16.
10. IARC Working Group on the Evaluation of Carcinogenic Risks to Humans. Schistosomes, liver flukes and *Helicobacter pylori*. IARC Monogr Eval Carcinog Risks Hum. 1994;61:1–241.
11. IARC Working Group on the Evaluation of Carcinogenic Risks to Humans. Biological agents. IARC Monogr Eval Carcinog Risks Hum. 2012;100B:1–441.
12. Brindley PJ, Loukas A. Helminth infection-induced malignancy. PLoS Pathog. 2017;13(7):e1006393.
13. Xu Z, Su DL. *Schistosoma japonicum* and colorectal cancer: an epidemiological study in the People's Republic of China. Int J Cancer. 1984;34(3):315–8.
14. Wang M, Wu QB, He WB, Wang ZQ. Clinicopathological characteristics and prognosis of schistosomal colorectal cancer. Colorectal Dis. 2016;18(10):1005–9.
15. Bray F, Laversanne M, Sung H, Ferlay J, Siegel RL, Soerjomataram I, et al. Global cancer statistics 2022: GLOBOCAN estimates of incidence and mortality worldwide for 36 cancers in 185 countries. CA Cancer J Clin. 2024;74(3):229–63.
16. Cancer Genome Atlas Network. Comprehensive molecular characterization of human colon and rectal cancer. Nature. 2012;487(7407):330–7.
17. Lin D, Song Q, Zhang Y, Liu J, Chen F, Du S, et al. *Bacillus subtilis* attenuates hepatic and intestinal injuries and modulates gut microbiota and gene expression profiles in mice infected with *Schistosoma japonicum*. Front Cell Dev Biol. 2021;9:766205. ⟦VERIFY authors/title/article number against the paper containing SRR15682843–48⟧
18. Chen S, Zhou Y, Chen Y, Gu J. fastp: an ultra-fast all-in-one FASTQ preprocessor. Bioinformatics. 2018;34(17):i884–90.
19. Patro R, Duggal G, Love MI, Irizarry RA, Kingsford C. Salmon provides fast and bias-aware quantification of transcript expression. Nat Methods. 2017;14(4):417–9.
20. Soneson C, Love MI, Robinson MD. Differential analyses for RNA-seq: transcript-level estimates improve gene-level inferences. F1000Res. 2015;4:1521.
21. Love MI, Huber W, Anders S. Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. Genome Biol. 2014;15(12):550.
22. Durinck S, Spellman PT, Birney E, Huber W. Mapping identifiers for the integration of genomic datasets with the R/Bioconductor package biomaRt. Nat Protoc. 2009;4(8):1184–91.
23. Colaprico A, Silva TC, Olsen C, Garofano L, Cava C, Garolini D, et al. TCGAbiolinks: an R/Bioconductor package for integrative analysis of TCGA data. Nucleic Acids Res. 2016;44(8):e71.
24. Zhu A, Ibrahim JG, Love MI. Heavy-tailed prior distributions for sequence count data: removing the noise and preserving large differences. Bioinformatics. 2019;35(12):2084–92.
25. Subramanian A, Tamayo P, Mootha VK, Mukherjee S, Ebert BL, Gillette MA, et al. Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. Proc Natl Acad Sci U S A. 2005;102(43):15545–50.
26. Korotkevich G, Sukhov V, Budin N, Shpak B, Artyomov MN, Sergushichev A. Fast gene set enrichment analysis. bioRxiv. 2021. doi:10.1101/060012.
27. Liberzon A, Birger C, Thorvaldsdóttir H, Ghandi M, Mesirov JP, Tamayo P. The Molecular Signatures Database (MSigDB) hallmark gene set collection. Cell Syst. 2015;1(6):417–25.
28. Wu T, Hu E, Xu S, Chen M, Guo P, Dai Z, et al. clusterProfiler 4.0: a universal enrichment tool for interpreting omics data. Innovation (Camb). 2021;2(3):100141.
29. Szklarczyk D, Kirsch R, Koutrouli M, Nastou K, Mehryary F, Hachilif R, et al. The STRING database in 2023: protein–protein association networks and functional enrichment analyses for any sequenced genome of interest. Nucleic Acids Res. 2023;51(D1):D638–46.
30. Chin CH, Chen SH, Wu HH, Ho CW, Ko MT, Lin CY. cytoHubba: identifying hub objects and sub-networks from complex interactome. BMC Syst Biol. 2014;8(Suppl 4):S11.
31. Csardi G, Nepusz T. The igraph software package for complex network research. InterJournal Complex Systems. 2006;1695.
32. Blondel VD, Guillaume JL, Lambiotte R, Lefebvre E. Fast unfolding of communities in large networks. J Stat Mech. 2008;2008:P10008.
33. Robin X, Turck N, Hainard A, Tiberti N, Lisacek F, Sanchez JC, et al. pROC: an open-source package for R and S+ to analyze and compare ROC curves. BMC Bioinformatics. 2011;12:77.
34. Becht E, Giraldo NA, Lacroix L, Buttard B, Elarouci N, Petitprez F, et al. Estimating the population abundance of tissue-infiltrating immune and stromal cell populations using gene expression. Genome Biol. 2016;17(1):218.
35. Pearce EJ, MacDonald AS. The immunobiology of schistosomiasis. Nat Rev Immunol. 2002;2(7):499–511.
36. Lord CJ, Ashworth A. PARP inhibitors: synthetic lethality in the clinic. Science. 2017;355(6330):1152–8.

---

## TABLES

**Table 1. Datasets analysed.**

| Dataset | Accession | Species | Tissue / comparison | Samples used | Role |
|---|---|---|---|---|---|
| Lin et al. 2021¹⁷ | SRR15682843–SRR15682848; Suppl. Table S5 | *Mus musculus* | Colon, *S. japonicum*-infected (8 wk) vs uninfected | ⟦R: n SI / n NG — 02_metadata/sra_runs.tsv⟧ | Discovery signature |
| TCGA-COAD¹⁶ | GDC | *Homo sapiens* | Colon adenocarcinoma vs solid-tissue normal | ⟦R⟧ / ⟦R⟧ | Primary human comparison |
| TCGA-READ¹⁶ | GDC | *Homo sapiens* | Rectal adenocarcinoma vs solid-tissue normal | ⟦R⟧ / ⟦R⟧ | Replication |
| MSigDB Hallmark²⁷ | v⟦R⟧ | — | 50 gene sets | — | Pathway analysis |
| Custom DDR set | Suppl. Table S1 | — | 93 genes, 12 modules | — | Hypothesis-driven pathway analysis |
| STRING v12²⁹ | — | *H. sapiens* | Score ≥ 0.700 | — | Network |

**Table 2. Top directionally concordant genes in *S. japonicum*-infected mouse colon and human colorectal cancer.** ⟦Paste from 07_tables/Table2_concordant_genes.tsv — top 20–30 rows: human gene, mouse gene, mouse log₂FC, COAD log₂FC, COAD FDR, replicated in READ, class.⟧

**Table 3. Candidate hub and DDR genes: function and annotation.** ⟦From 05_results/06_hubs.tsv + 07_validation.tsv; columns: gene, class, degree/MCC rank, principal function (UniProt), DDR module / immune / cancer-hallmark annotation, COAD tumour–normal FDR, stage/survival association (exploratory).⟧

## FIGURE LEGENDS

**Figure 1. Study workflow.** *S. japonicum*-infected versus uninfected mouse colon signature → one-to-one human orthologues → intersection with TCGA-COAD tumour-versus-normal differential expression (replication in TCGA-READ) → concordance testing, Hallmark/DDR GSEA, STRING network, exploratory clinical and immune analyses.

**Figure 2. Colonic transcriptional response to *S. japonicum* infection.** (A) Volcano plot of infected (SI) versus control (NG) colon; red, up-regulated; blue, down-regulated (FDR < 0.05, |log₂FC| ≥ 1). (B) Heatmap of top DEGs. (C) ⟦If available⟧ Principal component analysis of re-processed libraries.

**Figure 3. Cross-species overlap.** (A) Overlap of infection-associated orthologues with COAD DEGs within the shared universe, with hypergeometric test. (B) Mouse versus human log₂ fold changes of overlapping genes; concordant up (red), concordant down (blue), discordant (grey); Spearman ρ and binomial concordance test shown.

**Figure 4. Shared pathways.** (A) Normalized enrichment scores of pre-specified Hallmark and DDR gene sets in the infection signature, COAD and READ; point size −log₁₀ FDR, black outline FDR < 0.05. (B) GO Biological Process enrichment of concordant genes. (C) DDR module-level enrichment.

**Figure 5. STRING network of concordant genes** (combined score ≥ 0.700). Node colour indicates concordant up (red) or down (blue); node size is proportional to degree; labelled nodes are the ten candidate hub genes.

**Figure 6. Exploratory human validation.** (A) Expression of candidate genes in COAD tumour versus normal. (B) Single-gene ROC curves (descriptive). (C) Spearman correlation of candidate genes with MCP-counter immune scores and M2-like macrophage score in COAD tumours; * BH-FDR < 0.05.

**Figure 7. Conceptual model (hypothesis).** *S. japonicum* egg deposition → chronic colonic inflammation (NF-κB, IL-6/STAT3) → immune remodelling (M2-like macrophages) → oxidative stress and DDR perturbation → pro-oncogenic molecular state. Arrows indicate hypothesized, not demonstrated, relationships.

## SUPPLEMENTARY MATERIAL

- Supplementary File 1. Pre-specified analysis plan (00_protocol/Analysis_Plan_v1).
- Supplementary Table S1. DDR/genome-stability gene set (08_supplement/Table_S_DDR_geneset.tsv).
- Supplementary Table S2. Mouse–human orthologue mapping (08_supplement/Table_S2_orthologues.tsv).
- Supplementary Table S3. All overlapping genes with classification and READ replication (08_supplement/Table_S3_overlap_all.tsv).
- Supplementary Table S4. Network edges and centrality (08_supplement/Table_S4_network_edges.tsv; 05_results/06_hubs.tsv).
- Supplementary Table S5. Sensitivity analyses (05_results/04_overlap_stats.tsv).
- Supplementary Table S6. Full GSEA/ORA results (05_results/05_*.tsv).
