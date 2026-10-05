# 01c_reprocess_deseq2.R — DESeq2 on reprocessed salmon output (SI vs NG colon only).
# Only meaningful if >= 2 runs per group exist for colon. If each group has a single
# (pooled) library, the script stops: report this in the Limitations and rely on the
# published signature (Analysis_Plan §3, §8).

source("04_R_scripts/00_setup.R")
suppressPackageStartupMessages({ library(tximport); library(DESeq2); library(biomaRt) })

meta <- fread(P("02_metadata", "sra_runs.tsv"))   # columns: run, tissue, group (NG/SI/SIBS)
meta <- meta[tissue == "colon" & group %in% c("NG", "SI")]
reps <- meta[, .N, by = group]
print(reps)
if (any(reps$N < 2)) stop("Fewer than 2 colon libraries per group: no valid DESeq2 dispersion estimate. ",
                          "Use the published signature; record in Limitations.")

files <- setNames(P("03_processed_data", "salmon", meta$run, "quant.sf"), meta$run)
mart <- useEnsembl("genes", dataset = "mmusculus_gene_ensembl", version = 112)
t2g <- getBM(c("ensembl_transcript_id_version", "ensembl_gene_id", "external_gene_name"), mart = mart)
txi <- tximport(files, type = "salmon", tx2gene = t2g[, 1:2], ignoreTxVersion = FALSE)

coldata <- data.frame(row.names = meta$run, group = factor(meta$group, levels = c("NG", "SI")))
dds <- DESeqDataSetFromTximport(txi, coldata, ~ group)
dds <- dds[rowSums(counts(dds) >= 10) >= min(reps$N), ]
dds <- DESeq(dds)
res <- as.data.frame(results(dds, contrast = c("group", "SI", "NG")))
res$ensembl <- rownames(res)
res$gene <- t2g$external_gene_name[match(res$ensembl, t2g$ensembl_gene_id)]
fwrite(res, P("03_processed_data", "mouse_colon_deseq2_reprocessed.tsv"), sep = "\t")

vsd <- vst(dds, blind = TRUE)
pdf(P("06_figures", "Fig2_PCA_reprocessed.pdf"), 4, 3.5)
print(plotPCA(vsd, intgroup = "group") + theme_classic(base_size = 9))
dev.off()
