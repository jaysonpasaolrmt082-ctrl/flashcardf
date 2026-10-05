# 05_gsea.R — pathway analysis (H2): Hallmark + custom DDR modules, run on
# (a) the mouse infection signature (human orthologue space) and (b) TCGA-COAD / READ.
# Ranked GSEA if a full ranked list exists; ORA on DEGs is reported in addition.
# Also GO-BP / KEGG ORA of the concordant genes.
# OUTPUT: 05_results/05_gsea_*.tsv, 06_figures/Fig4_*.pdf

source("04_R_scripts/00_setup.R")
suppressPackageStartupMessages({ library(fgsea); library(msigdbr); library(clusterProfiler); library(org.Hs.eg.db) })

hall <- msigdbr(species = "Homo sapiens", category = "H")
sets <- split(hall$ensembl_gene, hall$gs_name)
ddr <- fread(P("08_supplement", "Table_S_DDR_geneset.tsv"))
ddr_ens <- AnnotationDbi::mapIds(org.Hs.eg.db, ddr$gene, "ENSEMBL", "SYMBOL")
ddr$ens <- ddr_ens[ddr$gene]
sets[["CUSTOM_DDR_ALL"]] <- na.omit(unique(ddr$ens))
for (m in unique(ddr$module)) {
  s <- na.omit(ddr[module == m]$ens)
  if (length(s) >= 5) sets[[paste0("CUSTOM_DDR_", toupper(gsub("[^A-Za-z]+", "_", m)))]] <- s
}
# Note: modules < PARAM$gsea_min genes are tested with minSize = 5 in a separate, labelled run.

run_gsea <- function(dt, label) {
  r <- dt[!is.na(stat) & is.finite(stat)][order(-abs(stat))]
  r <- unique(r, by = "hs_ensembl")
  ranks <- setNames(r$stat, r$hs_ensembl)
  big <- fgsea(sets, ranks, minSize = PARAM$gsea_min, maxSize = PARAM$gsea_max, eps = 0)
  small <- fgsea(sets[grepl("^CUSTOM_DDR_", names(sets))], ranks, minSize = 5, maxSize = PARAM$gsea_max, eps = 0)
  small[, padj := p.adjust(pval, "BH")]
  out <- rbind(big[, tier := "primary"], small[, tier := "DDR_modules"])
  out[, dataset := label][, leadingEdge := vapply(leadingEdge, paste, "", collapse = ";")]
  out
}

mm   <- fread(P("03_processed_data", "mouse_signature_human.tsv"))
coad <- fread(P("05_results", "03_TCGA-COAD_DESeq2.tsv"))
read <- fread(P("05_results", "03_TCGA-READ_DESeq2.tsv"))

full_mouse_rank <- mean(!is.na(mm$pvalue)) > 0.9 && nrow(mm) > 5000
res <- rbind(
  if (full_mouse_rank) run_gsea(mm, "Mouse_SI_vs_NG"),
  run_gsea(coad, "TCGA-COAD"),
  run_gsea(read, "TCGA-READ"), fill = TRUE)
fwrite(res, P("05_results", "05_gsea_all.tsv"), sep = "\t")

# ORA of mouse DEGs (always; required if only DEG list was published)
univ <- intersect(mm$hs_ensembl, coad[!is.na(padj)]$hs_ensembl)
t2g <- rbindlist(lapply(names(sets), function(n) data.table(term = n, gene = sets[[n]])))
ora <- rbindlist(lapply(c("UP", "DOWN"), function(d) {
  e <- enricher(mm[direction == d]$hs_ensembl, universe = univ, TERM2GENE = t2g,
                minGSSize = 5, pvalueCutoff = 1, qvalueCutoff = 1)
  if (is.null(e)) return(NULL)
  as.data.table(e@result)[, direction := d]
}))
fwrite(ora, P("05_results", "05_ora_mouse_hallmark_ddr.tsv"), sep = "\t")

# GO-BP / KEGG on concordant genes
conc <- fread(P("03_processed_data", "concordant_genes.tsv"))
ent <- bitr(conc$hs_ensembl, "ENSEMBL", "ENTREZID", org.Hs.eg.db)
uent <- bitr(univ, "ENSEMBL", "ENTREZID", org.Hs.eg.db)$ENTREZID
go <- enrichGO(ent$ENTREZID, org.Hs.eg.db, ont = "BP", universe = uent, readable = TRUE)
kg <- tryCatch(enrichKEGG(ent$ENTREZID, organism = "hsa", universe = uent), error = function(e) NULL)
if (!is.null(go)) fwrite(as.data.table(go@result), P("05_results", "05_concordant_GO_BP.tsv"), sep = "\t")
if (!is.null(kg)) fwrite(as.data.table(kg@result), P("05_results", "05_concordant_KEGG.tsv"), sep = "\t")

# Figure 4: NES heatmap-style dot plot for pre-specified pathways across datasets
focus <- c("HALLMARK_INFLAMMATORY_RESPONSE", "HALLMARK_TNFA_SIGNALING_VIA_NFKB",
           "HALLMARK_IL6_JAK_STAT3_SIGNALING", "HALLMARK_REACTIVE_OXYGEN_SPECIES_PATHWAY",
           "HALLMARK_DNA_REPAIR", "HALLMARK_P53_PATHWAY", "HALLMARK_APOPTOSIS",
           "HALLMARK_EPITHELIAL_MESENCHYMAL_TRANSITION", "HALLMARK_HYPOXIA",
           "HALLMARK_MYC_TARGETS_V1", "HALLMARK_PI3K_AKT_MTOR_SIGNALING",
           "HALLMARK_TGF_BETA_SIGNALING", "HALLMARK_WNT_BETA_CATENIN_SIGNALING",
           "HALLMARK_INTERFERON_GAMMA_RESPONSE", "HALLMARK_E2F_TARGETS", "HALLMARK_G2M_CHECKPOINT",
           grep("^CUSTOM_DDR_", names(sets), value = TRUE))
fd <- res[pathway %in% focus]
fd[, pathway := factor(sub("^HALLMARK_|^CUSTOM_", "", pathway), levels = rev(sub("^HALLMARK_|^CUSTOM_", "", focus)))]
g <- ggplot(fd, aes(dataset, pathway, colour = NES, size = -log10(padj))) +
  geom_point() + scale_colour_gradient2(low = "#2166AC", mid = "white", high = "#B2182B") +
  geom_point(data = fd[padj < PARAM$gsea_fdr], shape = 1, colour = "black") +
  labs(x = NULL, y = NULL, size = expression(-log[10]~FDR)) + theme_bw(base_size = 8)
ggsave(P("06_figures", "Fig4_pathway_NES.pdf"), g, width = 5, height = 6)
