# 08_immune_infiltration.R — exploratory: MCP-counter immune/stromal scores in TCGA-COAD
# tumours, Spearman correlation with candidate genes; M2-like macrophage score
# (CD163, MRC1, MSR1, CD209, F13A1) added given the helminth-associated Th2 milieu.
# OUTPUT: 05_results/08_immune_correlations.tsv, 06_figures/Fig6C_immune_heatmap.pdf

source("04_R_scripts/00_setup.R")
suppressPackageStartupMessages({ library(SummarizedExperiment); library(MCPcounter); library(ComplexHeatmap) })

vsd <- readRDS(P("03_processed_data", "TCGA-COAD_vst.rds"))
se  <- readRDS(P("03_processed_data", "TCGA-COAD_se.rds"))
vsd <- vsd[, vsd$condition == "Tumor"]
sym <- rowData(se)[rownames(vsd), "gene_name"]
ex <- assay(vsd); ex <- ex[!duplicated(sym), ]; rownames(ex) <- sym[!duplicated(sym)]

mcp <- MCPcounter.estimate(ex, featuresType = "HUGO_symbols")
m2 <- intersect(c("CD163", "MRC1", "MSR1", "CD209", "F13A1"), rownames(ex))
scores <- rbind(mcp, M2_like_macrophage = colMeans(ex[m2, ]))

cand <- intersect(fread(P("05_results", "07_validation.tsv"))[dataset == "TCGA-COAD"]$gene, rownames(ex))
cr <- rbindlist(lapply(cand, function(g) rbindlist(lapply(rownames(scores), function(s) {
  t <- cor.test(ex[g, ], scores[s, ], method = "spearman", exact = FALSE)
  data.table(gene = g, cell = s, rho = t$estimate, p = t$p.value) }))))
cr[, padj := p.adjust(p, "BH")]
fwrite(cr, P("05_results", "08_immune_correlations.tsv"), sep = "\t")

mat <- as.matrix(dcast(cr, gene ~ cell, value.var = "rho"), rownames = "gene")
sig <- as.matrix(dcast(cr, gene ~ cell, value.var = "padj"), rownames = "gene")
pdf(P("06_figures", "Fig6C_immune_heatmap.pdf"), 6, 4)
draw(Heatmap(mat, name = "Spearman rho", col = circlize::colorRamp2(c(-0.6, 0, 0.6), c("#2166AC", "white", "#B2182B")),
             cell_fun = function(j, i, x, y, w, h, f) if (sig[i, j] < 0.05) grid::grid.text("*", x, y),
             row_names_gp = grid::gpar(fontsize = 8), column_names_gp = grid::gpar(fontsize = 8)))
dev.off()
