# Pre-specified Analysis Plan — v1.0

**Study:** Cross-Species Transcriptomic Analysis Identifies Colorectal Cancer-Associated Molecular Pathways Induced by *Schistosoma japonicum* Infection
**Principal investigator:** Jayson Cagadas Pasaol, DVM, PhD
**Version / freeze date:** v1.0 — `2026-10-__` (fill in and export to PDF *before* opening any TCGA result or overlap output; commit the PDF hash to git)

Any deviation from this plan must be logged in §10 with date and justification, and reported in the manuscript as a protocol deviation.

---

## 1. Research question

Does *S. japonicum* infection induce colonic transcriptional programs that overlap with established molecular programs of human colorectal adenocarcinoma, particularly inflammation, oxidative stress, DNA-damage response (DDR), genomic instability and immune dysregulation?

**Not tested:** whether *S. japonicum* causes colorectal cancer (CRC). The design cannot address causality.

## 2. Hypotheses

- **H1 (primary):** Human orthologues of genes differentially expressed in *S. japonicum*-infected mouse colon overlap with genes differentially expressed in TCGA-COAD tumour vs. normal colon more than expected by chance, and the overlapping genes are directionally concordant more often than expected by chance (50%).
- **H2:** Hallmark inflammatory (TNFA_SIGNALING_VIA_NFKB, INFLAMMATORY_RESPONSE, IL6_JAK_STAT3_SIGNALING), oxidative-stress (REACTIVE_OXYGEN_SPECIES_PATHWAY) and genome-maintenance (DNA_REPAIR, P53_PATHWAY, plus the custom DDR set) gene sets are enriched in the same direction in both the infection signature and human CRC.
- **H3 (exploratory):** Concordant candidate hub genes are associated with tumour stage, survival and immune-cell infiltration in human CRC.

## 3. Datasets (fixed)

| ID | Source | Use |
|---|---|---|
| D1 | Supplementary DEG table (colon, SI vs NG) of the source study (Lin et al., 2021) | Primary discovery signature |
| D2 | SRA SRR15682843–SRR15682848 | Re-processing / ranked list for GSEA; sensitivity only |
| D3 | TCGA-COAD, STAR-Counts, Primary Tumor vs Solid Tissue Normal | Primary human comparison |
| D4 | TCGA-READ, same workflow | Independent replication |
| D5 | MSigDB Hallmark (v2023.2+ via `msigdbr`), KEGG, Reactome, GO-BP | Pathways |
| D6 | STRING v12, confidence ≥ 0.700 | PPI |

The *Bacillus subtilis*-treated arm (SIBS) is **excluded** from all primary analyses.
16S data (SRR15694234–SRR15694269) are **out of scope** for this paper.

## 4. Definitions and thresholds (fixed)

| Item | Rule |
|---|---|
| Mouse DEG (D1) | As defined by original authors (DESeq2); if full table available, re-filter at padj < 0.05 and \|log2FC\| ≥ 1 |
| Human DEG (D3, D4) | DESeq2, Benjamini–Hochberg FDR < 0.05 and \|log2FC\| ≥ 1 (lfcShrink "apeglm" for ranking/plots, unshrunk Wald for testing) |
| Orthology | Ensembl BioMart, `ortholog_one2one` only for primary analysis; one-to-many flagged and used only in a sensitivity analysis |
| Overlap universe | Genes with a one-to-one orthologue **and** tested (non-NA padj) in both datasets |
| Overlap test | One-sided hypergeometric test |
| Concordance test | Exact binomial test of concordant vs. discordant direction, H0 p = 0.5 |
| Fold-change agreement | Spearman ρ between mouse and human log2FC in overlapping genes |
| GSEA | fgsea, 10,000 permutations (or multilevel), min size 15, max 500; ranking metric = DESeq2 Wald statistic; significance BH-FDR < 0.05 (primary), < 0.25 reported as suggestive |
| ORA (if only DEG list available for mouse) | clusterProfiler `enricher`, universe as above, BH-FDR < 0.05 |
| PPI | STRING ≥ 0.700; hub ranking = consensus of degree, betweenness and MCC (top 10 by mean rank) |
| Correlation | Spearman, BH-adjusted |
| Survival | Cox PH (age, sex, stage adjusted) + Kaplan–Meier median split — **exploratory** |
| ROC | Single-gene AUC with 95% DeLong CI — **descriptive, not a diagnostic claim** |

## 5. Primary outcome

Number and proportion of concordantly dysregulated orthologues (infection ∩ TCGA-COAD) with the hypergeometric and binomial p-values.

## 6. Secondary outcomes

1. Shared Hallmark/DDR pathway enrichment directions (H2).
2. Replication of concordant genes in TCGA-READ (proportion with same direction and FDR < 0.05).
3. Candidate hub genes from the PPI network.

## 7. Exploratory outcomes

Stage trend, survival association, immune-infiltrate correlation, ROC AUC.

## 8. Sensitivity analyses

1. Include one-to-many orthologues.
2. Relax human threshold to \|log2FC\| ≥ 0.58 (1.5-fold).
3. Paired tumour–normal subset only (patients with both samples).
4. Mouse signature from independent re-processing of D2 instead of D1.
5. TCGA tumour vs GTEx normal colon (UCSC Xena TOIL recompute) instead of TCGA normal.

## 9. Reporting

Exploratory analyses will be labelled as such. All code, session info and intermediate tables will be deposited (GitHub + Zenodo DOI).

## 10. Deviation log

| Date | Deviation | Reason |
|---|---|---|
| | | |
