# Data sources — exact retrieval steps

## 1. Mouse infection data (Lin et al., 2021)
1. Open the paper whose Data Availability lists SRR15682843–SRR15682848 (transcriptome) and SRR15694234–SRR15694269 (16S). Confirm the full citation and update reference 17 in the manuscript.
2. Download the supplementary DEG table for colon **SI vs NG** (Table S5 per the paper) → save as `01_raw_data/Lin2021_TableS5_colon_SI_vs_NG.xlsx`.
   - Check whether it contains *all* genes (with p-values) or only DEGs. If only DEGs, mouse-side GSEA is replaced by over-representation analysis (05_gsea.R handles this automatically) — say so in Methods.
3. In the SRA Run Selector (https://www.ncbi.nlm.nih.gov/Traces/study/), search the six SRRs, download the RunInfo/metadata table, and fill `02_metadata/sra_runs.tsv` (tissue = colon / small_intestine; group = NG / SI / SIBS). Save the original RunInfo CSV here too.
   - Six runs across 3 groups × 2 tissues implies ~1 (possibly pooled) library per group-tissue. If so, 01c will stop by design — this is expected and is stated in the Limitations.

## 2. TCGA-COAD / TCGA-READ
Fetched automatically by `03_tcga_deseq2.R` (TCGAbiolinks, GDC STAR-Counts). ~1–2 GB per project. Needs internet access to api.gdc.cancer.gov.
Alternative (sensitivity 5): UCSC Xena TOIL TCGA+GTEx recompute matrices (https://xenabrowser.net/datapages/).

## 3. Gene sets / networks
MSigDB Hallmark via `msigdbr` (record version); STRING v12 via `STRINGdb` (downloads to 01_raw_data).
