# 01_mouse_signature.R — S. japonicum-infected (SI) vs normal (NG) mouse colon signature.
#
# INPUT (manual download, see 02_metadata/README_data_sources.md):
#   01_raw_data/Lin2021_TableS5_colon_SI_vs_NG.xlsx   (supplementary DEG table)
#   optional: 03_processed_data/mouse_colon_deseq2_reprocessed.tsv (from 01b_reprocess_raw.sh + 01c)
# OUTPUT:
#   03_processed_data/mouse_signature.tsv  (gene, ensembl, log2FC, pvalue, padj, stat, direction, source)
#   05_results/01_mouse_signature_summary.txt
#   06_figures/Fig2_volcano.pdf

source("04_R_scripts/00_setup.R")
library(readxl); library(ggrepel)

f_pub <- P("01_raw_data", "Lin2021_TableS5_colon_SI_vs_NG.xlsx")
stopifnot(file.exists(f_pub))

raw <- as.data.table(read_excel(f_pub))
# Column names differ between supplements; map them explicitly after inspecting.
# Print and check once, then edit the `colmap` below — this is the only manual step.
print(names(raw))
colmap <- c(gene = "gene_name", ensembl = "gene_id", log2FC = "log2FoldChange",
            pvalue = "pvalue", padj = "padj")
missing <- setdiff(colmap, names(raw))
if (length(missing)) stop("Edit `colmap` — columns not found: ", paste(missing, collapse = ", "))
sig <- raw[, ..colmap]; setnames(sig, names(colmap))

sig <- sig[!is.na(gene) & !is.na(log2FC)]
sig[, ensembl := sub("\\..*$", "", ensembl)]
# Signed ranking statistic for GSEA when the Wald stat is not supplied
sig[, stat := sign(log2FC) * -log10(pmax(pvalue, 1e-300))]
sig[, is_deg := !is.na(padj) & padj < PARAM$fdr & abs(log2FC) >= PARAM$lfc]
sig[, direction := fifelse(!is_deg, "NS", fifelse(log2FC > 0, "UP", "DOWN"))]
sig[, source := "published_TableS5"]
# Keep one row per gene (largest |stat|) — duplicates arise from multi-mapping IDs
setorder(sig, gene, -abs(stat)); sig <- unique(sig, by = "gene")

# Optional: independent reprocessing replaces published stats for sensitivity analysis 4
f_rep <- P("03_processed_data", "mouse_colon_deseq2_reprocessed.tsv")
if (file.exists(f_rep)) {
  rep <- fread(f_rep)
  m <- merge(sig[, .(gene, log2FC)], rep[, .(gene, log2FC_rep = log2FoldChange)], by = "gene")
  rho <- cor(m$log2FC, m$log2FC_rep, method = "spearman")
  cat(sprintf("Published vs reprocessed log2FC Spearman rho = %.3f (n = %d)\n", rho, nrow(m)),
      file = P("05_results", "01_reprocessing_agreement.txt"))
}

fwrite(sig, P("03_processed_data", "mouse_signature.tsv"), sep = "\t")

summ <- sig[, .N, by = direction]
writeLines(c(sprintf("Genes in table: %d", nrow(sig)),
             capture.output(print(summ)),
             "Published reference: 1,693 DEGs (598 up, 1,095 down)."),
           P("05_results", "01_mouse_signature_summary.txt"))

top <- sig[is_deg == TRUE][order(-abs(stat))][1:20]
g <- ggplot(sig, aes(log2FC, -log10(pvalue), colour = direction)) +
  geom_point(size = 0.6, alpha = 0.6) +
  scale_colour_manual(values = c(UP = "#B2182B", DOWN = "#2166AC", NS = "grey75")) +
  geom_vline(xintercept = c(-1, 1), linetype = 2, linewidth = 0.3) +
  geom_text_repel(data = top, aes(label = gene), size = 2.5, max.overlaps = 30, colour = "black") +
  labs(x = expression(log[2]~"fold change (SI vs NG)"), y = expression(-log[10]~italic(P)),
       title = "S. japonicum-infected vs normal mouse colon") +
  theme_classic(base_size = 9)
ggsave(P("06_figures", "Fig2_volcano.pdf"), g, width = 4.5, height = 4)
