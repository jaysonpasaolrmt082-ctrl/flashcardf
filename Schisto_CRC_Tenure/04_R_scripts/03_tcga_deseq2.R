# 03_tcga_deseq2.R — TCGA-COAD (primary) and TCGA-READ (replication):
# Primary Tumor vs Solid Tissue Normal, STAR - Counts, DESeq2.
# Usage: Rscript 04_R_scripts/03_tcga_deseq2.R COAD   (then again with READ)
# OUTPUT: 03_processed_data/TCGA-<P>_se.rds, _vst.rds, 05_results/03_TCGA-<P>_DESeq2.tsv

source("04_R_scripts/00_setup.R")
suppressPackageStartupMessages({ library(TCGAbiolinks); library(SummarizedExperiment); library(DESeq2) })

arg <- commandArgs(TRUE)[1]
proj <- paste0("TCGA-", if (!is.na(arg) && arg %in% c("COAD", "READ")) arg else "COAD")
f_se <- P("03_processed_data", paste0(proj, "_se.rds"))

if (!file.exists(f_se)) {
  q <- GDCquery(project = proj, data.category = "Transcriptome Profiling",
                data.type = "Gene Expression Quantification", workflow.type = "STAR - Counts",
                sample.type = c("Primary Tumor", "Solid Tissue Normal"))
  GDCdownload(q, directory = P("01_raw_data", "GDCdata"), files.per.chunk = 50)
  se <- GDCprepare(q, directory = P("01_raw_data", "GDCdata"))
  saveRDS(se, f_se)
}
se <- readRDS(f_se)

# One aliquot per sample (first by barcode order) and protein-coding + lncRNA genes
se <- se[, !duplicated(substr(colnames(se), 1, 16))]
se <- se[rowData(se)$gene_type %in% c("protein_coding", "lncRNA"), ]
cd <- as.data.frame(colData(se))
cd$condition <- factor(ifelse(cd$sample_type == "Solid Tissue Normal", "Normal", "Tumor"),
                       levels = c("Normal", "Tumor"))
cd$patient <- substr(rownames(cd), 1, 12)

dds <- DESeqDataSetFromMatrix(assay(se, "unstranded"), cd[, c("condition", "patient")], ~ condition)
dds <- dds[rowSums(counts(dds) >= 10) >= 10, ]
dds <- DESeq(dds, parallel = FALSE)
res <- results(dds, contrast = c("condition", "Tumor", "Normal"), alpha = PARAM$fdr)
shr <- lfcShrink(dds, coef = "condition_Tumor_vs_Normal", type = "apeglm")

out <- data.table(hs_ensembl = sub("\\..*$", "", rownames(res)),
                  hs_symbol = rowData(se)[rownames(res), "gene_name"],
                  baseMean = res$baseMean, log2FC = res$log2FoldChange, log2FC_shrunk = shr$log2FoldChange,
                  stat = res$stat, pvalue = res$pvalue, padj = res$padj)
out[, is_deg := !is.na(padj) & padj < PARAM$fdr & abs(log2FC) >= PARAM$lfc]
out[, direction := fifelse(!is_deg, "NS", fifelse(log2FC > 0, "UP", "DOWN"))]
fwrite(out, P("05_results", paste0("03_", proj, "_DESeq2.tsv")), sep = "\t")

vsd <- vst(dds, blind = FALSE)
saveRDS(vsd, P("03_processed_data", paste0(proj, "_vst.rds")))

# Sensitivity analysis 3: paired tumour-normal subset
paired <- names(which(table(cd$patient[cd$condition == "Normal"]) > 0))
paired <- intersect(paired, cd$patient[cd$condition == "Tumor"])
if (length(paired) >= 10) {
  keep <- cd$patient %in% paired
  ddp <- DESeqDataSetFromMatrix(assay(se, "unstranded")[, keep],
                                droplevels(cd[keep, c("condition", "patient")]), ~ patient + condition)
  ddp <- DESeq(ddp[rownames(dds), ])
  rp <- results(ddp, name = "condition_Tumor_vs_Normal")
  fwrite(data.table(hs_ensembl = sub("\\..*$", "", rownames(rp)), log2FC = rp$log2FoldChange,
                    stat = rp$stat, padj = rp$padj),
         P("05_results", paste0("03_", proj, "_DESeq2_paired.tsv")), sep = "\t")
}

writeLines(c(sprintf("%s: tumour n = %d, normal n = %d, paired patients = %d",
                     proj, sum(cd$condition == "Tumor"), sum(cd$condition == "Normal"), length(paired)),
             sprintf("Genes tested: %d; DEGs: %d (UP %d, DOWN %d)", sum(!is.na(out$padj)),
                     out[is_deg == TRUE, .N], out[direction == "UP", .N], out[direction == "DOWN", .N])),
           P("05_results", paste0("03_", proj, "_summary.txt")))
