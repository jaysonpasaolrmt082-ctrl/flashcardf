# =============================================================================
# SACC meta-analysis: shared functions
# Primary engine: metafor (REML random effects). Tested with R 4.3.3, metafor 4.4.0.
#
# Integrity guards built into every reader:
#   * only rows with verified == "yes" are analysed;
#   * an outcome cannot contain two rows from the same overlap_group;
#   * nothing is pooled when k < 2 (single studies are tabulated, not pooled).
# =============================================================================
suppressPackageStartupMessages({
  library(metafor)
  library(ggplot2)
})

Z975 <- qnorm(0.975)

# Species strata. The primary analysis uses S. japonicum (confirmed or presumed
# from an endemic-area cohort); other species are analysed separately.
PRIMARY_SPECIES <- c("S_japonicum_confirmed", "S_japonicum_presumed")

OUTCOME_LABELS <- c(
  male_sex = "Male sex", age_over_60 = "Age > 60 years",
  rectal_location = "Rectal location", sigmoid_location = "Sigmoid location",
  left_sided = "Left-sided tumour", advanced_stage_III_IV = "Stage III-IV",
  T3_T4 = "pT3-T4", LN_metastasis = "Lymph-node metastasis",
  distant_metastasis = "Distant metastasis", vascular_invasion = "Vascular invasion",
  lymphovascular_invasion = "Lymphovascular invasion",
  perineural_invasion = "Perineural invasion", tumor_budding = "Tumour budding",
  poor_differentiation = "Poor differentiation", mucinous = "Mucinous histology",
  signet_ring = "Signet-ring cell", multiple_primary = "Multiple primary CRC",
  synchronous = "Synchronous tumours", concomitant_polyps = "Concomitant polyps",
  positive_margin = "Positive margin", KRAS_mut = "KRAS mutation",
  NRAS_mut = "NRAS mutation", BRAF_mut = "BRAF mutation", TP53_mut = "TP53 mutation",
  p53_IHC_positive = "p53 IHC positive", MSI_H = "MSI-high", dMMR = "dMMR",
  CEA_elevated = "Elevated CEA", CA19_9_elevated = "Elevated CA19-9",
  recurrence = "Recurrence", right_sided = "Right-sided colon",
  tumor_size_5cm = "Tumour size >= 5 cm", age_older = "Older age",
  OS_hazard = "Overall survival hazard", DFS_hazard = "DFS/RFS hazard"
)
PRIMARY_BINARY <- c("advanced_stage_III_IV", "LN_metastasis", "distant_metastasis")

label_of <- function(x) ifelse(x %in% names(OUTCOME_LABELS), OUTCOME_LABELS[x], x)

# ---------------------------------------------------------------- readers ----
read_verified <- function(path) {
  if (!file.exists(path)) stop("Missing file: ", path)
  d <- read.csv(path, stringsAsFactors = FALSE, na.strings = c("", "NA", "NR"),
                check.names = FALSE)
  if (!"verified" %in% names(d)) return(d)
  d <- d[!is.na(d$verified) & tolower(trimws(d$verified)) == "yes", , drop = FALSE]
  d
}

check_overlap <- function(d, by) {
  if (!nrow(d) || !"overlap_group" %in% names(d)) return(invisible(TRUE))
  key <- interaction(d[[by]], d$overlap_group, drop = TRUE)
  dup <- d[!is.na(d$overlap_group) & duplicated(key), , drop = FALSE]
  if (nrow(dup)) {
    stop("Overlapping cohorts entered twice for the same outcome:\n",
         paste(unique(paste(dup[[by]], dup$overlap_group)), collapse = "\n"),
         "\nResolve in data/overlap_matrix.csv before pooling.")
  }
  invisible(TRUE)
}

study_label <- function(d) d$study_id

fmt_p <- function(p) ifelse(is.na(p), "NA", ifelse(p < 0.001, "<0.001", sprintf("%.3f", p)))

het_label <- function(res) {
  sprintf("RE model (REML): I-squared = %.0f%%, tau-squared = %.3f, Q = %.2f (df = %d, p = %s)",
          res$I2, res$tau2, res$QE, res$k - 1, fmt_p(res$QEp))
}

# Summarise a fitted rma object into one table row.
summarise_rma <- function(res, outcome, measure, nS = NA, nN = NA, analysis = "primary") {
  fe <- tryCatch(rma(yi = res$yi, vi = res$vi, method = "EE"), error = function(e) NULL)
  data.frame(
    outcome = outcome, analysis = analysis, k = res$k,
    n_SACC = nS, n_NSACC = nN, measure = measure,
    estimate = exp(res$b[1]), lower95 = exp(res$ci.lb), upper95 = exp(res$ci.ub),
    p_value = res$pval, I2 = res$I2, tau2 = res$tau2, Q = res$QE, Q_p = res$QEp,
    fixed_estimate = if (is.null(fe)) NA else exp(fe$b[1]),
    fixed_lower95 = if (is.null(fe)) NA else exp(fe$ci.lb),
    fixed_upper95 = if (is.null(fe)) NA else exp(fe$ci.ub),
    certainty_GRADE = "[TO BE ASSESSED]",
    stringsAsFactors = FALSE
  )
}

