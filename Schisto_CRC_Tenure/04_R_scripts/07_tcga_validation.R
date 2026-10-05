# 07_tcga_validation.R — exploratory clinical associations of candidate hub genes
# (and any concordant DDR genes) in TCGA-COAD, replicated in READ:
# tumour vs normal, stage trend, Cox PH (age/sex/stage adjusted), KM, single-gene ROC.
# OUTPUT: 05_results/07_validation.tsv, 06_figures/Fig6_*.pdf

source("04_R_scripts/00_setup.R")
suppressPackageStartupMessages({ library(SummarizedExperiment); library(survival); library(survminer); library(pROC); library(patchwork) })

hubs <- fread(P("05_results", "06_hubs.tsv"))[hub == TRUE]$gene
ddr  <- fread(P("08_supplement", "Table_S_DDR_geneset.tsv"))$gene
conc <- fread(P("03_processed_data", "concordant_genes.tsv"))
cand <- unique(c(hubs, intersect(conc$hs_symbol, ddr)))
cat("Candidates:", cand, "\n")

validate <- function(proj) {
  vsd <- readRDS(P("03_processed_data", paste0(proj, "_vst.rds")))
  sym <- rowData(readRDS(P("03_processed_data", paste0(proj, "_se.rds"))))[rownames(vsd), "gene_name"]
  cd <- as.data.frame(colData(vsd))
  se_cd <- as.data.frame(colData(readRDS(P("03_processed_data", paste0(proj, "_se.rds")))))
  cd <- cbind(cd, se_cd[rownames(cd), c("ajcc_pathologic_stage", "vital_status", "days_to_death",
                                         "days_to_last_follow_up", "age_at_index", "gender")])
  cd$stage <- factor(sub("^Stage (I{1,3}V?|IV).*", "\\1", cd$ajcc_pathologic_stage), levels = c("I", "II", "III", "IV"))
  cd$time  <- as.numeric(ifelse(cd$vital_status == "Dead", cd$days_to_death, cd$days_to_last_follow_up)) / 30.44
  cd$event <- as.integer(cd$vital_status == "Dead")
  tum <- cd$condition == "Tumor"

  rbindlist(lapply(cand, function(gname) {
    i <- which(sym == gname)[1]; if (is.na(i)) return(NULL)
    x <- assay(vsd)[i, ]
    w  <- wilcox.test(x[tum], x[!tum])
    roc_ <- roc(cd$condition, x, levels = c("Normal", "Tumor"), quiet = TRUE)
    ci <- ci.auc(roc_, method = "delong")
    st <- cor.test(as.numeric(cd$stage[tum]), x[tum], method = "spearman", exact = FALSE)
    d <- data.frame(time = cd$time[tum], event = cd$event[tum], z = as.numeric(scale(x[tum])),
                    age = cd$age_at_index[tum], sex = cd$gender[tum], stage = cd$stage[tum])
    d <- d[complete.cases(d) & d$time > 0, ]
    cx <- tryCatch(summary(coxph(Surv(time, event) ~ z + age + sex + stage, data = d))$coefficients["z", ],
                   error = function(e) rep(NA, 5))
    data.table(dataset = proj, gene = gname,
               median_tumour = median(x[tum]), median_normal = median(x[!tum]), p_wilcox = w$p.value,
               AUC = as.numeric(auc(roc_)), AUC_lo = ci[1], AUC_hi = ci[3],
               stage_rho = st$estimate, p_stage = st$p.value,
               HR_per_SD = exp(cx[1]), p_cox = cx[5], n_surv = nrow(d), events = sum(d$event))
  }))
}
val <- rbind(validate("TCGA-COAD"), validate("TCGA-READ"))
val[, `:=`(padj_wilcox = p.adjust(p_wilcox, "BH"), padj_stage = p.adjust(p_stage, "BH"),
           padj_cox = p.adjust(p_cox, "BH")), by = dataset]
fwrite(val, P("05_results", "07_validation.tsv"), sep = "\t")

# Figure 6A: tumour vs normal boxplots (COAD)
vsd <- readRDS(P("03_processed_data", "TCGA-COAD_vst.rds"))
sym <- rowData(readRDS(P("03_processed_data", "TCGA-COAD_se.rds")))[rownames(vsd), "gene_name"]
idx <- match(cand, sym); idx <- idx[!is.na(idx)]
long <- data.table(gene = rep(sym[idx], each = ncol(vsd)),
                   condition = rep(vsd$condition, length(idx)),
                   expr = as.vector(t(assay(vsd)[idx, , drop = FALSE])))
gA <- ggplot(long, aes(condition, expr, fill = condition)) + geom_boxplot(outlier.size = 0.3, linewidth = 0.3) +
  facet_wrap(~ gene, scales = "free_y", nrow = 2) + scale_fill_manual(values = c(Normal = "grey80", Tumor = "#D6604D")) +
  labs(x = NULL, y = "VST expression") + theme_classic(base_size = 8) + theme(legend.position = "none")
ggsave(P("06_figures", "Fig6A_tumour_normal.pdf"), gA, width = 7, height = 3.5)
