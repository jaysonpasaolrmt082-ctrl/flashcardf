# 04_cross_species_overlap.R — primary outcome (Analysis_Plan §5).
# Overlap of infection-associated orthologues with TCGA-COAD DEGs, concordance,
# fold-change agreement, READ replication and pre-specified sensitivity analyses.
# OUTPUT: 05_results/04_overlap_stats.tsv, 07_tables/Table2_concordant_genes.tsv,
#         03_processed_data/concordant_genes.tsv, 06_figures/Fig3_*.pdf

source("04_R_scripts/00_setup.R")
library(ggrepel)

overlap_test <- function(mm, hs, lfc_hs = PARAM$lfc, label = "primary") {
  hs <- copy(hs)[!is.na(padj)]
  hs[, deg := padj < PARAM$fdr & abs(log2FC) >= lfc_hs]
  m <- merge(mm[, .(gene, hs_ensembl, mm_lfc = log2FC, mm_deg = is_deg)],
             hs[, .(hs_ensembl, hs_symbol, hs_lfc = log2FC, hs_padj = padj, hs_deg = deg)],
             by = "hs_ensembl")                        # universe: tested in both
  N <- nrow(m); K <- sum(m$mm_deg); n <- sum(m$hs_deg)
  both <- m[mm_deg & hs_deg]
  both[, class := fcase(mm_lfc > 0 & hs_lfc > 0, "Concordant UP",
                        mm_lfc < 0 & hs_lfc < 0, "Concordant DOWN",
                        default = "Discordant")]
  k <- nrow(both); conc <- sum(both$class != "Discordant")
  p_hyper <- phyper(k - 1, K, N - K, n, lower.tail = FALSE)
  bt <- if (k > 0) binom.test(conc, k, 0.5, alternative = "greater") else list(p.value = NA, conf.int = c(NA, NA))
  rho <- if (k > 2) cor.test(both$mm_lfc, both$hs_lfc, method = "spearman", exact = FALSE) else NULL
  list(table = both,
       stats = data.table(analysis = label, universe = N, mouse_deg = K, human_deg = n, overlap = k,
                          expected = K * n / N, fold_enrichment = k / (K * n / N), p_hypergeom = p_hyper,
                          concordant = conc, concordant_up = sum(both$class == "Concordant UP"),
                          concordant_down = sum(both$class == "Concordant DOWN"),
                          pct_concordant = 100 * conc / k, p_binom = bt$p.value,
                          spearman_rho = rho$estimate %||% NA, p_spearman = rho$p.value %||% NA))
}
`%||%` <- function(a, b) if (is.null(a)) b else a

mm  <- fread(P("03_processed_data", "mouse_signature_human.tsv"))
mm1 <- fread(P("03_processed_data", "mouse_signature_human_incl_one2many.tsv"))
coad <- fread(P("05_results", "03_TCGA-COAD_DESeq2.tsv"))
read <- fread(P("05_results", "03_TCGA-READ_DESeq2.tsv"))

res <- list(
  primary_COAD  = overlap_test(mm, coad),
  replic_READ   = overlap_test(mm, read, label = "replication_READ"),
  sens1_one2many = overlap_test(unique(mm1, by = "hs_ensembl"), coad, label = "sens1_one2many"),
  sens2_lfc0.58 = overlap_test(mm, coad, lfc_hs = PARAM$lfc_sens, label = "sens2_lfc0.58"))
f_pair <- P("05_results", "03_TCGA-COAD_DESeq2_paired.tsv")
if (file.exists(f_pair)) res$sens3_paired <- overlap_test(mm, fread(f_pair), label = "sens3_paired")

stats <- rbindlist(lapply(res, `[[`, "stats"))
fwrite(stats, P("05_results", "04_overlap_stats.tsv"), sep = "\t")

# Concordant genes + READ replication flag
tab <- res$primary_COAD$table
tab <- merge(tab, read[, .(hs_ensembl, read_lfc = log2FC, read_padj = padj)], by = "hs_ensembl", all.x = TRUE)
tab[, replicated_READ := !is.na(read_padj) & read_padj < PARAM$fdr & sign(read_lfc) == sign(hs_lfc)]
fwrite(tab, P("08_supplement", "Table_S3_overlap_all.tsv"), sep = "\t")
conc <- tab[class != "Discordant"][order(-abs(mm_lfc * hs_lfc))]
fwrite(conc, P("03_processed_data", "concordant_genes.tsv"), sep = "\t")
fwrite(conc[1:min(.N, 30), .(Human_gene = hs_symbol, Mouse_gene = gene, Mouse_log2FC = round(mm_lfc, 2),
                             COAD_log2FC = round(hs_lfc, 2), COAD_FDR = signif(hs_padj, 3),
                             READ_replicated = replicated_READ, Class = class)],
       P("07_tables", "Table2_concordant_genes.tsv"), sep = "\t")

# Figure 3: fold-change scatter of overlapping genes
g <- ggplot(tab, aes(mm_lfc, hs_lfc, colour = class)) +
  geom_hline(yintercept = 0, linewidth = 0.3) + geom_vline(xintercept = 0, linewidth = 0.3) +
  geom_point(size = 1.2, alpha = 0.8) +
  geom_text_repel(data = conc[1:min(.N, 20)], aes(label = hs_symbol), size = 2.4, colour = "black") +
  scale_colour_manual(values = c("Concordant UP" = "#B2182B", "Concordant DOWN" = "#2166AC", Discordant = "grey60")) +
  labs(x = expression(log[2]*"FC, S. japonicum-infected vs normal mouse colon"),
       y = expression(log[2]*"FC, TCGA-COAD tumour vs normal"),
       subtitle = with(stats[analysis == "primary"], sprintf("Overlap %d (%.1fx expected, P = %.2g); concordant %.0f%% (binomial P = %.2g); rho = %.2f",
                                                           overlap, fold_enrichment, p_hypergeom, pct_concordant, p_binom, spearman_rho))) +
  theme_classic(base_size = 9) + theme(legend.position = "bottom", legend.title = element_blank())
ggsave(P("06_figures", "Fig3_crossspecies_scatter.pdf"), g, width = 5.5, height = 5)
