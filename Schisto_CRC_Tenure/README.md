# Schisto_CRC_Tenure

**Paper 1 (tenure):** *Cross-Species Transcriptomic Analysis Identifies Colorectal Cancer-Associated Molecular Pathways Induced by* Schistosoma japonicum *Infection* — J. C. Pasaol (sole/corresponding author).

## Status

| Component | State |
|---|---|
| Analysis plan (`00_protocol/Analysis_Plan_v1.md`) | Written. **Date it, export to PDF and commit before running script 04.** |
| Reproducible R pipeline (`04_R_scripts/`) | Written, not yet run (needs R + internet access to GDC/NCBI) |
| Manuscript (`09_manuscript/Manuscript.md`) | Full text: Introduction, Methods, Discussion, References, Tables, Figure legends. Results values are ⟦R⟧ slots |
| Cover letter and pre-submission inquiry | Drafted |
| DDR gene set (Suppl. Table S1) | 93 genes, 12 modules |

**No result in the manuscript has been filled in.** Every number marked ⟦R⟧ must come from the pipeline output. Before submission, `grep -c "⟦" 09_manuscript/*.md` must return 0.

## Run order

```bash
# 1. Manual: download Lin et al. Table S5 + SRA RunInfo (see 02_metadata/README_data_sources.md)
# 2. Optional raw reprocessing (Linux, sra-tools/fastp/salmon):
bash 04_R_scripts/01b_reprocess_raw.sh
# 3. Everything else:
bash 04_R_scripts/run_all.sh
```

| Script | Produces | Manuscript section |
|---|---|---|
| 01_mouse_signature.R | mouse signature, Fig 2A | Results 1 |
| 01b/01c | reprocessed DESeq2, PCA (sensitivity 4) | Results 1 |
| 02_orthologues.R | one-to-one orthologues, Table S2 | Results 2 |
| 03_tcga_deseq2.R COAD/READ | tumour vs normal DESeq2, paired subset | Results 3 |
| 04_cross_species_overlap.R | **primary outcome**, Table 2, Fig 3, sensitivity table | Results 3 |
| 05_gsea.R | Hallmark + DDR GSEA/ORA, GO/KEGG, Fig 4 | Results 4–5 |
| 06_ppi_network.R | STRING network, hub genes, Fig 5 | Results 6 |
| 07_tcga_validation.R | tumour/normal, ROC, stage, Cox, Fig 6A | Results 7 |
| 08_immune_infiltration.R | MCP-counter + M2 score correlations, Fig 6C | Results 7 |

## Before submission

1. Confirm the full citation of the source study (ref. 17) and check every reference against PubMed.
2. Run a systematic literature search (PubMed/Scopus: "Schistosoma japonicum" AND (colorectal OR colon) AND (transcriptom* OR RNA-seq)) before using "first" or "novel".
3. Rewrite every ⟦ADAPT⟧ paragraph so it matches the actual direction of the results, including null results.
4. Send `09_manuscript/Presubmission_Inquiry.md` to Acta Medica Philippina, and ask the UP Manila REB about an exemption determination.
5. Deposit the code on Zenodo (DOI) and the analysis plan on OSF.