# ---------------------------------------------------------------- models -----
fit_binary <- function(d) {
  rma(measure = "OR", ai = event_SACC, n1i = n_SACC, ci = event_NSACC, n2i = n_NSACC,
      data = d, method = "REML", slab = study_label(d))
}

fit_hr <- function(d) {
  d$yi  <- log(d$hr)
  d$sei <- (log(d$upper95) - log(d$lower95)) / (2 * Z975)
  rma(yi = yi, sei = sei, data = d, method = "REML", slab = study_label(d))
}

# Wan et al. 2014 (BMC Med Res Methodol 14:135), scenario C3 (median, IQR, n).
wan_mean_sd <- function(q1, m, q3, n) {
  list(mean = (q1 + m + q3) / 3,
       sd = (q3 - q1) / (2 * qnorm((0.75 * n - 0.125) / (n + 0.25))))
}

fit_md <- function(d) {
  rma(measure = "MD", m1i = mean_SACC, sd1i = sd_SACC, n1i = n_SACC,
      m2i = mean_NSACC, sd2i = sd_NSACC, n2i = n_NSACC,
      data = d, method = "REML", slab = study_label(d))
}

# ---------------------------------------------------------------- output -----
save_fig <- function(name, width, height, draw, outdir) {
  dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
  f <- file.path(outdir, name)
  grDevices::cairo_pdf(paste0(f, ".pdf"), width = width, height = height, family = "Arial")
  draw(); dev.off()
  svglite::svglite(paste0(f, ".svg"), width = width, height = height)
  draw(); dev.off()
  ragg::agg_png(paste0(f, ".png"), width = width, height = height, units = "in", res = 600)
  draw(); dev.off()
  ragg::agg_tiff(paste0(f, ".tiff"), width = width, height = height, units = "in",
                 res = 600, compression = "lzw")
  draw(); dev.off()
  invisible(f)
}

# Readable log-scale ticks (0.25, 0.5, 1, 2, 4 ...) covering the CIs.
log_ticks <- function(lo, hi) {
  cand <- c(0.01, 0.02, 0.05, 0.1, 0.2, 0.25, 0.5, 1, 2, 4, 5, 10, 20, 50, 100)
  lo <- min(exp(lo), 1); hi <- max(exp(hi), 1)
  a <- cand[cand >= cand[max(1, sum(cand <= lo))] & cand <= cand[min(length(cand), sum(cand < hi) + 1)]]
  log(a)
}

# Adds headers above ilab columns using positions returned by forest().
ilab_headers <- function(fp, labels) {
  text(fp$ilab.xpos, fp$ylim[2] - 1, labels, font = 2, cex = fp$cex)
}

# Study-level forest plot with SACC n, NSACC n and weight columns.
forest_study <- function(res, d, xlab, title) {
  w <- weights(res)
  k <- res$k
  par(mar = c(4, 0, 2, 0), family = "Arial", cex = 0.85)
  fp <- forest(res, atransf = exp, refline = 0, xlab = xlab, header = c("Study", "OR [95% CI]"),
         ilab = cbind(d$n_SACC, d$n_NSACC, sprintf("%.1f%%", w)),
         at = log_ticks(min(res$yi - Z975 * sqrt(res$vi)), max(res$yi + Z975 * sqrt(res$vi))),
         mlab = het_label(res), shade = TRUE,
         colout = "#1F4E79", col = "#B22222", annotate = TRUE)
  ilab_headers(fp, c("SACC n", "NSACC n", "Weight"))
  par(xpd = NA)
  usr <- par("usr")
  text(usr[1], k + 2.6, title, pos = 4, font = 2)
}

# ---------------------------------------------------------------- heatmap ----
plot_evidence_heatmap <- function(ev) {
  lv <- c("higher", "lower", "no_difference", "not_reported")
  lab <- c(higher = "Higher in SACC", lower = "Lower in SACC",
           no_difference = "No significant difference", not_reported = "Not reported")
  full <- expand.grid(study_id = unique(ev$study_id), feature = unique(ev$feature),
                      stringsAsFactors = FALSE)
  ev <- merge(full, ev[, c("study_id", "feature", "direction")], all.x = TRUE)
  ev$direction[is.na(ev$direction)] <- "not_reported"
  ev$direction <- factor(ev$direction, levels = lv)
  ev$feature <- factor(label_of(ev$feature), levels = rev(unique(label_of(ev$feature))))
  # Okabe-Ito based, colour-blind safe
  pal <- c(higher = "#D55E00", lower = "#0072B2", no_difference = "#BDBDBD", not_reported = "#FFFFFF")
  ggplot(ev, aes(study_id, feature, fill = direction)) +
    geom_tile(colour = "grey40", linewidth = 0.3) +
    scale_fill_manual(values = pal, labels = lab, drop = FALSE, name = NULL) +
    labs(x = NULL, y = NULL) +
    theme_minimal(base_family = "Arial", base_size = 9) +
    theme(axis.text.x = element_text(angle = 45, hjust = 1), panel.grid = element_blank(),
          legend.position = "bottom") +
    guides(fill = guide_legend(nrow = 2))
}
